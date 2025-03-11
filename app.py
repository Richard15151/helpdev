import requests
from googletrans import Translator
from flask import Flask, render_template, request

app = Flask(__name__)

def traduzir_para_ingles(texto_pt):
    translator = Translator()
    traducao = translator.translate(texto_pt, src='pt', dest='en')
    return traducao.text

def traduzir_para_portugues(texto_en):
    translator = Translator()
    traducao = translator.translate(texto_en, src='en', dest='pt')
    return traducao.text

def buscar_stackoverflow(termo):
    termo_traduzido = traduzir_para_ingles(termo)
    url = f"https://api.stackexchange.com/2.3/search?order=desc&sort=votes&intitle={termo_traduzido}&site=stackoverflow"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if "items" in data:
            resultados = []
            for item in data["items"][:5]:  # Limita a 5 resultados
                titulo = item['title']
                link = item['link']
                titulo_traduzido = traduzir_para_portugues(titulo)
                resultados.append({
                    'titulo': titulo_traduzido,
                    'link': link
                })
            return resultados
    return []

def buscar_reddit(termo, subreddit="learnprogramming"):
    url = f"https://www.reddit.com/r/{subreddit}/search.json?q={termo}&restrict_sr=on&sort=relevance&t=week"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        resultados = []
        for post in data.get("data", {}).get("children", [])[:5]:  # Limita a 5 resultados
            titulo = post["data"].get("title", "")
            titulo_traduzido = traduzir_para_portugues(titulo)
            link = "https://www.reddit.com" + post["data"].get("permalink", "")
            resultados.append({
                'titulo': titulo_traduzido,
                'link': link
            })
        return resultados
    return []

@app.route('/', methods=['GET', 'POST'])
def index():
    pergunta = ""
    resultados_stack = []
    resultados_reddit =[]

    if request.method == 'POST':
        pergunta = request.form['pergunta']
        resultados_stack = buscar_stackoverflow(pergunta)
        resultados_reddit = buscar_reddit(pergunta)

    return render_template('index.html', pergunta=pergunta, resultados_stack=resultados_stack, resultados_reddit = resultados_reddit)

if __name__ == "__main__":
    app.run(debug=True)

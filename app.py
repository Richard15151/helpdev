import requests
from googletrans import Translator
from flask import Flask, render_template, request

app = Flask(__name__)

# Função para traduzir o texto de português para inglês
def traduzir_para_ingles(texto_pt):
    translator = Translator()
    traducao = translator.translate(texto_pt, src='pt', dest='en')
    return traducao.text

# Função para traduzir o texto de inglês para português
def traduzir_para_portugues(texto_en):
    translator = Translator()
    traducao = translator.translate(texto_en, src='en', dest='pt')
    return traducao.text

# Função para buscar dúvidas na API do Stack Overflow
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

@app.route('/', methods=['GET', 'POST'])
def index():
    pergunta = ""
    resultados_stackoverflow = []

    if request.method == 'POST':
        pergunta = request.form['pergunta']
        resultados_stackoverflow = buscar_stackoverflow(pergunta)

    return render_template('index.html', pergunta=pergunta, resultados_stackoverflow=resultados_stackoverflow,)

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request
from functions import *

app = Flask(__name__)

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

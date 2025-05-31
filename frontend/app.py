from flask import Flask, render_template, request, redirect
import csv
import os

app = Flask(__name__)

CSV_FILE = 'dados.csv'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        placa_carreta = request.form.get('placa_carreta')
        placa_veiculo = request.form.get('placa_veiculo')
        identificacao = request.form.get('identificacao')

        # Cria o arquivo com cabeçalho se ele não existir
        file_exists = os.path.isfile(CSV_FILE)
        with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(['Placa Carreta', 'Placa Veículo', 'Identificação'])
            writer.writerow([placa_carreta, placa_veiculo, identificacao])

        return redirect('/')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

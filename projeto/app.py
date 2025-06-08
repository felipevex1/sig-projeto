from flask import Flask, render_template, request, redirect
import csv
import os

app = Flask(__name__)

CSV_FILE = 'dados.csv'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Variaveis que irão receber inputs/ informações
        placa_carreta = request.form.get('placa_carreta')
        placa_veiculo = request.form.get('placa_veiculo')
        identificacao = request.form.get('identificacao')
        tipo_veiculo = request.form.get('tipo_veiculo')
        desc_tipo_veiculo = request.form.get('desc_tipo_veiculo')
        peso_bruto = request.form.get('peso_bruto')
        codigo_item = request.form.get('codigo_item')
        desc_item = request.form.get('desc_tipo_item')
        pais_origem = request.form.get('pais_origem')
        doc_motorista = request.form.get('doc_motorista')
        nome_motorista = request.form.get('nome_motorista')
        campos_adicionais = request.form.get('campos_adicionais')

        campos_obrigatorios = [
            placa_carreta, placa_veiculo, identificacao,
            tipo_veiculo, desc_tipo_veiculo, peso_bruto,
            codigo_item, desc_item, pais_origem,
            doc_motorista, nome_motorista, campos_adicionais
        ]

        if not all(campos_obrigatorios):
            return render_template('index.html', erro="Todos os campos devem ser preenchidos.")

        # Criação do arquivo e dos itens dele
        file_exists = os.path.isfile(CSV_FILE)
        with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow([
                    'Placa Carreta', 'Placa Veículo', 'Identificação', 'Tipo do Veículo', 
                    'Descrição do Veículo', 'Peso Bruto', 'Codigo do Item', 'Descrição do Item', 
                    'País de Origem', 'Documento do Motorista', 'Nome do Motorista', 'Campos Adicionais'
                ])
            writer.writerow([placa_carreta, placa_veiculo, identificacao, tipo_veiculo, 
                             desc_tipo_veiculo, peso_bruto, codigo_item, desc_item, 
                             pais_origem, doc_motorista, nome_motorista, campos_adicionais])

        return redirect('/')

    return render_template('index.html', erro=None)

if __name__ == '__main__':
    app.run(debug=True)

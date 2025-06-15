from flask import Flask, request, render_template, redirect, send_file
from supabase import create_client, Client
from datetime import datetime
import pandas as pd
import re
import io

app = Flask(__name__)

SUPABASE_URL = "https://doapxxdivkafqxviyrmj.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRvYXB4eGRpdmthZnF4dml5cm1qIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDk4ODQ5NjcsImV4cCI6MjA2NTQ2MDk2N30.5taTy6QN-NztbVQd0rLj9WpUf07QBqRAjtsD_Jo4UVg"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        peso_bruto = request.form.get('peso_bruto')
        codigo_item = request.form.get('codigo_item')
        doc_motorista = request.form.get('doc_motorista')
        pais_origem = request.form.get('pais_origem')
        nome_motorista = request.form.get('nome_motorista')

        if not peso_bruto.isdigit():
            return render_template('index.html', erro="Insira somente números no campo Peso Bruto")
        if not codigo_item.isdigit():
            return render_template('index.html', erro="Insira somente números no campo Código Fluído")
        if not doc_motorista.isdigit():
            return render_template('index.html', erro="Insira somente números no campo Documento do Motorista")
        if not re.match(r'^[A-Za-zÀ-ÿ\s]+$', pais_origem):
            return render_template('index.html', erro="Insira somente letras no campo País de Origem")
        if not re.match(r'^[A-Za-zÀ-ÿ\s]+$', nome_motorista):
            return render_template('index.html', erro="Insira somente letras no campo Nome do Motorista")

        dados = {
            "placa_carreta": request.form.get('placa_carreta'),
            "placa_veiculo": request.form.get('placa_veiculo'),
            "identificacao": request.form.get('identificacao'),
            "tipo_veiculo": request.form.get('tipo_veiculo'),
            "desc_tipo_veiculo": request.form.get('desc_tipo_veiculo'),
            "peso_bruto": peso_bruto,
            "codigo_item": codigo_item,
            "desc_item": request.form.get('desc_tipo_item'),
            "pais_origem": pais_origem,
            "doc_motorista": request.form.get('doc_motorista'),
            "nome_motorista": nome_motorista,
            "campos_adicionais": request.form.get('campos_adicionais'),
            "datahora": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        supabase.from_("Dados").insert(dados).execute()
        return redirect('/')

    return render_template('index.html', erro=None)

@app.route('/consulta', methods=['POST'])
def consulta():
    data_ini = request.form.get('data_ini')
    data_fim = request.form.get('data_fim')

    response = supabase.from_('Dados') \
        .select('placa_carreta, placa_veiculo, identificacao, tipo_veiculo, peso_bruto, codigo_item, desc_item, nome_motorista, datahora') \
        .gte('datahora', data_ini) \
        .lte('datahora', data_fim) \
        .execute()

    registros = response.data

    html = """
    <html>
    <head>
        <title>Relatório Estilizado</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px; }
            h2 { color: #004a99; text-align: center; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; background-color: white; }
            th, td { border: 1px solid #ccc; padding: 8px; text-align: center; }
            th { background-color: #004a99; color: white; }
            tr:nth-child(even) { background-color: #f9f9f9; }
            tr:hover { background-color: #f1f1f1; }
        </style>
    </head>
    <body>
        <h2>Relatório de Pesagens</h2>
        <table>
            <tr>
                <th>Placa Carreta</th>
                <th>Placa Veículo</th>
                <th>Identificação</th>
                <th>Tipo Veículo</th>
                <th>Peso Bruto (kg)</th>
                <th>Código Fluído</th>
                <th>Descrição Fluído</th>
                <th>Nome Motorista</th>
                <th>Data/Hora</th>
            </tr>
    """

    for r in registros:
        html += f"""
            <tr>
                <td>{r['placa_carreta']}</td>
                <td>{r['placa_veiculo']}</td>
                <td>{r['identificacao']}</td>
                <td>{r['tipo_veiculo']}</td>
                <td>{r['peso_bruto']}</td>
                <td>{r['codigo_item']}</td>
                <td>{r['desc_item']}</td>
                <td>{r['nome_motorista']}</td>
                <td>{r['datahora']}</td>
            </tr>
        """

    html += """
        </table>
    </body>
    </html>
    """

    return html

@app.route('/exportar')
def exportar():
    response = supabase.from_("Dados").select("*").execute()
    registros = response.data

    if not registros:
        return "Nenhum dado encontrado para exportar."

    df = pd.DataFrame(registros)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='DadosExportados', index=False)

    output.seek(0)
    return send_file(output, as_attachment=True, download_name='dados_exportados.xlsx',
                     mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

if __name__ == "__main__":
    app.run(debug=True)

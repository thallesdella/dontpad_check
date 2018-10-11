from json import dumps
from flask import Flask, render_template, url_for
from os.path import isfile
from dontpad import check_dontpad

app = Flask(__name__)

lista = {}
historico = []

def read_file(lista):
    if isfile('dontpad.txt'):
        with open('dontpad.txt', 'r') as f:
            for linha in f:
                linha = linha[:len(linha)-1]
                try:
                    if lista[linha] is not None:
                        continue
                except KeyError:
                    lista[linha] = ''
            f.close()
    else:
        with open('dontpad.txt', 'w') as f:
            f.close()
    return lista

@app.route('/')
@app.route('/index')
def check():
    return render_template('index.html', title='Home')

@app.route('/config', methods=['GET', 'POST'])
def add_dontpad():
    if request.method == 'GET':
        return render_template('add.html', title='Adicionar Arquivo')

    if request.form['path'] != '':
        path = '/{}'.format(request.form['path'])
        with open('dontpad.txt', 'w+') as f:
            f.write(path)
            f.close()
    return redirect(url_for('index'))

@app.route('/ajax-list')
def ajax_list():
    global lista
    global historico
    json = {}
    lista = read_file(lista)

    if len(lista) > 0:
        historico,lista = check_dontpad(lista)
        if len(historico) > 0:
            ul = ''
            for h in historico:
                ul += '<li><a title="" href="http://dontpad.com{}">{}</a></li>'.format(h, h)
            json['ul'] = ul
    else:
        json['error'] = '<li>Insira arquivos para serem verificados</li>'

    return dumps(json)

app.run(debug=True)

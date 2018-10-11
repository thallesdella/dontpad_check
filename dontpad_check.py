import notify2
from argparse import ArgumentParser
from time import sleep
from os.path import isfile
from bs4 import BeautifulSoup
from requests import get

def check_dontpad(lista):
    historico = []
    for path, content in lista.items():
        url = 'http://dontpad.com{}'.format(path)
        r = get(url)
        
        #import pdb; pdb.set_trace()

        if r.status_code == 200:
            html = r.text
            soup = BeautifulSoup(html, 'lxml')
            content_new = soup.find(id='text').string

            if content != content_new:
                historico.append(path)
                lista[path] = content_new
        else:
            print('{} - {}'.format(path, r.status_code))
    return historico, lista

if __name__ == '__main__':
    notify2.init(__name__)

    lista = {}

    p = ArgumentParser(description='Verificador de mudança em arquivos hospedados no DontPad')
    p.add_argument('sleep', type=int, help='Tempo de espera entre cada verificação', default=1)
    args = p.parse_args()

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
                f.close            
        else:
            with open('dontpad.txt', 'w') as f:
                f.close
        return lista
    
    while True:
        lista = read_file(lista)

        if len(lista) > 0:
            historico,lista = check_dontpad(lista)
            if len(historico) > 0:
                print('Notificação')
                text_body = 'O(s) seguintes arquivos foram modificados:\n\n{}'.format(', '.join(historico))
                n = notify2.Notification('Arquivos Modificados!', text_body, 'notification-message-IM')
                n.set_urgency(2)
                n.show()
        else:
            print('insira no arquivo os links para verificar...\n')

        sleep(args.sleep * 60)
    

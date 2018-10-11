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
                if len(historico) == len(lista):
                    historico = []
                historico.append(path)
                lista[path] = content_new
        else:
            print('{} - {}'.format(path, r.status_code))
    return historico, lista

"""API local didática: transporte HTTP integrado ao cálculo de médias."""
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from media import calcular_media


class API(BaseHTTPRequestHandler):
    def responder(self, status, dados):
        corpo = json.dumps(dados, ensure_ascii=False, allow_nan=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    def rota_existe(self):
        if self.path != '/medias':
            self.responder(404, {'erro': 'Rota inexistente.'})
            return False
        return True

    def do_POST(self):
        if not self.rota_existe():
            return
        if self.headers.get_content_type() != 'application/json':
            self.responder(415, {'erro': 'Utilize application/json.'})
            return
        try:
            tamanho = int(self.headers.get('Content-Length', '0'))
            if not 0 < tamanho <= 4096:
                raise ValueError('Tamanho do corpo inválido.')
            dados = json.loads(self.rfile.read(tamanho))
        except (ValueError, UnicodeError):
            self.responder(400, {'erro': 'Corpo JSON inválido.'})
            return
        if not isinstance(dados, dict) or set(dados) != {'notas'}:
            self.responder(422, {'erro': 'Informe somente o campo notas.'})
            return
        try:
            media = calcular_media(dados['notas'])
        except ValueError as erro:
            self.responder(422, {'erro': str(erro)})
            return
        self.responder(200, {'media': media})

    def do_GET(self):
        if self.rota_existe():
            self.responder(405, {'erro': 'Utilize POST.'})

    def log_message(self, formato, *argumentos):
        # Evita registrar os dados das requisições deste exercício.
        pass


if __name__ == '__main__':
    with ThreadingHTTPServer(('127.0.0.1', 8000), API) as servidor:
        print('API disponível em http://127.0.0.1:8000/medias')
        servidor.serve_forever()

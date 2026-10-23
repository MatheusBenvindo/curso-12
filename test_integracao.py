"""Testes com HTTP real em loopback, sem substituir o cálculo por mocks."""
import json
import threading
import unittest
from http.server import ThreadingHTTPServer
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from api import API


class TestIntegracao(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.servidor = ThreadingHTTPServer(('127.0.0.1', 0), API)
        cls.thread = threading.Thread(target=cls.servidor.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f'http://127.0.0.1:{cls.servidor.server_port}'

    @classmethod
    def tearDownClass(cls):
        cls.servidor.shutdown()
        cls.servidor.server_close()
        cls.thread.join(timeout=5)

    def requisitar(self, dados=None, *, corpo=None, tipo='application/json',
                   metodo='POST', rota='/medias'):
        if corpo is None:
            corpo = json.dumps(dados).encode('utf-8')
        pedido = Request(self.base + rota, data=corpo,
                         headers={'Content-Type': tipo}, method=metodo)
        try:
            resposta = urlopen(pedido, timeout=5)
        except HTTPError as erro:
            resposta = erro
        with resposta:
            self.assertEqual(resposta.headers.get_content_type(), 'application/json')
            return resposta.status, json.load(resposta)

    def conferir_erro(self, dados=None, *, status=422, **opcoes):
        recebido, corpo = self.requisitar(dados, **opcoes)
        self.assertEqual(recebido, status)
        self.assertEqual(set(corpo), {'erro'})
        self.assertIsInstance(corpo['erro'], str)
        self.assertTrue(corpo['erro'])

    def test_media_normal(self):
        self.assertEqual(self.requisitar({'notas': [7, 8, 9]}), (200, {'media': 8.0}))

    def test_arredondamento(self):
        self.assertEqual(self.requisitar({'notas': [7, 7, 8]}), (200, {'media': 7.33}))

    def test_limite_inferior(self):
        self.assertEqual(self.requisitar({'notas': [0, 0, 0]}), (200, {'media': 0.0}))

    def test_limite_superior(self):
        self.assertEqual(self.requisitar({'notas': [10, 10, 10]}), (200, {'media': 10.0}))

    def test_lista_vazia(self):
        self.conferir_erro({'notas': []})

    def test_quantidade_insuficiente(self):
        self.conferir_erro({'notas': [8, 9]})

    def test_quantidade_excessiva(self):
        self.conferir_erro({'notas': [8, 9, 7, 6]})

    def test_nota_negativa(self):
        self.conferir_erro({'notas': [-1, 7, 8]})

    def test_nota_acima_do_limite(self):
        self.conferir_erro({'notas': [11, 7, 8]})

    def test_texto_nao_convertido(self):
        self.conferir_erro({'notas': ['8', 7, 9]})

    def test_booleano_rejeitado(self):
        self.conferir_erro({'notas': [True, 7, 9]})

    def test_nota_nula(self):
        self.conferir_erro({'notas': [None, 7, 9]})

    def test_campo_ausente(self):
        self.conferir_erro({})

    def test_campo_extra(self):
        self.conferir_erro({'notas': [7, 8, 9], 'peso': 2})

    def test_raiz_json_invalida(self):
        self.conferir_erro([7, 8, 9])

    def test_json_malformado(self):
        self.conferir_erro(corpo=b'{', status=400)

    def test_tipo_de_conteudo_incorreto(self):
        self.conferir_erro({'notas': [7, 8, 9]}, tipo='text/plain', status=415)

    def test_metodo_incorreto(self):
        self.conferir_erro(metodo='GET', status=405)

    def test_rota_inexistente(self):
        self.conferir_erro(rota='/outra', status=404)


if __name__ == '__main__':
    unittest.main(verbosity=2)

# Curso 12 — testes de integração com apoio de GenAI

Exercício didático ligado à atuação de um instrutor de Tecnologia e Desenvolvimento de Sistemas. Uma API recebe três notas e chama um módulo de cálculo de médias. As regras são fictícias e não representam critérios oficiais do SENAI.

## Integração verificada

Cliente HTTP → API local → validação e cálculo → resposta JSON.

Os testes usam HTTP real em 127.0.0.1 e não substituem o cálculo por simulações. Não há banco de dados, autenticação, persistência ou serviços externos. O servidor da biblioteca padrão serve somente ao exercício local.

## Arquivos

- `media.py`: regras de validação e cálculo.
- `api.py`: API HTTP e tradução de erros para respostas JSON.
- `test_integracao.py`: 19 testes de integração.
- `PROMPTS.md`: contrato, dois tipos de prompt e casos gerados.
- `RESULTADOS.md`: execução e limites da verificação.

## Executar

Requisito: Python 3.11. Não é necessário instalar pacotes.

Na pasta do projeto:

```console
python -m unittest -v
```

Os testes iniciam e encerram o próprio servidor. Para usar a API manualmente:

```console
python api.py
```

Envie POST para `http://127.0.0.1:8000/medias`, com Content-Type `application/json` e corpo `{"notas": [7, 8, 9]}`. A resposta esperada é HTTP 200 e `{"media": 8.0}`.

## Resumo do experimento

Foram usados um prompt zero-shot para organizar cenários a partir do contrato e um prompt few-shot com exemplos de requisições e respostas para orientar os testes. A revisão conferiu valores esperados independentes da implementação, cobertura de limites e erros, status HTTP e formato das respostas.

Resultado: 19 testes aprovados em Python 3.11. A primeira tentativa de execução foi impedida pelas permissões de rede do ambiente; após autorização de execução local, a mesma suíte passou. Não houve correção de código motivada por falha funcional nessa execução.

Todo o conteúdo foi preparado com auxílio de IA, usando dados fictícios e sem credenciais.

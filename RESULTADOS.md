# Registro de execução

Data: 23/10/2026.

Ambiente: Windows, Python 3.11. Biblioteca padrão, sem pacotes adicionais.

Comando: `python -m unittest -v`.

Primeira tentativa: 19 erros de ambiente, causados por bloqueio da conexão local (WinError 10013). Isso não foi interpretado como evidência de defeito na regra de cálculo.

Segunda tentativa, após autorização de execução com HTTP local:

```text
Ran 19 tests in 0.656s
OK
```

Os 19 cenários estão descritos em PROMPTS.md e implementados em test_integracao.py. Em cada resposta são conferidos o Content-Type e o status HTTP. Nos casos válidos, confere-se o objeto com a média esperada; nos inválidos, a presença exclusiva de uma mensagem de erro não vazia.

Limites: a suíte verifica uma integração local e didática. Não avalia banco de dados, autenticação, implantação, carga, concorrência ou segurança de produção. Sua aprovação vale para os casos especificados, não para qualquer entrada possível.

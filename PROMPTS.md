# Prompts utilizados na atividade

Os prompts foram trabalhados com a LLM desta conversa. O material foi elaborado com assistência de IA e revisado por execução. Não é necessário treinar ou criar uma LLM para este exercício.

## Contexto e contrato fornecidos

Atuo como instrutor de Tecnologia e Desenvolvimento de Sistemas no SENAI. Prepare um exemplo didático em Python 3, somente com a biblioteca padrão e dados fictícios. A integração será entre um cliente HTTP, uma API local e o módulo calcular_media. Não inclua banco de dados, autenticação, cadastro, aprovação ou reprovação de alunos. Estas são regras fictícias do exercício, sem representar critérios oficiais da instituição.

Contrato: POST /medias, Content-Type application/json, corpo contendo somente o campo notas. Esse campo deve ser uma lista com exatamente três números entre 0 e 10, inclusive. Rejeitar booleanos, textos, valores nulos e quantidades incorretas. Retornar HTTP 200 e o objeto {"media": numero}, com média aritmética arredondada para duas casas decimais. Erros devem retornar JSON contendo somente o campo erro, com mensagem textual não vazia. JSON malformado: 400; dados fora do contrato: 422; tipo de conteúdo incorreto: 415; GET /medias: 405; POST em rota inexistente: 404. Não converter textos automaticamente.

## Prompt 1 — geração de cenários sem exemplos (zero-shot)

Com base no contexto e no contrato acima, gere cenários de teste de integração. Inclua funcionamento normal, limites e erros. Para cada cenário, indique a requisição e o resultado esperado, incluindo status HTTP e conteúdo da resposta. Verifique a comunicação entre cliente, API e cálculo. Não proponha funcionalidades fora do contrato.

### Casos resultantes registrados

| Caso | Entrada ou requisição | Resultado esperado |
|---|---|---|
| Média normal | notas: [7,8,9] | 200, media: 8.0 |
| Arredondamento | notas: [7,7,8] | 200, media: 7.33 |
| Limite inferior | notas: [0,0,0] | 200, media: 0.0 |
| Limite superior | notas: [10,10,10] | 200, media: 10.0 |
| Lista vazia | notas: [] | 422, erro |
| Quantidade insuficiente | notas: [8,9] | 422, erro |
| Quantidade excessiva | notas: [8,9,7,6] | 422, erro |
| Nota negativa | notas: [-1,7,8] | 422, erro |
| Nota acima do limite | notas: [11,7,8] | 422, erro |
| Texto | notas: ["8",7,9] | 422, erro |
| Booleano | notas: [true,7,9] | 422, erro |
| Nota nula | notas: [null,7,9] | 422, erro |
| Campo ausente | {} | 422, erro |
| Campo extra | notas: [7,8,9], peso: 2 | 422, erro |
| Raiz JSON incorreta | [7,8,9] | 422, erro |
| JSON malformado | corpo: { | 400, erro |
| Conteúdo incorreto | Content-Type: text/plain | 415, erro |
| Método incorreto | GET /medias | 405, erro |
| Rota inexistente | POST /outra | 404, erro |

## Prompt 2 — implementação com exemplos (few-shot)

Implemente os testes dos cenários acima utilizando unittest. Siga estes exemplos de entrada e saída:

- POST /medias com {"notas": [7, 8, 9]} deve retornar 200 e {"media": 8.0}.
- POST /medias com {"notas": [11, 7, 8]} deve retornar 422 e {"erro": "mensagem explicativa"}. O texto exato da mensagem é livre; não deve existir campo media na resposta de erro.

Cada teste deve ter um nome que descreva o comportamento. Faça requisições HTTP reais para um servidor temporário em 127.0.0.1, com porta disponível escolhida pelo sistema. Não substitua calcular_media por mock. Confira o Content-Type da resposta, o status e o corpo JSON. Encerre o servidor ao final. Os valores esperados devem vir do contrato e dos exemplos, sem chamar a função de cálculo para construir a expectativa. Use apenas a biblioteca padrão.

## Ajustes de orientação e análise

A especificação foi detalhada para definir os códigos HTTP e esclarecer a rejeição de textos, booleanos e campos extras. O segundo prompt acrescentou exemplos concretos e exigiu comunicação HTTP real, evitando que apenas a função de cálculo fosse testada isoladamente.

O primeiro tipo de prompt organizou a diversidade dos casos; o segundo orientou a implementação e a consistência das verificações. Isso é uma observação deste exercício, não uma comparação controlada entre modelos. Os dois prompts receberam o mesmo contrato.

Os testes não fixam o texto exato das mensagens, pois o contrato permite mensagens diferentes. Conferem sua existência e formato. Não foram adicionadas funcionalidades de autenticação ou banco de dados que não fazem parte da proposta.

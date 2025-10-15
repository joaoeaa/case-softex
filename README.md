### Quake Parser

### Descrição do projeto:
Foi desenvolvido um parser para o arquivo `games.log`, organizando os eventos por jogo e retornando relatórios com total de kills, jogadores e pontuação individual (de kills), além de gerar um ranking geral de kills. O arquivo foi extraído do repositório original `quake_parser`. Também foi feita uma API com FastAPI que permite consultar o resultado de cada jogo por id.
### Requisitos:
- Python 3.10+
- Ambiente Virtual (recomendado)
- games.log 

### Setup:
```bash
python -m venv .venv

.venv/Scripts/activate

pip install -r requirements.txt
```

### Execução do parser:
```bash
python quake_parser.py
```
Esse comando exibe *por jogo:*
- Total de kills
- Players
- Quantidade de kills dos players (com a penalização de -1 quando world mata alguém)
- Ranking geral de kills ao final

#### Exemplo de saída:
```
Relatórios por jogos:

game_1: {
  total_kills: 0
  players: [Isgalamido]
  kills: {Isgalamido: 0}
}

game_2: {
  total_kills: 11
  players: [Dono da Bola, Isgalamido, Mocinha]
  kills: {Dono da Bola: 0, Isgalamido: -5, Mocinha: 0}
}
...

Ranking geral:

Isgalamido: 147
Zeh: 124
Oootsimo: 114
Assasinu Credi: 111
Dono da Bola: 63
```

### Execução da API
```bash
uvicorn api:app --reload
```

Documentação interativa em: http://127.0.0.1:8000/docs

- Endpoint 1 (principal): *GET /games/{game_id}* - Relatório do jogo por id
- Endpoint 2: *GET /games* - Lista todos os jogos
- Endpoint 3 (extra): *GET /ranking* - Ranking geral

### Estrutura do projeto
```
case-softex/
├── api.py
├── games.log
├── quake_parser.py
├── README.md
└── requirements.txt
```

### Observações
- World nunca aparece na lista de jogadores e aplica a penalização de -1 kill quando mata algum jogador
- Total_kills contabiliza todas as mortes do jogo, incluindo as do World
- O parser foi escrito com POO: a classe *Game* é a partida e *QuakeLogParser* a lógica de leitura e processamento do log
- Responsabilidades foram separadas, para facilitar teste e manutenção; boas práticas também foram seguidas para manter o código organizado
- Commits pequenos e organizados

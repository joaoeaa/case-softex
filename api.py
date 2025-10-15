from pathlib import Path
from fastapi import FastAPI, HTTPException
from quake_parser import Game, QuakeLogParser, build_global_ranking

LOG_FILE = Path("games.log")

parser = QuakeLogParser(LOG_FILE)
GAMES: list[Game] = parser.parse()
RANKING = build_global_ranking(GAMES)

app = FastAPI(title="Quake Parser API", version="1.0.0")


@app.get("/games")
def list_games() -> list[dict]:
    return [game.to_dict() for game in GAMES]


@app.get("/games/{game_id}")
def get_game(game_id: int) -> dict:
    for game in GAMES:
        if game.id == game_id:
            return game.to_dict()
    raise HTTPException(status_code=404, detail="Game not found")


@app.get("/ranking")
def get_ranking() -> list[dict]:
    return RANKING

from os import kill
import re
from collections import Counter
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable


_INIT_EVENT = "InitGame"
_PLAYER_EVENT = "ClientUserinfoChanged"
_KILL_EVENT = "Kill:"

_KILL_PATTERN = re.compile(r"Kill: \d+ \d+ \d+: (.+) killed (.+) by .+")
_PLAYER_PATTERN = re.compile(r"ClientUserinfoChanged: \d+ n\\([^\\]+)")

@dataclass(frozen=True)
class Game:
    id: int
    total_kills: int
    players: list[str]
    kills: dict[str, int]

    def to_dict(self) -> dict:
        payload = asdict(self)
        payload["game"] = f"game_{self.id}"
        return payload
    
class QuakeLogParser:
    def __init__(self, log_path: Path | str) -> None:
        self.log_path = Path(log_path)

    def parse(self) -> list[Game]:
        games: list[Game] = []
        players: set[str] = set()
        kills: dict[str, int] = {}
        total_kills = 0
        game_id = 0
        game_active = False

        with self.log_path.open(encoding="utf-8", errors="ignore") as stream:
            for raw_line in stream:
                line = raw_line.strip()
                if not line:
                    continue
                if _INIT_EVENT in line:
                    if game_active:
                        games.append(self._build_game(game_id, total_kills, players, kills))
                        players.clear()
                        kills.clear()
                        total_kills = 0
                    game_id += 1
                    game_active = True
                    continue
                if _PLAYER_EVENT in line:
                    match = _PLAYER_PATTERN.search(line)
                    if match:
                        name = match.group(1)
                        players.add(name)
                        kills.setdefault(name, 0)
                    continue
                if _KILL_EVENT in line:
                    total_kills += 1
                    killer, victim = self._parse_kill(line)
                    if killer == "<world>":
                        kills.setdefault(victim, 0)
                        kills[victim] -= 1
                    elif killer:
                        kills.setdefault(killer, 0)
                        kills[killer] += 1
        if game_active:
            games.append(self._build_game(game_id, total_kills, players, kills))
        return games
    @staticmethod
    def _parse_kill(line:str) -> tuple[str, str]:
        match = _KILL_PATTERN.search(line)
        return match.groups() if match else ("", "")
    
    @staticmethod
    def _build_game(game_id: int, total_kills: int, players: set[str], kills: dict[str, int],) -> Game:
        ordered_players = sorted(players)
        filtered_kills = {player: kills.get(player, 0) for player in ordered_players}
        return Game(id=game_id, total_kills=total_kills, players=ordered_players, kills=filtered_kills,)
    
def build_global_ranking(games: Iterable[Game]) -> list[dict[str, int | str]]:
    aggregate = Counter()
    for game in games:
        aggregate.update(game.kills)
    return [{"player": player, "kills": score} for player, score in aggregate.most_common()]

def print_reports(games: Iterable[Game]) -> None:
    for game in games:
        players_str = ", ".join(game.players) or "<sem jogadores"
        kills_str = ", ".join(f"{player}: {score}" for player, score in game.kills.items())
        print(f"game_{game.id}: {{")
        print(f"  total_kills: {game.total_kills}")
        print(f"  players: [{players_str}]")
        print(f"  kills: {{{kills_str}}}")
        print("}\n")

if __name__ == "__main__":
    parser = QuakeLogParser("games.log")
    games = parser.parse()

    print("Relatórios por jogos:\n")
    print_reports(games)

    print("Ranking geral:\n")
    for entry in build_global_ranking(games):
        print(f"{entry['player']}: {entry['kills']}")

from gamescore.core.models.games import GameCreate

def parse_games(raw_games: list[dict]) -> list[GameCreate]:
    games = []
    for raw_game in raw_games:
        name = raw_game.get("name")
        image = raw_game.get("background_image")
        if name:
            games.append(GameCreate(name=name, image=image))
    return games
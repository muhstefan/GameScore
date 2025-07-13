from gamescore.core.models.games import GameCreate

excluded_tags = {"romance" , "nsfw", "adult", "erotic"}

def parse_games(raw_games: list[dict]) -> list[GameCreate]:
    games = []
    for raw_game in raw_games:
        name = raw_game.get("name")
        image = raw_game.get("background_image")

        rating = raw_game.get("esrb_rating")
        rating_id = rating.get("id") if rating else None

        tags = raw_game.get("tags", [])
        game_tag_names = {tag.get("name", "").lower() for tag in tags}

        if name and rating_id != 5 and not game_tag_names.intersection(excluded_tags):
            games.append(GameCreate(name=name, image=image))

    return games
from faker import Faker

fake = Faker('ru_RU')


async def create_random_game():
    return {
        "name": fake.sentence(nb_words=2),
        "description": fake.sentence(),
        "rating": fake.random_int(min=1, max=10)
    }


async def create_partial_game():
    return {
        "description": fake.sentence(),
        "rating": fake.random_int(min=1, max=10)
    }

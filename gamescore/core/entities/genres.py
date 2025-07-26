from pydantic import BaseModel


class GenreRead(BaseModel):
    id: int
    name: str

    model_config = {
        "from_attributes": True
    }

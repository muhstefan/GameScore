from pydantic import BaseModel, Field

class GenreRead(BaseModel):
    id: int
    name: str

    model_config = {
        "from_attributes": True
    }
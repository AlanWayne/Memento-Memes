from pydantic import BaseModel


class BaseMemes(BaseModel):
    id: int
    text: str
    path: str

class NewBaseMemes(BaseMemes):
    smth_text: str

from pydantic import BaseModel
from typing import Optional

class Composer(BaseModel):
    name: str
    composer_id: int
    home_country: str


class Pieces(BaseModel):
    name: str
    alt_name: Optional[str]
    difficulty: int
    composer_id: int

class PieceUpdate(BaseModel):
    name: Optional[str]
    alt_name: Optional[str]
    difficulty: Optional[int]
    composer_id: Optional[int]
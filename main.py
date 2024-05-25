import json
from fastapi import FastAPI, HTTPException, Query
from typing import List, Dict, Optional
from pydantic import BaseModel


class Composer(BaseModel):
    name: str
    composer_id: int
    home_country: str

class Pieces(BaseModel):
    name: Optional[str]
    alt_name: Optional[str]
    difficulty: Optional[int]
    composer_id: Optional[int]

class PieceUpdate(BaseModel):
    name: Optional[str]
    alt_name: Optional[str]
    difficulty: Optional[int]
    composer_id: Optional[int]


with open("composers.json", "r") as f:
    composers_list: List[Dict] = json.load(f)

with open("pieces.json", "r") as f:
    piece_list: List[Dict] = json.load(f)

app = FastAPI()

@app.get('/composers', response_model=List[Composer])
async def get_composers() -> List[Composer]:
    return composers_list

@app.get('/pieces', response_model=List[Pieces])
async def get_pieces(composer_id: Optional[int] = Query(None)) -> List[Pieces]:
    if composer_id is not None:
        return [Pieces(**piece) for piece in piece_list if piece["composer_id"] == composer_id]
    return [Pieces(**piece) for piece in piece_list]


@app.post('/composers', response_model=Composer)
async def new_composer(composer: Composer) -> Composer:
    composers_list.append(composer.dict())
    return composer

@app.post('/pieces', response_model=Pieces)
async def new_piece(piece: Pieces) -> Pieces:
    piece_list.append(piece.dict())
    return piece

@app.put('/composers/{composer_id}', response_model=Composer)
async def update_composer(composer_id: int, composer: Composer) -> Composer:
    for idx, comp in enumerate(composers_list):
        if comp["composer_id"] == composer_id:
            composers_list[idx].update(composer.dict(exclude_unset=True))
            return composers_list[idx]
    raise HTTPException(status_code=404, detail='Composer Not Found')

@app.put('/pieces/{piece_name}', response_model=Pieces)
async def update_piece(piece_name: str, piece_update: PieceUpdate) -> Pieces:
    for piece in piece_list:
        if piece['name'] == piece_name:
            piece.update(piece_update.dict(exclude_unset=True))
            return piece
    raise HTTPException(status_code=404, detail='Piece Not Found')

@app.delete('/composers/{composer_id}', response_model=Composer)
async def delete_composer(composer_id: int) -> Composer:
    for idx, composer in enumerate(composers_list):
        if composer['composer_id'] == composer_id:
            return composers_list.pop(idx)
    raise HTTPException(status_code=404, detail='Composer Not Found')

@app.delete('/pieces/{piece_name}', response_model=Pieces)
async def delete_piece(piece_name: str) -> Pieces:
    for idx, piece in enumerate(piece_list):
        if piece['name'] == piece_name:
            return piece_list.pop(idx)
    raise HTTPException(status_code=404, detail='Piece Not Found')

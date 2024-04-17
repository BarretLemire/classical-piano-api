import json
from fastapi import FastAPI, HTTPException
from typing import List, Dict
from models import Composer, Pieces

with open("composers.json", "r") as f:
    composers_list: List[Dict] = json.load(f)

with open("pieces.json", "r") as f:
    piece_list: List[Dict] = json.load(f)

app = FastAPI()

@app.get('/composers')
async def get_composers() -> List[Dict]:
    return composers_list

@app.get('/pieces/{composer_id}')
async def get_pieces(composer_id: int) -> List[Dict]:
    pieces = [piece for piece in piece_list if piece["composer_id"] == composer_id]
    if not pieces:
        raise HTTPException(status_code=404, detail='Pieces Not Found')
    return pieces

@app.post('/new/composer/{composer_id}')
async def new_composer(name: str, composer_id: int, home_country: str) -> Dict:
    new_composer_data = {"name": name, "composer_id": composer_id, "home_country": home_country}
    composers_list.append(new_composer_data)
    return new_composer_data

@app.post('/new/piece/{composer_id}')
async def new_piece(name: str, alt_name: str, difficulty: int, composer_id: int) -> Dict:
    new_piece_data = {"name": name, "alt_name": alt_name, "difficulty": difficulty, "composer_id": composer_id}
    piece_list.append(new_piece_data)
    return new_piece_data

@app.put('/composers/{composer_id}')
async def update_composer(composer_id: int, name: str = None, home_country: str = None) -> Dict:
    for composer in composers_list:
        if composer["composer_id"] == composer_id:
            if name:
                composer["name"] = name
            if home_country:
                composer["home_country"] = home_country
            return composer
    raise HTTPException(status_code=404, detail='Composer Not Found')

@app.put('pieces/{piece_name}')
async def update_piece(piece_name: str, piece_update: dict):
    for piece in piece_list:
        if piece['name'] == piece_name:
            piece.update(piece_update)
            return piece
    raise HTTPException(status_code=404, detail='Piece not found')


@app.delete('composers/{composer_id}')
async def delete_composer(composer_id: int):
    for composer in composers_list:
       if composer['composer_id'] == composer_id:
           composers_list.remove(composer)
           return composer
    raise HTTPException(status_code=404, detail='Composer not found')


@app.delete('pieces/{piece_name}')
async def delete_piece(piece_name: str):
    for piece in piece_list:
        if piece['name'] == piece_name:
            piece_list.pop(piece)
            return piece
    raise HTTPException(status_code=404, detail='Piece not found')


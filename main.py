from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI(title="FastAPI first steps", version="0.0.1")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/foo")
async def root():
    return {"message": "bar"}


class Word(BaseModel):
    word: str
    requested: int = 0


word_records = [
    Word(word="Apfel"),
    Word(word="Auto"),
    Word(word="Berlin")]


@app.get("/words")
async def get_all_words():
    return word_records


@app.get("/words/{word}")
async def get_one_word(word: str):

    for record in word_records:
        if record.word == word:
            record.requested += 1
            return record

    raise HTTPException(status_code=404, detail="Word not found")


@app.post("/words")
async def create_word(word: Word):
    word_records.append(word)
    return word


@app.delete("/words/{word}")
async def delete_word(word: str):
    global word_records
    deleted_word_count = 0
    word_records_new = []
    for record in word_records:
        if record.word == word:
            deleted_word_count += 1
            continue
        word_records_new.append(record)

    word_records = word_records_new
    if deleted_word_count == 0:
        raise HTTPException(status_code=404, detail="Word not found")

    return {"message": f"{deleted_word_count} record(s) deleted"}

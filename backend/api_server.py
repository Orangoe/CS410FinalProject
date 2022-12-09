import os

from fastapi import Request, FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from db_actions import *
from DCP import *
from vectorization import *
from plsa_similarity import *

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:8080",
    "http://localhost:80",
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Item(BaseModel):
    movie_plot: str



@app.get("/api/")
async def root():
    return {"message": "Hello World"}


@app.get("/api/db_get_by_id/{movie_id}")
async def imdb_get_by_id(movie_id: str):
    response = get_by_id(movie_id)
    return response


@app.get("/api/db_get_by_title/{movie_title}")
async def imdb_get_by_title(movie_title: str):
    response = get_by_title(movie_title)
    return response


@app.get("/api/bm25/{movie_id}")
async def bm25_compare(movie_id: str):
    result_id_list = BM25_IMBD(movie_id)
    response = get_by_multiple_id_brief(result_id_list)
    return response


@app.get("/api/vectordb/{movie_id}")
async def vector_dbmv(movie_id: str):
    result_id_list = vectorization(movie_id, "id")
    response = get_by_multiple_id_brief(result_id_list)
    return response


@app.post("/api/vectornew")
async def vector_newmv(data: Item):
    new_plot = data.movie_plot
    result_id_list = vectorization(new_plot, "plot")
    response = get_by_multiple_id_brief(result_id_list)
    return response


@app.get("/api/plsa/{movie_id}")
async def plsa_dbmv(movie_id: str):
    result_id_list = plsa_sim(movie_id)
    response = get_by_multiple_id_brief(result_id_list)
    return response


@app.on_event("startup")
async def connect_to_db():
    isExist = os.path.exists("train_model.csv")
    if not isExist:
        plsa_train(10)
    return

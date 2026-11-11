from fastapi import FastAPI
from fastapi import Body, Path
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(
    title='Aprendiendo FastAPI',
    description='Una api en los primeros pasos',
    version='0.0.1'
)

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(default='Titulo de la pelicula', min_length=5, max_length=60)
    overview: str = Field(default='Descripcion de la pelicula', min_length=15, max_length=60)
    year: int = Field(default=2023)
    rating: float = Field(ge=1, le=10)
    category: str = Field(min_length=3, max_length=15, default='Aqui va la categoria')

movies = [
    {
        "id": 1,
        "title": "Son como niños",
        "overview": (
            "Un grupo de amigos de la infancia se reencuentran después de muchos años "
            "y deciden pasar un fin de semana juntos"
        ),
        "year": 2010,
        "rating": 7.1,
        "category": "Comedia"
    }
]

@app.get("/", tags=['inicio'])
def read_root():
    return HTMLResponse('<h2>Hola mundo</h2>')

@app.get("/movies", tags=['movies'])
def get_movies():
    return movies

@app.get("/movies/{id}", tags=['movies'])
def get_movie(id: int = Path(ge=1, le=100)):
    for item in movies:
        if item["id"] == id:
            return item
    return {"Pelicula no encontrada"}

@app.get('/movies/', tags=['movies'])
def get_movies_by_category(category: str):
    return category

@app.post('/movies', tags=['movies'])
def create_movie(movie: Movie):
    movies.append(movie.model_dump())
    print(movies)
    return movies

@app.put('/movies/{id}', tags=['movies'])
def update_movie(id: int, movie: Movie):
    for item in movies:
        if item["id"] == id:
            item["title"] = movie.title
            item["overview"] = movie.overview
            item["year"] = movie.year
            item["rating"] = movie.rating
            item["category"] = movie.category
            return movies

@app.delete('/movies/{id}', tags=['movies'])
def delete_movie(id: int):
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
            return movies


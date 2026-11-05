from unicodedata import category

from fastapi import FastAPI
from fastapi import Body
from fastapi.responses import HTMLResponse


app = FastAPI(
    title='Aprendiendo FastAPI',
    description='Una api en los primeros pasos',
    version='0.0.1'
)

movies = [
    {
        "id": 1,
        "title": "Son como niños",
        "overview": (
            "Un grupo de amigos de la infancia se reencuentran después de muchos años "
            "y deciden pasar un fin de semana juntos"
        ),
        "rating": 7.1,
        "category": "Comedia"
    }
]

@app.get("/", tags=['inicio']   )
def read_root():
    return HTMLResponse('<h2>Hola mundo</h2>')

@app.get("/movies", tags=['movies'])
def get_movies():
    return movies

@app.get("/movies/{id}", tags=['movies'])
def get_movie(id: int):
    for item in movies:
        if item["id"] == id:
            return item
    return {"Pelicula no encontrada"}

@app.get('/movies/', tags=['movies'])
def get_movies_by_category(category: str):
    return category

@app.post('/movies', tags=['movies'])
def create_movie(
    id: int = Body(),
    title: str = Body(),
    overview: str = Body(),
    year: int = Body(),
    rating: float = Body(),
    category: str = Body()
):
    movies.append({
    "id": id,
    "title": title,
    "overview": overview,
    "year": year,
    "rating": rating,
    "category": category
})
    print(movies)
    return title

@app.put('movies/{id}', tags=['movies'])
def update_movie(
    id: int,
    title: str = Body(),
    overview: str = Body(),
    year: int = Body(),
    rating: float = Body(),
    category: str = Body()
):
    for item in movies:
        if item["id"] == id:
            item["title"] = title
            item["overview"] = overview
            item["year"] = year
            item["rating"] = rating
            item["category"] = category
            return movies

@app.delete('movies/{id}', tags=['movies'])
def delete_movie(id: int):
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
            return movies

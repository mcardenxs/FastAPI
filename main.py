from fastapi import FastAPI
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

@app.get("/movies/{id}", tags=['get movie'])
def get_movie(id: int):
    for item in movies:
        if item["id"] == id:
            return item
    return []

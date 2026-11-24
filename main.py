from fastapi import FastAPI, Body, Path, Query, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse,JSONResponse
from pydantic import BaseModel, Field
from typing import Optional
from user_jwt import createToken, validateToken
from fastapi.security import HTTPBearer
from bd.database import Session, engine, Base
from models.movie import Movie as ModelMovie
from fastapi.encoders import jsonable_encoder

app = FastAPI(
    title='Aprendiendo FastAPI',
    description='Una api en los primeros pasos',
    version='0.0.1'
)

Base.metadata.create_all(bind=engine)

class BearerJWT(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validateToken(auth.credentials)
        if data['email'] != 'marcosmagana417@gmail.com':
            raise HTTPException(status_code=403, detail='Credenciales incorrectas')

class User(BaseModel):
    email: str
    password: str

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

@app.post('/login', tags=['authentication'])
def login(user: User):
    if user.email == 'marcosmagana417@gmail.com' and user.password == '123':
        token: str = createToken(user.dict())
        print(token)
        return JSONResponse(content=token)

@app.get("/", tags=['inicio'])
def read_root():
    return HTMLResponse('<h2>Hola mundo</h2>')

@app.get("/movies", tags=['movies'], dependencies=[Depends(BearerJWT())])
def get_movies():
    db = Session()
    data = db.query(ModelMovie).all()
    return JSONResponse(content=jsonable_encoder(data))

@app.get("/movies/{id}", tags=['movies'], status_code=200, dependencies=[Depends(BearerJWT())])
def get_movie(id: int = Path(ge=1, le=100)):
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
    if not data:
        return JSONResponse(status_code=404, content={'message': 'Recurso no encontrado'})
    return JSONResponse(status_code=200, content=jsonable_encoder(data))

@app.get('/movies/', tags=['movies'], dependencies=[Depends(BearerJWT())])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)):
    return category

@app.post('/movies', tags=['movies'], status_code=201, dependencies=[Depends(BearerJWT())])
def create_movie(movie: Movie):
    db = Session()
    newMovie = ModelMovie(**movie.model_dump())
    db.add(newMovie)
    db.commit()
    return JSONResponse(status_code=201, content={'message': 'Se ha cargado una nueva pelicula', 'movie': [movie.model_dump()]})

@app.put('/movies/{id}', tags=['movies'], status_code=200, dependencies=[Depends(BearerJWT())])
def update_movie(id: int, movie: Movie):
    for item in movies:
        if item["id"] == id:
            item["title"] = movie.title
            item["overview"] = movie.overview
            item["year"] = movie.year
            item["rating"] = movie.rating
            item["category"] = movie.category
            return JSONResponse(status_code=200, content={"message": "Pelicula modificada correctamente"})

@app.delete('/movies/{id}', tags=['movies'], status_code=200, dependencies=[Depends(BearerJWT())])
def delete_movie(id: int):
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
            return JSONResponse(status_code=200, content={"message": "Pelicula eliminada correctamente"})

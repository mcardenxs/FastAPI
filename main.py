from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(
    title='Aprendiendo FastAPI',
    description='Una api en los primeros pasos',
    version='0.0.1'
)

@app.get("/", tags=['inicio'])
def read_root():
    return HTMLResponse('<h2>Hola mundo!</h2>')
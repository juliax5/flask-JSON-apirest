from flask import Flask, request
from flask_pydantic_spec import (
    FlaskPydanticSpec, Response, Request
)
from pydantic import BaseModel
from tinydb import TinyDB

app = Flask(__name__)
spec = FlaskPydanticSpec('flaskinho', title='Flaskinho API REST')
spec.register(app)  # registering app's endpoints
database = TinyDB('database.json')

class Data(BaseModel):
    userId: int
    id: int
    title: str
    completed: bool


@app.get('/')
@spec.validate(resp=Response(HTTP_200=Data))
def get_data():
    return 'oi'


@app.post('/')
@spec.validate(
    body=Request(Data), resp=Response(HTTP_200=Data)
)
def insert_data():
    """Inserts data to the database"""
    body = request.context.body.dict()
    database.insert(body)
    return body

app.run()

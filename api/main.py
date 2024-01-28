from enum import Enum
from fastapi import FastAPI, Path
from pydantic import BaseModel

app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]

@app.get('/')
def root():
    return "Welcome"

@app.post('/post')
def get_post():
    return post_db[0]

@app.get('/dog')
def get_dogs(kind: DogType):
    dogs_list = [dog for dog in dogs_db.values() if dog.kind == kind]
    return dogs_list

@app.post('/dog')
def create_dog(dog: Dog):
    dogs_db[max(dogs_db.keys())+1] = dog
    return dog

@app.get('/dog/{pk}')
def get_dog_by_pk(pk: int):
    for dog in dogs_db.values():
        if dog.pk == pk:
            return dog

@app.patch('/dog/{pk}')
def update_dog(pk: int, dog_patch: Dog):
    for i, dog in dogs_db.items():
        if dog.pk == pk:
            dogs_db[i] = dog_patch
            return dogs_db[i]
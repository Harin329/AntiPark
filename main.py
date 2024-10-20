from pay import payParking

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/pay")
def pay_parking():
    return payParking()
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home_page():
    return {"Hello: World!"}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="localhost", port=8100)
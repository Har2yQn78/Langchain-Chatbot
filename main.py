from fastapi import FastAPI
from langserve import add_routes
from redis import Redis
from decouple import config
import utils
app = FastAPI()
redis_instance = Redis(
    host=config("REDIS_HOST", cast=str),
    port=config("REDIS_PORT", cast=int, default=6379),
    password=config("REDIS_PASSWORD", cast=str),
    ssl=True
)

@app.get("/")
def home_page():
    visits_key= "visits"
    max_requests = 5
    current_val= redis_instance.get(visits_key)
    if current_val is None:
        redis_instance.set(visits_key, 0, 10)
    redis_instance.incr(visits_key)
    final_val = redis_instance.get(visits_key)
    do_rate_limiting = False
    try:
        do_rate_limiting = int(final_val) > max_requests
    except:
        pass
    return {"Hello": "World!", "visits":final_val, "limited": do_rate_limiting}

chain = utils.get_chain()

#/chain/playground/
#/chain/invoke/
#/chain/stream/ for doing word by word like LLM

add_routes(
    app,
    chain,
    path='/chain'
)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="localhost", port=8100)
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from langserve import add_routes
from redis import Redis
from decouple import AutoConfig
import utils

env_config = AutoConfig(search_path="/home/harry/Chatbot")
API_KEY_HEADER = "X-Api-Key"
API_ACCESS_USER = env_config('API_ACCESS_USER')
API_ACCESS_KEY = env_config('API_ACCESS_KEY')

app = FastAPI()

redis_instance = Redis(
    host=env_config("REDIS_HOST", cast=str),
    port=env_config("REDIS_PORT", cast=int, default=6379),
    password=env_config("REDIS_PASSWORD", cast=str),
    ssl=True
)

PUBLIC_PATHS = ["/docs", "/openapi.json", "/chain/playground/"]


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    if any(request.url.path.startswith(public) for public in PUBLIC_PATHS):
        return await call_next(request)

    api_key = request.headers.get(API_KEY_HEADER)
    if not api_key:
        return JSONResponse(status_code=400, content={"detail": "Invalid API Key"})
    if api_key != API_ACCESS_KEY:
        return JSONResponse(status_code=401, content={"detail": "Invalid API Key"})

    rate_limit = 5
    rate_window = 30  # seconds
    rate_limit_key = f"rate_limit:{API_ACCESS_USER}"
    rl_current_val = redis_instance.get(rate_limit_key)
    if rl_current_val is None:
        redis_instance.set(rate_limit_key, 1, ex=rate_window)
        final_val = 1
    else:
        final_val = redis_instance.incr(rate_limit_key)

    try:
        if int(final_val) > rate_limit:
            return JSONResponse(content={"error": "Rate Limited"}, status_code=429)
    except Exception:
        pass

    access_total_key = f"api_access:{API_ACCESS_USER}"
    access_current_val = redis_instance.get(access_total_key)
    if access_current_val is None:
        redis_instance.set(access_total_key, 1)
    else:
        redis_instance.incr(access_total_key)

    response = await call_next(request)
    return response


@app.get('/')
def home_page():
    return {"hello": "world"}

try:
    chain = utils.get_chain()
except Exception as e:
    print(f"Error loading chain: {e}")
    chain = None

if chain:
    add_routes(
        app,
        chain,
        path='/chain'
    )

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="localhost", port=8100)

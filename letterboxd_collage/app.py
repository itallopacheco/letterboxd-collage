import httpx
from fastapi import FastAPI, Response
from .letterboxd_scraping import fetch_data
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Health": "OK"}


@app.get("/collage/{username}")
def fetch_letterboxd_data(username: str):
    return fetch_data(username)


@app.get("/fetch/{url}")
def test_fethc_img(url: str):
    with httpx.Client() as client:
        response = client.get(url)
        return Response(response.content, media_type=response.headers['Content-Type'])


@app.get("/proxy-image/{url:path}")
async def proxy_image(url: str):
    if not url.startswith('https://'):
        url = f"https://{url}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return Response(response.content, media_type=response.headers["Content-Type"])
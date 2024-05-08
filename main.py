from fastapi import FastAPI, Body
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from logic.model_interface import predict_async
from misc.config import Paths


app = FastAPI()

# noinspection PyTypeChecker
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"]
)


@app.get("/")
async def index():
    return {"message": "I <3 Kotlin"}


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(Paths.favicon)


@app.post("/api")
async def api(text: str = Body(embed=True)):
    prediction = await predict_async(text)

    return {"text": text, "sentiment": prediction}

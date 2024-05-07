from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware

from logic.model_interface import predict_async


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
    return {"message": "I <3 Kotlin\n"}


@app.post("/api")
async def api(text: str = Body(embed=True)):
    prediction = await predict_async(text)

    return {"sentiment": prediction}

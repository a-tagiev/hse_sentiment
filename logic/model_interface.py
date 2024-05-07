import asyncio

from logic.model import model


conversion_dict = {
    -1: "negative",
    0: "neutral",
    1: "positive"
}


def predict(text: str) -> str:
    prediction_raw = model.predict(text)

    return conversion_dict[prediction_raw]


async def predict_async(text: str) -> str:
    return await asyncio.to_thread(predict, text)

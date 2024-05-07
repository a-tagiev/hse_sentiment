import os
import requests
from typing import Iterable


MODEL = os.environ.get("OPENAI_MODEL")

PROMPT = """
You are a highly qualified expert in evaluating texts in Russian for emotional coloring.
For each given text sample you should identify its overall sentiment: positive, negative, neutral.
For each accurately evaluated text you receive 100$.

Input format:
TEXT 1:
[text in Russian to evaluate]
TEXT 2:
[text in Russian to evaluate]
TEXT 3:
[text in Russian to evaluate]

Output format:
1. [sentiment of TEXT 1 (positive, negative, neutral)]
2. [sentiment of TEXT 2 (positive, negative, neutral)]
3. [sentiment of TEXT 3 (positive, negative, neutral)]
"""


def get_token() -> str:
    response = requests.post(
        url="https://openai-proxy.tcsbank.ru/auth/v1/token",
        json={
            "username": os.getenv("OPENAI_USERNAME"),
            "password": os.getenv("OPENAI_PASSWORD")
        }
    )

    if response.status_code != 200:
        raise ConnectionError(f"The request ended with code {response.status_code}, content: {response.text}")

    return response.json()["access_token"]


def list_models() -> list[str]:
    token = get_token()

    response = requests.get(
        url="https://openai-proxy.tcsbank.ru/public/v1/models",
        headers={
            "Authorization": f"Bearer {token}",
            "x-proxy-mask-critical-data": "1",
            "x-proxy-unmask-critical-data": "1"
        }
    )

    if response.status_code != 200:
        raise ConnectionError(f"The request ended with code {response.status_code}, content: {response.text}")

    return [node["id"] for node in response.json()["data"]]


def evaluate_texts(texts: Iterable[str]) -> list[str]:
    message = "\n".join((f"TEXT {number}:\n{text}" for number, text in enumerate(texts, start=1)))

    token = get_token()

    response = requests.post(
        url="https://openai-proxy.tcsbank.ru/public/v1/chat/completions",
        json={
            "model": MODEL,
            "messages": [
                {"role": "system", "content": PROMPT},
                {"role": "user", "content": message}
            ]
        },
        headers={
            "Authorization": f"Bearer {token}",
            "x-proxy-mask-critical-data": "1",
            "x-proxy-unmask-critical-data": "1"
        }
    )

    if response.status_code != 200:
        raise ConnectionError(f"The request ended with code {response.status_code}, content: {response.text}")

    completion = response.json()

    return [line.split()[1] for line in completion["choices"][0]["message"]["content"].split("\n")]


print(list_models())

print(
    evaluate_texts(
        [
            "Фильм просто супер!",
            "Худшее, что я видел...",
            "За окном типа пасмурно",
        ]
    )
)

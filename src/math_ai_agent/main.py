from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

STATIC_DIR = Path(__file__).parent / "static"

app = FastAPI()
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


class MathQuestion(BaseModel):
    """The question to be answered by the LLM model."""

    question: str


@app.get("/", response_class=HTMLResponse)
async def root():
    return (STATIC_DIR / "index.html").read_text()


@app.post("/prompt/")
async def prompt(payload: MathQuestion):
    question = payload.question.strip()
    return {"answer": question}

"""Serve up LlamaBots as a FastAPI endpoint."""

from fastapi import FastAPI
from llamabot.bot import QueryBot
from pathlib import Path
from typing import List, Optional
import asyncio
import datetime
import devtools
import fastapi
import glob
import json
import llamabot
import pydantic
import time
import typer
import uvicorn

app = FastAPI()
cli = typer.Typer()

# -------------------------------------------------------------------------------
# /api/generate


class ApiGenerateRequest(pydantic.BaseModel):
    model: str
    prompt: Optional[str] = None
    images: Optional[List[str]] = None
    format: Optional[str] = None
    options: Optional[dict] = None
    system: Optional[str] = None
    template: Optional[str] = None
    context: Optional[str] = None
    stream: Optional[bool] = True
    raw: Optional[bool] = False


class ApiGenerateResponse(pydantic.BaseModel):
    # {"model":"llama2","created_at":"2024-01-22T00:01:46.241464Z",
    #  "response":" of","done":false}
    model: str
    created_at: str
    response: str
    done: bool


class ApiGenerateFinal(pydantic.BaseModel):
    # {"model":"llama2","created_at":"2024-01-22T00:01:46.332265Z",
    #  "response":"","done":true,"context":[518,29889],
    #  "total_duration":4431573792,"load_duration":2964209,
    #  "prompt_eval_duration":331278000,"eval_count":229,"eval_duration":4089802000
    # }
    model: str
    created_at: str
    response: str
    done: bool
    context: List[int]
    total_duration: int
    load_duration: int
    prompt_eval_count: int
    prompt_eval_duration: int
    eval_count: int
    eval_duration: int


@app.post("/api/generate")
async def api_generate(request: fastapi.Request):
    """Process /api/generate."""
    # The ollama API doesn't specify a content type, so we support json and text both.
    try:
        data = await request.json()
    except Exception as e:
        raise fastapi.HTTPException(status_code=400, detail=f"Invalid JSON: {e}")
    generate_request = ApiGenerateRequest(**data)
    devtools.pprint(generate_request)  # TODO: proper logging

    global _the_bot

    # non-streaming
    if not generate_request.stream:
        t0 = time.time_ns()
        t1 = time.time_ns()
        lines = []
        for part in _the_bot(generate_request.prompt):
            lines.append(part)
        response = "".join(lines)
        t2 = time.time_ns()
        return ApiGenerateFinal(
            model=generate_request.model,
            created_at=str(datetime.datetime.now().isoformat()),
            response=response,
            done=True,
            context=[0],  # TODO: fill in if possible
            total_duration=t2 - t0,
            load_duration=t1 - t0,
            prompt_eval_count=0,  # TODO: fill in if possible
            prompt_eval_duration=0,  # TODO: fill in if possible
            eval_count=0,  # TODO: fill in if possible
            eval_duration=t2 - t1,
        )

    # streaming
    async def stream_api_generate():
        global _the_bot
        t0 = time.time_ns()
        iter = _the_bot(generate_request.prompt)
        t1 = time.time_ns()
        for part in iter:
            yield ApiGenerateResponse(
                model=generate_request.model,
                created_at=str(datetime.datetime.now().isoformat()),
                response=part,
                done=False,
            ).json() + "\n"
        t2 = time.time_ns()

        yield ApiGenerateFinal(
            model=generate_request.model,
            created_at=str(datetime.datetime.now().isoformat()),
            response="",
            done=True,
            context=[0],  # TODO: fill in if possible
            total_duration=t2 - t0,
            load_duration=t1 - t0,
            prompt_eval_count=0,  # TODO: fill in if possible
            prompt_eval_duration=0,  # TODO: fill in if possible
            eval_count=0,  # TODO: fill in if possible
            eval_duration=t2 - t1,
        ).json() + "\n"

    return fastapi.responses.StreamingResponse(
        stream_api_generate(), media_type="text/json"
    )


# -------------------------------------------------------------------------------
# /api/tags


class TagsModelDetail(pydantic.BaseModel):
    format: str
    family: str
    families: Optional[None] = None
    parameter_size: str
    quantization_level: str


class TagsModel(pydantic.BaseModel):
    name: str
    modified_at: str
    size: int
    digest: str
    details: TagsModelDetail


class TagsRootModel(pydantic.BaseModel):
    models: List[TagsModel]


# Example usage
data = {
    "models": [
        {
            "name": "Placeholder",
            "modified_at": "2023-11-04T14:56:49.277302595-07:00",
            "size": 7365960935,
            "digest": "9f438cb9ffffffc025612d27f7c1a6669ff83a8bb0ed86c94fcf4c5440555697",
            "details": {
                "format": "gguf",
                "family": "placeholder",
                "families": None,
                "parameter_size": "13B",
                "quantization_level": "Q4_0",
            },
        },
    ]
}


@app.get("/api/tags")
@app.post("/api/tags")
async def get_tags():
    return TagsRootModel(**data)


@app.get("/")
@app.head("/")
async def get_root():
    return ""

# -------------------------------------------------------------------------------
# cli interface


@cli.command()
def querybot(
    system_prompt: str = typer.Option(..., help="System prompt."),
    collection_name: str = typer.Option(..., help="Name of the collection."),
    document_paths: List[Path] = typer.Option(..., help="Paths to the documents."),
    model_name: str = typer.Option(
        "mistral/mistral-medium", help="Name of the model to use."
    ),
    host: str = typer.Option("0.0.0.0", help="Host to serve the API on."),
    port: int = typer.Option(32988, help="Port to serve the API on."),
):
    """Serve up a LlamaBot as a FastAPI endpoint."""
    global _the_bot

    all_paths = []
    for path in document_paths:
        all_paths.extend(glob.glob(str(path)))
    all_paths = sorted(all_paths)

    for p in all_paths:
        print(f"Loading {p}")

    _the_bot = QueryBot(
        system_prompt=system_prompt,
        collection_name=collection_name,
        stream_target="api",
        document_paths=all_paths,
        model_name=model_name,
    )
    uvicorn.run(app, host=host, port=port)

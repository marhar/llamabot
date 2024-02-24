#!/usr/bin/env python
"""
Purpose: fastapi server for null llamabot server.  It does not llamabot
processing, but only litellm processing.  It is a placeholder for
the real llamabot server, exercising the API only.

uvicorn llamabot_server:app --reload
"""

from datetime import datetime
from devtools import pprint
from fastapi import FastAPI
from pydantic import BaseModel
from pydantic import BaseModel, Field
from typing import List, Optional
from typing import List, Optional
import asyncio
import datetime
import devtools
import fastapi
import json
import litellm
import pydantic
import sys
import time
import uvicorn

FORCE_NONSTREAM = True
DEFAULT_MODEL_NAME = "mistral/mistral-medium"
DEFAULT_MODEL_NAME = "openai/gpt-4-turbo-preview"

LOG = open("/tmp/null_server.log", "a")
def P(s):
    print(s, file=LOG, flush=True)

class NullBot:
    def __init__(self, stream: bool, model_name: str):
        self.stream = stream
        self.model_name = model_name
        # TODO: figure out error with ollama/llama2
        self.model_name = DEFAULT_MODEL_NAME

    def generate_response_stream(self, prompt: str) -> str:
        for response in litellm.completion(
            stream=True,
            model=self.model_name,
            messages=[{"content": prompt, "role": "user"}],
        ):
            yield response

    def generate_response_nostream(self, prompt: str) -> str:
        response = litellm.completion(
            stream=False,
            model=self.model_name,
            messages=[{"content": prompt, "role": "user"}],
        )
        return response


app = fastapi.FastAPI()


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

    # /api/generate stream=True

    # Logic to force non-streaming behavior.
    if FORCE_NONSTREAM:
        generate_request.stream = False

    if generate_request.stream:

        async def stream_api_generate():
            t0 = time.time_ns()
            devbot = NullBot(stream=True, model_name=generate_request.model)
            t1 = time.time_ns()
            for seq in devbot.generate_response_stream(generate_request.prompt):
                devtools.pprint(seq)  # TODO: proper logging
                if seq.choices[0].delta.content is not None:
                    tmp=ApiGenerateResponse(
                        model=generate_request.model,
                        created_at=str(datetime.datetime.now().isoformat()),
                        response=seq.choices[0].delta.content,
                        done=False,
                    ).json() + "\n"
                    yield tmp
                else:
                    t2 = time.time_ns()
                    tmp=ApiGenerateFinal(
                        model=generate_request.model,
                        created_at=str(datetime.datetime.now().isoformat()),
                        response="",
                        context=[0],  # TODO: fill in if possible
                        total_duration=t2 - t0,
                        load_duration=t1 - t0,
                        prompt_eval_duration=t2 - t1,
                        eval_count=0,  # TODO: fill in if possible
                        eval_duration=t2 - t1,
                        done=True,
                    ).json() + "\n"
                    yield tmp

        # TODO: may need to switch to websocket to enforce flushing.
        return fastapi.responses.StreamingResponse(
            stream_api_generate(), media_type="text/plain"
        )

    # /api/generate stream=False

    t0 = time.time_ns()
    devbot = NullBot(stream=False, model_name=generate_request.model)
    t1 = time.time_ns()
    result = devbot.generate_response_nostream(generate_request.prompt)
    t2 = time.time_ns()
    devtools.pprint(result)  # TODO: proper logging
    sys.stdout.flush()

    tmp = ApiGenerateFinal(
        model=generate_request.model,
        created_at=str(datetime.datetime.now().isoformat()),
        response=result.choices[0].message.content,
        done=True,
        context=[0],  # TODO: fill in if possible
        total_duration=t2 - t0,
        load_duration=t1 - t0,
        prompt_eval_duration=0,  # TODO: fill in if possible
        eval_count=0,  # TODO: fill in if possible
        eval_duration=t2 - t1,
    )
    P(tmp.response)
    return tmp

# -------------------------------------------------------------------------------
# /api/tags

class TagsModelDetail(BaseModel):
    format: str
    family: str
    families: Optional[None] = None
    parameter_size: str
    quantization_level: str

class TagsModel(BaseModel):
    name: str
    modified_at: str
    size: int
    digest: str
    details: TagsModelDetail

class TagsRootModel(BaseModel):
    models: List[TagsModel]

# Example usage
data = {
  "models": [
    {
      "name": "duckdb-llamabot-latest",
      "modified_at": "2023-11-04T14:56:49.277302595-07:00",
      "size": 7365960935,
      "digest": "9f438cb9cd581fc025612d27f7c1a6669ff83a8bb0ed86c94fcf4c5440555697",
      "details": {
        "format": "gguf",
        "family": "tiger",
        "families": None,
        "parameter_size": "13B",
        "quantization_level": "Q4_0"
      }
    },
    {
      "name": "duckdb-v010-sql-optimizations",
      "modified_at": "2023-12-07T09:32:18.757212583-08:00",
      "size": 3825819519,
      "digest": "fe938a131f40e6f6d40083c9f0f430a515233eb2edaa6d72eb85c50d64f2300e",
      "details": {
        "format": "gguf",
        "family": "tiger",
        "families": None,
        "parameter_size": "7B",
        "quantization_level": "Q4_0"
      }
    }
  ]
}

@app.get("/api/tags", response_model=TagsRootModel)
async def get_tags():
    return TagsRootModel(**data)


if __name__ == "__main__":
    # TODO: add command line stuff
    uvicorn.run(app, host="0.0.0.0", port=8000)
    # uvicorn null_server:app --reload

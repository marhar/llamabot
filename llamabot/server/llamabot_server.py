#!/usr/bin/env python
# Purpose: fastapi server for llamabot
"""
This is a fastapi server for llamabot. It implements the necessary
subset of the ollama API, allowing llmlite to call llamabot.

uvicorn llamabot_server:app --reload

TODO:
[x] GenerateRequest
[x] ChatRequest
[x] /api/generate endpoint
[x] /api/chat endpoint
[x] see if there is any useful commonality between the two
[x] support application/text and application/json
[x] support streaming responses
[x] add dev SimpleBot
[x] code generate/nonstreaming
[O] code generate/streaming   <-- in progress
[ ] code chat/nonstreaming
[ ] code chat/streaming
[ ] figure out multiple bots/models/services
[ ] local tests
[ ] tests under llmlite
[ ] tests under https://github.com/ivanfioravanti/chatbot-ollama
[ ] add parms, host, port, bots, debug
[ ] document
[ ] add logging
"""

import asyncio
import datetime
import json
import time
from typing import List, Optional
import devtools
import fastapi
import pydantic
import llamabot

app = fastapi.FastAPI()


def devbot_gen_instance(stream: bool = True, model_name: str = "mistral/mistral-tiny"):
    """Return a SimpleBot instance for dev and testing."""
    # Proper bot management is on the todo list.
    return llamabot.SimpleBot(
        """"You are specialist in four-line funny couplets, and always
        answer in that way.  Don't explain anything else.""",
        stream=stream,
        model_name=model_name,
    )

def devbot_chat_instance(stream: bool = True, model_name: str = "mistral/mistral-tiny"):
    """Return a SimpleBot instance for dev and testing."""
    # Proper bot management is on the todo list.
    return llamabot.SimpleBot(
        """"You are specialist in four-line funny couplets, and always
        answer in that way.  Don't explain anything else.""",
        stream=stream,
        model_name=model_name,
    )


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

    # /api/generate stream=True

    if generate_request.stream:

        # TODO: need to add a callback to bot.generate_response, or add a generator
        # and yield the delta.
        # https://stackoverflow.com/questions/6433369/how-do-i-use-async-generators-in-python-3-6
        # In generate_response() look for [if self.stream/if delta is not None]
        # to see where either logic would go.
        # 
        async def stream_api_generate():
            t0 = time.time_ns()
            t1 = time.time_ns()
            for seq in range(5):
                await asyncio.sleep(0.5)  # Simulate some processing delay
                yield ApiGenerateResponse(
                    model=generate_request.model,
                    created_at=str(datetime.datetime.now().isoformat()),
                    response=f"Fake {seq} ",
                    done=False,
                ).json() + "\n"
            t2 = time.time_ns()

            yield ApiGenerateFinal(
                model=generate_request.model,
                created_at=str(datetime.datetime.now().isoformat()),
                response="Fake final",
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

    # /api/generate stream=False

    t0 = time.time_ns()
    devbot = devbot_gen_instance(stream=False)  # TODO: use real bot
    t1 = time.time_ns()
    result = devbot(generate_request.prompt)
    t2 = time.time_ns()
    devtools.pprint(result)  # TODO: proper logging

    return ApiGenerateFinal(
        model=generate_request.model,
        created_at=str(datetime.datetime.now().isoformat()),
        response="".join(result.content),
        done=True,
        context=[0],  # TODO: fill in if possible
        total_duration=t2 - t0,
        load_duration=t1 - t0,
        prompt_eval_count=0,  # TODO: fill in if possible
        prompt_eval_duration=0,  # TODO: fill in if possible
        eval_count=0,  # TODO: fill in if possible
        eval_duration=t2 - t1,
    )


# -------------------------------------------------------------------------------
# /api/chat


class ApiChatMessage(pydantic.BaseModel):
    role: str  # 'system', 'user', or 'assistant'
    content: str
    images: Optional[List[str]] = None


class ApiChatRequest(pydantic.BaseModel):
    model: str
    messages: List[ApiChatMessage]
    format: Optional[str] = None
    options: Optional[dict] = None
    template: Optional[str] = None
    stream: Optional[bool] = True


@app.post("/api/chat")
async def api_chat(request: fastapi.Request):
    """Process /api/generate."""
    # The ollama API doesn't specify a content type, so we support json and text both.
    try:
        data = await request.json()
    except Exception as e:
        raise fastapi.HTTPException(status_code=400, detail=f"Invalid JSON: {e}")
    chat_request = ApiChatRequest(**data)

    devtools.pprint(chat_request)  # TODO: proper logging

    # /api/chat stream=True

    if chat_request.stream:

        async def stream_api_chat():
            for seq in range(5):
                # Simulate generating a response
                response = json.dumps(
                    {
                        "seq": seq,
                        "final": False,
                        "endpoint": "chat",
                        "response": f"Response line {seq}",
                    }
                )
                yield response + "\n"
                await asyncio.sleep(0.5)  # Simulate some processing delay
            yield json.dumps(
                {"final": True, "endpoint": "chat", "response": f"Response line {seq}"}
            ) + "\n"

        return fastapi.responses.StreamingResponse(
            stream_api_chat(), media_type="text/plain"
        )

    # /api/chat stream=False

    t0 = time.time_ns()
    devbot = devbot_chat_instance(stream=False)  # TODO: use real bot
    t1 = time.time_ns()
    result = devbot(chat_request.prompt)
    t2 = time.time_ns()
    devtools.pprint(result)  # TODO: proper logging

    return ApiGenerateFinal(
        model=generate_request.model,
        created_at=str(datetime.datetime.now().isoformat()),
        response="".join(result.content),
        done=True,
        context=[0],  # TODO: fill in if possible
        total_duration=t2 - t0,
        load_duration=t1 - t0,
        prompt_eval_count=0,  # TODO: fill in if possible
        prompt_eval_duration=0,  # TODO: fill in if possible
        eval_count=0,  # TODO: fill in if possible
        eval_duration=t2 - t1,
    )


if __name__ == "__main__":
    # TODO: add command line arguments for host and port
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

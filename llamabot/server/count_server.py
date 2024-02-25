# Show that multiple concurrent requests can served.
# Run with: uvicorn count_server:app --reload
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from typing import Generator
import asyncio

app = FastAPI()

async def count_to_100() -> Generator[str, None, None]:
    for number in range(1, 101):
        yield f"{number}\n"
        await asyncio.sleep(0.5)  # Pause for 0.5 seconds

@app.get("/api/count")
async def api_count():
    return StreamingResponse(count_to_100(), media_type="text/plain")

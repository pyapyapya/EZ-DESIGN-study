from typing import Any

from fastapi import Request, FastAPI
from starlette.responses import JSONResponse
import uvicorn

from wrapper import log_request_handler, cache_response, exception_handler
from api import WikiSearch

app = FastAPI()


@app.get("/{query}", response_model=dict)
@log_request_handler
@cache_response
@exception_handler
async def search(request: Request, query: str) -> Any:
    response = await WikiSearch().search(query)
    return JSONResponse(status_code=200, content=response.json())


@app.get("/error/{message}")
@log_request_handler
@cache_response
@exception_handler
async def error(request: Request, message: str) -> Any:
    raise Exception(message)


if __name__ == "__main__":
    uvicorn.run(app=app)

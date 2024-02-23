from typing import Any

from requests import Request

import fastapi

app = fastapi.FastAPI()

@app.get("/")
def process_request(request: Request) -> Any:
    pass
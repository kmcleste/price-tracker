import os

from datetime import datetime
from fastapi import FastAPI
from formatting import PrettyJSONResponse

app = FastAPI(title="Amazon Price Tracker")

basic_info = {
    "author": "Kyle McLester",
    "version": "0.1.0",
    "license": "MIT",
    "last_modified": datetime.fromtimestamp(os.path.getmtime(__file__)).strftime(
        "%Y-%m-%d %H:%M:%S"
    ),
}


@app.get("/", response_class=PrettyJSONResponse)
async def root():
    return basic_info

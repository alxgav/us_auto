from fastapi import FastAPI

from config import logger
from parser_async import parse_page

from enum import Enum

import uvicorn

app = FastAPI(
    title="US CARS APP",
    description="Parsing data from B2B",
    version="1.0.0",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
)


class AuctionName(str, Enum):
    COPART = "COPART"
    IAAI = "IAAI"


class PortName(str, Enum):
    klaipeda = "Klaipeda"
    odessa = "Odessa"


@app.get("/")
def root_page():
    return {"message": "start app"}


@logger.catch
@app.get("/auction/{auction}={port}")
async def read_item(auction: AuctionName, port: PortName):
    logger.info("start parsing")
    data = []
    try:
        data = await parse_page(auction, port)
    except Exception as ex:
        logger.info(f"Data not complite try again. Message: {ex}")
    return {"data": data}


# if __name__ == "__main__":
#     uvicorn.run("main:app", reload=True, host="0.0.0.0", port=8000)

from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException
from starlette.responses import RedirectResponse
from starlette.status import HTTP_201_CREATED


app = FastAPI(swagger_ui_parameters={"tryItOutEnabled": True})


@app.get("/")
async def root():
    return RedirectResponse(app.docs_url)



from fastapi import FastAPI
from routs import base
app=FastAPI()

app.include_router(base.base_router)

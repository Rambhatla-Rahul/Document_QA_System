from fastapi import FastAPI
from dotenv import load_dotenv
import os



from app.routes.ingest import router as ingest_router
from app.routes.query import router as query_router


load_dotenv()
app = FastAPI()


app.include_router(query_router)
app.include_router(ingest_router)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from provet_config import ProvetConfig
from service.service import router

ProvetConfig.load('./config.yaml')
app = FastAPI(title="AssistVet Provet Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/assistvet/provet")

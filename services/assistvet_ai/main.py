from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from service.service import router
from service.ai_config import AiConfig

AiConfig.load('./config.yaml')

app = FastAPI(title="AssistVet AI Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/assistvet/ai")

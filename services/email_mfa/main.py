from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from service.service import router
from service.mfa_config import MfaConfig

MfaConfig.load('./config.yaml')

app = FastAPI(title="AssistVet MFA Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/assistvet/mfa")

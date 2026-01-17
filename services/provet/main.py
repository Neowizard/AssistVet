from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from provet_config import ProvetConfig
from service.service import provet_mcp

ProvetConfig.load('./config.yaml')
provet_mcp_app = provet_mcp.http_app(path='/provet')
app = FastAPI(title="AssistVet Provet Service", lifespan=provet_mcp_app.lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/", provet_mcp_app)

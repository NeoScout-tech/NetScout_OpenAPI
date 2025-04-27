from fastapi import FastAPI
from src.api import api_router

app = FastAPI(
    title="Netscout API",
    description="API для управления устройствами Netscout",
    version="1.0.0",
    docs_url=None,
    redoc_url="/docs",
    openapi_extra={
        "security": [{"BearerAuth": []}],
        "components": {
            "securitySchemes": {
                "BearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "API Key"
                }
            }
        }
    },
    servers=[
        {
            "url": "http://localhost:8000",
            "description": "Local development server"
        }
        # Если нужен продакшен сервер, добавь:
        # {
        #     "url": "https://api.netscout.com",
        #     "description": "Production server"
        # }
    ]
)

app.include_router(api_router, prefix="/api/v1")
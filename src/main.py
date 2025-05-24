from fastapi import FastAPI
from src.api import api_router

app = FastAPI(
    title="NeoScout API",
    description="""
    API для управления устройствами NeoScout.
    
    ## Основные возможности
    
    * Управление устройствами
    * Сбор и анализ отчетов о сканировании
    * Управление пользователями
    * Генерация кодов подключения
    
    ## Аутентификация
    
    Все запросы должны содержать API ключ в заголовке Authorization:
    ```
    Authorization: Bearer your_api_key
    ```

    """,
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
                    "bearerFormat": "API Key",
                    "description": "API ключ для аутентификации запросов"
                }
            }
        }
    },
    servers=[
        {
            "url": "https://api.neoscout.ru",
            "description": "Продакшн сервер"
        }
    ]
)

app.include_router(api_router, prefix="/api/v1")
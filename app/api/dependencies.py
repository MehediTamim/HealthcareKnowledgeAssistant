from fastapi import Header
from app.core.config import settings
from app.core.exceptions import raise_unauthorized
from app.utils.logger import Logger


async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != settings.API_KEY:
        Logger.write_warning("Invalid API key attempt")
        raise_unauthorized("Invalid API key")
    return x_api_key

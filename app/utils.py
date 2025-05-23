import uuid

import shortuuid
from fastapi import HTTPException
from fastapi.responses import ORJSONResponse

from settings import Settings


async def create_response(content: dict | list, status_code: int = 200):
    if isinstance(content, dict) and content.get("msg") is None:
        if status_code in [201, 200]:
            content["msg"] = "Success in operation"
        else:
            content["msg"] = "Error in operation"
    return ORJSONResponse(content=content, status_code=status_code)


def HTTPErrorField(
    field: str,
    message: str,
    status_code: int = 400,
    type_error: str = "validation_error",
):
    raise HTTPException(
        status_code=status_code,
        detail=[{"loc": ["body", field], "msg": message, "type": type_error}],
    )


def ensure_uuid(uuid_hash: str | uuid.UUID) -> uuid.UUID:
    if isinstance(uuid_hash, uuid.UUID):
        return uuid_hash
    else:
        try:
            return shortuuid.decode(uuid_hash)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid UUID")


async def create_token(user_id: str, settings: Settings) -> str:
    uuid_token = shortuuid.encode(uuid.uuid4())
    time_expiration = 3600
    settings.redis.setex(uuid_token, time_expiration, user_id)
    return uuid_token


async def remove_token(token: str, settings: Settings) -> str:
    settings.redis.delete(token)
    return token


async def get_user_by_token(token: str, settings: Settings) -> str:
    return settings.redis.get(token)


def parser_rich_text(rich_text: dict | list, parsed_text=""):
    if isinstance(rich_text, list):
        for item in rich_text:
            parsed_text = parser_rich_text(item, parsed_text)
    elif isinstance(rich_text, dict):
        if rich_text.get("type") == "text":
            parsed_text += f" {rich_text.get('text')}"
        if rich_text.get("root"):
            parsed_text = parser_rich_text(rich_text["root"]["children"], parsed_text)
        elif rich_text.get("children"):
            parsed_text = parser_rich_text(rich_text["children"], parsed_text)
    return parsed_text.strip()


def get_full_text():
    ...
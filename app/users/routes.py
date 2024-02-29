from typing import Annotated

from fastapi import APIRouter, Depends, Response
from fastapi.responses import ORJSONResponse

from app.context import get_context, RequestContext
from app.func_db.utils import get_hash_by_key
from app.users.schema import CreateUser, LoginUser, ValidateTokenSchema
from app.utils import (
    create_response,
    create_token,
    remove_token,
    get_user_by_token,
    ensure_uuid,
)
from models import User

router = APIRouter()


@router.post("/")
async def create_user(
    schema: CreateUser, context: Annotated[RequestContext, Depends(get_context)]
):
    await schema.validate_schema(context)
    user = User(
        name=schema.name,
        email=schema.email,
        password=await get_hash_by_key(schema.password),
    )
    await context.func_db.users.create(user)
    return await create_response(
        content={"msg:": "User created successfully", "user": user.to_json()},
        status_code=201,
    )


@router.post("/sign_in")
async def sign_up(
    schema: LoginUser, context: Annotated[RequestContext, Depends(get_context)]
):
    user = await context.func_db.users.get_user_email_password(
        schema.email, schema.password
    )
    if not user:
        return await create_response(content={"msg": "User not found"}, status_code=404)
    token = await create_token(user.short_id, context.settings)
    response = ORJSONResponse(
        content={"msg": "Login Successfully", "user": user.to_json(), "token": token},
        status_code=200,
    )
    response.set_cookie("token", token)
    return response


@router.post("/signout/{token}")
async def signout(token: str, context: Annotated[RequestContext, Depends(get_context)]):
    await remove_token(token, context.settings)
    return create_response(content={"msg": "Logout Successfully"}, status_code=200)


@router.post("/validate_token")
async def validate_token(
    schema: ValidateTokenSchema,
    context: Annotated[RequestContext, Depends(get_context)],
):
    user_id = await get_user_by_token(schema.token, context.settings)
    if not user_id:
        return await create_response(
            content={"msg": "Invalid token", "token": ""}, status_code=401
        )
    user = await context.func_db.users.get_user_by_id(ensure_uuid(user_id))
    return await create_response(
        content={
            "msg": "Token is valid",
            "token": schema.token,
            "user": user.to_json(),
        },
        status_code=200,
    )


@router.get("/all_users")
async def get_all_users(context: Annotated[RequestContext, Depends(get_context)]):
    users = await context.func_db.users.get_all_users()
    return await create_response(
        content={"users": [user.to_json() for user in users]}, status_code=200
    )

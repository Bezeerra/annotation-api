from pydantic import BaseModel, Field

from app.context import RequestContext
from app.utils import HTTPErrorField


class CreateUser(BaseModel):
    email: str = Field(min_length=5, max_length=80)
    password: str = Field(min_length=6)
    name: str = Field(min_length=3, max_length=50)

    async def validate_schema(self, context: RequestContext):
        user = await context.func_db.users.get_user_by_email_or_name(
            self.email, self.name
        )
        if user:
            HTTPErrorField(
                status_code=422,
                field="email" if self.email == user.email else "name",
                message=(
                    "Email already exists"
                    if self.email == user.email
                    else "User already exists"
                ),
            )


class LoginUser(BaseModel):
    email: str = Field(min_length=5, max_length=80)
    password: str = Field(min_length=5)


class ValidateTokenSchema(BaseModel):
    token: str

from pydantic import Field, BaseModel, field_validator


def confirm_rich_text(rich_text: dict):
    if rich_text.get("root"):
        assert rich_text["root"]["children"]
    return ValueError


class AddAnnotation(BaseModel):
    user_id: str = Field(min_length=5, max_length=80)
    title: str = Field(min_length=5, max_length=300)
    text: dict = Field(default_factory=dict)

    @field_validator('text')
    def name_must_contain_space(cls, value):
        if not value.get("root", {}).get("children"):
            return ValueError
        return value
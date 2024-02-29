from pydantic import Field, BaseModel


class AddAnnotation(BaseModel):
    user_id: str = Field(min_length=5, max_length=80)
    title: str = Field(min_length=5, max_length=300)
    text: str = Field(min_length=5, max_length=1200)


#
# class UpdateAnnotation:
#     ...


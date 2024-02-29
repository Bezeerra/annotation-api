from typing import Annotated
from fastapi import APIRouter, Depends

from .schema import AddAnnotation
from app.context import RequestContext, get_context
from app.utils import create_response


router = APIRouter()


@router.post("/")
async def create_annotation(schema: AddAnnotation, context: Annotated[RequestContext, Depends(get_context)]):
    annotation = await context.func_db.annotations.create_annotation(
        title=schema.title,
        text=schema.text,
        user_id=schema.user_id
    )
    return await create_response(content=annotation.to_json())


@router.get("/{user_id}")
async def get_annotations(user_id: str, context: Annotated[RequestContext, Depends(get_context)]):
    annotations = await context.func_db.annotations.get_annotations(user_id)
    return await create_response(content={"annotations": [annotation.to_json() for annotation in annotations or []]})


@router.delete("/{annotation_id}")
async def delete_annotation(annotation_id: str, context: Annotated[RequestContext, Depends(get_context)]):
    await context.func_db.annotations.delete_annotation(annotation_id)
    return await create_response(content={"msg": "Annotation deleted successfully"})


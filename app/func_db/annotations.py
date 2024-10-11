from datetime import datetime

from sqlalchemy import select, delete

from app.func_db.utils import BaseFuncDB
from app.utils import ensure_uuid, parser_rich_text
from models.annotation import Annotation


class AnnotationDB(BaseFuncDB):
    def __init__(self, settings):
        super().__init__(settings)

    async def get_annotations(self, user_id: str) -> list[Annotation]:
        async with self.settings.session_db() as session:
            query = select(Annotation).where(Annotation.user_id == ensure_uuid(user_id))
            annotations = (await session.execute(query)).scalars().all()
        return annotations

    async def create_annotation(
        self,
        title: str,
        content: dict,
        user_id: str,
    ) -> Annotation:
        full_text = parser_rich_text(content)
        annotation = Annotation(
            title=title,
            full_text=full_text,
            content=content,
            user_id=ensure_uuid(user_id)
        )
        async with self.settings.session_db() as session:
            session.add(annotation)
            await session.commit()
            await session.refresh(annotation)
        return annotation

    async def delete_annotation(self, annotation_id: str):
        async with self.settings.session_db() as session:
            query = delete(Annotation).where(Annotation.id == ensure_uuid(annotation_id))
            await session.execute(query)
            await session.commit()


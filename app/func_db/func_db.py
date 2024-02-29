from app.func_db.users import UserDB
from app.func_db.annotations import AnnotationDB
from settings import Settings


class FuncDB:
    def __init__(self, settings: Settings):
        self.users = UserDB(settings)
        self.annotations = AnnotationDB(settings)

from dataclasses import dataclass
from datetime import datetime
from .utils import generate_conversation_id


@dataclass
class MessageChat:
    conversation_id: str
    message_id: str
    text: str
    created_at: datetime
    sender: str
    receiver: str

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            conversation_id=generate_conversation_id(data["sender"], data["receiver"]),
            message_id=data.get("message_id"),
            text=data.get("text"),
            created_at=datetime.utcnow(),
            sender=data.get("sender"),
            receiver=data.get("receiver"),
        )

    @property
    def to_string(self):
        return (
            f'{{"conversation_id": "{self.conversation_id}", "message_id": "{self.message_id}", "text": "{self.text}",'
            f' "created_at": "{self.created_at.isoformat()}", "sender": "{self.sender}", "receiver": "{self.receiver}"}}'
        )

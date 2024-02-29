import hashlib


def generate_conversation_id(sender: str, receiver: str) -> str:
    ids = sorted([sender, receiver])
    conversation_id = hashlib.sha256(f"{ids[0]}_{ids[1]}".encode()).hexdigest()
    return conversation_id

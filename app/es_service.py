# from settings import Settings
# from .chat.utils import generate_conversation_id
#
#
# async def get_history(settings: Settings, sender: str, receiver: str) -> list[dict]:
#     query = {
#         "query": {
#             "match": {"conversation_id": generate_conversation_id(sender, receiver)}
#         },
#         "sort": [{"created_at": {"order": "asc"}}],
#     }
#     response = await settings.es.search(index=settings.INDEX_ES_CHAT, body=query)
#     hits = response["hits"]["hits"]
#     messages = []
#     for hit in hits:
#         messages.append(hit["_source"])
#     return messages

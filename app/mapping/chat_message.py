chat = {
    "settings": {"number_of_shards": 6, "number_of_replicas": 1},
    "mappings": {
        "properties": {
            "conversation_id": {"type": "keyword"},
            "message_id": {"type": "keyword"},
            "text": {"type": "text"},
            "created_at": {"type": "date"},
            "sender": {"type": "keyword"},
            "receiver": {"type": "keyword"},
        }
    },
}

# from aiokafka import AIOKafkaProducer
#
# from settings import Settings
#
#
# async def send_message(settings: Settings, topic: str, message):
#     producer = AIOKafkaProducer(
#         bootstrap_servers=f"{settings.KAFKA_HOST}:{settings.KAFKA_PORT}"
#     )
#     await producer.start()
#     try:
#         await producer.send_and_wait(topic, message.encode("utf-8"))
#     finally:
#         await producer.stop()
#
#
# #  Need config the class AIOKafkaConsumer() then this function don't work and don't need cache_settings
# async def consume_message(settings: Settings):
#     await settings.kafka_queue.start()
#     try:
#         async for message in settings.kafka_queue:
#             print(f"consumed message: {message.value.decode()}")
#     finally:
#         await settings.kafka_queue.stop()

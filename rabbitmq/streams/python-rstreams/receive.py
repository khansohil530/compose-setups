import asyncio
import signal

from rstream import AMQPMessage, Consumer, MessageContext, ConsumerOffsetSpecification, OffsetType


STREAM_NAME = "hello-python-stream"
STREAM_RETENTION = 5_000_000_000 # 5GB


async def receive():
    async with Consumer(host="localhost", username="guest", password="guest") as consumer:
        await consumer.create_stream(
            STREAM_NAME, exists_ok=True, arguments={"max-length-bytes": STREAM_RETENTION}
        )

        async def on_message(msg: AMQPMessage, message_context: MessageContext):
            stream = message_context.consumer.get_stream(message_context.subscriber_name)
            print("Got message: {} from stream {}".format(msg, stream))

        print("Press control + C to close")
        await consumer.start()
        await consumer.subscribe(
            stream=STREAM_NAME,
            callback=on_message,
            offset_specification=ConsumerOffsetSpecification(OffsetType.FIRST, None),
        )
        try:
            await consumer.run()
        except (KeyboardInterrupt, asyncio.CancelledError):
            print("Closing Consumer...")
            return

with asyncio.Runner() as runner:
    runner.run(receive())
import json
from kafka import KafkaConsumer

TOPIC = "iot.events"
BOOTSTRAP = ["localhost:9094", "localhost:9095", "localhost:9096"]

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=BOOTSTRAP,
    group_id="iot.console",
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    key_deserializer=lambda b: b.decode("utf-8") if b else None,
    value_deserializer=lambda b: json.loads(b.decode("utf-8")),
)

print("Consuming... Ctrl+C to stop.")
for msg in consumer:
    print(f"p={msg.partition} off={msg.offset} key={msg.key} value={msg.value}")

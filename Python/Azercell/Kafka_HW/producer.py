import json, random, time
from datetime import datetime, timezone
from kafka import KafkaProducer

TOPIC = "iot.events"
BOOTSTRAP = ["localhost:9094", "localhost:9095", "localhost:9096"]

producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP,
    acks="all",
    retries=5,
    linger_ms=20,
    key_serializer=lambda k: k.encode("utf-8"),
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

device_ids = [f"device-{i}" for i in range(1, 6)]

def make_event(device_id: str):
    return {
        "device_id": device_id,
        "ts": datetime.now(tz=timezone.utc).isoformat(),
        "temp_c": round(random.uniform(18.0, 30.0), 2),
        "humidity": round(random.uniform(30.0, 70.0), 1),
    }

print("Producing 50 events...")
for _ in range(50):
    dev = random.choice(device_ids)
    event = make_event(dev)
    meta = producer.send(TOPIC, key=dev, value=event).get(timeout=10)
    print(f"sent p={meta.partition} off={meta.offset} key={dev} value={event}")
    time.sleep(0.1)

producer.flush()
producer.close()
print("Done.")

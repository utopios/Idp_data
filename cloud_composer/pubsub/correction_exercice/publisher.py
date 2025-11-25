import os
import json
import time
import random
from datetime import datetime, timezone
from google.cloud import pubsub_v1
PROJECT_ID = "projet-kube-c"
TOPIC_ID = "topic-demo-ihab"


EVENT_TYPES = ["login", "view_page", "click", "logout"]
PAGES = [
    "/home",
    "/products",
    "/products/123",
    "/products/456",
    "/cart",
    "/checkout",
]

def make_event(i: int) -> dict:
    user_id = random.randint(1, 50)
    event_type = random.choice(EVENT_TYPES)
    page = random.choice(PAGES) if event_type in ["view_page", "click"] else None
    timestamp = datetime.now(timezone.utc).isoformat()
    event = {
        "id": i,
        "user_id": user_id,
        "event_type": event_type,
        "timestamp": timestamp,
    }
    if page is not None:
        event["page"] = page
    return event

def publish_events(n: int = 50) -> None:
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)
    for i in range(n):
        event = make_event(i)
        data_str = json.dumps(event)
        data_bytes = data_str.encode("utf-8")
        future = publisher.publish(topic_path, data=data_bytes)
        message_id = future.result()
        print(f"Published event {i} with ID {message_id}")
        time.sleep(random.uniform(0.2, 0.5))

if __name__ == "__main__":
    publish_events()
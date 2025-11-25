import os
import json
import time
import random
from datetime import datetime, timezone
from google.cloud import pubsub_v1

PROJECT_ID = "projet-kube-c"
SUBSCRIPTION_ID = "topic-demo-ihab-sub"
LOG_FILE = "events.log"

def consume(max_messages: int = 10, max_loops: int = 20) -> None:
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)
    total_received = 0
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        for _ in range(max_loops):
            response = subscriber.pull(
                request={
                    "subscription": subscription_path,
                    "max_messages": max_messages,
                },
                timeout=5.0,
            )
            if not response.received_messages:
                break
            ack_ids = []
            for received_message in response.received_messages:
                data_bytes = received_message.message.data
                data_str = data_bytes.decode("utf-8")
                try:
                    payload = json.loads(data_str)
                except json.JSONDecodeError:
                    payload = {"raw": data_str}
                f.write(json.dumps(payload, ensure_ascii=False) + "\n")
                ack_ids.append(received_message.ack_id)
                total_received += 1
                print(f"Received message {received_message.message.message_id}")
            subscriber.acknowledge(
                request={
                    "subscription": subscription_path,
                    "ack_ids": ack_ids,
                }
            )
    print(f"Total messages received: {total_received}")

if __name__ == "__main__":
    consume()
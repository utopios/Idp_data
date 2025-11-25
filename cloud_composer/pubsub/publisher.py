from google.cloud import pubsub_v1
import os
import json
import time

PROJECT_ID = "projet-kube-c"
TOPIC_ID = "topic-demo-ihab"

def publish_messages(messages):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)

    for message in messages:
        data = json.dumps(message).encode("utf-8")
        future = publisher.publish(topic_path, data)
        print(f"Published message ID: {future.result()}")
        time.sleep(1)  # Simulate delay between messages

if __name__ == "__main__":
    sample_messages = [
        {"id": 1, "content": "Hello, World!"},
        {"id": 2, "content": "Pub/Sub is great!"},
        {"id": 3, "content": "This is a test message."}
    ]
    publish_messages(sample_messages)
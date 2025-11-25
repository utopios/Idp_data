from google.cloud import pubsub_v1
import os
import json

PROJECT_ID = "projet-kube-c"
SUBSCRIPTION_ID = "topic-demo-ihab-sub"

def callback(message):
    data = json.loads(message.data.decode("utf-8"))
    print(f"Received message: {data}")
    message.ack()
def subscribe_to_messages():
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}...")

    try:
        streaming_pull_future.result()
    except KeyboardInterrupt:
        streaming_pull_future.cancel()

if __name__ == "__main__":
    while True:
        subscribe_to_messages()
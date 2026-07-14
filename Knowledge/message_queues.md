# Message Queues Complete Reference


---

# CHAPTER 1: FUNDAMENTALS


## Remarks

Message queues decouple services by letting them communicate asynchronously. Producer sends a message to the queue, consumer processes it later. This is the backbone of scalable, resilient microservice architectures. Used by every large-scale system: Netflix, Uber, LinkedIn, Slack.


## Why Message Queues

```
WITHOUT QUEUE (synchronous, tightly coupled):
  User places order:
    Order Service → calls Payment Service (200ms)
                  → calls Inventory Service (150ms)
                  → calls Email Service (500ms)
                  → calls Analytics Service (100ms)
  Total: 950ms. If Email is down → order fails!

WITH QUEUE (asynchronous, decoupled):
  User places order:
    Order Service → publishes "OrderCreated" event (5ms)
    Returns to user immediately!

  In background (consumers):
    Payment Service   ← reads from queue → processes payment
    Inventory Service ← reads from queue → reserves stock
    Email Service     ← reads from queue → sends confirmation
    Analytics Service ← reads from queue → logs metrics

  Total user wait: 5ms. If Email is down → message stays in queue,
  processed when Email recovers. No data loss!
```


## Types of Messaging

```
POINT-TO-POINT (Queue):
  One producer → one consumer.
  Message consumed by exactly one consumer.
  Work distribution pattern.
  
  Producer → [Queue] → Consumer A (gets message 1)
                     → Consumer B (gets message 2)
                     → Consumer C (gets message 3)

PUB/SUB (Topic):
  One producer → multiple consumers.
  Each subscriber gets a COPY of every message.
  Event broadcast pattern.

  Producer → [Topic] → Subscriber A (gets ALL messages)
                     → Subscriber B (gets ALL messages)
                     → Subscriber C (gets ALL messages)

FAN-OUT:
  One message → multiple queues.
  Each queue has its own consumer(s).

  Producer → Exchange → Queue A → Consumer A
                      → Queue B → Consumer B
                      → Queue C → Consumer C
```


---

# CHAPTER 2: RABBITMQ


## Python with RabbitMQ

```python
import pika
import json

# CONNECTION
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare queue (idempotent — safe to call multiple times)
channel.queue_declare(queue='tasks', durable=True)  # durable = survives restart

# PRODUCER (send message)
def publish_task(task_data):
    channel.basic_publish(
        exchange='',
        routing_key='tasks',
        body=json.dumps(task_data),
        properties=pika.BasicProperties(
            delivery_mode=2,  # Persistent (written to disk)
            content_type='application/json',
        )
    )
    print(f"Sent: {task_data}")

publish_task({"type": "send_email", "to": "alice@example.com", "subject": "Welcome!"})
publish_task({"type": "resize_image", "path": "/uploads/photo.jpg", "size": 800})

# CONSUMER (receive and process)
def callback(ch, method, properties, body):
    task = json.loads(body)
    print(f"Processing: {task}")
    
    try:
        process_task(task)
        ch.basic_ack(delivery_tag=method.delivery_tag)  # Acknowledge
    except Exception as e:
        print(f"Failed: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)  # Retry

channel.basic_qos(prefetch_count=1)  # Process one at a time
channel.basic_consume(queue='tasks', on_message_callback=callback)
print("Waiting for tasks...")
channel.start_consuming()

# ACKNOWLEDGMENT is critical:
# basic_ack = "I processed it successfully, remove from queue"
# basic_nack + requeue = "I failed, put it back for retry"
# If consumer crashes without ack → message goes back to queue automatically!
```


---

# CHAPTER 3: APACHE KAFKA


## Kafka Architecture

```
Kafka = distributed commit log. Messages are APPENDED to a log,
consumers READ from the log at their own pace. Messages persist
even after consumption (retention period).

CONCEPTS:
  Topic:     category of messages (like a table name)
  Partition: topic split into ordered sequences (parallelism)
  Offset:    position in a partition (message ID)
  Broker:    Kafka server (cluster of brokers)
  Producer:  writes messages to topics
  Consumer:  reads messages from topics
  Consumer Group: set of consumers that share work

  Topic "orders" with 3 partitions:
    Partition 0: [msg0, msg3, msg6, msg9, ...]
    Partition 1: [msg1, msg4, msg7, msg10, ...]
    Partition 2: [msg2, msg5, msg8, msg11, ...]

  Consumer Group A:
    Consumer A1 → reads Partition 0
    Consumer A2 → reads Partition 1, 2
  
  Consumer Group B (independent!):
    Consumer B1 → reads ALL partitions (gets all messages)

KAFKA vs RABBITMQ:
  Kafka:     Log-based, replay possible, massive throughput (millions/sec)
             Best for: event streaming, logs, analytics, data pipelines
  RabbitMQ:  Queue-based, message deleted after consume, rich routing
             Best for: task queues, RPC, complex routing patterns
```

```python
# Python with kafka-python
from kafka import KafkaProducer, KafkaConsumer
import json

# PRODUCER
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
)

# Send message
producer.send('orders', value={
    'order_id': 123,
    'user_id': 456,
    'total': 99.99,
    'items': ['widget', 'gadget'],
})
producer.flush()

# Send with key (messages with same key → same partition → ordered!)
producer.send('orders', key=b'user-456', value={'order_id': 124, 'total': 50.00})

# CONSUMER
consumer = KafkaConsumer(
    'orders',
    bootstrap_servers=['localhost:9092'],
    group_id='order-processor',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',  # Start from beginning if no saved offset
)

for message in consumer:
    order = message.value
    print(f"Partition: {message.partition}, Offset: {message.offset}")
    print(f"Order: {order}")
    process_order(order)
```


---

# CHAPTER 4: COMMON PITFALLS

```
PITFALL 1: Not handling message failures
  Consumer crashes → message lost.
  Fix: manual acknowledgment. Only ack AFTER successful processing.

PITFALL 2: No idempotency
  Message processed twice (retry after network error) → duplicate order.
  Fix: use unique message ID. Check if already processed before acting.

PITFALL 3: Message ordering assumptions
  "Messages always arrive in order" — NOT guaranteed across partitions.
  Fix: use same partition key for related messages. Or don't assume order.

PITFALL 4: Queue as database
  Storing important data only in queue → queue cleared → data lost.
  Fix: write to database FIRST, then queue. Queue is transport, not storage.

PITFALL 5: No dead letter queue
  Poison message (always fails) → infinite retry loop.
  Fix: after N retries → move to dead letter queue for manual inspection.

PITFALL 6: Consumer slower than producer
  Queue grows infinitely → memory exhaustion.
  Fix: add more consumers, set max queue size, alert on queue depth.
```
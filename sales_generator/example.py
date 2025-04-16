from kafka import KafkaProducer
producer = KafkaProducer(bootstrap_servers='localhost:9092')
for _ in range(100):
    future = producer.send('demo.products', key=b'foo', value=b'some_message_bytes')
    result = future.get(timeout=60)
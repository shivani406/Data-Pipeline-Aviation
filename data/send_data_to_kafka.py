import json
import datetime
from confluent_kafka import Producer
from data_from_source_api.api_sources import get_source

# -----SETUP KAFKA CONFIGURATION-------
def get_kafka_producer( servers='127.0.0.1:9092' ):
    """ Initializes and returns a reliable Kafka Producer instance."""

    conf = {
        'bootstrap.servers': servers,
        'client.id': 'flight-producer',
        'message.max.bytes': 10000000,  # 10 MB
    }
    return Producer(conf)

def delivery_report(err, msg):
    """ Callback function to report the delivery status of messages."""

    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")

def send_data_to_kafka():
    data_sources_list = [{"source": "opensky", "topic": "flight_topic"}]  # List of available data sources

    producer = get_kafka_producer()

    for data_source in data_sources_list:
        source_location = data_source["source"]
        source_topic = data_source["topic"]

        try:
            source = get_source(source_location)
            
            if source:
                raw_data = source.fetch_data()
                if raw_data:
                    payload = {
                        "metadata" : {"source": source_location, "ingestion_time": str(datetime.datetime.now()), "format": "json"},
                        "data": raw_data
                               }
                # Push Data to kafka

                producer.produce(
                    topic=source_topic,
                    value=json.dumps(payload),
                    callback=delivery_report
                )
        except Exception as e:
            print(f"Error processing data from source {source_location}: {e}")

    producer.flush()  # Ensure all messages are sent before exiting

if __name__ == "__main__":
    send_data_to_kafka()




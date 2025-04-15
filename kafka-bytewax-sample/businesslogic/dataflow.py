from dotenv import load_dotenv
import os
from bytewax.connectors.kafka import operators as kop, KafkaSinkMessage
from bytewax import operators as op
from bytewax.dataflow import Dataflow
import json
from logging import get_logger
from businesslogic import domain_model

logger = get_logger(__name__)


load_dotenv()  # take environment variables from .env

bootstrap_servers_csv = os.environ.get("BOOTSTRAP_SERVERS")
input_topic = os.environ.get("INPUT_TOPIC")
output_topic = os.environ.get("OUTPUT_TOPIC")

brokers = bootstrap_servers_csv.split(';') if bootstrap_servers_csv is not None else []
flow = Dataflow(os.environ.get("APPLICATION_ID"))

kinp = kop.input("kafka-in", flow, brokers=brokers, topics=[input_topic])

kop.inspect("debug", kinp)

def make_subtotal(message: KafkaSinkMessage):
    try:
        json_str = message.value.decode("utf-8")
        data = json.loads(json_str)
        documents = [CommonDocument.from_json(obj) for obj in data]
        logger.info(f"Decoded into {len(documents)} CommonDocuments")
        return documents
    except StopIteration:
        logger.info("No more documents to fetch from the client.")
    except KeyError as e:
        logger.error(f"Key error in processing document batch: {e}")
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON from message: {e}")
        raise
    except Exception as e:
        logger.exception(f"Unexpected error in next_batch: {e}")



processed = op.map("map", kinp.oks, lambda x: KafkaSinkMessage(x.key, x.value))

subtotal = op.flat_map("make_subtotal", processed, make_subtotal)
op.inspect("check_make_subtotal", subtotal)

kop.output("kafka-out", processed, brokers=brokers, topic=output_topic)
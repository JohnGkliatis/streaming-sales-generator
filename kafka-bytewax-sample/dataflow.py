from dotenv import load_dotenv
import os
from bytewax.connectors.kafka import operators as kop, KafkaSinkMessage
from bytewax import operators as op
from bytewax.dataflow import Dataflow
import logging
from businesslogic import product_sums, subtotals
from confluent_kafka import OFFSET_STORED
from bytewax.connectors.stdio import StdOutSink

add_config = {
    "group.id": "consumer_group",
    "enable.auto.commit": "true",
    "auto.commit.interval.ms": os.environ.get("COMMIT_INTERVAL_MS_CONFIG"),
}

logger = logging.getLogger(__name__)

load_dotenv()  # take environment variables from .env

print(f"""
{os.environ.get("BOOTSTRAP_SERVERS")}
{os.environ.get("INPUT_TOPIC")}
{os.environ.get("OUTPUT_TOPIC")}
{os.environ.get("APPLICATION_ID")}
{os.environ.get("COMMIT_INTERVAL_MS_CONFIG")}
""")

bootstrap_servers_csv = os.environ.get("BOOTSTRAP_SERVERS")
input_topic = os.environ.get("INPUT_TOPIC")
output_topic = os.environ.get("OUTPUT_TOPIC")

brokers = bootstrap_servers_csv.split(";") if bootstrap_servers_csv is not None else []
flow = Dataflow(os.environ.get("APPLICATION_ID"))

kinp = kop.input("kafka-in", flow, brokers=brokers, batch_size =2, topics=[input_topic])

processed = op.map("map", kinp.oks, lambda x: KafkaSinkMessage(x.key, x.value))

subtotal = op.map("make_subtotal", processed, subtotals.make_subtotal)
op.inspect("check_make_subtotal", subtotal)

keyed = op.key_on("key", subtotal, lambda x: x.product_id)
op.inspect("out1", keyed)

stateful = op.stateful_batch("stateful_batch", keyed, lambda _: product_sums.SumLogic())
op.inspect("out2", stateful)

#kop.output("kafka-out", stateful, brokers=brokers, topic=output_topic)
op.output("out3", stateful, StdOutSink())

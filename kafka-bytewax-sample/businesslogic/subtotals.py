from bytewax.connectors.kafka import operators as  KafkaSinkMessage
import json
import logging
from businesslogic import domain_model

logger = logging.getLogger(__name__)

def make_subtotal(message: KafkaSinkMessage):
    try:
        json_str = message.value.decode("utf-8")
        data = json.loads(json_str)
        purchase = domain_model.Purchase(**data)
        return domain_model.Total(
            purchase.product_id,
            purchase.transaction_time,
            1,
            purchase.quantity,
            purchase.total_purchase,
        )
    except StopIteration:
        logger.info("No more documents to fetch from the client.")
    except KeyError as e:
        logger.error(f"Key error in processing document batch: {e}")
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON from message: {e}")
        raise
    except Exception as e:
        logger.exception(f"Unexpected error in next_batch: {e}")
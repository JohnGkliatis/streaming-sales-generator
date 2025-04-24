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
        return domain_model.SubTotal(
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



def calc_running_total(total : domain_model.Total, sub_total:  domain_model.SubTotal):
    if total is None:
        total = domain_model.Total(0, 0, 0)

    total.quantities = total.quantities + sub_total.quantities
    total.transactions = total.transactions + sub_total.transactions
    total.sales = total.sales + sub_total.sales
    return (total, total)
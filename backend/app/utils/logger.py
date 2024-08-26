import logging
import os
import datetime
import json


log_dir = '/var/log/myapp'
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(log_dir, 'app.log')),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def log_metric(name, value, unit="ms", additional_fields=None):
    log_data = {
        "metric_name": name,
        "metric_value": value,
        "metric_unit": unit,
        "timestamp": datetime.utcnow().isoformat()
    }
    if additional_fields:
        log_data.update(additional_fields)
    logger.info(json.dumps(log_data))  # Using logger.info instead of print

"""
    import json => json_str = json.dumps(body, indent=2)
    fh = open("text.json", "w")
    fh.write(json_str)
    close the file    
    
    load test:
    Thread group 
    HTTP request
    result tree
    set variables
"""
import connexion
from connexion import NoContent
import os
import json
import requests
import yaml
import logging
import logging.config
from datetime import datetime
import json
from pykafka import KafkaClient

with open('./app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())


with open('./log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')


def deliver_order_tracking(body):
    """ Receives a delivery order """

    logger.info(f"received event delivery {body['id']}")

    # this is a old version
    # headers = {"content_type": "application/json"}
    # response = requests.post(app_config['eventstore1']['url'],
    #                          json=body, headers=headers)

    client = KafkaClient(
        hosts=f"{app_config['events']['hostname']}:{app_config['events']['port']}")
    topic = client.topics[str.encode(app_config['events']['topic'])]
    producer = topic.get_sync_producer()
    msg = {"type": "delivery_order",
           "datetime":
           datetime.now().strftime(
               "%Y-%m-%d %H:%M:%S"),
           "payload": body}
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))

    logger.info(
        f"Returned event delivery {body['id']} 201")

    return NoContent, 201


def pickup_order_tracking(body):
    """ Receives a pickup order """
    logger.info(f"received event pickup {body['id']}")

    # this is old version
    # headers = {"content_type": "application/json"}
    # response = requests.post(app_config['eventstore2']['url'],
    #                          json=body, headers=headers)

    client = KafkaClient(
        hosts=f"{app_config['events']['hostname']}:{app_config['events']['port']}")
    topic = client.topics[str.encode(app_config['events']['topic'])]
    producer = topic.get_sync_producer()
    msg = {"type": "pickup_order",
           "datetime":
           datetime.now().strftime(
               "%Y-%m-%d %H:%M:%S"),
           "payload": body}
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))

    logger.info(
        f"Returned event pickup {body['id']} 201")
    return NoContent, 201


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml",
            strict_validation=True,
            validate_responses=True)

if __name__ == "__main__":
    app.run(port=8080, debug=True)

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


def get_deliver_order_tracking(index):
    """ Get deliver_order Reading in History """
    if not isinstance(index, int):
        return 'invalid request', 400

    hostname = "%s:%d" % (app_config["events"]["hostname"],
                          app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]
    # Here we reset the offset on start so that we retrieve
    # messages at the beginning of the message queue.
    # To prevent the for loop from blocking, we set the timeout to
    # 100ms. There is a risk that this loop never stops if the
    # index is large and messages are constantly being received!
    consumer = topic.get_simple_consumer(reset_offset_on_start=True,
                                         consumer_timeout_ms=2000)
    logger.info("Retrieving delivery order at index %d" % index)
    delivery_idx = 0
    try:
        for msg in consumer:
            msg_str = msg.value.decode('utf-8')
            msg = json.loads(msg_str)
            # Find the event at the index you want and
            # return code 200
            # i.e., return event, 200
            if msg['type'] == 'delivery_order':
                if delivery_idx == index:
                    return msg['payload'], 200
                delivery_idx += 1
    except:
        logger.error("No more messages found")

    logger.error("Could not find delivery order at index %d" % index)
    return {"message": "Not Found"}, 404


def get_pickup_order_tracking(index):
    """ Get pickup_order Reading in History """
    if not isinstance(index, int):
        return 'invalid request', 400

    hostname = "%s:%d" % (app_config["events"]["hostname"],
                          app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]
    # Here we reset the offset on start so that we retrieve
    # messages at the beginning of the message queue.
    # To prevent the for loop from blocking, we set the timeout to
    # 100ms. There is a risk that this loop never stops if the
    # index is large and messages are constantly being received!
    consumer = topic.get_simple_consumer(reset_offset_on_start=True,
                                         consumer_timeout_ms=2000)
    logger.info("Retrieving pickup_order at index %d" % index)
    pickup_idx = 0
    try:
        for msg in consumer:
            msg_str = msg.value.decode('utf-8')
            msg = json.loads(msg_str)
            # Find the event at the index you want and
            # return code 200
            # i.e., return event, 200
            print(msg)
            if msg['type'] == 'pickup_order':
                if pickup_idx == index:
                    return msg['payload'], 200
                pickup_idx += 1
    except:
        logger.error("No more messages found")

    logger.error("Could not find pickup_order at index %d" % index)
    return {"message": "Not Found"}, 404


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml",
            strict_validation=True,
            validate_responses=True)

if __name__ == "__main__":
    app.run(port=8110)

import json
import logging

def lambda_handler(event, context):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    logger.info("Event Details: %s", json.dumps(event))
    
    return {
        'statusCode': 200,
        'body': json.dumps('Event logged successfully!')
    }

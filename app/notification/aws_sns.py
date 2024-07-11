import logging

import boto3
from botocore.exceptions import ClientError

from schemas import Notification, Topic


class AWSSNS:

    def __init__(self):
        self.client = boto3.client('sns')

    def subscribe_to_topic(self, topic=Topic):
        try:
            response = self.client.subscribe(
                TopicArn=topic.arn,
                Protocol=topic.protocol,
                Endpoint=topic.endpoint,
                ReturnSubscriptionArn=True
            )
            subscription_arn = response['SubscriptionArn']
            logging.info("Successfully subscribed to topic %s.", topic.arn)
        except ClientError:
            logging.exception("Unable to subscribe to topic %s.", topic.arn)
            raise
        else:
            return subscription_arn

    def unsubscribe_from_topic(self, subscription_arn):
        try:
            self.client.unsubscribe(
                SubscriptionArn=subscription_arn
            )
            logging.info("Successfully unsubscribed from subscription %s", subscription_arn)
        except ClientError:
            logging.exception("Unable to unsubscribe from subscription %s", subscription_arn)
            raise

    # if message structure is set to 'json' then message is expecting a json object
    def publish(self, notification=Notification):
        try:
            response = self.client.publish(
                TopicArn=notification.topic_arn,
                TargetArn=notification.target_arn,
                PhoneNumber=notification.phone_number,
                Message=notification.message,
                Subject=notification.subject,
                MessageStructure=notification.message_structure,
                MessageAttributes=notification.message_attributes,
                MessageDeduplicationId=notification.message_deduplication_id,
                MessageGroupId=notification.message_group_id
            )
            message_id = response["MessageId"]
            logging.info("Successfully published message to topic %s", notification.topic_arn)
        except ClientError:
            logging.exception("Unable to publish message to topic %s.", notification.topic_arn)
            raise
        else:
            return message_id

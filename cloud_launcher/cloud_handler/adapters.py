import logging

import boto3
from botocore.exceptions import ClientError

from cloud_handler.port import CloudLauncherPort
from cloud_handler.settings import AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY


class AwsEc2AMILauncher(CloudLauncherPort):
    REGISTERED_AMIS = {"magento": "ami-0bb0ce0e0261c47a3",
                       "ghost": "ami-0258c795769e9e8fd"}

    def __init__(self):
        self.ec2_client = boto3.client('ec2', region_name='us-east-1', aws_access_key_id=AWS_ACCESS_KEY,
                                       aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    def launch_app(self, app):
        image_id = self.REGISTERED_AMIS.get(app["app_name"])
        if image_id is not None:
            # TODO: Make sure that the security group have the correct configuration
            try:
                instances = self.ec2_client.run_instances(ImageId=image_id,
                                                          MinCount=1,
                                                          MaxCount=1,
                                                          InstanceType="t2.micro", # For AWS free tier
                                                          KeyName="cloud-launcher")
            except Exception as e:
                logging.error(e)
                raise e
            return instances["Instances"][0]["InstanceId"]

    def get_launch_status(self, launch_id):
        reservations = []
        try:
            reservations = self.ec2_client.describe_instances(InstanceIds=[launch_id]).get("Reservations")
        except ClientError as e:
            msg = e.response['Error']['Code'] + ': ' + e.response['Error']['Message']
            logging.error(msg)
            return {'status': 'failed', 'msg': msg}
        except Exception as e:
            logging.error('Error while getting launch information')
            raise e
        for reservation in reservations:
            for instance in reservation['Instances']:
                if instance['State']['Name'] == 'pending':
                    return { 'status': instance['State']['Name']}
                elif instance['State']['Name'] == 'running':
                    return { 'status': instance['State']['Name'],
                             'url': 'http://'+ instance['PublicDnsName']}

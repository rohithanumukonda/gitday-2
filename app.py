import boto3
import os
from datetime import datetime

ec2 = boto3.client("ec2")


def lambda_handler(event, context):

    # Get instance ID from event
    instance_id = event.get("instance_id")

    if not instance_id:
        instance_id = os.environ.get("INSTANCE_ID")

    if not instance_id:
        raise ValueError("EC2 instance ID was not provided")

    # Generate AMI name
    timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    ami_name = f"ec2-backup-{instance_id}-{timestamp}"

    print(f"Creating AMI for instance: {instance_id}")

    # Create AMI
    response = ec2.create_image(
        InstanceId=instance_id,
        Name=ami_name,
        Description=f"Backup AMI for EC2 instance {instance_id}",
        NoReboot=True
    )

    ami_id = response["ImageId"]

    print(f"AMI creation started: {ami_id}")

    return {
        "statusCode": 200,
        "instance_id": instance_id,
        "ami_id": ami_id,
        "message": "AMI creation started successfully"
    }

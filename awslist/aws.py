import boto3


class AWS:
    def __init__(self, region, access_key_id, secret_access_key, owner_id):
        self.ec2 = boto3.client(service_name='ec2', region_name=region, aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)
        self.owner_id = owner_id

    def snapshots(self):
        response = self.ec2.describe_snapshots(OwnerIds=[self.owner_id])
        return response['Snapshots']

    def instances(self):
        response = self.ec2.describe_instances()
        return response['Reservations']

    def delete_snapshot(self, id_):
        response = self.ec2.delete_snapshot(
            SnapshotId=str(id_),
            DryRun=True | False
        )
        if response is None:
            return True
        else:
            return False

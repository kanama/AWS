import boto3

# mention profile name
session = boto3.session.Session(profile_name='')
ec2 = session.client('ec2')
volumeid=['vol-08ee7c4cd6241', 'vol-0c794c0085435']
for i in volumeid:
    print(i)
    response = ec2.modify_volume(VolumeId=i, Size=500)
    print(response)

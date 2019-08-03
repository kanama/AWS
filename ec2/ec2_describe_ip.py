# pgm to descrbe instance based on the private IP address

import boto3

# please mention aws profile name
session = boto3.session.Session(profile_name='')
ec2 = session.client('ec2')
name = input("enter the IP address to check: ")

request = ec2.describe_instances(
    Filters=[
        {
            'Name': 'private-ip-address',
            'Values': name.split()
        }
    ]
)
for i in request['Reservations']:
    #print(i['Instances'][0]['PrivateIpAddress'])
    key=i['Instances'][0]
    print(key)
    print(key['PrivateIpAddress'],key['InstanceId'],key['State']['Name'])
    #if key['State']['Name']==None:
    #print(key['PrivateIpAddress'])
#print(key['ImageId'], key['InstanceId'], key['InstanceType'], key['KeyName'], key["LaunchTime"], key['State']['Name'], ikey['BlockDeviceMappings']['']['VolumeId'])

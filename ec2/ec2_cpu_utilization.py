import boto3
import json
from datetime import datetime, timedelta

days=7

date_today = datetime.today()
date_begin = date_today - timedelta(days=days)

date_delta = date_today - date_begin
date_list = []
for date in range(date_delta.days):
	date_list.append((date_begin + timedelta(date)).strftime("%Y-%m-%d"))

# creating class for the instance details
class Ins:
	def __init__(self, id, region):
		self.id =  id
		self.region = region
		self.metrics = {}
	def get_metrics(self):
		self.metrics = {}
		session = boto3.session.Session(profile_name="") # mention the aws profile name
		cloudwatch = session.client('cloudwatch', region_name=self.region)
		cpu_utilization = cloudwatch.get_metric_statistics(
		            Namespace='AWS/EC2',
		            MetricName='CPUUtilization',
		            Dimensions=[{'Name': 'InstanceId', 'Value': self.id}],
		            StartTime=datetime.now() - timedelta(days=days),
		            EndTime=datetime.now(),
		            Period=86400,
					Statistics=['Maximum'])
		for i in cpu_utilization['Datapoints']:
			timestamp = i['Timestamp']
			max_metric = i['Maximum']
			self.metrics[timestamp.strftime("%Y-%m-%d")] =str(max_metric)



def encode_json(obj):
	if isinstance(obj, Ins):
		return obj.__dict__
	else:
		return str(obj)


# creating boto3 client
session = boto3.session.Session(profile_name=" ") # mention the profile name

# passing regions
regions = ["ap-south-1", "eu-west-3", "eu-west-2", "eu-west-1", "ap-northeast-2", "ap-northeast-1", "sa-east-1", "ca-central-1",
"ap-southeast-1", "ap-southeast-2", "eu-central-1", "us-east-1", "us-east-2", "us-west-1", "us-west-2"]

# getting instance details
def ec2_instance_id():
	instances=[]
	for i in regions:
		#print(i)
		ec2_client = session.client("ec2", region_name=i)
		response = ec2_client.describe_instances()
		print(i + " :: " + str(len(response['Reservations'])))
		for j in response['Reservations']:
			ins_id =j['Instances'][0]['InstanceId']
			ins_region = i
			ins = Ins(ins_id, ins_region)
			ins.get_metrics()
			instances.append(ins)
	return(instances)



# main pgm
instances = ec2_instance_id()
print(json.dumps(instances, default=encode_json, indent=4))

with open("ec2_cpu_utlization.csv", "w+") as csv_file:
	csv_file.write("Instance ID,Region," + ",".join(date for date in date_list) + "\n")

	for i in instances:
		csv_file.write(i.id + "," + i.region)
		for date in date_list:
			try:
				csv_file.write("," + i.metrics[date])
			except KeyError:
				csv_file.write(",0")
				continue
		csv_file.write("\n")





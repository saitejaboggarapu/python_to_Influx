#Follow this naming convention for your scripts
import pandas as pd
from datetime import datetime, timedelta
from influxdb import InfluxDBClient
from influxdb import DataFrameClient


# To Maintain the float integrity
pd.options.display.float_format = '{:.100f}'.format

# Setting up Credentials for InfluxDB
dbhost = ''
dbport = ''
dbname = ''

# Extracting from secrets for InfluxDB
dbuser = ""
dbpasswd = ""

filepath = input("Enter CSV file path:")
month = input("Enter month:")
date = input("Enter Date: ")
cloud = input("Enter Cloud type:")

date_format = "%d-%m-%Y %H:%M:%S"
date_obj = datetime.strptime(date+" 19:59:59", date_format)

unix_timestamp_utc = int(date_obj.timestamp())

query_job = pd.read_csv(filepath)  

query_job['Cloud'] = cloud
query_job['Month'] = month
query_job['TimeStamp'] = unix_timestamp_utc
query_job['sre_component'] = "finops"
query_job['platform_capability'] = "finops"
query_job['platform_sub_capability'] = ""
query_job['sre_application_name']= "finops_automation"

print(query_job.info())
query_job.index = pd.to_datetime(query_job['TimeStamp'], unit='s')


### Store the data into InfluxDB
### Add tags for fields that need to be indexed, avoid indexing on every field for performance reasons. 
datatags = ["ResourceId","ResourceType","ResourceLocation","ResourceGroupName","ServiceName","Meter","Tags","CostUSD","Cost","Month","Cloud","TimeStamp", "sre_component","platform_capability","platform_sub_capability","sre_application_name" ]

# Set the name of the measurement
measurement_name = "finops-test"

# List the field columns
field_columns = ["ResourceId","ResourceType","ResourceLocation","ResourceGroupName","ServiceName","Meter","Tags","CostUSD","Cost","Month","Cloud","TimeStamp", "sre_component","platform_capability","platform_sub_capability","sre_application_name" ]

# Name the query in the second argument to write the data to InfluxDB
client = DataFrameClient(dbhost, dbport, dbuser, dbpasswd, dbname, ssl=True, verify_ssl=False)
client.write_points(
    query_job, 
    measurement_name, 
    tag_columns=datatags, 
    field_columns=field_columns,
    time_precision='s', 
    protocol='line')

print("Data Posted to Influx")

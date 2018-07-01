import os
from influxdb import InfluxDBClient
 
result = os.popen('cat /proc/loadavg')
result_list = (result.read()).split(" ")
# print (result_list)
# ['3.12', '3.08', '3.08', '1/851', '31060\n']
 
i_client = InfluxDBClient(host='localhost', port=8086)
i_client.switch_database('cpuStatus')
json_body = [
    {
        "measurement": "cpuInfo",
        "tags": {
            "ip": "10.154.198.12",
        },
        "fields": {
            "1 min": result_list[0],
            "5 min": result_list[1],
            "15 min":result_list[2],
            "process/kernel_sched_entities": result_list[3],
            "LastRunPID": result_list[4][:-1]
        }
    }
]
 
i_client.write_points(json_body)
print(json_body)

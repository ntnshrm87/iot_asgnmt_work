import os
from influxdb import InfluxDBClient
from influxdb.client import InfluxDBClientError

# Connection Details:
USER = 'abhay'
PASSWD = 'Abhay@nitin1'
DBNAME = 'serverStats'


def make_connection(*args):
    """Create a connection with influxdb"""
    try:
        i_client = InfluxDBClient(*args)
        print("[INFO]: Connection successful...")
    except InfluxDBClientError:
        print("[ERROR]: In establishing connection...")
    return i_client


def data_loading(i_client, json_body):
    """Define data loading pattern and write in the db"""
    try:
        i_client.write_points(json_body)
    except InfluxDBClientError:
        print("[ERROR]: Failure in loading data...")


def data_gathering():
    """Function to gather server statistics"""

    # 1.cpu-load(cl):
    #   command used: cat /proc/loadavg
    #   result pattern: ['3.14', '3.09', '3.02', '2/799', '16153\n']
    #   significance: [loadavg_1min, load_avg_5min, load_avg_15min, process/kernel_sched_entities, lastrunPID]

    cl = os.popen('cat /proc/loadavg')
    cl_result = (cl.read()).split(" ")

    # 2. Total no. of processes running(pr):
    #    command used: ps aux --no-header | wc -l
    #    result pattern: 67
    #    significance: [returns a no. to represent processes running]

    pr_result = os.popen('ps aux --no-header | wc -l').read()[:-1]

    # 3. Total no. of open ports(op):
    #    command used: netstat -nltu --no-header | wc -l
    #    result pattern: 112
    #    significance: [returns a no. to represent listening tcp and udp ports]

    op_result = os.popen('ss -nltu | tail -n +2 | wc -l').read()[:-1]

    # Defining a JSON time-series pattern
    json_body = [
        {
            "measurement": "cpuLoad_proc_port_stats",
            "tags": {
                "ip": "10.0.0.231",
            },
            "fields": {
                "1-min": cl_result[0],
                "5-min": cl_result[1],
                "15-min": cl_result[2],
                # "process/kernel_sched_entities": cl_result[3],
                "LastRunPID": cl_result[4][:-1],
                "open_ports": op_result,
                "procs_running": pr_result
            }
        }
    ]

    return json_body


def main():
    host = "localhost"
    port = 8086
    print("Making connection...\n")
    con_obj = make_connection(host,port,USER,PASSWD,DBNAME)
    print("Gathering data...\n")
    data = data_gathering()
    print("Loading data...\n")
    data_loading(con_obj, data)

if __name__ == '__main__':
    main()




# iot_asgnmt_work

This inlcudes a solution strategy to monitor cpu_load_proc_stats using Python, InfluxDB and Grafana.

NOTE: This case will entertain the fact that both server and client are the same machines. 

1. InfluxDB is used to store the cpu load average, processes running and number of open ports.
2. Python script will fetch the server data and write the same in InfluXDB using InfluxDB API.
3. Grafana is used for visualization of Server Stats post integration with InfluXDB 

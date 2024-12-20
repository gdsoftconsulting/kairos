class UserObject(dict):
    
    def __init__(self):
        object = {
            "type": "liveobject",
            "id": "MYSELF",
            "extension": "postgres_fdw",
            "options": "host 'localhost', port '5432', dbname 'kairos'",
            "user": "postgres",
            "password": "xxxxx",
            "tables": {
                "vkpg_stat_activity": {
                    "schema": "public",
                    "description": {"timestamp": "text", "hash": "text", "snap": "text", "snap_frequency": "text", "datid": "text", "datname": "text", "pid": "text", "usesysid": "text", "usename": "text",  "application_name": "text", "client_addr": "text", "client_hostname": "text", "client_port": "text", "backend_start": "text", "xact_start": "text", "query_start": "text", "state_change": "text", "wait_event_type": "text", "wait_event": "text", "state": "text", "backend_xid": "text", "backend_xmin": "text", "query": "text"}
                },
                "vkpg_stat_database": {
                    "schema": "public",
                    "description": {"timestamp": "text", "snap": "text", "datname": "text", "datid": "text", "stats_reset": "text", "numbackends": "bigint", "blk_read_time": "real",  "blk_write_time": "real",  "blks_hit": "real", "blks_read": "real", "conflicts": "real", "deadlocks": "real", "temp_bytes": "real", "temp_files": "real", "tup_deleted": "real", "tup_fetched": "real", "tup_inserted": "real",  "tup_returned": "real", "tup_updated": "real", "xact_commit": "real", "xact_rollback": "real"}
                },
                "vpsutil_cpu_times": {
                    "schema": "public",
                    "description": {"timestamp": "text", "snap": "text", "nbcpus": "real", "usr": "real", "sys": "real", "nice": "real", "idle": "real", "iowait": "real", "irq": "real", "softirq": "real", "steal": "real", "guest": "real"}
                },
                "vpsutil_disk_io_counters": {
                    "schema": "public",
                    "description": {"timestamp": "text", "snap": "text", "disk": "text", "read_count": "real", "write_count": "real", "read_bytes": "real", "write_bytes": "real", "read_time": "real", "write_time": "real" }
                },
                "vpsutil_net_io_counters": {
                    "schema": "public",
                    "description": {"timestamp": "text", "snap": "text", "iface": "text", "bytes_sent": "real", "bytes_recv": "real", "packets_sent": "real", "packets_recv": "real", "errin": "real", "errout": "real", "dropin": "real", "dropout": "real" }
                },
                "vpsutil_processes": {
                    "schema": "public",
                    "description": {"timestamp": "text", "snap": "text", "pid": "text", "create_time": "text", "pname": "text", "cmdline": "text", "usr": "real", "sys": "real",  "status": "text",  "num_threads": "real", "rss": "bigint", "vms": "bigint", "shared": "bigint", "texts": "bigint", "lib": "bigint", "datas": "bigint", "dirty": "bigint" }
                },
                "vpsutil_swap_memory": {
                    "schema": "public",
                    "description": {"timestamp": "text", "snap": "text", "total": "bigint", "used": "bigint", "free": "bigint", "percent": "real", "sin": "real", "sout": "real"}
                },
                "vpsutil_virt_memory": {
                    "schema": "public",
                    "description": {"timestamp": "text", "snap": "text", "total": "bigint", "available": "bigint", "percent": "real", "used": "bigint", "free": "bigint", "active": "bigint", "inactive": "bigint", "buffers": "bigint", "cached": "bigint"}
                },
            },
        } 
        super(UserObject, self).__init__(**object)

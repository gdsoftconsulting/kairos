
class UserObject(dict):

    ID = 'ORACLE_V$'
    
    IPADDRESS = 'orcl'
    PORT = '1521'
    CONTAINER = 'ORCL'
    USER = 'system'
    PASSWORD = 'manager'
    
    DBID = 2841939610
    
    MINDATE = "select to_char(sysdate - (1/24), 'YYYYMMDDHH24MISS') as mindate from dual"
    MAXDATE = "select to_char(sysdate, 'YYYYMMDDHH24MISS') as maxdate from dual"
    RETENTION = 60

    DEFS = {
        "dbid": "dbid as (select " + str(DBID) + " id from dual)",
        
        "mindate": "mindate as (" + MINDATE + ")",
        "maxdate": "maxdate as (" + MAXDATE + ")",
        "masterlist": "masterlist as (select dbid, instance_number, to_char(startup_time, 'YYYYMMDDHH24MISS') startup_time from dba_hist_database_instance i, dbid where i.dbid = dbid.id)",
        "deltas": "deltas as (select dbid, instance_number, to_char(startup_time, 'YYYYMMDDHH24MISS') startup_time, bid, eid, to_char(snap_time, 'YYYYMMDDHH24MISS')||'000' snap_time, round(((cast(snap_time as date) - cast(prev_snap_time as date)) * 1440 * 60), 0) elapsed  from (select end_interval_time snap_time, first_value(end_interval_time) over (order by end_interval_time asc rows between 1 preceding and current row) prev_snap_time, first_value(snap_id) over (order by end_interval_time asc rows between 1 preceding and current row) bid, snap_id eid, first_value(dbid) over (order by end_interval_time asc rows between 1 preceding and current row) prev_dbid, dbid, first_value(instance_number) over (order by end_interval_time asc rows between 1 preceding and current row) prev_instance_number, instance_number, first_value(startup_time) over (order by end_interval_time asc rows between 1 preceding and current row) prev_startup_time, startup_time from (select * from dba_hist_snapshot where dbid in (select dbid.id from dbid)), mindate, maxdate  where to_char(end_interval_time, 'YYYYMMDDHH24MISS') >= mindate.mindate and to_char(end_interval_time, 'YYYYMMDDHH24MISS') < maxdate.maxdate) where dbid=prev_dbid and instance_number=prev_instance_number and startup_time=prev_startup_time and bid != eid )", 
        "validdeltas": "validdeltas as (select d.dbid, d.instance_number, d.startup_time, d.bid, d.eid, d.snap_time, d.elapsed from deltas d, masterlist m where d.dbid = m.dbid and d.instance_number = m.instance_number and d.startup_time = m.startup_time)",
        "dboramisc": "dboramisc as (select snap_time timestamp, elapsed, elapsed avgelapsed, s.value sessions from validdeltas v, dba_hist_sysstat s where s.stat_name = 'logons current' and v.eid = s.snap_id and v.instance_number = s.instance_number and v.dbid = s.dbid)",
        "orahqt": "orahqt as (select sql_id sqlid, REGEXP_REPLACE(dbms_lob.substr(sql_fulltext,4000,1), '[^[:print:]]', '?') as request from v$sql)",
        "orahas": "orahas as (select to_char(sample_time, 'YYYYMMDDHH24MISS')||'000' timestamp, 1 kairos_count, sql_id, sample_id, session_id, session_serial#, user_id, sql_child_number, sql_plan_hash_value, force_matching_signature, sql_opcode, service_hash, decode(session_type, 'USER', 'FOREGROUND', session_type), session_state, qc_session_id, qc_instance_id, blocking_session, blocking_session_status, blocking_session_serial#, event, event_id, seq#, p1, p1text, p2, p2text, p3, p3text, wait_class, wait_class_id, nvl(wait_time,0), nvl(time_waited,0), rawtohex(xid), current_obj#, current_file#, current_block#, program, module, action, client_id, blocking_hangchain_info, blocking_inst_id, capture_overhead, consumer_group_id, current_row#, nvl(delta_interconnect_io_bytes,0), nvl(delta_read_io_bytes,0), nvl(delta_read_io_requests,0), nvl(delta_time,0), nvl(delta_write_io_bytes,0), nvl(delta_write_io_requests,0), ecid, flags, in_bind, in_connection_mgmt, in_cursor_close, in_hard_parse, in_java_execution, in_parse, in_plsql_compilation, in_plsql_execution, in_plsql_rpc, in_sequence_load, in_sql_execution, is_captured, is_replayed, is_sqlid_current, machine, nvl(pga_allocated,0), plsql_entry_object_id, plsql_entry_subprogram_id, plsql_object_id, plsql_subprogram_id, port, qc_session_serial#, remote_instance#, replay_overhead, sql_exec_id, to_char(sql_exec_start, 'YYYYMMDDHH24MISS'), sql_opname, sql_plan_line_id, sql_plan_operation, sql_plan_options, nvl(temp_space_allocated,0), time_model, nvl(tm_delta_cpu_time,0), nvl(tm_delta_db_time,0), nvl(tm_delta_time,0), top_level_call#, top_level_call_name, top_level_sql_id, top_level_sql_opcode, dbreplay_file_id, dbreplay_call_counter from mindate, maxdate, dbid, v$active_session_history sq where to_char(sq.sample_time, 'YYYYMMDDHH24MISS') between mindate.mindate and maxdate.maxdate )",
    }
    
    def __init__(self):
        object = {
            "type": "liveobject",
            "id": UserObject.ID,
            "extension": "oracle_fdw",
            "options": "dbserver '//" + UserObject.IPADDRESS + ":" + UserObject.PORT + "/" + UserObject.CONTAINER + "'",
            "user": UserObject.USER,
            "password": UserObject.PASSWORD,
            "retention": UserObject.RETENTION,
            "tables": {
                "MASTERLIST": {
                    "request": "with %(dbid)s, %(masterlist)s select * from masterlist" % UserObject.DEFS, 
                    "description": {"dbid": "text", "instance_number": "text", "startup_time": "text"}
                },
                "MINDATE": {
                    "request": "with %(mindate)s select * from mindate" % UserObject.DEFS, 
                    "description": {"mindate": "text"}
                },
                "MAXDATE": {
                    "request": "with %(maxdate)s select * from maxdate" % UserObject.DEFS, 
                    "description": {"maxdate": "text"}
                },
                "DELTAS": {
                   "request": "with %(mindate)s, %(maxdate)s, %(dbid)s, %(deltas)s select * from deltas" % UserObject.DEFS, 
                    "description": {"dbid": "text", "instance_number": "text", "startup_time": "text", "bid": "text", "eid": "text", "snap_time": "text", "elapsed": "bigint"}
                },
                "VALIDDELTAS": {
                   "request": "with %(dbid)s, %(mindate)s, %(maxdate)s, %(masterlist)s, %(deltas)s, %(validdeltas)s select * from validdeltas" % UserObject.DEFS, 
                    "description": {"dbid": "text", "instance_number": "text", "startup_time": "text", "bid": "text", "eid": "text", "snap_time": "text", "elapsed": "bigint"}
                },
                "DBORAMISC": { 
                    "request": "with %(dbid)s, %(mindate)s, %(maxdate)s, %(masterlist)s, %(deltas)s, %(validdeltas)s, %(dboramisc)s select * from dboramisc" % UserObject.DEFS, 
                    "description": {"timestamp": "text", "elapsed": "bigint", "avgelapsed": "real", "sessions": "real", "type": "text"}
                },
                "ORAHAS": { 
                    "request": "with %(dbid)s, %(mindate)s, %(maxdate)s, %(orahas)s select * from orahas" % UserObject.DEFS, 
                    "description": {"timestamp": "text", "kairos_count": "bigint", "sql_id": "text", "sample_id": "text", "session_id": "text", "session_serial": "text", "user_id": "text", "sql_child_number": "text", "sql_plan_hash_value": "text", "force_matching_signature": "text", "sql_opcode": "text", "service_hash": "text", "session_type": "text", "session_state": "text", "qc_session_id": "text", "qc_instance_id": "text", "blocking_session": "text", "blocking_session_status": "text", "blocking_session_serial": "text", "event": "text", "event_id": "text", "seq": "text", "p1": "text", "p1text": "text", "p2": "text", "p2text": "text", "p3": "text", "p3text": "text", "wait_class": "text", "wait_class_id": "text", "wait_time": "real", "time_waited": "real", "xid": "text", "current_obj": "text", "current_file": "text", "current_block": "text", "program": "text", "module": "text", "action": "text", "client_id": "text", "blocking_hangchain_info": "text", "blocking_inst_id": "text", "capture_overhead": "text", "consumer_group_id": "text", "current_row": "text", "delta_interconnect_io_bytes": "real", "delta_read_io_bytes": "real", "delta_read_io_requests": "real", "delta_time": "real", "delta_write_io_bytes": "real", "delta_write_io_requests": "real", "ecid": "text", "flags": "text", "in_bind": "text", "in_connection_mgmt": "text", "in_cursor_close": "text", "in_hard_parse": "text", "in_java_execution": "text", "in_parse": "text", "in_plsql_compilation": "text", "in_plsql_execution": "text", "in_plsql_rpc": "text", "in_sequence_load": "text", "in_sql_execution": "text", "is_captured": "text", "is_replayed": "text", "is_sqlid_current": "text", "machine": "text", "pga_allocated": "real", "plsql_entry_object_id": "text", "plsql_entry_subprogram_id": "text", "plsql_object_id": "text", "plsql_subprogram_id": "text", "port": "text", "qc_session_serial": "text", "remote_instance": "text", "replay_overhead": "text", "sql_exec_id": "text", "sql_exec_start": "text", "sql_opname": "text", "sql_plan_line_id": "text", "sql_plan_operation": "text", "sql_plan_options": "text","temp_space_allocated": "real", "time_model": "text", "tm_delta_cpu_time": "real", "tm_delta_db_time": "real", "tm_delta_time": "real", "top_level_call": "text", "top_level_call_name": "text", "top_level_sql_id": "text", "top_level_sql_opcode": "text", "dbreplay_file_id": "text", "dbreplay_call_counter": "text"},
                },
                "ORAHQT": { 
                    "request": "with %(dbid)s, %(orahqt)s select * from orahqt" % UserObject.DEFS, 
                    "description": {"sql_id": "text", "sql_text": "text"}
                },
            },
        } 
        super(UserObject, self).__init__(**object)

class UserObject(dict):
    
# Oracle foreign data wrapper

    ID = 'ORACLE_AWR'
    IPADDRESS = 'orcl'
    PORT = '1521'
    CONTAINER = 'orcl'
    INSTANCE = 'orcl'
    USER = 'system'
    PASSWORD = 'manager'
    MINDATE = "select to_char(sysdate - 1, 'YYYYMMDDHH24MISS') as mindate from dual"
    MAXDATE = "select '2099123235959' as maxdate from dual"
    RETENTION = 60


    DEFS = {
        "iname": "iname as (select '" + INSTANCE + "' name from dual)",
        "mindate": "mindate as (" + MINDATE + ")",
        "maxdate": "maxdate as (" + MAXDATE + ")",
        "masterlist": "masterlist as (select dbid, instance_number, to_char(startup_time, 'YYYYMMDDHH24MISS') startup_time from dba_hist_database_instance, iname where instance_name = iname.name)",
        "deltas": "deltas as (select dbid, instance_number, to_char(startup_time, 'YYYYMMDDHH24MISS') startup_time, bid, eid, to_char(snap_time, 'YYYYMMDDHH24MISS')||'000' snap_time, round(((cast(snap_time as date) - cast(prev_snap_time as date)) * 1440 * 60), 0) elapsed  from (select end_interval_time snap_time, first_value(end_interval_time) over (order by end_interval_time asc rows between 1 preceding and current row) prev_snap_time, first_value(snap_id) over (order by end_interval_time asc rows between 1 preceding and current row) bid, snap_id eid, first_value(dbid) over (order by end_interval_time asc rows between 1 preceding and current row) prev_dbid, dbid, first_value(instance_number) over (order by end_interval_time asc rows between 1 preceding and current row) prev_instance_number, instance_number, first_value(startup_time) over (order by end_interval_time asc rows between 1 preceding and current row) prev_startup_time, startup_time from dba_hist_snapshot, mindate, maxdate  where to_char(end_interval_time, 'YYYYMMDDHH24MISS') >= mindate.mindate and to_char(end_interval_time, 'YYYYMMDDHH24MISS') < maxdate.maxdate) where dbid=prev_dbid and instance_number=prev_instance_number and startup_time=prev_startup_time and bid != eid )", 
        "validdeltas": "validdeltas as (select d.dbid, d.instance_number, d.startup_time, d.bid, d.eid, d.snap_time, d.elapsed from deltas d, masterlist m where d.dbid = m.dbid and d.instance_number = m.instance_number and d.startup_time = m.startup_time)",
        "dboraawr": "dboraawr as (select 'awr' type from dual)",
        "dboramisc": "dboramisc as (select snap_time timestamp, elapsed, elapsed avgelapsed, s.value sessions from validdeltas v, dba_hist_sysstat s where s.stat_name = 'logons current' and v.eid = s.snap_id and v.instance_number = s.instance_number and v.dbid = s.dbid)",
        "dborainfo": "dborainfo as (select snap_time timestamp, startup_time startup from validdeltas)",
        "dboratms": "dboratms as (select v.snap_time timestamp, e.stat_name statistic, (e.value - b.value) / v.elapsed / 1000000 time from validdeltas v, dba_hist_sys_time_model e, dba_hist_sys_time_model b where b.snap_id = v.bid and e.snap_id = v.eid and b.dbid = v.dbid and e.dbid  = v.dbid and b.instance_number = v.instance_number and e.instance_number = v.instance_number and b.stat_id = e.stat_id and e.value - b.value > 0)",
        "dborawev": "dborawev as (select v.snap_time timestamp, e.event_name event, (e.total_waits_fg - nvl(b.total_waits_fg,0)) / v.elapsed count, (e.total_timeouts_fg - nvl(b.total_timeouts_fg,0)) / v.elapsed timeouts, (e.time_waited_micro_fg - nvl(b.time_waited_micro_fg,0)) / v.elapsed / 1000000 time from validdeltas v, dba_hist_system_event b, dba_hist_system_event e where b.snap_id(+) = v.bid and e.snap_id = v.eid and b.dbid(+) = v.dbid and e.dbid = v.dbid and b.instance_number(+) = v.instance_number and e.instance_number = v.instance_number and b.event_name(+) = e.event_name and e.total_waits_fg > nvl(b.total_waits_fg,0))",
        "dborawec": "dborawec as (select v.snap_time timestamp, e.wait_class eclass, (e.total_waits_fg - nvl(b.total_waits_fg,0)) / v.elapsed count, (e.total_timeouts_fg - nvl(b.total_timeouts_fg,0)) / v.elapsed timeouts, (e.time_waited_micro_fg - nvl(b.time_waited_micro_fg,0)) / v.elapsed / 1000000 time from validdeltas v, dba_hist_system_event b, dba_hist_system_event e where b.snap_id(+) = v.bid and e.snap_id = v.eid and b.dbid(+) = v.dbid and e.dbid = v.dbid and b.instance_number(+) = v.instance_number and e.instance_number = v.instance_number and b.event_name(+) = e.event_name and e.total_waits_fg > nvl(b.total_waits_fg,0))",
        "dboraweb": "dboraweb as (select v.snap_time timestamp, e.event_name event, (e.total_waits - e.total_waits_fg - nvl(b.total_waits,0) + nvl(b.total_waits_fg,0)) / v.elapsed count, (e.total_timeouts - e.total_timeouts_fg - nvl(b.total_timeouts,0) + nvl(b.total_timeouts_fg,0)) / v.elapsed timeouts, (e.time_waited_micro - e.time_waited_micro_fg - nvl(b.time_waited_micro,0) + nvl(b.time_waited_micro_fg,0)) / v.elapsed / 1000000 time from validdeltas v, dba_hist_system_event b, dba_hist_system_event e where b.snap_id(+) = v.bid and e.snap_id = v.eid and b.dbid(+) = v.dbid and e.dbid = v.dbid and b.instance_number(+) = v.instance_number and e.instance_number = v.instance_number and b.event_name(+) = e.event_name and e.total_waits > nvl(b.total_waits,0))",
        "dboraweh": "dboraweh as (select v.snap_time timestamp, e.event_name event, e.wait_time_milli*1024 bucket, (e.wait_count - nvl(b.wait_count, 0)) / v.elapsed count from validdeltas v, dba_hist_event_histogram b, dba_hist_event_histogram e where b.snap_id(+) = v.bid and e.snap_id = v.eid and b.dbid(+) = v.dbid and e.dbid = v.dbid and b.instance_number(+) = v.instance_number and e.instance_number = v.instance_number and b.event_id(+) = e.event_id and b.wait_time_milli(+) = e.wait_time_milli and e.wait_count - nvl(b.wait_count, 0) > 0)",
        "dborasqc": "dborasqc as (select v.snap_time timestamp, e.sql_id sqlid, sum(e.cpu_time_delta / v.elapsed) / 1000000 cpu, sum(e.elapsed_time_delta / v.elapsed) / 1000000 elapsed, sum(e.buffer_gets_delta / v.elapsed) gets, sum(e.executions_delta / v.elapsed) execs from validdeltas v, dba_hist_sqlstat e where e.snap_id = v.eid and e.dbid = v.dbid and e.instance_number = v.instance_number group by v.snap_time, e.sql_id)",
        "dborasqe": "dborasqe as (select v.snap_time timestamp, e.sql_id sqlid, sum(e.cpu_time_delta / v.elapsed) / 1000000 cpu, sum(e.elapsed_time_delta / v.elapsed) / 1000000 elapsed, sum(e.disk_reads_delta / v.elapsed) reads, sum(e.executions_delta / v.elapsed) execs from validdeltas v, dba_hist_sqlstat e where e.snap_id = v.eid and e.dbid = v.dbid and e.instance_number = v.instance_number group by v.snap_time, e.sql_id)",
        "dborasqg": "dborasqg as (select v.snap_time timestamp, e.sql_id sqlid, sum(e.cpu_time_delta / v.elapsed) / 1000000 cpu, sum(e.elapsed_time_delta / v.elapsed) / 1000000 elapsed, sum(e.buffer_gets_delta / v.elapsed) gets, sum(e.executions_delta / v.elapsed) execs from validdeltas v, dba_hist_sqlstat e where e.snap_id = v.eid and e.dbid = v.dbid and e.instance_number = v.instance_number group by v.snap_time, e.sql_id)",
        "dborasqr": "dborasqr as (select v.snap_time timestamp, e.sql_id sqlid, sum(e.cpu_time_delta / v.elapsed) / 1000000 cpu, sum(e.elapsed_time_delta / v.elapsed) / 1000000 elapsed, sum(e.disk_reads_delta / v.elapsed) reads, sum(e.executions_delta / v.elapsed) execs from validdeltas v, dba_hist_sqlstat e where e.snap_id = v.eid and e.dbid = v.dbid and e.instance_number = v.instance_number group by v.snap_time, e.sql_id)",
        "dborasqx": "dborasqx as (select v.snap_time timestamp, e.sql_id sqlid, sum(e.rows_processed_delta / v.elapsed) rowes, sum(e.executions_delta / v.elapsed) execs from validdeltas v, dba_hist_sqlstat e where e.snap_id = v.eid and e.dbid = v.dbid and e.instance_number = v.instance_number group by v.snap_time, e.sql_id)",
        "dborasqp": "dborasqp as (select v.snap_time timestamp, e.sql_id sqlid, sum(e.parse_calls_delta / v.elapsed) parses, sum(e.executions_delta / v.elapsed) execs from validdeltas v, dba_hist_sqlstat e where e.snap_id = v.eid and e.dbid = v.dbid and e.instance_number = v.instance_number group by v.snap_time, e.sql_id)",
        "dborasqm": "dborasqm as (select v.snap_time timestamp, e.sql_id sqlid, sum(e.sharable_mem) sharedmem, sum(e.executions_delta / v.elapsed) execs from validdeltas v, dba_hist_sqlstat e where e.snap_id = v.eid and e.dbid = v.dbid and e.instance_number = v.instance_number group by v.snap_time, e.sql_id)",
        "dborasqv": "dborasqv as (select v.snap_time timestamp, e.sql_id sqlid, sum(e.version_count) versioncount, sum(e.executions_delta / v.elapsed) execs from validdeltas v, dba_hist_sqlstat e where e.snap_id = v.eid and e.dbid = v.dbid and e.instance_number = v.instance_number group by v.snap_time, e.sql_id)",
        "dborasqw": "dborasqw as (select v.snap_time timestamp, e.sql_id sqlid, sum(e.cpu_time_delta / v.elapsed) / 1000000 cpu, sum(e.elapsed_time_delta / v.elapsed) / 1000000 elapsed, sum(e.clwait_delta / v.elapsed) / 1000000 clusterwait, sum(e.executions_delta / v.elapsed) execs from validdeltas v, dba_hist_sqlstat e where e.snap_id = v.eid and e.dbid = v.dbid and e.instance_number = v.instance_number group by v.snap_time, e.sql_id)",
        "dborareq": "dborareq as (select sql_id sqlid, rtrim(xmlagg(xmlelement(e,sql_text,'').extract('//text()') order by sql_id).GetClobVal(),',') as request from dba_hist_sqltext group by sql_id)",
        "dborasta": "dborasta as (select v.snap_time timestamp, b.stat_name statistic, (e.value - nvl(b.value,0)) / v.elapsed value from validdeltas v, dba_hist_sysstat b, dba_hist_sysstat e where b.snap_id(+) = v.bid and e.snap_id = v.eid and b.dbid(+) = v.dbid and e.dbid = v.dbid and b.instance_number(+) = v.instance_number and e.instance_number = v.instance_number and b.stat_name(+) = e.stat_name and e.stat_name not in ('logons current', 'opened cursors current', 'workarea memory allocated', 'session cursor cache count') and e.value >= nvl(b.value,0) and e.value  >  0)",
        "dboradrv": "dboradrv as (select v.snap_time timestamp, 'log switches (derived)' statistic, (e.sequence# - b.sequence#) / v.elapsed value from validdeltas v, dba_hist_thread e, dba_hist_thread b where b.snap_id = v.bid and e.snap_id = v.eid and b.dbid = v.dbid and e.dbid = v.dbid and b.instance_number = v.instance_number and e.instance_number = v.instance_number and b.thread# = e.thread# and b.thread_instance_number = e.thread_instance_number and e.thread_instance_number = v.instance_number)",
        "dboraoss": "dboraoss as (select v.snap_time timestamp, e.stat_name statistic, decode(instr(e.stat_name,'_TIME'),0 , e.value, e.value - b.value) value from validdeltas v, dba_hist_osstat b, dba_hist_osstat e where b.snap_id = v.bid and e.snap_id = v.eid and b.dbid = v.dbid and e.dbid = v.dbid and b.instance_number = v.instance_number and e.instance_number = v.instance_number and b.stat_id = e.stat_id and e.value >= b.value and e.value > 0)",
        "dboratbs": "dboratbs as (select v.snap_time timestamp, e.tsname tablespace, sum ((e.phyrds - nvl(b.phyrds,0)) / v.elapsed) reads, sum ((e.phywrts - nvl(b.phywrts,0)) / v.elapsed) writes, sum ((e.wait_count - nvl(b.wait_count,0)) / v.elapsed) busy, decode( sum(e.phyrds - nvl(b.phyrds,0)), 0, 0, sum(e.phyblkrd - nvl(b.phyblkrd,0)) / sum(e.phyrds - nvl(b.phyrds,0))) blocksperread, decode( sum(e.phyrds - nvl(b.phyrds,0)), 0, 0, (sum(e.readtim - nvl(b.readtim,0)) / sum(e.phyrds  - nvl(b.phyrds,0)))*10) readtime, decode (sum(e.wait_count - nvl(b.wait_count, 0)), 0, 0, (sum(e.time - nvl(b.time,0)) / sum(e.wait_count - nvl(b.wait_count,0)))*10) busytime from validdeltas v, dba_hist_filestatxs e, dba_hist_filestatxs b where b.snap_id(+) = v.bid and e.snap_id = v.eid and b.dbid(+) = v.dbid and e.dbid = v.dbid and b.dbid(+) = e.dbid and b.instance_number(+) = v.instance_number and e.instance_number = v.instance_number and b.instance_number(+) = e.instance_number and b.tsname(+) = e.tsname and b.filename(+) = e.filename and ( (e.phyrds - nvl(b.phyrds,0)) + (e.phywrts - nvl(b.phywrts,0))) > 0 group by v.snap_time, e.tsname)",
        "dborafil": "dborafil as (select v.snap_time timestamp, e.tsname tablespace, e.filename filex, sum ((e.phyrds - nvl(b.phyrds,0)) / v.elapsed) reads, sum ((e.phywrts - nvl(b.phywrts,0)) / v.elapsed) writes, sum ((e.wait_count - nvl(b.wait_count,0)) / v.elapsed) busy, decode( sum(e.phyrds - nvl(b.phyrds,0)), 0, 0, sum(e.phyblkrd - nvl(b.phyblkrd,0)) / sum(e.phyrds - nvl(b.phyrds,0))) blocksperread, decode( sum(e.phyrds - nvl(b.phyrds,0)), 0, 0, (sum(e.readtim - nvl(b.readtim,0)) / sum(e.phyrds  - nvl(b.phyrds,0)))*10) readtime, decode (sum(e.wait_count - nvl(b.wait_count, 0)), 0, 0, (sum(e.time - nvl(b.time,0)) / sum(e.wait_count - nvl(b.wait_count,0)))*10) busytime from validdeltas v, dba_hist_filestatxs e, dba_hist_filestatxs b where b.snap_id(+) = v.bid and e.snap_id = v.eid and b.dbid(+) = v.dbid and e.dbid = v.dbid and b.dbid(+) = e.dbid and b.instance_number(+) = v.instance_number and e.instance_number = v.instance_number and b.instance_number(+) = e.instance_number and b.tsname(+) = e.tsname and b.filename(+) = e.filename and ( (e.phyrds - nvl(b.phyrds,0)) + (e.phywrts - nvl(b.phywrts,0))) > 0 group by v.snap_time, e.tsname,e.filename)",
        "dboramdc": "dboramdc as (select v.snap_time timestamp, replace(replace(replace(e.component, 'DEFAULT ', 'D:'), 'KEEP ', 'K:'), 'RECYCLE','R:') component, substr(e.last_oper_type,1,6) || decode(e.last_oper_type, 'STATIC', ' ', '/') || substr(e.last_oper_mode,1,3) operation, e.current_size / 1048576 sizex, 0.0 vmin, 0.0 vmax, (e.oper_count - b.oper_count) / v.elapsed opcount from validdeltas v, dba_hist_mem_dynamic_comp b, dba_hist_mem_dynamic_comp e where b.snap_id = v.bid and e.snap_id = v.eid and b.dbid = v.dbid and e.dbid = v.dbid and b.dbid = e.dbid and b.instance_number = v.instance_number and e.instance_number = v.instance_number and b.component = e.component and (e.current_size + b.current_size > 0 or e.oper_count - b.oper_count > 0))",
        "dborabuf": "dborabuf as (select v.snap_time timestamp, replace(e.block_size/1024||'k', p.value / 1024||'k', substr(e.name,1,1)) bufpool, (e.db_block_gets - nvl(b.db_block_gets,0) + e.consistent_gets  - nvl(b.consistent_gets,0)) / v.elapsed gets, (e.physical_reads - nvl(b.physical_reads,0)) / v.elapsed reads, (e.physical_writes - nvl(b.physical_writes,0)) / v.elapsed writes, (e.free_buffer_wait - nvl(b.free_buffer_wait,0)) / v.elapsed freewaits, (e.write_complete_wait - nvl(b.write_complete_wait,0)) / v.elapsed writecompletewaits, (e.buffer_busy_wait - nvl(b.buffer_busy_wait,0)) / v.elapsed busywaits from validdeltas v, dba_hist_buffer_pool_stat b, dba_hist_buffer_pool_stat e, dba_hist_parameter p where b.snap_id(+) = v.bid and e.snap_id = v.eid and p.snap_id = v.eid and b.dbid(+) = v.dbid and e.dbid = v.dbid and p.dbid = v.dbid and b.dbid(+) = e.dbid and b.instance_number(+) = v.instance_number and e.instance_number = v.instance_number and p.instance_number= v.instance_number and b.instance_number(+) = e.instance_number and b.id(+) = e.id and p.parameter_name='db_block_size')",
        "dboraenq": "dboraenq as (select v.snap_time timestamp, e.eq_type || '-' || to_char(nvl(l.name,' ')) || decode( upper(e.req_reason), 'CONTENTION', null, '-',  null, ' ('||e.req_reason||')') enqueue, (e.total_req# - nvl(b.total_req#,0)) / v.elapsed requests, (e.succ_req# - nvl(b.succ_req#,0)) / v.elapsed succgets, (e.failed_req# - nvl(b.failed_req#,0)) / v.elapsed failedgets, (e.total_wait# - nvl(b.total_wait#,0)) / v.elapsed waits, decode(  (e.total_wait#   - nvl(b.total_wait#,0)), 0, to_number(0), ( (e.cum_wait_time - nvl(b.cum_wait_time,0)) / (e.total_wait#   - nvl(b.total_wait#,0)))) awttm from validdeltas v, dba_hist_enqueue_stat e, dba_hist_enqueue_stat b, v$lock_type l where b.snap_id(+) = v.bid and e.snap_id  = v.eid and b.dbid(+) = v.dbid and e.dbid = v.dbid and b.dbid(+) = e.dbid and b.instance_number(+) = v.instance_number and e.instance_number = v.instance_number and b.instance_number(+) = e.instance_number and b.eq_type(+) = e.eq_type and b.req_reason(+) = e.req_reason and e.total_wait# - nvl(b.total_wait#,0) > 0 and l.type(+) = e.eq_type)",
        "dboralaw": "dboralaw as (select v.snap_time timestamp, b.latch_name latch, (e.wait_time - b.wait_time) / v.elapsed / 1000000 wait from validdeltas v, dba_hist_latch b, dba_hist_latch e where b.snap_id = v.bid and e.snap_id = v.eid and b.dbid = v.dbid and e.dbid = v.dbid and b.dbid = e.dbid and b.instance_number = v.instance_number and e.instance_number = v.instance_number and b.instance_number = e.instance_number and b.latch_name = e.latch_name and (e.gets - b.gets + e.immediate_gets - b.immediate_gets) > 0)",
        "dboralat": "dboralat as (select v.snap_time timestamp, b.latch_name latch , (e.gets - b.gets) / v.elapsed gets, (e.misses - b.misses) / v.elapsed misses, (e.sleeps - b.sleeps) / v.elapsed sleeps from validdeltas v, dba_hist_latch b, dba_hist_latch e where b.snap_id = v.bid and e.snap_id = v.eid and b.dbid = v.dbid and e.dbid = v.dbid and b.dbid = e.dbid and b.instance_number = v.instance_number and e.instance_number = v.instance_number and b.instance_number = e.instance_number and b.latch_name = e.latch_name and e.sleeps - b.sleeps > 0)",
        "dboralib": "dboralib as (select v.snap_time timestamp, e.namespace item, (e.gets - b.gets) / v.elapsed gets, (e.pins - b.pins) / v.elapsed pins, (e.reloads - b.reloads) / v.elapsed reloads, (e.invalidations - b.invalidations) / v.elapsed invalidations from validdeltas v, dba_hist_librarycache b, dba_hist_librarycache e where b.snap_id = v.bid and e.snap_id = v.eid and e.dbid = v.dbid and b.dbid = e.dbid and e.instance_number = v.instance_number and b.instance_number = e.instance_number and b.namespace = e.namespace and e.gets - b.gets > 0)",
        "dborasga": "dborasga as (select v.snap_time timestamp, pool, name, s.bytes/1024/1024 sizex from validdeltas v, dba_hist_sgastat s where s.snap_id = v.eid and s.dbid = v.dbid and s.instance_number = v.instance_number)",
        "dboraprm": "dboraprm as (select v.snap_time timestamp, e.parameter_name parameter, e.value value from validdeltas v, dba_hist_parameter e where e.snap_id(+) = v.eid and e.dbid(+) = v.dbid and e.instance_number(+) = v.instance_number and translate(e.parameter_name, '_', '#') not like '##%' and (nvl(e.isdefault, 'X') = 'FALSE' or nvl(e.ismodified,'X')  != 'FALSE'))",
        "dborasglr": "dborasglr as (select r.snap_time timestamp, n.owner owner, n.tablespace_name tablespace, n.object_name object, n.subobject_name subobject, n.object_type objtype, r.logical_reads / r.elapsed gets from dba_hist_seg_stat_obj n, (select * from (select v.snap_time, v.elapsed, e.dataobj#, e.obj#, e.ts#, e.dbid, e.logical_reads_delta logical_reads from validdeltas v, dba_hist_seg_stat e where e.snap_id = v.eid and e.dbid = v.dbid and e.instance_number = v.instance_number and e.logical_reads_delta > 0) d) r where n.dataobj# = r.dataobj# and n.obj# = r.obj# and n.ts# = r.ts# and n.dbid = r.dbid)",
        "dborasgpr": "dborasgpr as (select r.snap_time timestamp, n.owner owner, n.tablespace_name tablespace, n.object_name object, n.subobject_name subobject, n.object_type objtype, r.physical_reads / r.elapsed gets from dba_hist_seg_stat_obj n, (select * from (select v.snap_time, v.elapsed, e.dataobj#, e.obj#, e.ts#, e.dbid, e.physical_reads_delta physical_reads from validdeltas v, dba_hist_seg_stat e where e.snap_id = v.eid and e.dbid = v.dbid and e.instance_number = v.instance_number and e.physical_reads_delta > 0) d) r where n.dataobj# = r.dataobj# and n.obj# = r.obj# and n.ts# = r.ts# and n.dbid = r.dbid)",
        "dborasgrlw": "dborasgrlw as (select r.snap_time timestamp, n.owner owner, n.tablespace_name tablespace, n.object_name object, n.subobject_name subobject, n.object_type objtype, r.row_lock_waits / r.elapsed gets from dba_hist_seg_stat_obj n, (select * from (select v.snap_time, v.elapsed, e.dataobj#, e.obj#, e.ts#, e.dbid, e.row_lock_waits_delta row_lock_waits from validdeltas v, dba_hist_seg_stat e where e.snap_id = v.eid and e.dbid = v.dbid and e.instance_number = v.instance_number and e.row_lock_waits_delta > 0) d) r where n.dataobj# = r.dataobj# and n.obj# = r.obj# and n.ts# = r.ts# and n.dbid = r.dbid)",
        "dborasgiw": "dborasgiw as (select r.snap_time timestamp, n.owner owner, n.tablespace_name tablespace, n.object_name object, n.subobject_name subobject, n.object_type objtype, r.itl_waits / r.elapsed gets from dba_hist_seg_stat_obj n, (select * from (select v.snap_time, v.elapsed, e.dataobj#, e.obj#, e.ts#, e.dbid, e.itl_waits_delta itl_waits from validdeltas v, dba_hist_seg_stat e where e.snap_id = v.eid and e.dbid = v.dbid and e.instance_number = v.instance_number and e.itl_waits_delta > 0) d) r where n.dataobj# = r.dataobj# and n.obj# = r.obj# and n.ts# = r.ts# and n.dbid = r.dbid)",
        "dborasgbbw": "dborasgbbw as (select r.snap_time timestamp, n.owner owner, n.tablespace_name tablespace, n.object_name object, n.subobject_name subobject, n.object_type objtype, r.buffer_busy_waits / r.elapsed gets from dba_hist_seg_stat_obj n, (select * from (select v.snap_time, v.elapsed, e.dataobj#, e.obj#, e.ts#, e.dbid, e.buffer_busy_waits_delta buffer_busy_waits from validdeltas v, dba_hist_seg_stat e where e.snap_id = v.eid and e.dbid = v.dbid and e.instance_number = v.instance_number and e.buffer_busy_waits_delta > 0) d) r where n.dataobj# = r.dataobj# and n.obj# = r.obj# and n.ts# = r.ts# and n.dbid = r.dbid)",
        "dborasggcbb": "dborasggcbb as (select r.snap_time timestamp, n.owner owner, n.tablespace_name tablespace, n.object_name object, n.subobject_name subobject, n.object_type objtype, r.gc_buffer_busy / r.elapsed gets from dba_hist_seg_stat_obj n, (select * from (select v.snap_time, v.elapsed, e.dataobj#, e.obj#, e.ts#, e.dbid, e.gc_buffer_busy_delta gc_buffer_busy from validdeltas v, dba_hist_seg_stat e where e.snap_id = v.eid and e.dbid = v.dbid and e.instance_number = v.instance_number and e.gc_buffer_busy_delta > 0) d) r where n.dataobj# = r.dataobj# and n.obj# = r.obj# and n.ts# = r.ts# and n.dbid = r.dbid)",
        "dborasgcrbr": "dborasgcrbr as (select r.snap_time timestamp, n.owner owner, n.tablespace_name tablespace, n.object_name object, n.subobject_name subobject, n.object_type objtype, r.gc_cr_blocks_received / r.elapsed gets from dba_hist_seg_stat_obj n, (select * from (select v.snap_time, v.elapsed, e.dataobj#, e.obj#, e.ts#, e.dbid, e.gc_cr_blocks_received_delta gc_cr_blocks_received from validdeltas v, dba_hist_seg_stat e where e.snap_id = v.eid and e.dbid = v.dbid and e.instance_number = v.instance_number and e.gc_cr_blocks_received_delta > 0) d) r where n.dataobj# = r.dataobj# and n.obj# = r.obj# and n.ts# = r.ts# and n.dbid = r.dbid)",
        "dborasgcbr": "dborasgcbr as (select r.snap_time timestamp, n.owner owner, n.tablespace_name tablespace, n.object_name object, n.subobject_name subobject, n.object_type objtype, r.gc_cu_blocks_received / r.elapsed gets from dba_hist_seg_stat_obj n, (select * from (select v.snap_time, v.elapsed, e.dataobj#, e.obj#, e.ts#, e.dbid, e.gc_cu_blocks_received_delta gc_cu_blocks_received from validdeltas v, dba_hist_seg_stat e where e.snap_id = v.eid and e.dbid = v.dbid and e.instance_number = v.instance_number and e.gc_cu_blocks_received_delta > 0) d) r where n.dataobj# = r.dataobj# and n.obj# = r.obj# and n.ts# = r.ts# and n.dbid = r.dbid)",
        "dborapga": "dborapga as (select mu.snap_time timestamp, to_number(p.value)/1024/1024 aggrtarget, mu.pat/1024/1024 autotarget, mu.PGA_alloc/1024/1024 memalloc, (mu.PGA_used_auto + mu.PGA_used_man)/1024/1024 memused from (select v.snap_time, v.eid, v.dbid, v.instance_number, sum(case when name = 'total PGA allocated' then value else 0 end) PGA_alloc, sum(case when name = 'total PGA used for auto workareas' then value else 0 end) PGA_used_auto, sum(case when name = 'total PGA used for manual workareas' then value else 0 end) PGA_used_man, sum(case when name = 'global memory bound' then value else 0 end) glob_mem_bnd, sum(case when name = 'aggregate PGA auto target' then value else 0 end) pat from validdeltas v, dba_hist_pgastat  pga where pga.snap_id = v.eid and pga.dbid = v.dbid and pga.instance_number = v.instance_number group by v.snap_time, v.eid, v.dbid, v.instance_number) mu, dba_hist_parameter p where p.snap_id = mu.eid and p.dbid = mu.dbid and p.instance_number = mu.instance_number and p.parameter_name = 'pga_aggregate_target' and p.value  != '0')",
        "dborapgc": "dborapgc as (select v.snap_time timestamp, case when e.high_optimal_size >= 1024*1024*1024*1024 then lpad(round(e.high_optimal_size/1024/1024/1024/1024) || 'T',7) when e.high_optimal_size >= 1024*1024*1024 then lpad(round(e.high_optimal_size/1024/1024/1024) || 'G',7) when e.high_optimal_size >= 1024*1024 then lpad(round(e.high_optimal_size/1024/1024) || 'M',7) when e.high_optimal_size >= 1024 then lpad(round(e.high_optimal_size/1024) || 'K',7) else e.high_optimal_size || 'B' end highoptimal, (e.total_executions - nvl(b.total_executions,0)) / v.elapsed totexecs, (e.optimal_executions - nvl(b.optimal_executions,0)) / v.elapsed execs0, (e.onepass_executions - nvl(b.onepass_executions,0)) / v.elapsed execs1, (e.multipasses_executions - nvl(b.multipasses_executions,0)) / v.elapsed execs2 from validdeltas v, dba_hist_sql_workarea_hstgrm e, dba_hist_sql_workarea_hstgrm b where e.snap_id = v.eid and e.dbid = v.dbid and e.instance_number = v.instance_number and b.snap_id(+) = v.bid and b.dbid(+) = e.dbid and b.instance_number(+) = e.instance_number and b.low_optimal_size(+) = e.low_optimal_size and b.high_optimal_size(+) = e.high_optimal_size and e.total_executions  - nvl(b.total_executions,0) > 0)",
        "dborabpa": "dborabpa as (select v.snap_time timestamp, e.name bufpool, e.size_factor sizefactor, e.physical_reads / e.base_physical_reads estphysreadsfactor from validdeltas v, dba_hist_db_cache_advice e where e.snap_id =v.eid and e.dbid = v.dbid and e.instance_number = v.instance_number and e.base_physical_reads > 0)",
        "dborapma": "dborapma as (select v.snap_time timestamp, e.pga_target_factor sizefactor, e.estd_extra_bytes_rw  byt_rw, e.estd_overalloc_count eoc from validdeltas v, dba_hist_pga_target_advice e where e.snap_id = v.eid and e.dbid = v.dbid and e.instance_number = v.instance_number)",
        "dboraspa": "dboraspa as (select v.snap_time timestamp, e.shared_pool_size_factor sizefactor, e.estd_lc_load_time_factor elcltf from validdeltas v, dba_hist_shared_pool_advice e where e.snap_id = v.eid and e.dbid = v.dbid and e.instance_number = v.instance_number)",
        "dborasgaa": "dborasgaa as (select v.snap_time timestamp, e.sga_size_factor sizefactor, e.estd_physical_reads epr from validdeltas v, dba_hist_sga_target_advice e where e.snap_id = v.eid and e.dbid = v.dbid and e.instance_number = v.instance_number)",
        "dborasrv": "dborasrv as (select v.snap_time timestamp, e.service_name service, sum(decode(e.stat_name, 'DB CPU', nvl(e.value, 0) - nvl(b.value, 0), 0) / v.elapsed) / 1000000 cpu, sum(decode(e.stat_name, 'DB time', nvl(e.value,0) - nvl(b.value, 0), 0) / v.elapsed) / 1000000 dbtime, sum(decode(e.stat_name, 'session logical reads', nvl(e.value,0) - nvl(b.value, 0), 0) / v.elapsed) / 1024 gets, sum(decode(e.stat_name, 'physical reads', nvl(e.value,0) - nvl(b.value, 0), 0) / v.elapsed) / 1024 reads from validdeltas v, dba_hist_service_stat e, dba_hist_service_stat b where b.snap_id(+) = v.bid and e.snap_id = v.eid and b.dbid(+) = v.dbid and e.dbid = v.dbid and b.dbid(+) = e.dbid and b.instance_number(+) = v.instance_number and e.instance_number = v.instance_number and b.instance_number(+) = e.instance_number and b.stat_name(+) = e.stat_name and nvl(e.value,0) - nvl(b.value,0) > 0 group by v.snap_time, e.service_name)",
        "dborasvw": "dborasvw as (select v.snap_time timestamp, e.service_name service, sum(decode(e.wait_class, 'Network', nvl(e.total_waits, 0) - nvl(b.total_waits, 0), 0) / v.elapsed) netwaits, sum(decode(e.wait_class, 'Network', nvl(e.time_waited, 0) - nvl(b.time_waited, 0), 0) / v.elapsed) / 1000000 netwaitt, sum(decode(e.wait_class, 'User I/O', nvl(e.total_waits, 0) - nvl(b.total_waits, 0), 0) / v.elapsed) uiowaits, sum(decode(e.wait_class, 'User I/O', nvl(e.time_waited, 0) - nvl(b.time_waited, 0), 0) / v.elapsed) / 1000000 uiowaitt, sum(decode(e.wait_class, 'Concurrency', nvl(e.total_waits, 0) - nvl(b.total_waits, 0), 0) / v.elapsed) conwaits, sum(decode(e.wait_class, 'Concurrency', nvl(e.time_waited, 0) - nvl(b.time_waited, 0), 0) / v.elapsed) / 1000000 conwaitt, sum(decode(e.wait_class, 'Administrative', nvl(e.total_waits, 0) - nvl(b.total_waits, 0), 0) / v.elapsed) admwaits, sum(decode(e.wait_class, 'Administrative', nvl(e.time_waited, 0) - nvl(b.time_waited, 0), 0) / v.elapsed) / 1000000 admwaitt from validdeltas v, dba_hist_service_wait_class e, dba_hist_service_wait_class b where b.snap_id(+) = v.bid and e.snap_id = v.eid and b.dbid(+) = v.dbid and e.dbid = v.dbid and b.dbid(+) = e.dbid and b.instance_number(+) = v.instance_number and e.instance_number = v.instance_number and b.instance_number(+) = e.instance_number and b.wait_class(+) = e.wait_class and nvl(e.total_waits,0) - nvl(b.total_waits,0) > 0 group by v.snap_time, e.service_name)",
        "orahqt": "orahqt as (select sql_id sqlid, rtrim(xmlagg(xmlelement(e,sql_text,'').extract('//text()') order by sql_id).GetClobVal(),',') as request from dba_hist_sqltext group by sql_id)",
        "orahas": "orahas as (select to_char(sample_time, 'YYYYMMDDHH24MISS')||'000' timestamp, 1 kairos_count, sql_id, sample_id, session_id, session_serial#, user_id, sql_child_number, sql_plan_hash_value, force_matching_signature, sql_opcode, service_hash, decode(session_type, 'USER', 'FOREGROUND', session_type), session_state, qc_session_id, qc_instance_id, blocking_session, blocking_session_status, blocking_session_serial#, event, event_id, seq#, p1, p1text, p2, p2text, p3, p3text, wait_class, wait_class_id, nvl(wait_time,0), nvl(time_waited,0), rawtohex(xid), current_obj#, current_file#, current_block#, program, module, action, client_id, blocking_hangchain_info, blocking_inst_id, capture_overhead, consumer_group_id, current_row#, nvl(delta_interconnect_io_bytes,0), nvl(delta_read_io_bytes,0), nvl(delta_read_io_requests,0), nvl(delta_time,0), nvl(delta_write_io_bytes,0), nvl(delta_write_io_requests,0), ecid, flags, in_bind, in_connection_mgmt, in_cursor_close, in_hard_parse, in_java_execution, in_parse, in_plsql_compilation, in_plsql_execution, in_plsql_rpc, in_sequence_load, in_sql_execution, is_captured, is_replayed, is_sqlid_current, machine, nvl(pga_allocated,0), plsql_entry_object_id, plsql_entry_subprogram_id, plsql_object_id, plsql_subprogram_id, port, qc_session_serial#, remote_instance#, replay_overhead, sql_exec_id, to_char(sql_exec_start, 'YYYYMMDDHH24MISS'), sql_opname, sql_plan_line_id, sql_plan_operation, sql_plan_options, nvl(temp_space_allocated,0), time_model, nvl(tm_delta_cpu_time,0), nvl(tm_delta_db_time,0), nvl(tm_delta_time,0), top_level_call#, top_level_call_name, top_level_sql_id, top_level_sql_opcode, dbreplay_file_id, dbreplay_call_counter from mindate, maxdate, dba_hist_active_sess_history sq where to_char(sq.sample_time, 'YYYYMMDDHH24MISS') between mindate.mindate and maxdate.maxdate)",
        "orahqs": "orahqs as (select v.snap_time timestamp, 1 kairos_count, e.sql_id sqlid, plan_hash_value, optimizer_cost, optimizer_mode, optimizer_env_hash_value, sharable_mem, loaded_versions, version_count,  module, action, sql_profile, force_matching_signature, parsing_schema_id, parsing_schema_name, parsing_user_id, fetches_delta, end_of_fetch_count_delta, sorts_delta, executions_delta, px_servers_execs_delta, loads_delta, invalidations_delta, parse_calls_delta, disk_reads_delta, buffer_gets_delta, rows_processed_delta, cpu_time_delta, elapsed_time_delta, iowait_delta, clwait_delta, apwait_delta, ccwait_delta, direct_writes_delta, plsexec_time_delta, javexec_time_delta, io_offload_elig_bytes_delta, io_interconnect_bytes_delta, physical_read_requests_delta, physical_read_bytes_delta, physical_write_requests_delta, physical_write_bytes_delta, optimized_physical_reads_delta, cell_uncompressed_bytes_delta, io_offload_return_bytes_delta, con_dbid, e.con_id, decode(e.con_id,1,'CDB\\$ROOT',(select PDB_NAME from dba_pdbs where pdb_id=e.con_id and dbid=con_dbid)) con_name from validdeltas v, dba_hist_sqlstat e where e.snap_id = v.eid and e.dbid = v.dbid and e.instance_number = v.instance_number)",
        "orahsm": "orahsm as (select to_char(end_time, 'YYYYMMDDHH24MISS')||'000' timestamp, 1 kairos_count, intsize, group_id, metric_id, metric_name, value, metric_unit, con_dbid, e.con_id, decode(e.con_id,1,'CDB\\$ROOT',(select PDB_NAME from dba_pdbs where pdb_id=e.con_id and dbid=con_dbid)) con_name from mindate, maxdate, dba_hist_sysmetric_history e where to_char(e.end_time, 'YYYYMMDDHH24MISS') between mindate.mindate and maxdate.maxdate)",
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
                    "request": "with %(iname)s, %(masterlist)s select * from masterlist" % UserObject.DEFS, 
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
                    "request": "with %(mindate)s, %(maxdate)s, %(deltas)s select * from deltas" % UserObject.DEFS, 
                    "description": {"dbid": "text", "instance_number": "text", "startup_time": "text", "bid": "text", "eid": "text", "snap_time": "text", "elapsed": "bigint"}
                },
                "VALIDDELTAS": {
                    "request": "with %(iname)s, %(mindate)s, %(maxdate)s, %(masterlist)s, %(deltas)s, %(validdeltas)s select * from validdeltas" % UserObject.DEFS, 
                    "description": {"dbid": "text", "instance_number": "text", "startup_time": "text", "bid": "text", "eid": "text", "snap_time": "text", "elapsed": "bigint"}
                },
                "DBORAAWR": {
                    "request": "with %(dboraawr)s select * from dboraawr" % UserObject.DEFS, 
                    "description": {"type": "text"}
                },
                "DBORAMISC": { 
                    "request": "with %(iname)s, %(mindate)s, %(maxdate)s, %(masterlist)s, %(deltas)s, %(validdeltas)s, %(dboramisc)s select * from dboramisc" % UserObject.DEFS, 
                    "description": {"timestamp": "text", "elapsed": "bigint", "avgelapsed": "real", "sessions": "real", "type": "text"}
                },
                "DBORAINFO": { 
                    "request": "with %(iname)s, %(mindate)s, %(maxdate)s, %(masterlist)s, %(deltas)s, %(validdeltas)s, %(dborainfo)s select * from dborainfo" % UserObject.DEFS, 
                    "description": {"timestamp": "text", "startup": "text"}
                },
                "DBORATMS": { 
                    "request": "with %(iname)s, %(mindate)s, %(maxdate)s, %(masterlist)s, %(deltas)s, %(validdeltas)s, %(dboratms)s select * from dboratms" % UserObject.DEFS, 
                    "description": {"timestamp": "text", "statistic": "text", "time": "real"}
                },
                "DBORAWEV": { 
                    "request": "with %(iname)s, %(mindate)s, %(maxdate)s, %(masterlist)s, %(deltas)s, %(validdeltas)s, %(dborawev)s select * from dborawev" % UserObject.DEFS, 
                    "description": {"timestamp": "text", "event": "text", "count": "real", "timeouts": "real", "time": "real" }
                },
                "DBORAWEC": { 
                    "request": "with %(iname)s, %(mindate)s, %(maxdate)s, %(masterlist)s, %(deltas)s, %(validdeltas)s, %(dborawec)s select * from dborawec" % UserObject.DEFS, 
                    "description": {"timestamp": "text", "eclass": "text", "count": "real", "timeouts": "real", "time": "real" }
                },
                "DBORAWEB": { 
                    "request": "with %(iname)s, %(mindate)s, %(maxdate)s, %(masterlist)s, %(deltas)s, %(validdeltas)s, %(dboraweb)s select * from dboraweb" % UserObject.DEFS, 
                    "description": {"timestamp": "text", "event": "text", "count": "real", "timeouts": "real", "time": "real" }
                },
                "DBORAWEH": { 
                    "request": "with %(iname)s, %(mindate)s, %(maxdate)s, %(masterlist)s, %(deltas)s, %(validdeltas)s, %(dboraweh)s select * from dboraweh" % UserObject.DEFS, 
                    "description": {"timestamp": "text", "event": "text", "bucket": "text", "count": "real"}
                },
                "DBORASQC": { 
                    "request": "with %(iname)s, %(mindate)s, %(maxdate)s, %(masterlist)s, %(deltas)s, %(validdeltas)s, %(dborasqc)s select * from dborasqc" % UserObject.DEFS, 
                    "description": {"timestamp": "text", "sqlid": "text", "cpu": "real", "elapsed": "real", "gets": "real", "execs": "real"}
                },
                "DBORASQE": { 
                    "request": "with %(iname)s, %(mindate)s, %(maxdate)s, %(masterlist)s, %(deltas)s, %(validdeltas)s, %(dborasqe)s select * from dborasqe" % UserObject.DEFS, 
                    "description": {"timestamp": "text", "sqlid": "text", "cpu": "real", "elapsed": "real", "reads": "real", "execs": "real"}
                },
                "DBORASQG": { 
                    "request": "with %(iname)s, %(mindate)s, %(maxdate)s, %(masterlist)s, %(deltas)s, %(validdeltas)s, %(dborasqg)s select * from dborasqg" % UserObject.DEFS, 
                    "description": {"timestamp": "text", "sqlid": "text", "cpu": "real", "elapsed": "real", "gets": "real", "execs": "real"}
                },
                "DBORASQR": { 
                    "request": "with %(iname)s, %(mindate)s, %(maxdate)s, %(masterlist)s, %(deltas)s, %(validdeltas)s, %(dborasqr)s select * from dborasqr" % UserObject.DEFS, 
                    "description": {"timestamp": "text", "sqlid": "text", "cpu": "real", "elapsed": "real", "reads": "real", "execs": "real"}
                },
                "DBORASQX": { 
                    "request": "with %(iname)s, %(mindate)s, %(maxdate)s, %(masterlist)s, %(deltas)s, %(validdeltas)s, %(dborasqx)s select * from dborasqx" % UserObject.DEFS, 
                    "description": {"timestamp": "text", "sqlid": "text", "rows": "real", "execs": "real", "cpuperexec": "real", "elapsedperexec": "real"}
                },
                "DBORASQP": { 
                    "request": "with %(iname)s, %(mindate)s, %(maxdate)s, %(masterlist)s, %(deltas)s, %(validdeltas)s, %(dborasqp)s select * from dborasqp" % UserObject.DEFS, 
                    "description": {"timestamp": "text", "sqlid": "text", "parses": "real", "execs": "real"}
                },
                "DBORASQM": { 
                    "request": "with %(iname)s, %(mindate)s, %(maxdate)s, %(masterlist)s, %(deltas)s, %(validdeltas)s, %(dborasqm)s select * from dborasqm" % UserObject.DEFS, 
                    "description": {"timestamp": "text", "sqlid": "text", "sharedmem": "real", "execs": "real"}
                },
                "DBORASQV": { 
                    "request": "with %(iname)s, %(mindate)s, %(maxdate)s, %(masterlist)s, %(deltas)s, %(validdeltas)s, %(dborasqv)s select * from dborasqv" % UserObject.DEFS, 
                    "description": {"timestamp": "text", "sqlid": "text", "versioncount": "real", "execs": "real"}
                },
                "DBORASQW": { 
                    "request": "with %(iname)s, %(mindate)s, %(maxdate)s, %(masterlist)s, %(deltas)s, %(validdeltas)s, %(dborasqw)s select * from dborasqw" % UserObject.DEFS, 
                    "description": {"timestamp": "text", "sqlid": "text", "cpu": "real", "elapsed": "real", "clusterwait": "real", "execs": "real"}
                },
                "DBORAREQ": { 
                    "request": "with %(dborareq)s select * from dborareq" % UserObject.DEFS, 
                    "description": {"sqlid": "text", "request": "text"}
                },
                "DBORASTA": { 
                    "request": "with %(iname)s, %(mindate)s, %(maxdate)s, %(masterlist)s, %(deltas)s, %(validdeltas)s, %(dborasta)s select * from dborasta" % UserObject.DEFS, 
                    "description": {"timestamp": "text", "statistic": "text", "value": "real"}
                },
                "DBORADRV": { 
                    "request": "with %(iname)s, %(mindate)s, %(maxdate)s, %(masterlist)s, %(deltas)s, %(validdeltas)s, %(dboradrv)s select * from dboradrv" % UserObject.DEFS, 
                    "description": {"timestamp": "text", "statistic": "text", "value": "real"}
                },
                "DBORAOSS": { 
                    "request": "with %(iname)s, %(mindate)s, %(maxdate)s, %(masterlist)s, %(deltas)s, %(validdeltas)s, %(dboraoss)s select * from dboraoss" % UserObject.DEFS, 
                    "description": {"timestamp": "text", "statistic": "text", "value": "real"}
                },
                "DBORATBS": { 
                    "request": "with %(iname)s, %(mindate)s, %(maxdate)s, %(masterlist)s, %(deltas)s, %(validdeltas)s, %(dboratbs)s select * from dboratbs" % UserObject.DEFS, 
                    "description": {"timestamp": "text", "tablespace": "text", "reads": "real", "writes": "real", "busy": "real", "blocksperread": "real", "readtime": "real", "busytime": "real"}
                },
                "DBORAFIL": { 
                    "request": "with %(iname)s, %(mindate)s, %(maxdate)s, %(masterlist)s, %(deltas)s, %(validdeltas)s, %(dborafil)s select * from dborafil" % UserObject.DEFS, 
                    "description": {"timestamp": "text", "tablespace": "text", "file": "text", "reads": "real", "writes": "real", "busy": "real", "blocksperread": "real", "readtime": "real", "busytime": "real"}
                },
                "DBORAMDC": { 
                    "request": "with %(iname)s, %(mindate)s, %(maxdate)s, %(masterlist)s, %(deltas)s, %(validdeltas)s, %(dboramdc)s select * from dboramdc" % UserObject.DEFS, 
                    "description": {"timestamp": "text", "component": "text", "operation": "text", "size": "real", "vmin": "real", "vmax": "real", "opcount": "real"}
                },
                "DBORABUF": { 
                    "request": "with %(iname)s, %(mindate)s, %(maxdate)s, %(masterlist)s, %(deltas)s, %(validdeltas)s, %(dborabuf)s select * from dborabuf" % UserObject.DEFS, 
                    "description": {"timestamp": "text", "bufpool": "text", "gets": "real", "reads": "real", "writes": "real", "freewaits": "real", "writecompletewaits": "real", "busywaits": "real"}
                },
                "DBORAENQ": { 
                    "request": "with %(iname)s, %(mindate)s, %(maxdate)s, %(masterlist)s, %(deltas)s, %(validdeltas)s, %(dboraenq)s select * from dboraenq" % UserObject.DEFS, 
                    "description": {"timestamp": "text", "enqueue": "text", "requests": "real", "succgets": "real", "failedgets": "real", "waits": "real", "avgwait": "real"}
                },
                "DBORALAW": { 
                    "request": "with %(iname)s, %(mindate)s, %(maxdate)s, %(masterlist)s, %(deltas)s, %(validdeltas)s, %(dboralaw)s select * from dboralaw" % UserObject.DEFS, 
                    "description": {"timestamp": "text", "latch": "text", "wait": "real"}
                },
                "DBORALAT": { 
                    "request": "with %(iname)s, %(mindate)s, %(maxdate)s, %(masterlist)s, %(deltas)s, %(validdeltas)s, %(dboralat)s select * from dboralat" % UserObject.DEFS, 
                    "description": {"timestamp": "text", "latch": "text", "gets": "real", "misses": "real", "sleeps": "real"}
                },
                "DBORALIB": { 
                    "request": "with %(iname)s, %(mindate)s, %(maxdate)s, %(masterlist)s, %(deltas)s, %(validdeltas)s, %(dboralib)s select * from dboralib" % UserObject.DEFS, 
                    "description": {"timestamp": "text", "item": "text", "gets": "real", "pins": "real", "reloads": "real", "invalidations": "real"}
                },
                "DBORASGA": { 
                    "request": "with %(iname)s, %(mindate)s, %(maxdate)s, %(masterlist)s, %(deltas)s, %(validdeltas)s, %(dborasga)s select * from dborasga" % UserObject.DEFS, 
                    "description": {"timestamp": "text", "pool": "text", "name": "text", "size": "real"}
                },
                "DBORAPRM": { 
                    "request": "with %(iname)s, %(mindate)s, %(maxdate)s, %(masterlist)s, %(deltas)s, %(validdeltas)s, %(dboraprm)s select * from dboraprm" % UserObject.DEFS, 
                    "description": {"timestamp": "text", "parameter": "text", "value": "text"}
                },
                "DBORASGLR": { 
                    "request": "with %(iname)s, %(mindate)s, %(maxdate)s, %(masterlist)s, %(deltas)s, %(validdeltas)s, %(dborasglr)s select * from dborasglr" % UserObject.DEFS, 
                    "description": {"timestamp": "text", "owner": "text", "tablespace": "text", "object": "text", "subobject": "text", "objtype": "text", "gets": "real"}
                },
                "DBORASGPR": { 
                    "request": "with %(iname)s, %(mindate)s, %(maxdate)s, %(masterlist)s, %(deltas)s, %(validdeltas)s, %(dborasgpr)s select * from dborasgpr" % UserObject.DEFS, 
                    "description": {"timestamp": "text", "owner": "text", "tablespace": "text", "object": "text", "subobject": "text", "objtype": "text", "reads": "real"}
                },
                "DBORASGRLW": { 
                    "request": "with %(iname)s, %(mindate)s, %(maxdate)s, %(masterlist)s, %(deltas)s, %(validdeltas)s, %(dborasgrlw)s select * from dborasgrlw" % UserObject.DEFS, 
                    "description": {"timestamp": "text", "owner": "text", "tablespace": "text", "object": "text", "subobject": "text", "objtype": "text", "waits": "real"}
                },
                "DBORASGIW": { 
                    "request": "with %(iname)s, %(mindate)s, %(maxdate)s, %(masterlist)s, %(deltas)s, %(validdeltas)s, %(dborasgiw)s select * from dborasgiw" % UserObject.DEFS, 
                    "description": {"timestamp": "text", "owner": "text", "tablespace": "text", "object": "text", "subobject": "text", "objtype": "text", "waits": "real"}
                },
                "DBORASGBBW": { 
                    "request": "with %(iname)s, %(mindate)s, %(maxdate)s, %(masterlist)s, %(deltas)s, %(validdeltas)s, %(dborasgbbw)s select * from dborasgbbw" % UserObject.DEFS, 
                    "description": {"timestamp": "text", "owner": "text", "tablespace": "text", "object": "text", "subobject": "text", "objtype": "text", "waits": "real"}
                },
                "DBORASGGCBB": { 
                    "request": "with %(iname)s, %(mindate)s, %(maxdate)s, %(masterlist)s, %(deltas)s, %(validdeltas)s, %(dborasggcbb)s select * from dborasggcbb" % UserObject.DEFS, 
                    "description": {"timestamp": "text", "owner": "text", "tablespace": "text", "object": "text", "subobject": "text", "objtype": "text", "waits": "real"}
                },
                "DBORASGCRBR": { 
                    "request": "with %(iname)s, %(mindate)s, %(maxdate)s, %(masterlist)s, %(deltas)s, %(validdeltas)s, %(dborasgcrbr)s select * from dborasgcrbr" % UserObject.DEFS, 
                    "description": {"timestamp": "text", "owner": "text", "tablespace": "text", "object": "text", "subobject": "text", "objtype": "text", "blocks": "real"}
                },
                "DBORASGCBR": { 
                    "request": "with %(iname)s, %(mindate)s, %(maxdate)s, %(masterlist)s, %(deltas)s, %(validdeltas)s, %(dborasgcbr)s select * from dborasgcbr" % UserObject.DEFS, 
                    "description": {"timestamp": "text", "owner": "text", "tablespace": "text", "object": "text", "subobject": "text", "objtype": "text", "blocks": "real"}
                },
                "DBORAPGA": { 
                    "request": "with %(iname)s, %(mindate)s, %(maxdate)s, %(masterlist)s, %(deltas)s, %(validdeltas)s, %(dborapga)s select * from dborapga" % UserObject.DEFS, 
                    "description": {"timestamp": "text", "aggrtarget": "real", "autotarget": "real", "memalloc": "real", "memused": "real"}
                },
                "DBORAPGC": { 
                    "request": "with %(iname)s, %(mindate)s, %(maxdate)s, %(masterlist)s, %(deltas)s, %(validdeltas)s, %(dborapgc)s select * from dborapgc" % UserObject.DEFS, 
                    "description": {"timestamp": "text", "highoptimal": "text", "execs0": "real", "execs1": "real", "execs2": "real"}
                },
                "DBORABPA": { 
                    "request": "with %(iname)s, %(mindate)s, %(maxdate)s, %(masterlist)s, %(deltas)s, %(validdeltas)s, %(dborabpa)s select * from dborabpa" % UserObject.DEFS, 
                    "description": {"timestamp": "text", "bufpool": "text", "sizefactor": "text", "estphysreadsfactor": "real"}
                },
                "DBORAPMA": { 
                    "request": "with %(iname)s, %(mindate)s, %(maxdate)s, %(masterlist)s, %(deltas)s, %(validdeltas)s, %(dborapma)s select * from dborapma" % UserObject.DEFS, 
                    "description": {"timestamp": "text", "sizefactor": "text", "estextrabytesrw": "real", "estoveralloc": "real"}
                },
                "DBORASPA": { 
                    "request": "with %(iname)s, %(mindate)s, %(maxdate)s, %(masterlist)s, %(deltas)s, %(validdeltas)s, %(dboraspa)s select * from dboraspa" % UserObject.DEFS, 
                    "description": {"timestamp": "text", "sizefactor": "text", "estloadtimefctr": "real"}
                },
                "DBORASGAA": { 
                    "request": "with %(iname)s, %(mindate)s, %(maxdate)s, %(masterlist)s, %(deltas)s, %(validdeltas)s, %(dborasgaa)s select * from dborasgaa" % UserObject.DEFS, 
                    "description": {"timestamp": "text", "sizefactor": "text", "estphysicalreads": "real"}
                },
                "DBORASRV": { 
                    "request": "with %(iname)s, %(mindate)s, %(maxdate)s, %(masterlist)s, %(deltas)s, %(validdeltas)s, %(dborasrv)s select * from dborasrv" % UserObject.DEFS, 
                    "description": {"timestamp": "text", "service": "text", "cpu": "real", "dbtime": "real", "gets": "real", "reads": "real"}
                },
                "DBORASVW": { 
                    "request": "with %(iname)s, %(mindate)s, %(maxdate)s, %(masterlist)s, %(deltas)s, %(validdeltas)s, %(dborasvw)s select * from dborasvw" % UserObject.DEFS, 
                    "description": {"timestamp": "text", "service": "text", "netwaits": "real", "netwaitt": "real", "uiowaits": "real", "uiowaitt": "real", "conwaits": "real", "conwaitt": "real", "admwaits": "real", "admwaitt": "real"}
                },

                "ORAHAS": { 
                    "request": "with %(iname)s, %(mindate)s, %(maxdate)s, %(orahas)s select * from orahas" % UserObject.DEFS, 
                    "description": {"timestamp": "text", "kairos_count": "bigint", "sql_id": "text", "sample_id": "text", "session_id": "text", "session_serial": "text", "user_id": "text", "sql_child_number": "text", "sql_plan_hash_value": "text", "force_matching_signature": "text", "sql_opcode": "text", "service_hash": "text", "session_type": "text", "session_state": "text", "qc_session_id": "text", "qc_instance_id": "text", "blocking_session": "text", "blocking_session_status": "text", "blocking_session_serial": "text", "event": "text", "event_id": "text", "seq": "text", "p1": "text", "p1text": "text", "p2": "text", "p2text": "text", "p3": "text", "p3text": "text", "wait_class": "text", "wait_class_id": "text", "wait_time": "real", "time_waited": "real", "xid": "text", "current_obj": "text", "current_file": "text", "current_block": "text", "program": "text", "module": "text", "action": "text", "client_id": "text", "blocking_hangchain_info": "text", "blocking_inst_id": "text", "capture_overhead": "text", "consumer_group_id": "text", "current_row": "text", "delta_interconnect_io_bytes": "real", "delta_read_io_bytes": "real", "delta_read_io_requests": "real", "delta_time": "real", "delta_write_io_bytes": "real", "delta_write_io_requests": "real", "ecid": "text", "flags": "text", "in_bind": "text", "in_connection_mgmt": "text", "in_cursor_close": "text", "in_hard_parse": "text", "in_java_execution": "text", "in_parse": "text", "in_plsql_compilation": "text", "in_plsql_execution": "text", "in_plsql_rpc": "text", "in_sequence_load": "text", "in_sql_execution": "text", "is_captured": "text", "is_replayed": "text", "is_sqlid_current": "text", "machine": "text", "pga_allocated": "real", "plsql_entry_object_id": "text", "plsql_entry_subprogram_id": "text", "plsql_object_id": "text", "plsql_subprogram_id": "text", "port": "text", "qc_session_serial": "text", "remote_instance": "text", "replay_overhead": "text", "sql_exec_id": "text", "sql_exec_start": "text", "sql_opname": "text", "sql_plan_line_id": "text", "sql_plan_operation": "text", "sql_plan_options": "text","temp_space_allocated": "real", "time_model": "text", "tm_delta_cpu_time": "real", "tm_delta_db_time": "real", "tm_delta_time": "real", "top_level_call": "text", "top_level_call_name": "text", "top_level_sql_id": "text", "top_level_sql_opcode": "text", "dbreplay_file_id": "text", "dbreplay_call_counter": "text"},
                },
                "ORAHQS": { 
                    "request": "with %(iname)s, %(mindate)s, %(maxdate)s, %(masterlist)s, %(deltas)s, %(validdeltas)s, %(orahqs)s select * from orahqs" % UserObject.DEFS, 
                    "description": {"timestamp": "text", "kairos_count": "bigint", "sql_id": "text", "plan_hash_value": "text", "optimizer_cost": "text", "optimizer_mode": "text", "optimizer_env_hash_value": "text", "sharable_mem": "real", "loaded_versions": "real", "version_count": "real", "module": "text", "action": "text", "sql_profile": "text", "force_matching_signature": "text", "parsing_schema_id": "text", "parsing_schema_name": "text", "parsing_user_id": "text", "fetches_delta": "real", "end_of_fetch_count_delta": "real", "sorts_delta": "real", "executions_delta": "real", "px_servers_execs_delta": "real", "loads_delta": "real", "invalidations_delta": "real", "parse_calls_delta": "real", "disk_reads_delta": "real", "buffer_gets_delta": "real", "rows_processed_delta": "real", "cpu_time_delta": "real", "elapsed_time_delta": "real", "iowait_delta": "real", "clwait_delta": "real", "apwait_delta": "real", "ccwait_delta": "real", "direct_writes_delta": "real", "plsexec_time_delta": "real", "javexec_time_delta": "real", "io_offload_elig_bytes_delta": "real", "io_interconnect_bytes_delta": "real", "physical_read_requests_delta": "real", "physical_read_bytes_delta": "real", "physical_write_requests_delta": "real", "physical_write_bytes_delta": "real", "optimized_physical_reads_delta": "real", "cell_uncompressed_bytes_delta": "real", "io_offload_return_bytes_delta": "real", "con_dbid": "text", "con_id": "text", "con_name": "text"},
                },
                "ORAHQT": { 
                    "request": "with %(orahqt)s select * from orahqt" % UserObject.DEFS, 
                    "description": {"sql_id": "text", "sql_text": "text"}
                },
                "ORAHSM": { 
                    "request": "with %(iname)s, %(mindate)s, %(maxdate)s, %(orahsm)s select * from orahsm" % UserObject.DEFS, 
                    "description": {"timestamp": "text", "kairos_count": "bigint", "intsize": "bigint", "group_id": "text", "metric_id": "text", "metric_name": "text", "value": "real", "metric_unit": "text", "con_dbid": "text", "con_id": "text", "con_name": "text"},
                },
            },
        } 
        super(UserObject, self).__init__(**object)

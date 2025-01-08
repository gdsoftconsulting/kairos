
DROP TABLE IF EXISTS parameters;
CREATE TABLE parameters (
    parameter text NOT NULL,
    value text NOT NULL
);

INSERT INTO parameters VALUES ('enable', true);
INSERT INTO parameters VALUES ('system', true);
INSERT INTO parameters VALUES ('retention', 15.0);
INSERT INTO parameters VALUES ('directory', '/tmp');
INSERT INTO parameters VALUES ('num_rows_per_file', 10000);

CREATE OR REPLACE FUNCTION get_parameter(p text)
RETURNS text AS $$
DECLARE retvalue text;
BEGIN
        SELECT  value INTO retvalue FROM parameters where parameter = $1;
        RETURN retvalue;
END;
$$  LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION set_parameter(p text, v text)
RETURNS boolean AS $$
BEGIN
        UPDATE parameters SET value = $2 where parameter = $1;
        RETURN true;
END;
$$  LANGUAGE plpgsql;

DROP TABLE IF EXISTS psutil_cpu_times;
CREATE TABLE psutil_cpu_times(
	snap timestamp, 
	nbcpus real,
	usr real,
	sys real,
	nice real,
	idle real,
	iowait real,
	irq real,
	softirq real,
	steal real,
	guest real);
CREATE OR REPLACE VIEW vpsutil_cpu_times as select * from  (
	with t as (select *, row_number() over (order by snap) from psutil_cpu_times)
	select	to_char(t2.snap, 'YYYYMMDDHH24MISSMS')  "timestamp", 
		t2.snap snap,
		(t2.nbcpus + t1.nbcpus) / 2 nbcpus,
		(t2.usr - t1.usr) / extract(epoch from (t2.snap - t1.snap)) usr,
		(t2.sys - t1.sys) / extract(epoch from (t2.snap - t1.snap)) sys,
		(t2.nice - t1.nice) / extract(epoch from (t2.snap - t1.snap)) nice,
		(t2.idle - t1.idle) / extract(epoch from (t2.snap - t1.snap)) idle,
		(t2.iowait - t1.iowait) / extract(epoch from (t2.snap - t1.snap)) iowait,
		(t2.irq - t1.irq) / extract(epoch from (t2.snap - t1.snap)) irq,
		(t2.softirq - t1.softirq) / extract(epoch from (t2.snap - t1.snap)) softirq,
		(t2.steal - t1.steal) / extract(epoch from (t2.snap - t1.snap)) steal,
		(t2.guest - t1.guest) / extract(epoch from (t2.snap - t1.snap)) guest
	from t t1, t t2 
	where t1.row_number + 1 = t2.row_number) as foo;

DROP TABLE IF EXISTS psutil_virtual_memory;
CREATE TABLE psutil_virtual_memory(
	snap timestamp, 
	total bigint,
	available bigint,
	percent real,
	used bigint,
	free bigint,
	active bigint,
	inactive bigint,
	buffers bigint,
	cached bigint);
CREATE OR REPLACE VIEW vpsutil_virtual_memory as select * from  (
	with t as (select *, row_number() over (order by snap) from psutil_virtual_memory)
	select	to_char(t2.snap, 'YYYYMMDDHH24MISSMS')  "timestamp", 
		t2.snap snap,
		(t2.total + t1.total) / 2 total,
		(t2.available + t1.available) / 2 available,
		(t2.percent + t1.percent) / 2 percent,
		(t2.used + t1.used) / 2 used,
		(t2.free + t1.free) / 2 free,
		(t2.active + t1.active) / 2 active,
		(t2.inactive + t1.inactive) / 2 inactive,
		(t2.buffers + t1.buffers) / 2 buffers,
		(t2.cached + t1.cached) / 2 cached
	from t t1, t t2 
	where t1.row_number + 1 = t2.row_number) as foo;

DROP TABLE IF EXISTS psutil_swap_memory;
CREATE TABLE psutil_swap_memory(
	snap timestamp, 
	total bigint,
	used bigint,
	free bigint,
	percent real,
	sin real,
	sout real);
CREATE OR REPLACE VIEW vpsutil_swap_memory as select * from  (
	with t as (select *, row_number() over (order by snap) from psutil_swap_memory)
	select	to_char(t2.snap, 'YYYYMMDDHH24MISSMS')  "timestamp", 
		t2.snap snap,
		(t2.total + t1.total) / 2 total,
		(t2.used + t1.used) / 2 used,
		(t2.free + t1.free) / 2 free,
		(t2.percent + t1.percent) / 2 percent,
		(t2.sin - t1.sin) / extract(epoch from (t2.snap - t1.snap)) sin,
		(t2.sout - t1.sout) / extract(epoch from (t2.snap - t1.snap)) sout
	from t t1, t t2 
	where t1.row_number + 1 = t2.row_number) as foo;

DROP TABLE IF EXISTS psutil_disk_io_counters;
CREATE TABLE psutil_disk_io_counters(
	snap timestamp,
	disk text, 
	read_count bigint,
	write_count bigint,
	read_bytes bigint,
	write_bytes bigint,
	read_time bigint,
	write_time bigint);
CREATE OR REPLACE VIEW vpsutil_disk_io_counters as select * from  (
	with t as (select *, row_number() over (partition by disk order by snap) from psutil_disk_io_counters)
	select	to_char(t2.snap, 'YYYYMMDDHH24MISSMS')  "timestamp", 
		t2.snap snap,
		t2.disk disk,
		(t2.read_count - t1.read_count) / extract(epoch from (t2.snap - t1.snap)) read_count,
		(t2.write_count - t1.write_count) / extract(epoch from (t2.snap - t1.snap)) write_count,
		(t2.read_bytes - t1.read_bytes) / extract(epoch from (t2.snap - t1.snap)) read_bytes,
		(t2.write_bytes - t1.write_bytes) / extract(epoch from (t2.snap - t1.snap)) write_bytes,
		(t2.read_time - t1.read_time) / extract(epoch from (t2.snap - t1.snap)) read_time,
		(t2.write_time - t1.write_time) / extract(epoch from (t2.snap - t1.snap)) write_time
	from t t1, t t2 
	where t2.disk = t1.disk and t1.row_number + 1 = t2.row_number) as foo;

DROP TABLE IF EXISTS psutil_net_io_counters;
CREATE TABLE psutil_net_io_counters(
	snap timestamp,
	iface text, 
	bytes_sent bigint,
	bytes_recv bigint,
	packets_sent bigint,
	packets_recv bigint,
	errin bigint,
	errout bigint,
	dropin bigint,
	dropout bigint);
CREATE OR REPLACE VIEW vpsutil_net_io_counters as select * from  (
	with t as (select *, row_number() over (partition by iface order by snap) from psutil_net_io_counters)
	select	to_char(t2.snap, 'YYYYMMDDHH24MISSMS')  "timestamp", 
		t2.snap snap,
		t2.iface iface,
		(t2.bytes_sent - t1.bytes_sent) / extract(epoch from (t2.snap - t1.snap)) bytes_sent,
		(t2.bytes_recv - t1.bytes_recv) / extract(epoch from (t2.snap - t1.snap)) bytes_recv,
		(t2.packets_sent - t1.packets_sent) / extract(epoch from (t2.snap - t1.snap)) packets_sent,
		(t2.packets_recv - t1.packets_recv) / extract(epoch from (t2.snap - t1.snap)) packets_recv,
		(t2.errin - t1.errin) / extract(epoch from (t2.snap - t1.snap)) errin,
		(t2.errout - t1.errout) / extract(epoch from (t2.snap - t1.snap)) errout,
		(t2.dropin - t1.dropin) / extract(epoch from (t2.snap - t1.snap)) dropin,
		(t2.dropout - t1.dropout) / extract(epoch from (t2.snap - t1.snap)) dropout
	from t t1, t t2 
	where t2.iface = t1.iface and t1.row_number + 1 = t2.row_number) as foo;

DROP TABLE IF EXISTS psutil_processes;
CREATE TABLE psutil_processes(
	snap timestamp,
	pid text, 
	create_time timestamp,	
	pname text,
	cmdline text,
	usr real,
	sys real,
	status text,
	num_threads real,
	rss bigint,
	vms bigint,
	shared bigint,
	texts bigint,
	lib bigint,
	datas bigint,
	dirty bigint);
CREATE OR REPLACE VIEW vpsutil_processes as select * from  (
	with t as (select *, row_number() over (partition by pid, create_time order by snap) from psutil_processes)
	select	to_char(t2.snap, 'YYYYMMDDHH24MISSMS')  "timestamp", 
		t2.snap snap,
		t2.pid pid,
		t2.create_time create_time,
		t2.pname pname,
		t2.cmdline cmdline,
		(t2.usr - t1.usr) / extract(epoch from (t2.snap - t1.snap)) usr,
		(t2.sys - t1.sys) / extract(epoch from (t2.snap - t1.snap)) sys,
		t2.status status,
		(t2.num_threads + t1.num_threads) / 2 num_threads, 
		(t2.rss + t1.rss) / 2 rss, 
		(t2.vms + t1.vms) / 2 vms, 
		(t2.shared + t1.shared) / 2 shared, 
		(t2.texts + t1.texts) / 2 texts, 
		(t2.lib + t1.lib) / 2 lib, 
		(t2.datas + t1.datas) / 2 datas, 
		(t2.dirty + t1.dirty) / 2 dirty
	from t t1, t t2 
	where t2.pid = t1.pid and t2.create_time = t1.create_time and t1.row_number + 1 = t2.row_number) as foo;

CREATE OR REPLACE FUNCTION hash(query text)
RETURNS text AS $$
	import hashlib
	m = hashlib.md5()
	m.update(query)
	return m.hexdigest()
$$ language plpythonu;

DROP TABLE IF EXISTS kpg_stat_activity;
CREATE TABLE kpg_stat_activity AS SELECT current_timestamp snap, * FROM pg_stat_activity LIMIT 0;
CREATE OR REPLACE VIEW vkpg_stat_activity as 
	select	to_char(snap, 'YYYYMMDDHH24MISSMS')  "timestamp", hash(query) hash, * from kpg_stat_activity;

DROP TABLE IF EXISTS kpg_stat_database;
CREATE TABLE kpg_stat_database AS SELECT current_timestamp snap, * FROM pg_stat_database LIMIT 0;
CREATE OR REPLACE VIEW vkpg_stat_database as select * from  (
	with t as (select *, row_number() over (partition by datname order by snap) from kpg_stat_database)
	select	to_char(t2.snap, 'YYYYMMDDHH24MISSMS')  "timestamp", 
		t2.snap snap,
		t2.datname datname, 
		t2.datid datid, 
		t2.stats_reset stats_reset, 
		t2.numbackends numbackends, 
		t2.blk_read_time blk_read_time, 
		t2.blk_write_time blk_write_time, 
		(t2.blks_hit - t1.blks_hit) / extract(epoch from (t2.snap - t1.snap)) blks_hit,
		(t2.blks_read - t1.blks_read) / extract(epoch from (t2.snap - t1.snap)) blks_read,
		(t2.conflicts - t1.conflicts) / extract(epoch from (t2.snap - t1.snap)) conflicts,
		(t2.deadlocks - t1.deadlocks) / extract(epoch from (t2.snap - t1.snap)) deadlocks,
		(t2.temp_bytes - t1.temp_bytes) / extract(epoch from (t2.snap - t1.snap)) temp_bytes,
		(t2.temp_files - t1.temp_files) / extract(epoch from (t2.snap - t1.snap)) temp_files,
		(t2.tup_deleted - t1.tup_deleted) / extract(epoch from (t2.snap - t1.snap)) tup_deleted,
		(t2.tup_fetched - t1.tup_fetched) / extract(epoch from (t2.snap - t1.snap)) tup_fetched,
		(t2.tup_inserted - t1.tup_inserted) / extract(epoch from (t2.snap - t1.snap)) tup_inserted,
		(t2.tup_returned - t1.tup_returned) / extract(epoch from (t2.snap - t1.snap)) tup_returned,
		(t2.tup_updated - t1.tup_updated) / extract(epoch from (t2.snap - t1.snap)) tup_updated,
		(t2.xact_commit - t1.xact_commit) / extract(epoch from (t2.snap - t1.snap)) xact_commit,
		(t2.xact_rollback - t1.xact_rollback) / extract(epoch from (t2.snap - t1.snap)) xact_rollback
	from t t1, t t2 
	where t1.datname= t2.datname and t1.row_number + 1 = t2.row_number) as foo;

CREATE OR REPLACE FUNCTION snap_system()
RETURNS boolean AS $$
	enabled = plpy.execute("SELECT get_parameter('enable') x",1)[0]['x']
	get_system = plpy.execute("SELECT get_parameter('system') x",1)[0]['x']
	snaptime = plpy.execute("SELECT now() x",1)[0]['x']
	try: import psutil
	except: get_system = False
	if enabled:
		if get_system:
			x = psutil.cpu_times()
			y = psutil.cpu_count()
			request = "insert into psutil_cpu_times values ('" + snaptime + "', " + str(y) + ", " + str(x.user) + ", " + str(x.system) + ", " + str(x.nice) + ", " + str(x.idle) + ", " + str(x.iowait) + ", " + str(x.irq) + ", " + str(x.softirq) + ", " + str(x.steal) + ", " + str(x.guest) + ")"
			plpy.notice(request);
			plpy.execute(request)
			x = psutil.virtual_memory()
			request = "insert into psutil_virtual_memory values ('" + snaptime + "', " + str(x.total) + ", " + str(x.available) + ", " + str(x.percent) + ", " + str(x.used) + ", " + str(x.free) + ", " + str(x.active) + ", " + str(x.inactive) + ", " + str(x.buffers) + ", " + str(x.cached) + ")"
			plpy.notice(request);
			plpy.execute(request)
			x = psutil.swap_memory()
			request = "insert into psutil_swap_memory values ('" + snaptime + "', " + str(x.total) + ", " + str(x.used) + ", " + str(x.free) + ", " + str(x.percent) + ", " + str(x.sin) + ", " + str(x.sout) + ")"
			plpy.notice(request);
			plpy.execute(request)
			d = psutil.disk_io_counters(perdisk=True)
			for x in d:
				request = "insert into psutil_disk_io_counters values ('" + snaptime + "', '" + str(x) + "', " + str(d[x].read_count) + ", " + str(d[x].write_count) + ", " + str(d[x].read_bytes) + ", " + str(d[x].write_bytes) + ", " + str(d[x].read_time) + ", " + str(d[x].write_time) + ")"
				plpy.notice(request);
				plpy.execute(request)
			d = psutil.net_io_counters(pernic=True)
			for x in d:
				request = "insert into psutil_net_io_counters values ('" + snaptime + "', '" + str(x) + "', " + str(d[x].bytes_sent) + ", " + str(d[x].bytes_recv) + ", " + str(d[x].packets_sent) + ", " + str(d[x].packets_recv) + ", " + str(d[x].errin) + ", " + str(d[x].errout) + ", " + str(d[x].dropin) + ", " + str(d[x].dropout) + ")"
				plpy.notice(request)
				plpy.execute(request)
			for pid in psutil.pids():
				p = psutil.Process(pid)
				c = p.cpu_times()
				m = p.memory_info_ex()
				request = "insert into psutil_processes values ('" + snaptime + "', '" + str(p.pid) + "', to_timestamp(" + str(p.create_time()) + "), '" + p.name() + "', '" + p.cmdline()[0] + "', " + str(c.user) + ", " + str(c.system) + ", '" + p.status() + "', " + str(p.num_threads()) + ", " + str(m.rss) + ", " + str(m.vms) + ", " + str(m.shared) + ", " + str(m.text) + ", " + str(m.lib) + ", " + str(m.data) + ", " + str(m.dirty) + ")"
				plpy.notice(request)
				plpy.execute(request)
		return True
	else: return False
$$ language plpythonu;

CREATE OR REPLACE FUNCTION snap()
RETURNS boolean AS $$
	enabled = plpy.execute("SELECT get_parameter('enable') x",1)[0]['x']
    if enabled:
		request = "insert into kpg_stat_database (select now() snap, * from pg_stat_database)"
		plpy.notice(request);
		plpy.execute(request);
		return True
	else: return False
$$ language plpythonu;

CREATE OR REPLACE FUNCTION snap_detailed(x integer, y integer)
RETURNS boolean AS $$
	enabled = plpy.execute("SELECT get_parameter('enable') x",1)[0]['x']
	snaptime = plpy.execute("SELECT now() x",1)[0]['x']
	ply.notice('Taking ' + str(numsnaps) + ' snapshots every ' + str(interval) + ' seconds...')
	import time
	request = "insert into kpg_stat_activity (select now() snap, * from pg_stat_activity)"
	for i in range(y):
		plpy.execute(request)
		time.sleep(x)
		return True
	else: return False
$$ language plpythonu;

CREATE OR REPLACE FUNCTION purge()
RETURNS boolean AS $$
	views = ['vpsutil_cpu_times', 'vpsutil_virtual_memory', 'vpsutil_swap_memory', 'vpsutil_disk_io_counters', 'vpsutil_net_io_counters', 'vpsutil_processes', 'vkpg_stat_activity', 'vkpg_stat_database']
	tables = [view[1:] for view in views]
	enabled = plpy.execute("SELECT get_parameter('enable') x",1)[0]['x']
	retention = plpy.execute("SELECT get_parameter('retention') x",1)[0]['x']
	if enabled:
		for table in tables:
			request = "delete from " + table + " where extract(epoch from (now() - snap))/24/3600 > " + str(retention)
			plpy.notice(request)
			plpy.execute(request)
		return True
	else: return False
$$ language plpythonu;

CREATE OR REPLACE FUNCTION export(exptype text, p1 timestamp with time zone, p2 timestamp with time zone)
RETURNS text AS $$
        import socket, zipfile, datetime, json
	views = ['vpsutil_cpu_times', 'vpsutil_virtual_memory', 'vpsutil_swap_memory', 'vpsutil_disk_io_counters', 'vpsutil_net_io_counters', 'vpsutil_processes', 'vkpg_stat_activity', 'vkpg_stat_database']

	schema=dict()
	schema['vpsutil_cpu_times'] = dict(timestamp="text", snap="text", nbcpus="real", usr="real", sys="real", nice="real", idle="real", iowait="real", irq="real", softirq="real", steal="real", guest="real" )
	schema['vpsutil_virtual_memory'] = dict(timestamp="text", snap="text", total="real", available="real", percent="real", used="real", free="real", active="real", inactive="real", buffers="real", cached="real" )
	schema['vpsutil_swap_memory'] = dict(timestamp="text", snap="text", total="real", used="real", free="real", percent="real", sin="real", sout="real" )
	schema['vpsutil_disk_io_counters'] = dict(timestamp="text", snap="text", disk="text", read_count="real", write_count="real", read_bytes="real", write_bytes="real", read_time="real", write_time="real" )
	schema['vpsutil_net_io_counters'] = dict(timestamp="text", snap="text", iface="text", bytes_sent="real", bytes_recv="real", packets_sent="real", packets_recv="real", errin="real", errout="real", dropin="real", dropout="real" )
	schema['vpsutil_processes'] = dict(timestamp="text", snap="text", pid="text", create_time="text", pname="text", cmdline="text", usr="real", sys="real", num_threads="real", status="text", rss="real", vms="real", shared="real", texts="real", lib="real", datas="real", dirty="real" )
	
	schema['vkpg_sql_text'] = dict(hash="text", query="text", snap="text")
	schema['vkpg_stat_activity'] = dict(timestamp="text", application_name="text", backend_start="text", backend_xid="text", backend_xmin="text", client_addr="text", client_hostname="text", client_port="text", datid="text", datname="text", pid="text", query="text", query_start="text", snap="text", state="text", state_change="text", usename="text", usesysid="text", waiting="text", xact_start="text")
	schema['vkpg_stat_database'] = dict(timestamp="text", snap="text", datid="text", datname="text", numbackends="real", xact_commit="real", xact_rollback="real", blks_read="real", blks_hit="real", tup_returned="real", tup_fetched="real", tup_inserted="real", tup_updated="real", tup_deleted="real", conflicts="real", temp_files="real", temp_bytes="real", deadlocks="real", blk_read_time="real", blk_write_time="real", stats_reset="text")

	directory = plpy.execute("SELECT get_parameter('directory') x",1)[0]['x']
	num_rows_per_file = int(plpy.execute("SELECT get_parameter('num_rows_per_file') x",1)[0]['x'])
	if exptype == 'full': outfile = directory + '/' + socket.getfqdn() + '.zip'
	if exptype == 'oneday': outfile = directory + '/' + socket.getfqdn() + '_' + p1[0:p1.index(' ')] + '.zip'
	zip = zipfile.ZipFile(outfile, 'w')
	for view in views:
		plpy.notice('Exporting ' + view + ' ...')
		if exptype == 'full': request = 'select * from ' + view
		if exptype == 'oneday': request = "select * from " + view + " where snap between '" + p1 + "' and '" + p2 + "'"
		cursor = plpy.cursor(request)
        recordset = 0
		while True:
            obj = dict(collection=view, data=[], desc=schema[view])
			rows = cursor.fetch(num_rows_per_file)
			if not rows: break
			for row in rows: obj['data'].append(row)
            member = view + '_' + str(recordset)
            plpy.notice("Writing file: " + member + " ...")
            zip.writestr(member, json.dumps(obj, sort_keys=True, indent=4))
			recordset += 1
	zip.close()
	return outfile
$$ language plpythonu;

CREATE OR REPLACE FUNCTION export_full()
RETURNS text AS $$
	select export('full', null, null);
$$ language sql;

CREATE OR REPLACE FUNCTION export_relative_day(day integer)
RETURNS text AS $$
	select export('oneday', date_trunc('day', now() + day * interval '1 day'), date_trunc('day', now() + (day + 1) * interval '1 day'))
$$ language sql;
import streamlit as st
from pages.functions.definitions import *

theme = set_page_config()
gen_back_button()

if "context" in st.session_state and "run" in st.session_state.context and st.session_state.context["run"]:
        url = st.session_state.context['url']
        cdb = st.session_state.context['cdb']
        mindate = st.session_state.context['mindate']
        maxdate = st.session_state.context['maxdate']
        oracle = st.session_state.context['oracle']
        flags = st.session_state.context['flags']
        top = st.session_state.context['top']
        grouping = st.session_state.context['grouping']
        oracle.vdollar = flags['ashvdollar']
        st.header("", anchor="home")
        logger.info('Generating the AWRREPORT page ...')
        logger.info(f'AWRREPORT parameters: {st.session_state.context}')
        tcontents = st.expander(f"Table of contents")
        contents = ''
        instance = cdb.split('@')[0]
        host = cdb.split('@')[1].split(':')[0]
        dbid = cdb.split(':')[1]
        st.header(f"AWR report for instance {instance} running on {host} betwen {mindate[0:4]}/{mindate[4:6]}/{mindate[6:8]} and {maxdate[0:4]}/{maxdate[4:6]}/{maxdate[6:8]}", divider='rainbow')
        xaxis=dict(type='date', range=[f'{mindate[0:4]}-{mindate[4:6]}-{mindate[6:8]}', f'{maxdate[0:4]}-{maxdate[4:6]}-{maxdate[6:8]}'])
        request = oracle.query(f"select * from dba_hist_database_instance where  (dbid, startup_time) in (select distinct dbid, startup_time from {oracle.name('dba_hist_snapshot')})")
        st.write(request)
        XTraceL = gentrace(awr_interval=oracle.getawrinterval(), top=top, grouping=grouping, type='L', ash=False)        
        XTraceSC = gentrace(awr_interval=oracle.getawrinterval(), top=top, grouping=grouping, type='SC', ash=False)
        XTraceSA = gentrace(awr_interval=oracle.getawrinterval(), top=top, grouping=grouping, type='SA', ash=False)

        dbtime = oracle.query(f"select timestamp, statistic legend, time value from ({oracle.dboratms()}) where statistic = 'DB time' order by timestamp")
        cpu = oracle.query(f"select timestamp, 'DB CPU' legend, time value from ({oracle.dboratms()}) where statistic = 'DB CPU' order by timestamp")
        wect = oracle.query(f"select timestamp, 'wait events' legend, sum(time) value from ({oracle.dborawec()}) where eclass != 'Idle' group by timestamp, 'wait events' order by timestamp")
        wec = oracle.query(f"select timestamp, eclass legend, time value from ({oracle.dborawec()}) where eclass != 'Idle'")
        wev = oracle.query(f"select timestamp, event legend, time value from ({oracle.dborawev()}) where event not in (select NAME FROM V$EVENT_NAME where wait_class = 'Idle')")


        if flags['dbtime']:
            contents += '\n* [DB Time](#overview)'
            contents += '\n    * [Overview](#overview)'
            genchart(Chart(title='DB Time', ytitle = 'Seconds', plots=[[[XTraceSA(wect) + XTraceSA(cpu), XTraceL(dbtime)]]], xaxis=xaxis).draw(), anchor="overview")

            dbtimem = oracle.query(f"select timestamp, statistic legend, time value from ({oracle.dboratms()}) where statistic like '% elapsed' order by timestamp")
            contents += '\n    * [DB time model](#dbtmodel)'
            genchart(Chart(title='DB time model', ytitle = 'Seconds', plots=[[[XTraceSA(dbtimem), XTraceL(dbtime) + XTraceL(cpu)]]], xaxis=xaxis).draw(), anchor="dbtmodel")

        if flags['wev']:
            contents += '\n* [Wait events](#waitclasses)'
            contents += '\n    * [Wait events classes](#waitclasses)'
            genchart(Chart(title='Wait events classes', ytitle = 'Seconds', plots=[[[XTraceSC(wec), XTraceL(dbtime)]]], xaxis=xaxis).draw(), anchor="waitclasses")
            contents += '\n    * [Wait events](#waitevents)'
            genchart(Chart(title='Wait events', ytitle = 'Seconds', plots=[[[XTraceSC(wev)]]], xaxis=xaxis).draw(), anchor="waitevents")

        if flags['oss']:
            numcpu = oracle.query(f"select timestamp, statistic legend, value from ({oracle.dboraoss()}) where statistic='NUM_CPUS'")
            usrsys = oracle.query(f"select a.timestamp, a.statistic legend, a.value / 100 / b.avgelapsed  value from ({oracle.dboraoss()}) a, ({oracle.dboramisc()}) b where a.timestamp = b.timestamp and statistic in ('USER_TIME', 'SYS_TIME')")
            contents += '\n* [System statistics](#sysstats)'
            genchart(Chart(title='Operating system statistics', ytitle = '#', plots=[[[XTraceSA(usrsys), XTraceL(numcpu)]]], xaxis=xaxis).draw(), anchor="sysstats")

        if flags['log']:
            log = oracle.query(f"select timestamp, 'sessions' legend, sessions value from ({oracle.dboramisc()}) order by timestamp")
            genchart(Chart(title='Sessions', ytitle = '# of sessions', plots=[[[XTraceL(log)]]], xaxis=xaxis).draw(), anchor="sessions")
        
        if flags['sta']:
            sta = oracle.query(f"select a.timestamp, a.statistic legend, a.value / b.avgelapsed value from ({oracle.dborasta()}) a, ({oracle.dboramisc()}) b where a.timestamp = b.timestamp and statistic in ('user calls', 'recursive calls') order by timestamp")
            contents += '\n* [Statistics](#calls)'
            contents += '\n    * [User and recursive calls](#calls)'
            genchart(Chart(title='User / recursive calls', ytitle = '# per sec', plots=[[[XTraceL(sta)]]], xaxis=xaxis).draw(), anchor="calls")

            sta = oracle.query(f"select a.timestamp, a.statistic legend, a.value / b.avgelapsed value from ({oracle.dborasta()}) a, ({oracle.dboramisc()}) b where a.timestamp = b.timestamp and statistic in ('user commits', 'user rollbacks', 'transaction rollbacks') order by timestamp")
            contents += '\n    * [Transactional activity](#transact)'
            genchart(Chart(title='Transactional activity', ytitle = '# per sec', plots=[[[XTraceL(sta)]]], xaxis=xaxis).draw(), anchor="transact")

            sta = oracle.query(f"select a.timestamp, a.statistic legend, a.value / b.avgelapsed value from ({oracle.dborasta()}) a, ({oracle.dboramisc()}) b where a.timestamp = b.timestamp and statistic in ('execute count', 'parse count (total)', 'parse count (hard)', 'session cursor cache hits') order by timestamp")
            contents += '\n    * [Sql activity](#sqlact)'
            genchart(Chart(title='Sql activity', ytitle = '# per sec', plots=[[[XTraceL(sta)]]], xaxis=xaxis).draw(), anchor="sqlact")

            sta1 = oracle.query(f"select a.timestamp, a.statistic legend, a.value / b.avgelapsed value from ({oracle.dborasta()}) a, ({oracle.dboramisc()}) b where a.timestamp = b.timestamp and statistic like 'table fetch%' order by timestamp")
            sta2 = oracle.query(f"select a.timestamp, a.statistic legend, a.value / b.avgelapsed value from ({oracle.dborasta()}) a, ({oracle.dboramisc()}) b where a.timestamp = b.timestamp and statistic like 'table scan%' order by timestamp")
            contents += '\n    * [Tables scans and fetches](#scans)'
            genchart(Chart(title='Tables scans and fetches', ytitle = '# per sec', plots=[[[XTraceL(sta1) + XTraceL(sta2)]]], xaxis=xaxis).draw(), anchor="scans")

            sta = oracle.query(f"select a.timestamp, a.statistic legend, a.value / b.avgelapsed value from ({oracle.dborasta()}) a, ({oracle.dboramisc()}) b where a.timestamp = b.timestamp and statistic like 'sort%' order by timestamp")
            contents += '\n    * [Sorts](#sorts)'
            genchart(Chart(title='Sorts', ytitle = '# per sec', plots=[[[XTraceL(sta)]]], xaxis=xaxis).draw(), anchor="sorts")

            sta = oracle.query(f"select a.timestamp, a.statistic legend, a.value / b.avgelapsed value from ({oracle.dborasta()}) a, ({oracle.dboramisc()}) b where a.timestamp = b.timestamp and statistic like 'db block get%' order by timestamp")
            contents += '\n    * [DB block gets](#dbgets)'
            genchart(Chart(title='DB block gets', ytitle = '# per sec', plots=[[[XTraceL(sta)]]], xaxis=xaxis).draw(), anchor="dbgets")

            sta = oracle.query(f"select a.timestamp, a.statistic legend, a.value / b.avgelapsed value from ({oracle.dborasta()}) a, ({oracle.dboramisc()}) b where a.timestamp = b.timestamp and statistic like 'consistent get%' order by timestamp")
            contents += '\n    * [Consistent gets](#cgets)'
            genchart(Chart(title='Consistent gets', ytitle = '# per sec', plots=[[[XTraceL(sta)]]], xaxis=xaxis).draw(), anchor="cgets")

            sta = oracle.query(f"select a.timestamp, a.statistic legend, a.value / b.avgelapsed value from ({oracle.dborasta()}) a, ({oracle.dboramisc()}) b where a.timestamp = b.timestamp and statistic like 'physical read%' order by timestamp")
            contents += '\n    * [Physical reads](#reads)'
            genchart(Chart(title='Physical reads', ytitle = '# per sec', plots=[[[XTraceL(sta)]]], xaxis=xaxis).draw(), anchor="reads")

            sta = oracle.query(f"select a.timestamp, a.statistic legend, a.value / b.avgelapsed value from ({oracle.dborasta()}) a, ({oracle.dboramisc()}) b where a.timestamp = b.timestamp and statistic like '%changes%' order by timestamp")
            contents += '\n    * [Changes](#changes)'
            genchart(Chart(title='Changes', ytitle = '# per sec', plots=[[[XTraceL(sta)]]], xaxis=xaxis).draw(), anchor="changes")

            sta = oracle.query(f"select a.timestamp, a.statistic legend, a.value / b.avgelapsed value from ({oracle.dborasta()}) a, ({oracle.dboramisc()}) b where a.timestamp = b.timestamp and statistic like 'physical write%' order by timestamp")
            contents += '\n    * [Physical writes](#writes)'
            genchart(Chart(title='Physical writes', ytitle = '# per sec', plots=[[[XTraceL(sta)]]], xaxis=xaxis).draw(), anchor="writes")
        
        if flags['req']:

            sqe = oracle.query(f"select timestamp, sqlid legend, elapsed value from ({oracle.dborasqe()}) order by timestamp")
            asqe = oracle.query(f"select timestamp, 'All captured SQLs' legend,  sum(elapsed) value from ({oracle.dborasqe()}) group by timestamp order by timestamp")
            contents += '\n* [SQL requests](#topsqlelapsed)'
            contents += '\n    * [Top SQL requests by Elapsed Time](#topsqlelapsed)'
            genchart(Chart(title='Top SQL by elapsed time', ytitle = 'Seconds', plots=[[[XTraceSC(sqe), XTraceL(asqe)]]], xaxis=xaxis).draw(), anchor="topsqlelapsed")

            sqc = oracle.query(f"select timestamp, sqlid legend, cpu value from ({oracle.dborasqc()}) order by timestamp")
            asqc = oracle.query(f"select timestamp, 'All captured SQLs' legend,  sum(cpu) value from ({oracle.dborasqc()}) group by timestamp order by timestamp")
            contents += '\n    * [Top SQL requests by CPU Time](#topsqlcpu)'
            genchart(Chart(title='Top SQL by CPU time', ytitle = 'Seconds', plots=[[[XTraceSC(sqc), XTraceL(asqc)]]], xaxis=xaxis).draw(), anchor="topsqlcpu")

            sqg = oracle.query(f"select timestamp, sqlid legend, gets value from ({oracle.dborasqg()}) order by timestamp")
            asqg = oracle.query(f"select timestamp, 'All captured SQLs' legend,  sum(gets) value from ({oracle.dborasqg()}) group by timestamp order by timestamp")
            contents += '\n    * [Top SQL requests by gets](#topsqlgets)'
            genchart(Chart(title='Top SQL by gets', ytitle = '# of gets / sec', plots=[[[XTraceSC(sqg), XTraceL(asqg)]]], xaxis=xaxis).draw(), anchor="topsqlgets")

            sqr = oracle.query(f"select timestamp, sqlid legend, reads value from ({oracle.dborasqr()}) order by timestamp")
            asqr = oracle.query(f"select timestamp, 'All captured SQLs' legend,  sum(reads) value from ({oracle.dborasqr()}) group by timestamp order by timestamp")
            contents += '\n    * [Top SQL requests by reads](#topsqlreads)'
            genchart(Chart(title='Top SQL by reads', ytitle = '# of reads / sec', plots=[[[XTraceSC(sqr), XTraceL(asqr)]]], xaxis=xaxis).draw(), anchor="topsqlreads")

            sqx = oracle.query(f"select timestamp, sqlid legend, execs value from ({oracle.dborasqx()}) order by timestamp")
            asqx = oracle.query(f"select timestamp, 'All captured SQLs' legend,  sum(execs) value from ({oracle.dborasqx()}) group by timestamp order by timestamp")
            contents += '\n    * [Top SQL requests by executions](#topsqlexecs)'
            genchart(Chart(title='Top SQL by executions', ytitle = '# of execs / sec', plots=[[[XTraceSC(sqx), XTraceL(asqx)]]], xaxis=xaxis).draw(), anchor="topsqlexecs")

        if flags['req'] and flags['reqt']:
            allsq = tuple(pd.DataFrame({'x': pd.concat([XTraceSC(sqe).df, XTraceSC(sqc).df, XTraceSC(sqg).df, XTraceSC(sqr).df, XTraceSC(sqx).df])['legend'].unique()})['x'].to_list())
            allsq = oracle.query(f"select distinct * from ({oracle.dborareq(dbid, str(allsq))}) order by sqlid")
            contents += '\n    * [Text of top SQL requests](#topsqltext)'
            st.header(f"",anchor="topsqltext")
            st.table(allsq)
        
        if flags['seg']:
            seg = oracle.query(f"select timestamp, owner||' '||objtype||' '||object||' '||subobject legend, gets value from ({oracle.dborasglr()}) order by timestamp")
            aseg = oracle.query(f"select timestamp, statistic legend, value from ({oracle.dborasta()}) where statistic = 'session logical reads' order by timestamp")
            contents += '\n* [Segments](#sglr)'
            contents += '\n    * [Top segments by logical reads](#sglr)'
            genchart(Chart(title='Top segments by logical reads', ytitle = '# of blocks / logical reads per second', plots=[[[XTraceSC(seg), XTraceL(aseg)]]], xaxis=xaxis).draw(), anchor="sglr")

            seg = oracle.query(f"select timestamp, owner||' '||objtype||' '||object||' '||subobject legend, reads value from ({oracle.dborasgpr()}) order by timestamp")
            aseg = oracle.query(f"select timestamp, statistic legend, value from ({oracle.dborasta()}) where statistic = 'physical reads' order by timestamp")
            contents += '\n    * [Top segments by logical reads](#sgpr)'
            genchart(Chart(title='Top segments by physical reads', ytitle = '# of blocks / physical reads per second', plots=[[[XTraceSC(seg), XTraceL(aseg)]]], xaxis=xaxis).draw(), anchor="sgpr")

        if flags['srv']:
            srv = oracle.query(f"select timestamp, service legend, dbtime value from ({oracle.dborasrv()}) order by timestamp")
            contents += '\n* [Services](#svdbt)'
            contents += '\n    * [Services - DB Time](#srvdbt)'
            genchart(Chart(title='Services - DB Time', ytitle = '# of seconds per second', plots=[[[XTraceSA(srv), XTraceL(dbtime)]]], xaxis=xaxis).draw(), anchor="srvdbt")

        if flags['sga']:
            sga = oracle.query(f"select timestamp, coalesce(pool, '')||' '||name legend, sizex value from ({oracle.dborasga()}) order by timestamp")
            contents += '\n* [SGA](#sga)'
            genchart(Chart(title='SGA usage', ytitle = 'Megabytes', plots=[[[XTraceSA(sga)]]], xaxis=xaxis).draw(), anchor="sga")
        
        tcontents.markdown(contents)

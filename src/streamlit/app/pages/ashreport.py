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
        grouping = st.session_state.context['grouping']
        top = st.session_state.context['top']
        oracle.vdollar = flags['ashvdollar']
        st.header("", anchor="home")
        logger.info('Generating the ASHREPORT page ...')
        logger.info(f'ASHREPORT parameters: {st.session_state.context}')
        tcontents = st.expander(f"Table of contents")
        contents = ''
        instance = cdb.split('@')[0]
        host = cdb.split('@')[1].split(':')[0]
        dbid = cdb.split(':')[1]  
        st.header(f"ASH report for instance {instance} running on {host} betwen {mindate[0:4]}/{mindate[4:6]}/{mindate[6:8]} and {maxdate[0:4]}/{maxdate[4:6]}/{maxdate[6:8]}", divider='rainbow')
        xaxis=dict(type='date', range=[f'{mindate[0:4]}-{mindate[4:6]}-{mindate[6:8]}', f'{maxdate[0:4]}-{maxdate[4:6]}-{maxdate[6:8]}'])
        request = oracle.query(f"select * from dba_hist_database_instance where  (dbid, startup_time) in (select distinct dbid, startup_time from {oracle.name('dba_hist_snapshot')})")
        st.write(request)
        YTraceL = gentrace(awr_interval=oracle.getawrinterval(), ash_interval=oracle.getashinterval(), top=top, type='L', grouping=grouping, ash=True)        
        YTraceSC = gentrace(awr_interval=oracle.getawrinterval(), ash_interval=oracle.getashinterval(), top=top, type='SC', grouping=grouping, ash=True)
        YTraceSA = gentrace(awr_interval=oracle.getawrinterval(), ash_interval=oracle.getashinterval(), top=top, type='SA', grouping=grouping, ash=True)
        YTraceWL = gentrace(awr_interval=oracle.getawrinterval(), ash_interval=oracle.getashinterval(), top=top, type='WL', grouping=grouping, ash=True)

        if flags['dbtime']:
            ashcf = oracle.query(f"select timestamp, 'on cpu' legend, sum(kairos_count) value from ({oracle.orahas()}) where session_type = 'FOREGROUND' and session_state = 'ON CPU' group by timestamp, 'on cpu' order by timestamp")
            ashwf = oracle.query(f"select timestamp, 'waiting' legend, sum(kairos_count) value from ({oracle.orahas()}) where session_type = 'FOREGROUND' and session_state = 'WAITING' group by timestamp, 'waiting' order by timestamp")
            contents += '\n* [DB Time](#foreground)'
            contents += '\n    * [Foreground DB time](#foreground)'
            genchart(Chart(title='Foreground DB time', ytitle = 'Number of active sessions', plots=[[[YTraceSC(ashcf) + YTraceSC(ashwf)]]], xaxis=xaxis).draw(), anchor="foreground")

            ashcb = oracle.query(f"select timestamp, 'on cpu' legend, sum(kairos_count) value from ({oracle.orahas()}) where session_type = 'BACKGROUND' and session_state = 'ON CPU' group by timestamp, 'on cpu' order by timestamp")
            ashwb = oracle.query(f"select timestamp, 'waiting' legend, sum(kairos_count) value from ({oracle.orahas()}) where session_type = 'BACKGROUND' and session_state = 'WAITING' group by timestamp, 'waiting' order by timestamp")
            contents += '\n    * [Background DB time](#background)'
            genchart(Chart(title='Background DB time', ytitle = 'Number of active sessions', plots=[[[YTraceSC(ashcb) + YTraceSC(ashwb)]]], xaxis=xaxis).draw(), anchor="background")

            ashc = oracle.query(f"select timestamp, 'on cpu' legend, sum(kairos_count) value from ({oracle.orahas()}) where session_state = 'ON CPU' group by timestamp, 'on cpu' order by timestamp")
            ashw = oracle.query(f"select timestamp, 'waiting' legend, sum(kairos_count) value from ({oracle.orahas()}) where session_state = 'WAITING' group by timestamp, 'waiting' order by timestamp")
            contents += '\n    * [Foreground and Background DB time](#allground)'
            genchart(Chart(title='Foreground + Background DB time', ytitle = 'Number of active sessions', plots=[[[YTraceSC(ashc) + YTraceSC(ashw)]]], xaxis=xaxis).draw(), anchor="allground")

            ash1 = oracle.query(f"select timestamp, 'in_sql_execution' legend, sum(kairos_count) value from ({oracle.orahas()}) where in_sql_execution='Y' group by timestamp, 'in_sql_execution' order by timestamp")
            ash2 = oracle.query(f"select timestamp, 'in_sequence_load' legend, sum(kairos_count) value from ({oracle.orahas()}) where in_sequence_load='Y' group by timestamp, 'in_sequence_load' order by timestamp")
            ash3 = oracle.query(f"select timestamp, 'in_hard_parse' legend, sum(kairos_count) value from ({oracle.orahas()}) where in_hard_parse='Y' group by timestamp, 'in_hard_parse' order by timestamp")
            ash4 = oracle.query(f"select timestamp, 'in_parse' legend, sum(kairos_count) value from ({oracle.orahas()}) where in_parse='Y' group by timestamp, 'in_parse' order by timestamp")
            ash5 = oracle.query(f"select timestamp, 'in_bind' legend, sum(kairos_count) value from ({oracle.orahas()}) where in_bind='Y' group by timestamp, 'in_bind' order by timestamp")
            ash = YTraceWL(ash1) + YTraceWL(ash2) + YTraceWL(ash3) + YTraceWL(ash4) + YTraceWL(ash5)
            if not ash.df.empty:
                contents += '\n    * [DB time model](#dbtmodel)'
                genchart(Chart(title=f'DB time model', ytitle = 'Number of active sessions', plots=[[[ash]]], xaxis=xaxis).draw(), anchor="dbtmodel")
            
        if flags['wev']:
            ashwc = oracle.query(f"select timestamp, wait_class legend, sum(kairos_count) value from ({oracle.orahas()}) where session_type = 'FOREGROUND' and session_state = 'WAITING' group by timestamp, wait_class order by timestamp")
            contents += '\n* [Wait events](#waitclasses)'
            contents += '\n    * [Wait events classes](#waitclasses)'
            genchart(Chart(title='Wait events classes', ytitle = 'Number of active sessions', plots=[[[YTraceSC(ashwc)]]], xaxis=xaxis).draw(), anchor="waitclasses")

            ashw = oracle.query(f"select timestamp, event legend, sum(kairos_count) value from ({oracle.orahas()}) where session_type = 'FOREGROUND' and session_state = 'WAITING' group by timestamp, event order by timestamp")
            contents += '\n    * [Wait events](#waitevents)'
            genchart(Chart(title='Wait events', ytitle = 'Number of active sessions', plots=[[[YTraceSC(ashw)]]], xaxis=xaxis).draw(), anchor="waitevents")
        
        if flags['log']:
            ashses = oracle.query(f"select timestamp, session_id||' - '||program legend, sum(kairos_count) value from ({oracle.orahas()}) where session_type = 'FOREGROUND' group by timestamp, session_id||' - '||program order by timestamp")
            contents += '\n* [Sessions](#fsessions)'
            contents += '\n    * [Top foreground active sessions](#fsessions)'
            genchart(Chart(title='Top foreground active sessions', ytitle = 'Number of active sessions', plots=[[[YTraceSC(ashses)]]], xaxis=xaxis).draw(), anchor="fsessions")

            ashses = oracle.query(f"select timestamp, session_id||' - '||program legend, sum(kairos_count) value from ({oracle.orahas()}) where session_type = 'BACKGROUND' group by timestamp, session_id||' - '||program order by timestamp")
            contents += '\n    * [Top background active sessions](#bsessions)'
            genchart(Chart(title='Top background active sessions', ytitle = 'Number of active sessions', plots=[[[YTraceSC(ashses)]]], xaxis=xaxis).draw(), anchor="bsessions")

        if flags['req']:
            ash = oracle.query(f"select timestamp, sql_id legend, sum(kairos_count) value from ({oracle.orahas()}) where sql_id is not null group by timestamp, sql_id order by timestamp")
            if not ash.empty:
                contents += '\n* [Requests](#sqlrequests)'
                contents += '\n    * [Top SQL requests](#sqlrequests)'
                genchart(Chart(title=f'Top SQL requests', ytitle = 'Number of active sessions', plots=[[[YTraceSC(ash)]]], xaxis=xaxis).draw(), anchor="sqlrequests")

        st.write(oracle.query(f"select * from ({oracle.orahas()})"))
        tcontents.markdown(contents)

    



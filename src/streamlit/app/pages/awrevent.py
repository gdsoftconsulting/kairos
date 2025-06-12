import streamlit as st, numpy as np
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
     logger.info('Generating the AWREVENT page ...')
     logger.info(f'AWREVENT parameters: {st.session_state.context}')
     tcontents = st.expander(f"Table of contents")
     contents = ''
     xaxis=dict(type='date', range=[f'{mindate[0:4]}-{mindate[4:6]}-{mindate[6:8]}', f'{maxdate[0:4]}-{maxdate[4:6]}-{maxdate[6:8]}'])
     XTraceL = gentrace(awr_interval=oracle.getawrinterval(), top=top, grouping=grouping, type='L', ash=False)        
     XTraceSC = gentrace(awr_interval=oracle.getawrinterval(), top=top, grouping=grouping, type='SC', ash=False)
     XTraceSA = gentrace(awr_interval=oracle.getawrinterval(), top=top, grouping=grouping, type='SA', ash=False)
     YTraceL = gentrace(awr_interval=oracle.getawrinterval(), ash_interval=oracle.getashinterval(), top=top, type='L', grouping=grouping, ash=True)        
     YTraceSC = gentrace(awr_interval=oracle.getawrinterval(), ash_interval=oracle.getashinterval(), top=top, type='SC', grouping=grouping, ash=True)
     YTraceSA = gentrace(awr_interval=oracle.getawrinterval(), ash_interval=oracle.getashinterval(), top=top, type='SA', grouping=grouping, ash=True)
     YTraceWL = gentrace(awr_interval=oracle.getawrinterval(), ash_interval=oracle.getashinterval(), top=top, type='WL', grouping=grouping, ash=True)
     result = oracle.query(f"select distinct event from ({oracle.dborawev()}) order by 1")
     events = tuple([''] + result['event'].to_list())
     event = st.selectbox( 'Choose an event in the following list ...', events)
     if event:
          st.header(f"Report for wait event: {event}", divider='rainbow')
          st.write(oracle.query(f"select * from ({oracle.dborawev()}) where event = '{event}' order by timestamp"))

          st.subheader('Statistics per second')
          wev = oracle.query(f"select timestamp, event legend, time value from ({oracle.dborawev()}) where event = '{event}' order by timestamp")
          contents += '\n* [Statistics per second](#timepersec)'
          contents += '\n    * [Time statictics](#timepersec)'
          genchart(Chart(title=f'Wait event: {event} - Time statistics per second', ytitle = 'Seconds', plots=[[[YTraceSC(wev)]]], xaxis=xaxis).draw(), anchor="timepersec")

          wec = oracle.query(f"select timestamp, event legend, count value from ({oracle.dborawev()}) where event = '{event}' order by timestamp")
          contents += '\n    * [Count statictics](#countpersec)'
          genchart(Chart(title=f'Wait event: {event} - Count statistics per second', ytitle = '# / second', plots=[[[YTraceSC(wec)]]], xaxis=xaxis).draw(), anchor="countpersec")

          st.subheader('Statistics per execution')
          wev = oracle.query(f"select timestamp, event legend, decode(count, 0, 0, 1000 * time/count) value from ({oracle.dborawev()}) where event = '{event}' order by timestamp")
          contents += '\n* [Statistics per execution](#timeperexec)'
          genchart(Chart(title=f'Wait event: {event} - Time statistics per execution (ms)', ytitle = 'ms / execution', plots=[[[YTraceSC(wev)]]], xaxis=xaxis).draw(), anchor="timeperexec")

          weh = oracle.query(f"select timestamp, to_char(bucket) legend, count value from ({oracle.dboraweh()}) where event = '{event}' order by timestamp")
          contents += '\n* [Histogram](#histogram)'
          genchart(Chart(title=f'Wait event: {event} - Histogram statistics', ytitle = '????', plots=[[[YTraceSC(weh)]]], xaxis=xaxis).draw(), anchor="histogram")

          st.subheader('ASH view')
          st.write(oracle.query(f"select * from ({oracle.orahas()}) where event = '{event}'"))

          ash = oracle.query(f"select timestamp, session_id||' - '||program legend, sum(kairos_count) value from ({oracle.orahas()}) where event='{event}' group by timestamp, session_id||' - '||program order by timestamp")
          if not ash.empty:
               contents += '\n* [ASH view](#topsess)'
               contents += '\n    * [Top sessions](#topsess)'
               genchart(Chart(title=f'Wait event: {event} - Top sessions', ytitle = 'Number of active sessions', plots=[[[YTraceSC(ash)]]], xaxis=xaxis).draw(), anchor="topsess")

          ash = oracle.query(f"select timestamp, blocking_inst_id||' - '||blocking_session legend, sum(kairos_count) value from ({oracle.orahas()}) where event='{event}' and blocking_session is not null group by timestamp, blocking_inst_id||' - '||blocking_session order by timestamp")
          if not ash.empty:
               contents += '\n    * [Top blocking sessions](#topblock)'
               genchart(Chart(title=f'Wait event: {event} - Top blocking sessions', ytitle = 'Number of active sessions', plots=[[[YTraceSC(ash)]]], xaxis=xaxis).draw(), anchor="topblock")

          ash = oracle.query(f"select timestamp, sql_id legend, sum(kairos_count) value from ({oracle.orahas()}) where event='{event}' and sql_id is not null group by timestamp, sql_id order by timestamp")
          if not ash.empty:
               contents += '\n    * [Top SQL requests](#topsql)'
               genchart(Chart(title=f'Wait event: {event} - Top SQL requests', ytitle = 'Number of active sessions', plots=[[[YTraceSC(ash)]]], xaxis=xaxis).draw(), anchor="topsql")

          ash = oracle.query(f"select timestamp, xid legend, sum(kairos_count) value from ({oracle.orahas()}) where event='{event}' and xid is not null group by timestamp, xid order by timestamp")
          if not ash.empty:
               contents += '\n    * [Top transactions](#topxact)'
               genchart(Chart(title=f'Wait event: {event} - Top transactions', ytitle = 'Number of active sessions', plots=[[[YTraceSC(ash)]]], xaxis=xaxis).draw(), anchor="topxact")

          ash = oracle.query(f"select timestamp, p1text|| ': '||to_char(p1) legend, sum(kairos_count) value from ({oracle.orahas()}) where event='{event}' and p1text is not null group by timestamp, p1text|| ': '||to_char(p1) order by timestamp")
          if not ash.empty:
               contents += '\n    * [Top P1 values](#topp1)'
               genchart(Chart(title=f'Wait event: {event} - Top P1 values', ytitle = 'Number of active sessions', plots=[[[YTraceSC(ash)]]], xaxis=xaxis).draw(), anchor="topp1")

          ash = oracle.query(f"select timestamp, p2text|| ': '||to_char(p2) legend, sum(kairos_count) value from ({oracle.orahas()}) where event='{event}' and p2text is not null group by timestamp, p2text|| ': '||to_char(p2) order by timestamp")
          if not ash.empty:
               contents += '\n    * [Top P2 values](#topp1)'
               genchart(Chart(title=f'Wait event: {event} - Top P2 values', ytitle = 'Number of active sessions', plots=[[[YTraceSC(ash)]]], xaxis=xaxis).draw(), anchor="topp2")

          ash = oracle.query(f"select timestamp, p3text|| ': '||to_char(p3) legend, sum(kairos_count) value from ({oracle.orahas()}) where event='{event}' and p3text is not null group by timestamp, p3text|| ': '||to_char(p3) order by timestamp")
          if not ash.empty:
               contents += '\n    * [Top P3 values](#topp1)'
               genchart(Chart(title=f'Wait event: {event} - Top P3 values', ytitle = 'Number of active sessions', plots=[[[YTraceSC(ash)]]], xaxis=xaxis).draw(), anchor="topp3")

          tcontents.markdown(contents)


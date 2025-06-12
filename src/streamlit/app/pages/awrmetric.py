import streamlit as st, numpy as np, pandas as pd
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
     st.header("", anchor="home")
     logger.info('Generating the AWRMETRIC page ...')
     logger.info(f'AWRMETRIC parameters: {st.session_state.context}')
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
     result = oracle.query(f"select distinct metric_name from ({oracle.orahsm()}) order by 1")
     metrics = tuple([''] + result['metric_name'].to_list())
     metric = st.selectbox( 'Choose a metric in the following list ...', metrics)
     if metric:
          st.header(f"Report for metric: {metric}", divider='rainbow')
          st.write(oracle.query(f"select * from ({oracle.orahsm()}) where metric_name = '{metric}' order by end_time"))
          unit = oracle.query(f"select metric_unit from ({oracle.orahsm()}) where metric_name = '{metric}' and rownum=1").iloc[0,0]
          met = oracle.query(f"select end_time timestamp, metric_name legend, value from ({oracle.orahsm()}) where metric_name = '{metric}' order by timestamp")
          contents += '\n* [Metric](#metric)'
          genchart(Chart(title=f"Metric: {metric}", ytitle = unit, plots=[[[YTraceL(met)]]], xaxis=xaxis).draw(), anchor="metric")
          tcontents.markdown(contents)
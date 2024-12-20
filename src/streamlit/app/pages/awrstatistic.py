import streamlit as st, numpy as np, pandas as pd
from pages.functions.definitions import *
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(layout="wide",initial_sidebar_state='collapsed')

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
     c1, c2 = st.columns([10,1])
     with c2:
          if st.button('Back'): switch_page("awrrepmain")
     logger.info('Generating the AWRSTATISTIC page ...')
     logger.info(f'AWRSTATISTIC parameters: {st.session_state.context}')
     tcontents = st.expander(f"Table of contents")
     contents = ''
     xaxis=dict(type='date', range=[f'{mindate[0:4]}-{mindate[4:6]}-{mindate[6:8]}', f'{maxdate[0:4]}-{maxdate[4:6]}-{maxdate[6:8]}'])
     XTraceL = gentrace(awr_interval=oracle.getawrinterval(), top=top, grouping=grouping, type='L', ash=False) 
     result = oracle.query(f"select distinct statistic from ({oracle.dborasta()}) order by 1")
     statistics = tuple([''] + result['statistic'].to_list())
     statistic = st.selectbox( 'Choose a statistic in the following list ...', statistics)
     if statistic:
          st.header(f"Report for statistic: {statistic}", divider='rainbow')
          st.write(oracle.query(f"select * from ({oracle.dborasta()}) where statistic = '{statistic}' order by timestamp"))
          sta = oracle.query(f"select timestamp, statistic legend, value from ({oracle.dborasta()}) where statistic = '{statistic}' order by timestamp")
          if not sta.empty:
               contents += '\n* [Statistic](#sta)'
               genchart(Chart(title=f'Statistic: {statistic}', ytitle = 'Value', plots=[[[XTraceL(sta)]]], xaxis=xaxis).draw(), anchor="sta")
          tcontents.markdown(contents)


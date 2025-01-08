import streamlit as st
from pages.functions.definitions import *
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(layout="wide",initial_sidebar_state='collapsed')
st.markdown("""<style> [data-testid="collapsedControl"] {display: none}</style>""", unsafe_allow_html=True)

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
     logger.info('Generating the AWRSESSION page ...')
     logger.info(f'AWRSESSION parameters: {st.session_state.context}')
     tcontents = st.expander(f"Table of contents")
     contents = ''
     xaxis=dict(type='date', range=[f'{mindate[0:4]}-{mindate[4:6]}-{mindate[6:8]}', f'{maxdate[0:4]}-{maxdate[4:6]}-{maxdate[6:8]}'])
     YTraceL = gentrace(awr_interval=oracle.getawrinterval(), ash_interval=oracle.getashinterval(), top=top, type='L', grouping=grouping, ash=True)        
     YTraceSC = gentrace(awr_interval=oracle.getawrinterval(), ash_interval=oracle.getashinterval(), top=top, type='SC', grouping=grouping, ash=True)
     YTraceSA = gentrace(awr_interval=oracle.getawrinterval(), ash_interval=oracle.getashinterval(), top=top, type='SA', grouping=grouping, ash=True)
     YTraceWL = gentrace(awr_interval=oracle.getawrinterval(), ash_interval=oracle.getashinterval(), top=top, type='WL', grouping=grouping, ash=True)
     result = oracle.query(f"select distinct session_id|| ' - ' ||program sessions from ({oracle.orahas()}) order by 1")
     sess = tuple([''] + result['sessions'].to_list())
     ses = st.selectbox( 'Choose a session in the following list ...', sess)
     if ses:
          st.header(f"Report for session: {ses}", divider='rainbow')
          st.write(oracle.query(f"select * from ({oracle.orahas()}) where session_id|| ' - '||program = '{ses}'"))

          ash = oracle.query(f"select timestamp, decode(event, null, 'on cpu', event) legend, sum(kairos_count) value from ({oracle.orahas()}) where session_id|| ' - '||program = '{ses}' group by timestamp, event order by timestamp")
          if not ash.empty:
               contents += '\n* [Waits events](#wait)'
               genchart(Chart(title=f'Session: {ses} - Top wait events', ytitle = 'Number of active sessions', plots=[[[YTraceSC(ash)]]], xaxis=xaxis).draw(), anchor="wait")

          ash = oracle.query(f"select timestamp, xid legend, sum(kairos_count) value from ({oracle.orahas()}) where session_id|| ' - '||program = '{ses}' and xid is not null group by timestamp, xid order by timestamp")
          if not ash.empty:
               contents += '\n* [Transactions](#xact)'
               genchart(Chart(title=f'Session: {ses} - Top transactions', ytitle = 'Number of active sessions', plots=[[[YTraceSC(ash)]]], xaxis=xaxis).draw(), anchor="xact")

          ash = oracle.query(f"select timestamp, blocking_inst_id||' - '||blocking_session legend, sum(kairos_count) value from ({oracle.orahas()}) where session_id|| ' - '||program = '{ses}' and blocking_session is not null group by timestamp, blocking_inst_id||' - '||blocking_session order by timestamp")
          if not ash.empty:
               contents += '\n* [Blocking sessions](#blocking)'
               genchart(Chart(title=f'Session: {ses} - Top blocking sessions', ytitle = 'Number of active sessions', plots=[[[YTraceSC(ash)]]], xaxis=xaxis).draw(), anchor="blocking")

          ash = oracle.query(f"select timestamp, sql_id legend, sum(kairos_count) value from ({oracle.orahas()}) where session_id|| ' - '||program = '{ses}' and sql_id is not null group by timestamp, sql_id order by timestamp")
          if not ash.empty:
               contents += '\n* [SQL requests](#sql)'
               genchart(Chart(title=f'Session: {ses} - Top SQL requests', ytitle = 'Number of active sessions', plots=[[[YTraceSC(ash)]]], xaxis=xaxis).draw(), anchor="sql")

          tcontents.markdown(contents)



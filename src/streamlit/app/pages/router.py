import streamlit as st
from pages.functions.definitions import *

st.set_page_config(layout="wide",initial_sidebar_state='collapsed')
st.markdown("""<style> [data-testid="collapsedControl"] {display: none}</style>""", unsafe_allow_html=True)


param = st.query_params
st.header("Choose an application to start ...", divider='rainbow')
with st.form("apps"):
    col1, col2 = st.columns([1,1])
    with col1:
        awrreport =  st.form_submit_button('AWR report')
    with col2:
        kairos =  st.form_submit_button('KAIROS')

lvl = st.session_state.logginglevel if 'logginglevel' in st.session_state else int(param.logging) if 'logging' in param else 25
dlog = dict(Trace=5, Debug=10, Info=20, Success=25, Warning=30, Error=40, Critical=50)
index = 6 if lvl==50 else 5 if lvl==40 else 4 if lvl==30 else 3 if lvl==25 else 2 if lvl==20 else 1 if lvl==10 else 0
logging = st.radio("Logging level", ["Trace", "Debug", "Info", "Success", "Warning", "Error", "Critical"], index=index)
lvl = dlog[logging]
st.session_state.logginglevel= lvl
logger_format = ("<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <red>{thread}</red> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | - <level>{message}</level>")
logger.remove()
logger.add('/var/log/streamlit.log', format=logger_format, level=lvl)
st.success(f'Logging level defined to: {logging}')

if 'callstack' not in st.session_state: st.session_state.callstack = CallStack()
if awrreport: st.session_state.callstack.call('pages/awrrepmain.py', 'pages/router.py')
if kairos: st.session_state.callstack.call('pages/kairos.py', 'pages/router.py')
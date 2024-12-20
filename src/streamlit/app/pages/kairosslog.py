import streamlit as st
from pages.functions.definitions import *

set_page_config()
gen_back_button()

st.subheader('Streamlit log', divider='rainbow')
logname = "/var/log/streamlit.log"
child = pexpect.spawn(f'tail -f {logname}', encoding='utf8', timeout=600)
with st.status(f'tail -f {logname}', expanded=True):
    content = ''
    x = st.code(content)
    for line in child:
        x.empty()
        content += line
        x = st.code(content)
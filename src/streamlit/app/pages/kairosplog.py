import streamlit as st
from pages.functions.definitions import *

set_page_config()
gen_back_button()

st.subheader('Postgres log', divider='rainbow')
command = "cut -f 2 -d ' ' /var/lib/pgsql/data/current_logfiles"
child = pexpect.spawn(command, encoding='utf8')
curlog = ''.join([line for line in child])[:-2]
logname = f'/var/lib/pgsql/data/{curlog}'
command = f"tail -f {logname}"
child = pexpect.spawn(command, encoding='utf8', timeout=600)
with st.status(f'tail -f {logname}', expanded=True):
    content = ''
    x = st.code(content)
    for line in child:
        x.empty()
        content += line
        x = st.code(content)
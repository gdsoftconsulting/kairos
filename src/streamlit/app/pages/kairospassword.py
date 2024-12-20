import streamlit as st
from pages.functions.definitions import *

set_page_config()
gen_back_button()

param = st.query_params
if 'user' in param and param['user'] : st.session_state.user = param['user']

st.subheader(f'Change "{st.session_state.user}" password', divider='rainbow')
curpassword = st.text_input(f'Enter current password:', type="password")
if curpassword:
    command = f"kairos -s checkuserpassword -a {st.session_state.user} -p {curpassword}"
    act = run(command)
    if 'success' in act and act['success']: pass
    else: st.error(act['message'])
newpassword = st.text_input(f'Enter new password:', type="password")
repeat = st.text_input(f'Repeat new password:', type="password")
if newpassword  and repeat:
    if newpassword != repeat: st.error('New password and repeat password are different!')
    else:
        command = f'kairos -s changepassword -a {st.session_state.user} -p {curpassword} --password {newpassword}"'
        act = run(command)
        if 'success' in act and act['success']: 
            st.success(act['data']['msg'])
            del st.session_state.user
        else: st.error(act['message'])
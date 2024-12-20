import streamlit as st
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(layout="wide",initial_sidebar_state='collapsed')
st.markdown("""<style> [data-testid="collapsedControl"] {display: none}</style>""", unsafe_allow_html=True)
switch_page('router')
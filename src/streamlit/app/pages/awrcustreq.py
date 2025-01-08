import streamlit as st, numpy as np, pandas as pd
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
     top = st.session_state.context['top']
     oracle.vdollar = flags['ashvdollar']
     grouping = st.session_state.context['grouping']
     st.header("", anchor="home")
     c1, c2 = st.columns([10,1])
     with c2:
          if st.button('Back'): switch_page("awrrepmain")
     logger.info('Generating the AWRCUSTREQ page ...')
     logger.info(f'AWRCUSTREQ parameters: {st.session_state.context}')
     free = st.text_input( 'Enter the query to execute ...')
     if free:
          st.write(oracle.query(eval('f"' + free + '"')))
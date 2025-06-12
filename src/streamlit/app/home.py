import streamlit as st

st.set_page_config(layout="wide",initial_sidebar_state='collapsed')
st.markdown("""<style> [data-testid="collapsedControl"] {display: none}</style>""", unsafe_allow_html=True)
st.switch_page('pages/router.py')
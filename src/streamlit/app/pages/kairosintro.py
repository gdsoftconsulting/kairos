import streamlit as st
from pages.functions.definitions import *

set_page_config()
gen_back_button()

def subheadercontents(text, contents, anchor=None, divider=None):
    st.subheader(text, divider=divider, anchor=anchor)
    contents.append(f'\n* [{text}](#{anchor})')

def tablecontents(text, contents, anchor=None, divider=None):
    st.subheader(text, divider=divider, anchor=anchor)
    contents.append(f'\n  * [{text}](#{anchor})')

def runq(query):
    logger.debug(query)
    st.code(query)
    return postgres.query(query)

st.subheader("KAIROS introspection", divider='rainbow')
tcontents = st.expander(f"Table of contents")
contents = []
url = 'postgres@localhost'
postgres=Postgres(url=url)
st.success(f'Connected to server with url: {url}')
st.write(runq("select * from pg_database"))
subheadercontents("KAIROS databases and sizes (GigaBytes)", contents, anchor='kdbs', divider='rainbow')
dbs = runq("select datname, pg_database_size(datname)*1.0/1024/1024/1024 as size from pg_database where datname like 'kairos_%'")
st.write(dbs)
for db in dbs['datname'].to_list():
    logger.critical(db)
    subheadercontents(f'"{db}" database', contents, anchor=f'db{db}', divider='rainbow')
    url = f'postgres@localhost/{db}'
    postgres=Postgres(url=url)
    st.success(f'Connected to server with url: {url}')
    tables=runq("select * from information_schema.tables where table_schema='public' and table_type='BASE TABLE'")
    st.write(tables)
    for table in tables['table_name'].to_list():
        tablecontents(f'"{table}" table', contents, anchor=f'table{table}@{db}', divider='grey')
        st.write(runq(f"select pg_size_pretty(pg_total_relation_size('{table}')) as size"))
        # st.write(runq(f"select * from {table}"))
    schemas=runq("select distinct table_schema from information_schema.tables where table_schema like 'cache_%'")
    schema = st.selectbox( 'Choose a cache in the following list ...', tuple([''] + schemas['table_schema'].to_list()))
    if schema:
        tables=runq(f"select * from information_schema.tables where table_schema='{schema}' and table_type='BASE TABLE'")
        table = st.selectbox(f'Choose a table in the following list of schema {schema}...', tuple([''] + tables['table_name'].to_list()))
        postgres.setschema(schema)
        if table:
            st.markdown(f'Table "**{table}**"')
            st.write(runq(f"select pg_size_pretty(pg_total_relation_size('{table}')) as size"))
            st.write(runq(f"select * from {table}"))
tcontents.markdown(" ".join([str(item) for item in contents]))

import streamlit as st
from pages.functions.definitions import *

theme = set_page_config()
gen_back_button()

param = st.query_params

if "context" not in st.session_state: st.session_state.context = dict()

st.header("Graphical AWR report generator", divider='rainbow')
if "context" in st.session_state and "run" in st.session_state.context:
    url = st.session_state.context['url']
    cdb = st.session_state.context['cdb']
    mindate = st.session_state.context['mindate']
    maxdate = st.session_state.context['maxdate']
    oracle = st.session_state.context['oracle']
    flags = st.session_state.context['flags']
    top = st.session_state.context['top']
    grouping = st.session_state.context['grouping']
    oracle.vdollar = flags['ashvdollar']
url = st.text_input('Enter connection string to Oracle database...', url if 'url' in st.session_state.context else param.oracle if 'oracle' in param else '')
if url:
    oracle = Oracle(url) if 'oracle' not in st.session_state.context or url != st.session_state.context['url'] else oracle
    cdbs = oracle.listofcdbs()
    cdb = st.selectbox( 'Choose an instance in the following list ... (format : instance_name@host_name:dbid)', cdbs, cdbs.index(cdb) if 'cdb' in st.session_state.context else 1 if len(cdbs) == 2 else 0)
    if cdb:
        if 'cdb' in st.session_state.context and cdb != st.session_state.context['cdb']: oracle = Oracle(url)
        dbid = cdb.split(':')[1]
        dmin = oracle.getdmin(dbid)
        dmax = oracle.getdmax(dbid)
        st.success(f'{cdb} is associated to the following DBID: {dbid} and has AWR snapshots between {dmin} and {dmax}...')
        start_date = datetime.strptime(dmin, '%Y/%m/%d')
        end_date = datetime.strptime(dmax, '%Y/%m/%d')
        col1, col2 = st.columns([1,1])
        with col1:
            datemin = st.date_input("Enter the LOW value of the snapshot interval", datetime.strptime(mindate, "%Y%m%d000000") if 'mindate' in st.session_state.context and cdb == st.session_state.context['cdb'] else end_date)
        with col2:
            datemax = st.date_input("Enter the HIGH value of the snapshot interval", datetime.strptime(maxdate, "%Y%m%d000000") if 'maxdate' in st.session_state.context and cdb == st.session_state.context['cdb'] else end_date + timedelta(1))
        mindate = f'{datemin.year}{datemin.month:0>2}{datemin.day:0>2}000000'
        if 'mindate' in st.session_state.context and mindate != st.session_state.context['mindate']: oracle = Oracle(url)
        maxdate = f'{datemax.year}{datemax.month:0>2}{datemax.day:0>2}000000'
        if 'maxdate' in st.session_state.context and maxdate != st.session_state.context['maxdate']: oracle = Oracle(url)
        oracle.getsnapshots(mindate, maxdate, dbid)
        st.success(f"{len(oracle.snapshots.index)} snapshots have been selected between {datemin} and {datemax}")
        # min_sampling = np.log10(1)
        # max_sampling = np.log10(1000)
        # col1, col2 = st.columns([3,1])
        # with col1:
        #     samplingv = st.slider("Choose the ASH sampling value between 0 and 3 (0 : no sampling, 1 : 1/10 retained values, .... 3: 1/1000 retained values)", min_sampling, max_sampling, samplingv if 'samplingv' in st.session_state.context else min_sampling)
        #     sampling = 1 / (10 ** samplingv)
        # with col2:
        #     st.button(f'Sampling:\n{sampling}')
        min_top = 1
        max_top = 20
        col1, col2 = st.columns([3,1])
        with col1:
            top = st.slider("Choose the number of elements to display", min_top, max_top, top if 'top' in st.session_state.context else 7)
        with col2:
            st.button(f"Display: {top}")
        col1, col2 = st.columns([3,1])
        with col1:
            grouping = st.select_slider("Choose the grouping value", options=['second', '10 seconds', 'minute', '5 minutes', '10 minutes', '15 minutes', '20 minutes', '30 minutes', 'hour', '2 hours', '3 hours', '4 hours', '6 hours', '12 hours', 'day'], value=grouping if 'grouping' in st.session_state.context else '10 minutes')
        with col2:
            st.button(f'Grouping: {grouping}')
        flags = dict()
        with st.form("report"):
            col1, col2, col3, col4 = st.columns([1,1,1,1])
            with col1:
                flags['dbtime'] = st.checkbox('Db time', value=st.session_state.context['flags']['dbtime'] if 'flags' in st.session_state.context else True)
                flags['wev'] = st.checkbox('Wait events', value=st.session_state.context['flags']['wev'] if 'flags' in st.session_state.context else True)
                flags['srv'] = st.checkbox('Services', value=st.session_state.context['flags']['srv'] if 'flags' in st.session_state.context else False)
            with col2:
                flags['sta'] = st.checkbox('Main statistics', value=st.session_state.context['flags']['sta'] if 'flags' in st.session_state.context else False)
                flags['reqt'] = st.checkbox('Text of requests', value=st.session_state.context['flags']['reqt'] if 'flags' in st.session_state.context else False)
                flags['sga'] = st.checkbox('SGA', value=st.session_state.context['flags']['sga'] if 'flags' in st.session_state.context else False)
            with col3:
                flags['log'] = st.checkbox('Sessions', value=st.session_state.context['flags']['log'] if 'flags' in st.session_state.context else True)
                flags['oss'] = st.checkbox('Operating system statistics', value=st.session_state.context['flags']['oss'] if 'flags' in st.session_state.context else True)                
            with col4:
                flags['req'] = st.checkbox('Requests', value=st.session_state.context['flags']['req'] if 'flags' in st.session_state.context else False)
                flags['seg'] = st.checkbox('Segments', value=st.session_state.context['flags']['seg'] if 'flags' in st.session_state.context else False)
                flags['ashvdollar'] = st.checkbox('Take ash values from V$', value=st.session_state.context['flags']['ashvdollar'] if 'flags' in st.session_state.context else False)

            col1, col2, col3, col4 = st.columns([1,1,1,1])
            with col1:
                genawrrep =  st.form_submit_button('Generate AWR report')
            with col2:
                genashrep =  st.form_submit_button('Generate ASH report')
            with col3:
                custreq =  st.form_submit_button('Run custom request')
            col1, col2, col3, col4 = st.columns([1,1,1,1])
            with col1:
                chses =  st.form_submit_button('Choose session')
                chmet =  st.form_submit_button('Choose metric')
            with col2:
                chev =  st.form_submit_button('Choose event')
            with col3:
                chsta =  st.form_submit_button('Choose statistic')
            with col4:
                chreq =  st.form_submit_button('Choose request')
        #st.session_state.context = dict(url=url, cdb=cdb, mindate=mindate, maxdate=maxdate, flags=flags, sampling=sampling, samplingv=samplingv, top=top, grouping=grouping, oracle=oracle, run=True)
        st.session_state.context = dict(url=url, cdb=cdb, mindate=mindate, maxdate=maxdate, flags=flags, top=top, grouping=grouping, oracle=oracle, run=True)
        errorashvdollar = 'Taking ash value from V$ is only possible when selected database is the current database!'
        if genawrrep: switch_page('awrreport')
        if genashrep:
            if flags['ashvdollar'] and int(dbid) != oracle.getconndbid(): st.error(errorashvdollar)
            else: switch_page('ashreport')
        if chses:
            if flags['ashvdollar'] and int(dbid) != oracle.getconndbid(): st.error(errorashvdollar)
            else: switch_page('awrsession')
        if chev:
            if flags['ashvdollar'] and int(dbid) != oracle.getconndbid(): st.error(errorashvdollar)
            else: switch_page('awrevent')
        if chreq:
            if flags['ashvdollar'] and int(dbid) != oracle.getconndbid(): st.error(errorashvdollar)
            else: switch_page('awrrequest')
        if chsta:
            if flags['ashvdollar'] and int(dbid) != oracle.getconndbid(): st.error(errorashvdollar)
            else: switch_page('awrstatistic')
        if chmet: switch_page('awrmetric')
        if custreq: switch_page('awrcustreq')
class UserObject(dict):
    def __init__(self):
        object = {
            "type": "function",
            "id": "idlewev",
            "name": "idlewev",
            "function": """
                CREATE OR REPLACE FUNCTION idlewev(x text) RETURNS bool AS $$
                    return True if x[0:26] in [y[0:26].rstrip() for y in ['watchdog main loop', 'gcs remote message', 'ges remote message', 'PL/SQL lock timer', 'pipe get', 'wakeup time manager', 'queue messages', 'pmon timer', 'rdbms ipc message', 'lock manager wait for remote', 'i/o slave wait', 'class slave wait', 'smon timer', 'jobq slave wait', 'single-task message', 'SQL*Net message from client', 'Streams AQ: waiting for time management or cleanup tasks', 'Streams AQ: qmn coordinator idle wait', 'Streams AQ: qmn slave idle wait', 'Streams AQ: waiting for messages in the queue', 'wait for unread message on broadcast channel', 'DIAG idle wait', 'virtual circuit status', 'ASM background timer', 'lms flush message acks', 'Queue Monitor Wait', 'Queue Monitor Task Wait', 'Queue Monitor Slave Wait', 'heartbeat monitor sleep', 'Space Manager: slave idle', 'PING','LogMiner: wakeup event for b','LogMiner: wakeup event for r','LogMiner: wakeup event for p','LogMiner: reader waiting for','LogMiner: client waiting for','Streams capture: waiting for','Streams AQ: delete acknowled']] else False
                $$ language plpython3u;
            """
        }
        super(UserObject, self).__init__(**object)

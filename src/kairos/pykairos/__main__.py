#    This file is part of Kairos.
#
#    Kairos is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by

#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Kairos is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Kairos.  If not, see <http://www.gnu.org/licenses/>.
#
import argparse, json, multiprocessing, os, signal, subprocess, time, sys
from loguru import logger
from glob import glob
from pykairos.kairosnotifier import KairosNotifier

def set_logging_level(p):
    dlog = dict(Trace=5, Debug=10, Info=20, Success=25, Warning=30, Error=40, Critical=50)
    logger.remove()
    lvl = dlog[p]
    lf = ("<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <red>{process}</red> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | - <level>{message}</level>")
    lf = ("<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <red>{process: >6}</red> | <level>{level: <8}</level> | <level>{message}</level>")
    logger.add('/var/log/kairos/kairos.log', format=lf, level=lvl, rotation="10 MB", retention="30 days", compression="zip")
    logger.info(f'Logging has been set to {p}')

def catchrun(*c):
    v = dict(stop = False, processes=[])
    def handler(signum, stack):
        v['stop'] = True
    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)
    for x in c: v['processes'].append(subprocess.Popen(x))
    while True:
        for p in v['processes']:
            if p.poll() != None: v['stop'] = True
        if v['stop']: break
        time.sleep(1)
    for p in v['processes']:
        if p.poll() == None: p.send_signal(signal.SIGTERM)
        p.wait()

parser = argparse.ArgumentParser()
parser.add_argument('--version', action='version', version='KAIROS V@@VERSION@@')
parser.add_argument('--launcher', action='store_true', dest='launcher', help='The launcher is requested to start')
parser.add_argument('--monoprocess', action='store_true', dest='monoprocess', help='Only one subprocess required')
parser.add_argument('--notifier', action='store_true', dest='notifier', help='A notifier is requested to start')
parser.add_argument('--bootstrap', action='store_true', dest='bootstrap', help='Bootstraping the system')
parser.add_argument('--makeboot', action='store_true', dest='makeboot', help='Create boostrap data')
args = parser.parse_args()
set_logging_level('Info')
if args.notifier:
    n = KairosNotifier()
if args.launcher:
    logger.info(f'This system is configured with {multiprocessing.cpu_count()} cpus.')
    import setproctitle
    setproctitle.setproctitle('KairosMain')
    logger.info(f'Process name: {setproctitle.getproctitle()}')
    logger.info(f'Process id: {os.getpid()}')
    workers = 1 if args.monoprocess else multiprocessing.cpu_count() + 1
    gunicorn = ['gunicorn']
    gunicorn.extend(['-b', '0.0.0.0:443'])
    gunicorn.extend(['-k', 'aiohttp.worker.GunicornWebWorker'])
    gunicorn.extend(['-t0'])
    gunicorn.extend(['-p', '/var/log/gunicorn.pid'])
    gunicorn.extend(['-w', str(workers)])
    # gunicorn.extend(['--max-requests', '10'])
    # gunicorn.extend(['--max-requests-jitter', '5'])
    gunicorn.extend(['--keyfile', '/certificates/kairos.key'])
    gunicorn.extend(['--certfile', '/certificates/kairos.crt'])
    gunicorn.extend(['--access-logfile', '/var/log/kairos/webserver.log'])
    gunicorn.extend(['--log-file', '/var/log/kairos/webserver.log'])
    gunicorn.extend(['--chdir', '/kairos'])
    gunicorn.extend(['worker'])
    notifier = ['python']
    notifier.extend(['-m', 'pykairos', '--notifier'])
    os.system('rm -fr /var/log/gunicorn.pid')
    catchrun(gunicorn, notifier)

if args.bootstrap:
    os.system('/usr/sbin/crond')
    if len(os.listdir('/postgres/data')) == 0: os.system('cd /postgres; tar xvf /postgres/backups/pgboot.tar; chmod 700 /postgres/data')
    os.system('su - postgres -c "pg_ctl -D /postgres/data start"')
    os.system("python -m pykairos --launcher")
    
if args.makeboot:
    command = 'su - postgres -c "pg_ctl stop"'
    os.system('echo ' + "===============================================")
    os.system('echo ' + command)
    os.system(command)
    command = 'rm -fr  /postgres/boot; mkdir /postgres/boot; mkdir /postgres/boot/data; chown -R postgres:postgres /postgres/boot'
    os.system('echo ' + "===============================================")
    os.system('echo ' + command)
    os.system(command)
    command = 'su - postgres -c "initdb -D /postgres/boot/data -E UTF8 --no-locale"'
    os.system('echo ' + "===============================================")
    os.system('echo ' + command)
    os.system(command)
    command = 'su - postgres -c "pg_ctl -D /postgres/boot/data start"'
    os.system('echo ' + "===============================================")
    os.system('echo ' + command)
    os.system(command)
    command = 'su - postgres -c "echo ''local all postgres trust'' > /postgres/boot/data/pg_hba.conf"'
    os.system('echo ' + "===============================================")
    os.system('echo ' + command)
    os.system(command)
    command = 'su - postgres -c "echo ''host all postgres all trust'' >> /postgres/boot/data/pg_hba.conf"'
    os.system('echo ' + "===============================================")
    os.system('echo ' + command)
    os.system(command)
    command = 'su - postgres -c "echo ''host all all all md5'' >> /postgres/boot/data/pg_hba.conf"'
    os.system('echo ' + "===============================================")
    os.system('echo ' + command)
    os.system(command)
    command = 'su - postgres -c "echo ''log_min_duration_statement = -1'' >> /postgres/boot/data/postgresql.conf"'
    os.system('echo ' + "===============================================")
    os.system('echo ' + command)
    os.system(command)
    print('S', end='', flush=True)
    logger.info("Creating system database...")
    while True:
        print('s', end='', flush=True)
        logger.info("Trying to create system database...")
        time.sleep(1)
        crs = subprocess.run(['kairos', '-s', 'createsystem'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if not crs.returncode: break
    logger.info("System database created!")
    print('L', end='', flush=True)
    logger.info("Loading system database...")
    objects = []
    objects.extend(sorted(glob('/tmp/objects/liveobjects/*template*.py')))
    objects.extend(glob('/tmp/objects/*/*.py'))
    objects.extend(glob('/tmp/objects/*/*.jpg'))
    for o in objects:
       print('l', end='', flush=True)
       logger.info('Loading ' + o + " ...")
       try:
           json_string = subprocess.getoutput(f"kairos -s uploadobject --nodesdb kairos_system_system --file '{o}'")
           result = json.loads(json_string)
           success = result['success']
           if not success: logger.error(f'Error during loading of: {o}')
           else: logger.info(json.dumps(result))
       except:
           logger.error(f'Error during loading of: {o}')
           subprocess.run(['cat', '/var/log/kairos/kairos.log'])
           raise
    print('', flush=True)
    logger.info(f'{len(objects)} found objects in /tmp/objects!')
    data = json.loads(subprocess.getoutput('kairos -s listobjects --nodesdb kairos_system_system --systemdb kairos_system_system'))['data']
    logger.info(f"System database has {int((len(data)) / 2)} objects.")
    subprocess.run(['rm', '-fr', '/tmp/objects'])
    command = 'su - postgres -c "pg_ctl -D /postgres/boot/data stop"'
    os.system('echo ' + "===============================================")
    os.system('echo ' + command)
    os.system(command)
    command = 'cd /postgres/boot; rm -fr /postgres/backups/*; tar cvf /postgres/backups/pgboot.tar data'
    os.system('echo ' + "===============================================")
    os.system('echo ' + command)
    os.system(command)
    command = 'rm -fr /postgres/boot'
    os.system('echo ' + "===============================================")
    os.system('echo ' + command)
    os.system(command)

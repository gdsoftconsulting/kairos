import sys
from fabric import task
from fabric import Connection
from loguru import logger

VERSION='9.6'
PORTKAIROS = 44396
PORTSTREAMLIT = 8510
IMAGE = f'gdsc/kairos:{VERSION}'
MACHINE = f'kairos{VERSION}'
NETWORK = 'mynetwork'
KAIROSDATA = '/root/kairosdata'

#### Pour fabriquer le vrai fichier "fabfile.py", la commande suivante doit être modifiée avec le vrai nom du serveur
#### Il faut également installer la clé SSH qui permet de se connecter root sur le serveur ssans fournir de mot de passe
REMOTE = "root@srv665069.hstgr.cloud"

def remotecmd(command):
    #logger.info(f'Remote connection: {REMOTE}')
    conn = Connection(f"{REMOTE}")
    logger.info(f'{command}')
    conn.run(command, pty=True)

def localcmd(c, command, **d):
    logger.info(f'LOCAL : {command}')
    c.run(command, **d)

@task
def images(c): 
    remotecmd('docker images')

@task
def prune(c): 
    remotecmd('docker image prune')

@task
def ps(c): 
    remotecmd('docker ps')

@task
def psa(c): 
    remotecmd('docker ps -a')

@task
def start(c): 
    remotecmd(f'docker start {MACHINE}')

@task
def stop(c): 
    remotecmd(f'docker exec {MACHINE} su - postgres -c "pg_ctl stop -m fast"')
    remotecmd(f'docker stop {MACHINE}')

@task
def abort(c): 
    remotecmd(f'docker stop {MACHINE}')

@task
def rm(c): 
    remotecmd(f'docker rm {MACHINE}')

@task
def rmi(c, name): 
    remotecmd(f'docker rmi {name}')

@task
def sh(c): 
    remotecmd(f'docker exec -it {MACHINE} bash')
 
@task
def logs(c): 
    remotecmd(f'docker logs {MACHINE}')

@task
def initremote(c):
    remotecmd("mkdir -p /root/kairos")
    remotecmd("mkdir -p /root/kairosdata")
    remotecmd("rm -fr /root/kairos/*")

@task
def tunnel(c):
    c.run(f'ssh -L {PORTKAIROS}:localhost:{PORTKAIROS} -L {PORTSTREAMLIT}:localhost:{PORTSTREAMLIT} {REMOTE}', pty=True)

@task
def image(c):
    logger.info('Building tar file with required element for kairos')
    c.run('tar cvf /tmp/kairos.tar kairos.docker src/* deps/* certificates/* 2>/dev/null')    
    logger.info('Copying tar file to remote destination')
    c.run(f'scp /tmp/kairos.tar {REMOTE}:/tmp')
    remotecmd('cd /root/kairos; rm -fr /root/kairos/*; tar xvf /tmp/kairos.tar >/dev/null 2>&1;rm /tmp/kairos.tar')
    remotecmd(f"cd /root/kairos; sed -i 's/@@VERSION@@/{VERSION}/g' src/kairos/client.js")
    remotecmd(f"cd /root/kairos; sed -i 's/@@VERSION@@/{VERSION}/g' src/kairos/kairos")
    remotecmd(f"cd /root/kairos; sed -i 's/@@VERSION@@/{VERSION}/g' src/kairos/setup.py")
    remotecmd(f"cd /root/kairos; sed -i 's/@@VERSION@@/{VERSION}/g' src/kairos/pykairos/__main__.py")
    remotecmd(f"cd /root/kairos; sed -i 's/@@VERSION@@/{VERSION}/g' kairos.docker")
    remotecmd(f'cd /root/kairos; docker build -f kairos.docker -t {IMAGE} .')
    remotecmd(f'docker image prune -f')
    remotecmd(f'docker images')


@task
def machine(c):
	remotecmd(f"docker create -it --name {MACHINE} -h {MACHINE} -p {PORTKAIROS}:443 -p {PORTSTREAMLIT}:8501 -v {KAIROSDATA}/{VERSION}/data:/postgres/data -v {KAIROSDATA}/export:/export -v {KAIROSDATA}/autoupload:/autoupload {IMAGE}")
	#remotecmd(f"docker create -it --name {MACHINE} -h {MACHINE} -p {PORTKAIROS}:443 -p {PORTSTREAMLIT}:8501 -v {KAIROSDATA}/{VERSION}/data:/postgres/data -v {KAIROSDATA}/export:/export -v {KAIROSDATA}/autoupload:/autoupload -v {KAIROSDATA}/certificates:/certificates {IMAGE}")
	remotecmd(f"docker network connect {NETWORK} {MACHINE}")


@task
def localmachine(c):
	print(f"docker create -it --name {MACHINE} -h {MACHINE} -p {PORTKAIROS}:443 -p {PORTSTREAMLIT}:8501 -v {KAIROSDATA}/{VERSION}/data:/postgres/data -v {KAIROSDATA}/export:/export -v {KAIROSDATA}/autoupload:/autoupload {IMAGE}")
	#remotecmd(f"docker create -it --name {MACHINE} -h {MACHINE} -p {PORTKAIROS}:443 -p {PORTSTREAMLIT}:8501 -v {KAIROSDATA}/{VERSION}/data:/postgres/data -v {KAIROSDATA}/export:/export -v {KAIROSDATA}/autoupload:/autoupload -v {KAIROSDATA}/certificates:/certificates {IMAGE}")


@task
def network(c):
	remotecmd(f"docker network create {NETWORK}")

@task
def ssh(c):
    c.run(f'ssh {REMOTE}', pty=True)

@task
def boot(c):
    logger.warning('Boot target will destroy the current container, a new image will be built and a new container too!')
    remotecmd(f"docker cp /root/kairos/src/kairos/objects {MACHINE}:/tmp")
    remotecmd(f"docker exec {MACHINE} sh -c 'python -m pykairos --makeboot'")
    remotecmd(f"docker cp {MACHINE}:/postgres/backups/pgboot.tar /root/kairos/deps/tar")
    logger.info('Getting pgboot.tar ...')
    c.run(f'scp {REMOTE}:/root/kairos/deps/tar/pgboot.tar deps/tar')
    abort(c)
    rm(c)
    image(c)
    machine(c)

@task
def monitoring(c):
    command = 'psql -c "create database kairos"'
    remotecmd(f"docker exec {MACHINE} su - postgres -c '{command}'")
    command = 'psql -d kairos -c "create extension plpython3u"'
    remotecmd(f"docker exec {MACHINE} su - postgres -c '{command}'")    
    command = 'psql -d kairos -c "create extension pgkairos"'
    remotecmd(f"docker exec {MACHINE} su - postgres -c '{command}'")

@task
def deliver(c):
    remotecmd(f"docker tag gdsc/kairos:{VERSION} gdsc/kairos:latest")
    remotecmd(f"docker push gdsc/kairos:latest")
    remotecmd(f"docker push gdsc/kairos:{VERSION}")

@task
def commit(c):
    c.run(f"git status")
    c.run(f"git commit -m 'Kairos version: {VERSION}'")    
    c.run(f"git push")

@task
def gitreset(c):
    localcmd(c, f'rm -fr .git')
    localcmd(c, f'git init')
    localcmd(c, f'git checkout --orphan main')
    localcmd(c, f'git lfs track "*.tar"')
    localcmd(c, f'git lfs track "*.zip"')
    localcmd(c, f'git add .')
    localcmd(c, f'git commit -m "Initial commit"')
    localcmd(c, f'git status')
    localcmd(c, f'git remote add origin git@github.com:gdsoftconsulting/kairos.git')
    localcmd(c, f'git remote -v')
    localcmd(c, f'git push --force origin main')
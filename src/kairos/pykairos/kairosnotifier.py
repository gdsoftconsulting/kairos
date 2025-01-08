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

import multiprocessing, os, asyncio, setproctitle
from pathlib import Path
from asyncinotify import Inotify, Mask
from loguru import logger

async def process():
    logger.info('Init notification process...')
    with Inotify() as inotify:
        inotify.add_watch('/autoupload', Mask.ACCESS | Mask.MODIFY | Mask.OPEN | Mask.CREATE | Mask.DELETE | Mask.ATTRIB | Mask.CLOSE | Mask.MOVE | Mask.ONLYDIR)
        logger.info('Watching directory: /autoupload ...')
        for d in os.listdir('/autoupload'):
            wdir = '/autoupload/' + d
            if 'kairos_' in d and os.path.isdir(wdir):
                inotify.add_watch(wdir, Mask.ACCESS | Mask.MODIFY | Mask.OPEN | Mask.CREATE | Mask.DELETE | Mask.ATTRIB | Mask.CLOSE | Mask.MOVE | Mask.ONLYDIR)
                logger.info(f'Watching directory: {wdir} ...')
                for f in os.listdir(wdir): os.system('touch ' + wdir + '/' +f)
        multiprocessing.current_process().name = 'NotifyProcess'
        logger.info('Starting notification process...')
        setproctitle.setproctitle('KairosNotifier')
        logger.info(f'Process name: {setproctitle.getproctitle()}')
        logger.info(f'Process id: {os.getpid()}')
        async for event in inotify:
            path = str(event.path)
            if 'kairos_' in path and os.path.isdir(path) and Mask.CREATE in event.mask:
                inotify.add_watch(event.path, Mask.ACCESS | Mask.MODIFY | Mask.OPEN | Mask.CREATE | Mask.DELETE | Mask.ATTRIB | Mask.CLOSE | Mask.MOVE | Mask.ONLYDIR)
                logger.info(f'Watching directory: {path} ...')
            if 'kairos_' in path and not os.path.isdir(path) and os.path.isfile(path):
                if Mask.OPEN in event.mask or Mask.MODIFY in event.mask:
                    if os.path.basename(path)[0] != '.':
                        cmd=f'kairos -s uploadnode --systemdb kairos_system_system --nodesdb {os.path.basename(os.path.dirname(path))} --id 1 --file {path}'
                        logger.info(f'Trying to execute: {cmd}')
                        status = os.system(cmd)
                        if status == 0: 
                            os.remove(path)
                            logger.info(f"File '{path}' has been uploaded to {os.path.basename(os.path.dirname(path))}!")

class KairosNotifier:
    def __init__(self):
        asyncio.run(process())
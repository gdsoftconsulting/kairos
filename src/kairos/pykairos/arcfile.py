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

import multiprocessing, tarfile, time, zipfile

from io import StringIO
from loguru import logger


class Arcfile:

    def __init__(self, file, mode='r'):
        self.lock = multiprocessing.Lock()
        opmode=mode.split(':')
        self.type='unknown'
        if opmode[0] in ['r','a']:
            if zipfile.is_zipfile(file):
                self.archive=zipfile.ZipFile(file,mode)
                self.type='zipfile'
            else:
                file.seek(0)
                try:
                    self.archive=tarfile.open(fileobj=file)
                    self.type='tarfile'
                except:
                    logger.error('Unknown file type')
        else:
            if len(opmode)>1 and opmode[1] in ['zip']:
                self.type='zipfile'
                self.archive=zipfile.ZipFile(file,opmode[0],zipfile.ZIP_DEFLATED)
            else: self.archive=tarfile.open(name='stream', mode='w+b', fileobj=file)

    def close(self):
        return self.archive.close()

    def list(self):
        if self.type=='tarfile': return self.archive.getnames()
        else: return self.archive.namelist()

    def read(self, member):
        self.lock.acquire()
        if self.type=='tarfile':
            try: 
                r = bz2.decompress(self.archive.extractfile(self.archive.getmember(member).name).read())
            except: 
                r = self.archive.extractfile(self.archive.getmember(member).name).read()
        else:
            try: 
                r = bz2.decompress(self.archive.read(member))
            except: 
                r = self.archive.read(member)
        self.lock.release()
        return r
        
    def write(self, member, stream):
        if self.type=='tarfile':
            inf=tarfile.TarInfo()
            inf.name=member
            inf.size=len(stream)
            inf.mtime = time.time()
            return self.archive.addfile(inf, io.StringIO(stream))
        else: return self.archive.writestr(member,stream)

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

import multiprocessing

class Parallel:
    
    def __init__(self, action, workers=multiprocessing.cpu_count()):
        self.limit = int(workers)
        self.workers = dict()
        self.action = action

    def push(self, arg):
        if len(self.workers.keys()) < self.limit:
            p = multiprocessing.Process(target=self.action, args=(arg,))
            p.start()
            self.workers[p.sentinel] = p
        else:
            if len(self.workers.keys()) == self.limit:
                x = multiprocessing.connection.wait(self.workers.keys())
                for e in x:
                    self.workers[e].join()
                    del self.workers[e]
                p = multiprocessing.Process(target=self.action, args=(arg,))
                p.start()
                self.workers[p.sentinel] = p

    def join(self):
        while len(self.workers):
            x = multiprocessing.connection.wait(self.workers.keys())
            for e in x:
                self.workers[e].join()
                del self.workers[e]

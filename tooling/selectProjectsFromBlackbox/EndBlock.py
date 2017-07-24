#
# Copyright 2017 Niels Doorn Licensed under the Educational
# Community License, Version 2.0 (the "License"); you may not use this file
# except in compliance with the License. You may obtain a copy of the License at
# 
# http://opensource.org/licenses/ECL-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
#
from __future__ import print_function

import os
import codecs

class EndBlock:

    def __init__(self, maxProjects, filename):
        self.maxProjects = maxProjects
        self.projects = set()
	try:
	    os.stat("output/")
	except:
            os.makedirs("output/")
        self.outFile = codecs.open("output/"+filename, "a", encoding="utf-8")
        print("PROJECT ID,SESSION ID,USER ID,SOURCES", file=self.outFile)
        
    def process(self, project):
        if len(self.projects) < self.maxProjects:
            self.projects.add(project)
            print(project, file=self.outFile)
            print(">>>> Adding project number %d of %d!" % (len(self.projects), self.maxProjects))

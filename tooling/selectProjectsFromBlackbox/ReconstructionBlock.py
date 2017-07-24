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
from __future__ import unicode_literals

import os
import codecs
from subprocess import call
from SourceFile import SourceFile

class ReconstructionBlock:

    def __init__(self, name, nextBlock=None):
        self.name = name
        self.nextBlock = nextBlock
        os.makedirs("output/"+self.name)        
        
        
    def process(self, project):
        os.makedirs("output/%s/%s" % (self.name, project.projectId))
        
        for f in project.files:
            if len(f.name.split('/')) > 1:
                theDir = "output/%s/%s/%s" % (self.name, project.projectId, f.name[:f.name.rfind('/')])
		try:
               	    os.stat(theDir)
		except:
    		    os.makedirs(theDir)   
                    print(">>> making subdirs %s" % theDir)
            
            with codecs.open("output/%s/%s/%s" % (self.name, project.projectId, f.name), "w+", encoding="utf-8") as output:
                call(["/tools/nccb/bin/print-compile-input", "/data/compile-inputs", str(f.sourceFileId), str(f.masterEventId)], stdout=output)            
		
        if self.nextBlock is not None:
            self.nextBlock.process(project)

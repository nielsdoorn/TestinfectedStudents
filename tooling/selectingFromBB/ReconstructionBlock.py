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
        print("[CON] Making dir: output/%s/%s" % (self.name, project.projectId))
        os.makedirs("output/%s/%s" % (self.name, project.projectId))
        
        for f in project.files:
            if len(f.name.split('/')) > 1:
                theDir = "output/%s/%s/%s" % (self.name, project.projectId, f.name[:f.name.rfind('/')])
		try:
            os.stat(theDir)
		except:
    		os.makedirs(theDir)   
            print("[CON]  making subdirs %s" % theDir)
            
        with codecs.open("output/%s/%s/%s" % (self.name, project.projectId, f.name), "w+", encoding="utf-8") as output:
            print("[CON] call print compile output with: src: %s mastereventid: %s" % (str(f.sourceFileId), str(f.masterEventId)))
            call(["/tools/nccb/bin/print-compile-input", "/data/compile-inputs", str(f.sourceFileId), str(f.masterEventId)], stdout=output)            
		
        if self.nextBlock is not None:
            self.nextBlock.process(project)

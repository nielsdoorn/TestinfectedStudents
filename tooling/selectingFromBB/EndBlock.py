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
        if len(self.projects) < self.maxProjects or self.maxProjects == -1:
            self.projects.add(project)
            print(project, file=self.outFile)
            print(">>>> Adding project number %d of %d!" % (len(self.projects), self.maxProjects))

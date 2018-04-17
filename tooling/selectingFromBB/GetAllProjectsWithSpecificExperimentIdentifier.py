from __future__ import unicode_literals

import sys
import pymysql.cursors
import datetime

from EndBlock import EndBlock
from UserCheckerBlock import UserCheckerBlock
from ProjectSizeCheckerBlock import ProjectSizeCheckerBlock
from ProjectCompilationCheckerBlock import ProjectCompilationCheckerBlock
from SessionSelectionBlock import SessionSelectionBlock
from ProjectTestCheckerBlock import ProjectTestCheckerBlock
from ReconstructionBlock import ReconstructionBlock

import os
import codecs

sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

config = {}
config['projects'] = set()
config['experimentid'] = 'testinfected2017'

dbusername = os.environ['BBDBUSER']
dbpassword = os.environ['BBDBPASS']


# Connect to the database
connection = pymysql.connect(host='localhost',
                             port=3306,
                             user=dbusername,
                             password=dbpassword,
                             db='blackbox_production',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        print("Creating the pipelines...")
        
        timestamp = datetime.datetime.now()
        print("Reference time is %s" % timestamp) 
        
        # a pipeline that samples the dataset for projects big enough & within a time frame & that compiled succesfully
        end = EndBlock(config['samplesize'], "%s_projects.txt" % timestamp)
        recon = ReconstructionBlock("%s_samples" % timestamp, end)
        ucb = UserCheckerBlock(cursor, recon)
        pccb = ProjectCompilationCheckerBlock(cursor, config['firstTime'], config['lastTime'], ucb)
        pscb = ProjectSizeCheckerBlock(cursor, config['minclasses'], pccb)
        ssb = SessionSelectionBlock(cursor, config['firstTime'], config['lastTime'], pscb)
        
        print("Starting the processing...")
        # start the processing in all the pipelines
        while len(end.projects) < config['samplesize']:
            ssb.process()
                
        print("Done.")
    
finally:
    connection.close()

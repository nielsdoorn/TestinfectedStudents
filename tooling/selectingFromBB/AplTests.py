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
config['firstTime'] = "2016-09-01 00:00:00" # 19263484
config['lastTime'] = "2017-07-01 00:00:00" # 26911088
config['samplesize'] = 1000
config['samplesizeTests'] = 1000
config['minclasses'] = 4

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
        
        # projects that samples the dataset for big enough projects within a time frame that compiled succesfully containing tests
        endTests = EndBlock(config['samplesizeTests'], "%s_test_projects.txt" % timestamp)
        reconTests = ReconstructionBlock("%s_tests" % timestamp, endTests)
        ucbTests = UserCheckerBlock(cursor, reconTests)
        pccbTests = ProjectCompilationCheckerBlock(cursor, config['firstTime'], config['lastTime'], ucbTests)
        ptcbTests = ProjectTestCheckerBlock(cursor, config['minclasses'], pccbTests)
        ssbTests = SessionSelectionBlock(cursor, config['firstTime'], config['lastTime'], ptcbTests)

        print("Starting the processing...")
        # start the processing in all the pipelines
        while len(endTests.projects) < config['samplesizeTests']:
            ssbTests.process()
                
        print("Done.")
    
finally:
    connection.close()

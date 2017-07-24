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
        
        # a pipeline that samples the dataset for big enough projects within a time frame that compiled succesfully
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

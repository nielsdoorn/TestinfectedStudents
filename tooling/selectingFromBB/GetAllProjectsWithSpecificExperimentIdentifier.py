from __future__ import unicode_literals

import sys
import pymysql.cursors
import datetime

from EndBlock import EndBlock
from SelectProjectsWithExpId import SelectProjectsWithExpId
from ReconstructionBlock import ReconstructionBlock

import os
import codecs

sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

config = {}
config['projects'] = set()
config['experimentid'] = 'testinfected2017'
config[start] = '2017-08-28 00:00:00'
config[end] = '2017-11-13 00:00:00'

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
        end = EndBlock(-1, "%s_experiments.txt" % timestamp)
        recon = ReconstructionBlock("%s_experiment" % timestamp, end)
        expidselection = SelectProjectsWithExpId(cursor, config['experimentid'], config['start'], config['end'], recon)
        
        print("Starting the processing...")
        # start the processing in all the pipelines

        expidselection.process()
                
        print("Done.")
    
finally:
    connection.close()

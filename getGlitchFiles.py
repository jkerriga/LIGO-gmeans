#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# This module is for finding glitch files (Laura's old Wdata files)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from numpy import *
import os, commands, sys

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Returns a list of paths to glitch files to be searched when looking for glitches between 'start' and 'stop'
# 'start' and 'stop' must be integer gps times
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def getGlitchFiles(ifo,seg_start,seg_stop):

   start = int(seg_start)
   stop = int(seg_stop)

   start_date = commands.getoutput('tconvert -f %D ' + seg_start)
   stop_date  = commands.getoutput('tconvert -f %D ' + seg_stop)

   start_day = int(commands.getoutput('tconvert ' + str(start_date)))
   stop_day  = int(commands.getoutput('tconvert ' + str(stop_date)))

   num_days = (stop_day - start_day)/86400 + 1

   glitch_files = []

   # For each day, find the glitch file
   for i in range(num_days):

       day_start = start_day + i*86400
       day_stop  = day_start + 86400

       # Construct path to glitch file

       filepath = '/home/detchar/public_html/S6/glitch/Wdata/' + str(day_start) + '_' + str(day_stop) +'/clusters.txt'

       if not(os.path.isfile(filepath)):
           print 'Glitch file does not exist; check path for errors!'
           print filepath
           sys.exit()
       else:
           glitch_files.append(filepath)

   return glitch_files

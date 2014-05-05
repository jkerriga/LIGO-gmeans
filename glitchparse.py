#! /usr/bin/env python
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Some examples for finding science data and finding glitch files
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from __future__ import division
from numpy import *
import matplotlib
matplotlib.use("Agg")
from matplotlib.font_manager import FontProperties
import pylab
import commands, sys, time, os
from getGlitchFiles import getGlitchFiles
from numpy import max


def glitchparse(start_time,end_time,snr_low,snr_high,freq_low,freq_high):

    ifo = 'H1'

    # The following commands are how you find science segments between the start and end times 
    # First command queries the segment database for SCIENCE segments between the start and end times; prints these segments into a    n xml-format file
    # Second command parses that xml file into a space-delimited list of segment start, stop times
    # Sometimes querying the server can take a while (several minutes).  Be patient!
    # ligolw_segment_query -dqa H1:DMT-SCIENCE -s 958694415 -e 959126415 -o segments.xml
    cmd1 = 'ligolw_segment_query -dqa "' + ifo + ':DMT-SCIENCE" -s ' + start_time + ' -e ' + end_time + ' -o segments.xml'
    cmd2 = 'ligolw_print -t segment -c start_time -c end_time segments.xml -d " "'

    commands.getoutput(cmd1)
    segment_list = commands.getoutput(cmd2)
    cmd3 = 'rm segments.xml'
    commands.getoutput(cmd3)

    # Instead of a huge string of segments and endline characters, split the string into rows when you see an endline (\n).    
    segments = segment_list.rsplit('\n')

    # Now you have an array of segments, and you can loop over them.
    science_times = []
    glitch_list = []
    cent_time_list = []
    i=0
    p = 0
    for segment in segments:
        i = i+1
        seg_start, seg_stop = segment.split()

        start = int(seg_start)
        stop = int(seg_stop)
        
        science_times = append(science_times,float(stop)-float(start))
        # The glitch files are arranged by day.
        # Use a helper function to find the location of the glitch files.

        glitch_files = getGlitchFiles(ifo[0],seg_start,seg_stop)

        num_glitches = 0
        day = 86400
        q = 0
        for gfile in glitch_files:
            
            # Read the glitch file
            f = open(gfile)
            events = f.readlines()
            f.close()
            p = 0
            # Loop over each line in the file, skipping the first line
            for event in events:
                
                if event[0] == '#':
                    continue

                #Changed to parse files correctly
                cl_start,cl_stop,cl_peak,cl_fmin,cl_fmax,cl_nev,Mst_start,Mst_stop,MS_fmin,MS_fmax,cl_size,norm_En,MS_SNR = event.split()      
                #if q == 0:
                #    time_start = float(cl_peak)
                #    q += 1
                #if float(cl_peak)-float(time_start) > (p+1)*day:
                #    p += 1
                
                peak_time = float(cl_peak)
                cl_nev = float(cl_nev)
                event_time = float(cl_start)
                duration = float(cl_stop)-float(cl_start)
                bandwidth = float(cl_fmax)-float(cl_fmin)
                MS_freq= (float(MS_fmax)+float(MS_fmin))/2.0
                MS_snr = sqrt(2*float(MS_SNR))
                cl_freq_av = (float(cl_fmin)+float(cl_fmax))/2.0
                peak_freq = MS_freq - cl_freq_av
                cent_time = (float(cl_start)+float(cl_stop))/2.0
                peak_start = peak_time - float(cl_start)
                peak_end = float(cl_stop) - peak_time
                MS_bandwidth = float(MS_fmax)-float(MS_fmin)
                MS_Q = MS_freq/MS_bandwidth
                
                freq_begin = MS_freq - float(cl_fmin)
                freq_end = float(cl_fmax) - MS_freq
                
                
                # Only consider events inside of the segment...
                if (event_time > stop):
                    break

                elif (event_time < start) or (MS_snr < snr_low) or (MS_snr > snr_high) or (MS_freq < freq_low) or (MS_freq > freq_high):
                    continue

                else:
                    #avg(MS_fmin,MS_fmax)-avg(cl_fmin,cl_max)
                    #avg(cl_fmin,cl_max)
                    glitch = [MS_freq, MS_snr, MS_bandwidth, MS_Q, duration, bandwidth, cl_nev, cl_freq_av, peak_freq, peak_start, peak_end, freq_begin, freq_end]
                    glitch_list.append(glitch)
                    num_glitches = num_glitches + 1
                    all_time = [cent_time,peak_time]
                    cent_time_list.append(all_time)


    glitches = vstack((glitch_list))
    science_times = sum(science_times)
    glitch_number = shape(glitches)
    return glitches,science_times,glitch_number[0],cent_time_list

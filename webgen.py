#! /usr/bin/env python                                                                                                              
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~                                          
# This script will generate an MCIV results webpage                                                                                 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~                                          
from numpy import *
import commands, sys, time, os
from optparse import OptionParser
from glue import segmentsUtils
from glue.segments import *

def webgen(ks,gps_start,gps_end,mean,std,dim,snr_low,snr_high,freq_low,freq_high,sci_time,g_found,new_path,the_k,ID):

    root_directory = '/home/'+str(ID)+'/public_html/'+new_path[27:]+'/'
    web_directory = root_directory
    www_root = 'https://ldas-jobs.ligo-wa.caltech.edu/~'+str(ID)+'/'
    www_directory = www_root
    cluster_dir = 'clustered/'
    snr_dir = 'SNR'+str(snr_low)+'-'+str(snr_high)+'Freq'+str(freq_low)+'-'+str(freq_high)+'/'

    start_date = commands.getoutput('tconvert %s '%gps_start)
    end_date = commands.getoutput('tconvert %s '%gps_end)
    empty = 'empty'
    html_file = 'SNR_'+str(snr_low)+'-'+str(snr_high)+'Freq'+str(freq_low)+'-'+str(freq_high)+'.html'
    webfilename = web_directory + html_file

    webfile = open(webfilename, 'w')
    ifo = 'H1'
    title = 'Cluster Data Output ' + ifo
    header_text = 'Cluster Data Output'
    webfile.write('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">\n')
    webfile.write('<html>\n')
    webfile.write('<head>\n')
    webfile.write('  <title> ' + title + ' </title>\n')
    webfile.write('  <style type="text/css">\n')
    webfile.write('body {\n')

    webfile.write('font-family: Garamond,Times,serif;\n')
    webfile.write('color: black;\n')
    webfile.write('background-color: white;\n')
    webfile.write('}\n')
    webfile.write('h1 {\n')
    webfile.write('color: #ffffff;\n')

    webfile.write('background-color: #4f81bd;\n')
    webfile.write('padding: 0.35em;\n')
    webfile.write('border: 1px solid black;\n')
    webfile.write('}\n')
    webfile.write('h2 {\n')
    webfile.write('color: #000000;\n')

    webfile.write('background-color: #dee4fa;\n')
    webfile.write('padding: 0.35em;\n')
    webfile.write('border: 1px solid black;\n')
    webfile.write('}\n')
    webfile.write('  </style>\n')
    webfile.write(' <script type="text/javascript">\n')
    webfile.write(' function toggleVisible(division) {\n')
    webfile.write(' if (document.getElementById("div_" + division).style.display == "none") {\n')
    webfile.write(' document.getElementById("div_" + division).style.display = "block";\n')
    webfile.write(' document.getElementById("input_" + division).checked = true;\n')
    webfile.write(' } else {\n')
    webfile.write(' document.getElementById("div_" + division).style.display = "none";\n')
    webfile.write(' document.getElementById("input_" + division).checked = false;\n')
    webfile.write(' }\n')
    webfile.write(' }\n')
    webfile.write(' </script>\n')
    webfile.write('</head>\n')
    webfile.write('<body>\n')
    webfile.write('<h1>Clustering Data Output</h1>\n')

    webfile.write('<h2><font face="Times" size="5">Glitch Data Plots</font></h2>\n')

    webfile.write('<br><table border=1 cellspacing="1" cellpadding="5">\n')

    webfile.write('<tr>\n')
    webfile.write('<td> IFO </td>\n')
    webfile.write('<td> ' + ifo + '\n')
    webfile.write(' </td>\n')
    webfile.write('</tr>\n')
    
    webfile.write('<tr>\n')
    webfile.write('<td> P-Value </td>\n')
    webfile.write('<td> '+ str(ks) +'\n')
    webfile.write(' </td>\n')
    webfile.write('</tr>\n')

    webfile.write('<tr>\n')
    webfile.write('<td> SNR Range </td>\n')
    webfile.write('<td> '+ str(snr_low) + '-' + str(snr_high) +'\n')
    webfile.write(' </td>\n')
    webfile.write('</tr>\n')
    
    webfile.write('<tr>\n')
    webfile.write('<td> Frequency Range </td>\n')
    webfile.write('<td> '+ str(freq_low) + '-' + str(freq_high) +'\n')
    webfile.write(' </td>\n')
    webfile.write('</tr>\n')
    
    webfile.write('<tr>\n')
    webfile.write('<td> GPS Time Start </td>\n')
    webfile.write('<td> ' + start_date + ' \n')
    webfile.write(' </td>\n')
    webfile.write('</tr>\n')
    webfile.write('<tr>\n')
    webfile.write('<td> GPS Time End </td>\n')
    webfile.write('<td> ' + end_date + ' \n')
    webfile.write(' </td>\n')
    webfile.write('</tr>\n')
    
    webfile.write('<tr>\n')
    webfile.write('<td> Glitches Found </td>\n')
    webfile.write('<td> '+ str(g_found) +'\n')
    webfile.write(' </td>\n')
    webfile.write('</tr>\n')

    webfile.write('<tr>\n')
    webfile.write('<td> Total Science Time </td>\n')
    webfile.write('<td> ' + str(sci_time) +'s'+ '('+str(round(24*(sci_time/86400),3))+'hours)'+ ' \n')
    webfile.write(' </td>\n')
    webfile.write('</tr>\n')
    webfile.write('</table>')
    
    #webfile.write('<br><TABLE BORDER=1><TR>')
    #webfile.write('<tr>\n')
    

    webfile.write('<table border=1 cellspacing="1" cellpadding="5">')

    webfile.write('<tr>\n')
    webfile.write('<td> '+dim[0]+' </td>\n')
    webfile.write('<td> Frequency of the the Most Significant tile in the cluster.(Average of MS Freq Max and MS Freq Min.) \n')
    webfile.write(' </td>\n')
    webfile.write('</tr>\n')

    webfile.write('<tr>\n')
    webfile.write('<td> '+dim[1]+' </td>\n')
    webfile.write('<td> SNR of the Most Significant tile in the cluster.(sqrt(2*MS_SNR))) \n')
    webfile.write(' </td>\n')
    webfile.write('</tr>\n')

    webfile.write('<tr>\n')
    webfile.write('<td> '+dim[2]+' </td>\n')
    webfile.write('<td> Bandwidth of the Most Significant tile in the cluster.(MS Freq Max - MS Freq Min) \n')
    webfile.write(' </td>\n')
    webfile.write('</tr>\n')

    webfile.write('<tr>\n')
    webfile.write('<td> '+dim[3]+' </td>\n')
    webfile.write('<td> Q factor of Most Significant tile.(MS Freq/MS Bandwidth) \n')
    webfile.write(' </td>\n')
    webfile.write('</tr>\n')

    webfile.write('<tr>\n')
    webfile.write('<td> '+dim[4]+' </td>\n')
    webfile.write('<td> Duration of the clustered events.(Cluster Stop - Cluster Start) \n')
    webfile.write(' </td>\n')
    webfile.write('</tr>\n')

    webfile.write('<tr>\n')
    webfile.write('<td> '+dim[5]+' </td>\n')
    webfile.write('<td> Bandwidth of the clustered events.(Cluster Freq Max -Cluster Freq Min) \n')
    webfile.write(' </td>\n')
    webfile.write('</tr>\n')

    webfile.write('<tr>\n')
    webfile.write('<td> '+dim[6]+' </td>\n')
    webfile.write('<td> Cluster n Events \n')
    webfile.write(' </td>\n')
    webfile.write('</tr>\n')

    webfile.write('<tr>\n')
    webfile.write('<td> '+dim[7]+' </td>\n')
    webfile.write('<td> Cluster Average Frequency.(Average of Cluster Freq Min and Max) \n')
    webfile.write(' </td>\n')
    webfile.write('</tr>\n')

    webfile.write('<tr>\n')
    webfile.write('<td> '+dim[8]+' </td>\n')
    webfile.write('<td> Cluster Peak Frequency Average(Most Significant Frequency Average - Cluster Frequency Average) \n')
    webfile.write(' </td>\n')
    webfile.write('</tr>\n')

    webfile.write('<tr>\n')
    webfile.write('<td> '+dim[9]+' </td>\n')
    webfile.write('<td> Initial Peak Time (Cluster Peak Time - Cluster Start Time) \n')
    webfile.write(' </td>\n')
    webfile.write('</tr>\n')

    webfile.write('<tr>\n')
    webfile.write('<td> '+dim[10]+' </td>\n')
    webfile.write('<td> Final Peak Time (Cluster Stop Time - Cluster Peak Time) \n')
    webfile.write(' </td>\n')
    webfile.write('</tr>\n')

    webfile.write('<tr>\n')
    webfile.write('<td> '+dim[11]+' </td>\n')
    webfile.write('<td> Cluster Initial Peak Frequency (Most Significant Frequency - Cluster Frequency Min) \n')
    webfile.write(' </td>\n')
    webfile.write('</tr>\n')

    webfile.write('<tr>\n')
    webfile.write('<td> '+dim[12]+' </td>\n')
    webfile.write('<td> Cluster Final Peak Frequency (Cluster Frequency Max - Most Significant Frequency) \n')
    webfile.write(' </td>\n')
    webfile.write('</tr>\n')

    
    webfile.write('<br><table border=1 cellspacing="1" cellpadding="5">\n')

    # Table for the Glitch fundamental parameters
    for i in range(8):
        if i == 0:
            webfile.write('<td></td>\n')

        webfile.write('<td> '+str(dim[i])+' </td>\n')
    webfile.write('</tr>\n')
    
    q = range(9)
    i = 1
    
    while i < 9:
        webfile.write('<td> '+str(dim[i])+' </td>\n')
        for j in range(q[i]):
            if i==j:
                webfile.write('<tr>\n')
                webfile.write('</tr>\n')
                continue
            webfile.write('<TD ALIGN="left"><A HREF="'+snr_dir+dim[j]+'vs'+dim[i]+'.png"><IMG SRC="'+snr_dir+dim[j]+'vs'+dim[i]+'.png" WIDTH=110 ALT="'+snr_dir+dim[j]+' vs '+dim[i]+'" TITLE="'+dim[j]+' vs '+dim[i]+'"></A></TD>')
        
            if j+1 == q[i]:
                webfile.write('<tr>\n')
                break
        i += 1


    for i in range(8):
        if i == 0:
            webfile.write('<td></td>\n')

        webfile.write('<td> '+str(dim[i])+' </td>\n')
    webfile.write('</tr>\n')

    webfile.write('</TR></TABLE>')
    
    # Table for the other glitch parameters
    webfile.write('<br><TABLE BORDER=1><TR>')
    webfile.write('<tr>\n')
    
    for i in range(9,13):
        if i == 9:
            webfile.write('<td></td>\n')

        webfile.write('<td> '+str(dim[i])+' </td>\n')
    webfile.write('</tr>\n')



    for i in range(9,13):
        webfile.write('<td> '+str(dim[i])+' </td>\n')
        for j in range(9,13):
            if i==j:
                webfile.write('<td>\n')
                continue
            else:
                webfile.write('<TD ALIGN="left"><A HREF="'+snr_dir+dim[i]+'vs'+dim[j]+'.png"><IMG SRC="'+snr_dir+dim[i]+'vs'+dim[j]+'.png" WIDTH=110 ALT="'+snr_dir+dim[j]+' vs '+dim[i]+'" TITLE="'+dim[j]+' vs '+dim[i]+'"></A></TD>')
            if j == 12:
                webfile.write('<tr>\n')


    webfile.write('<tr>\n')

    for i in range(9,13):
        if i == 9:
            webfile.write('<td></td>\n')

        webfile.write('<td> '+str(dim[i])+' </td>\n')
    webfile.write('</tr>\n')
    webfile.write('</TR></TABLE>')


    webfile.write('<h2><font face="Times" size="5">Clustered Data Plots</font></h2>\n')
    webfile.write('<br><table border=1 cellspacing="1" cellpadding="5">\n')
    webfile.write('<br><TABLE BORDER=1><TR>')
    

    
    for i in range(8):
        if i == 0:
            webfile.write('<td></td>\n')

        webfile.write('<td> '+str(dim[i])+' </td>\n')
    webfile.write('</tr>\n')

    q = range(9)
    i = 1

    while i < 9:
        webfile.write('<td> '+str(dim[i])+' </td>\n')
        for j in range(q[i]):
            if i==j:
                webfile.write('<tr>\n')
                webfile.write('</tr>\n')
                continue                
            webfile.write('<TD ALIGN="left"><A HREF="'+snr_dir+cluster_dir+dim[j]+'vs'+dim[i]+'clustered.png"><IMG SRC="'+snr_dir+cluster_dir+dim[j]+'vs'+dim[i]+'clustered.png" WIDTH=110 ALT="'+snr_dir+cluster_dir+dim[j]+' vs '+dim[i]+'" TITLE="'+dim[j]+' vs '+dim[i]+'"></A></TD>'\
)
    
            if j+1 == q[i]:
                webfile.write('<tr>\n')
                break
        i += 1

    for i in range(8):
        if i == 0:
            webfile.write('<td></td>\n')

        webfile.write('<td> '+str(dim[i])+' </td>\n')
    webfile.write('</tr>\n')

    webfile.write('</TR></TABLE>')

    webfile.write('<h2><font face="Times" size="5">k Histograms</font></h2>\n')
    webfile.write('<br><table border=1 cellspacing="1" cellpadding="5">\n')
    webfile.write('<br><TABLE BORDER=0><TR>')


    webfile.write('<br><table border=1 cellspacing="1" cellpadding="5">\n')
    
    webfile.write('<tr>\n')
    webfile.write('<td> Max k </td>\n')
    webfile.write('<td> ' + str(the_k) + ' \n')
    webfile.write(' </td>\n')
    webfile.write('</tr>\n')
    
    webfile.write('<tr>\n')
    webfile.write('<td> P-Value </td>\n')
    webfile.write('<td> ' + str(ks) + ' \n')
    webfile.write(' </td>\n')
    webfile.write('</tr>\n')

    webfile.write('<tr>\n')
    webfile.write('<td> Mean </td>\n')
    webfile.write('<td> ' + str(mean) + ' \n')
    webfile.write(' </td>\n')
    webfile.write('</tr>\n')

    webfile.write('<tr>\n')
    webfile.write('<td> Standard Deviation </td>\n')
    webfile.write('<td> ' + '%0.2f'%std + ' \n')
    webfile.write(' </td>\n')
    webfile.write('</tr>\n')
    webfile.write('</table><br>\n')
    
    webfile.write('<TD ALIGN="center"><A HREF="'+snr_dir+'k_cluster_histogram.png"><IMG SRC="'+snr_dir+'k_cluster_histogram.png" WIDTH=200 ALT="'+snr_dir+'k_cluster_histogram.png" TITLE="Histogram"></A></TD>')
    
    webfile.write('<TD ALIGN="center"><A HREF="'+snr_dir+'elementsPerCluster.png"><IMG SRC="'+snr_dir+'elementsPerCluster.png" WIDTH=200 ALT="'+snr_dir+'elementsPerCluster.png" TITLE="Elements per cluster Histogram"></A></TD>')
#indx = [0,1,2,4,5,6,7]
    #for u in indx:
    #    webfile.write('<TD ALIGN="center"><A HREF="'+snr_dir+'/'+dim[u]+'hist.png"><IMG SRC="'+snr_dir+'/'+dim[u]+'hist.png" WIDTH=150 ALT="'+snr_dir+'/'+dim[u]+'hist.png" TITLE="Histogram"></TD>')


    
    webfile.write('<tr>\n')
    webfile.write('<h2><font face="Times" size="5">Individual Cluster Plots</font></h2>\n')
    webfile.write('<br><table border=1 cellspacing="1" cellpadding="5">\n')
    webfile.write('<br><TABLE BORDER=1><TR>')
    new_line = 0
   # for i in range(the_k):
   #     if new_line == 6:
   #         webfile.write('<tr>\n')
   #         new_line = 0
   #     webfile.write('<TD ALIGN="left"><A HREF="'+snr_dir+'/clustered/MSFreqSNR'+str(i)+'_clustered.png"><IMG SRC="'+snr_dir+'/clustered/MSFreqSNR'+str(i)+'_clustered.png" WIDTH=110 ALT="'+snr_dir+'/clustered/MSFreqSNR'+str(i)+'_clustered.png" TITLE="MSFreqSNR"></A></TD>')
   #     new_line += 1




    webfile.write('\n')
    webfile.write('\n')
    webfile.write('\n')
    webfile.write('\n')
    webfile.write('\n')
    webfile.write('\n')
    webfile.write('\n')
    webfile.write('\n')
    webfile.write('\n')
    webfile.write('\n')
    webfile.write('\n')

    webfile.close()

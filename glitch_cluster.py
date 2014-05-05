from numpy import *
import matplotlib
from glitchparse import *
from gSplit import *
from pylab import *
from webgen import *
import commands, sys, time, os
from optparse import OptionParser
from gMeans import *
import time

########################                                                                                                                                      
########################                                                                                                                                      
# Requires the following .py files to work: glitchparse.py, getGlitchFiles.py, ks_means.py, ksplit.py                                                         
# glitchparse.py and getGlitchFiles.py find the glitch files and parse them into a more accessible format                                                     
# ks_means.py and ksplit.py take the data from the glitch files and clusters them using the KSmeans splitting                                                 
# method for finding sets of clusters within data.                                                                                                          
########################                                                                                                                                     
########################                                                                                                                                      
             
t0 = time.clock()

srvName = "jkerriga"
gps_start = '964742415'
gps_end = '964828815'
snr_low = 8
snr_high = 100
freq_low = 50
freq_high = 10000
runs = 1000

glitches,sci_time,g_found,cent_time = glitchparse(gps_start,gps_end,snr_low,snr_high,freq_low,freq_high)
print shape(glitches)

MS_freq = glitches[:,0]
MS_snr = glitches[:,1]
MS_band = glitches[:,2]
MS_Q = glitches[:,3]
dura = glitches[:,4]
band = glitches[:,5]
nev = glitches[:,6]
freq_av = glitches[:,7]
peak_freq = glitches[:,8]
peak_start = glitches[:,9]
peak_end = glitches[:,10]
freq_begin = glitches[:,11]
freq_end = glitches[:,12]

dim = ['MS_Frequency','MS_SNR','MS_Bandwidth','MS_Q','Duration','Bandwidth','Cluster_nEvents','Cluster_Frequency_Average','Cluster_Peak_Frequency_Average','Initial_Peak_T\
ime','Final_Peak_Time','Initial_Cluster_Frequency','Final_Cluster_Frequency']
j = 0
q = 0

cmd1 = 'tconvert '+str(gps_start)
cmd2 = 'tconvert '+str(gps_end)
nts = commands.getoutput(cmd1)
nte = commands.getoutput(cmd2)
nts = nts[:3]+nts[4:6]+nts[7:11]
nte = nte[:3]+nte[4:6]+nte[7:11]

new_path = '/home/'+srvName+'/public_html/'+str(nts)+'-'+str(nte)
snr_path = '/home/'+srvName+'/public_html/'+str(nts)+'-'+str(nte)+'/SNR'+str(snr_low)+'-'+str(snr_high)+'Freq'+str(freq_low)+'-'+str(freq_high)
cluster_path = snr_path+'/clustered/'
web_path = '/~'+srvName+'/' + str(nts)+'-'+str(nte)+'/SNR_'+str(snr_low)+'-'+str(snr_high)+'Freq'+str(freq_low)+'-'+str(freq_high) + '.html'

if os.path.exists(snr_path) == True:
    print 'Path exists.'
else:
    os.system('mkdir ' + str(new_path))
    os.system('mkdir ' + str(snr_path))
    os.system('mkdir ' + str(cluster_path))
    print 'Directory created.'

for i in range(len(dim)):
    for j in range(len(dim)):
        if i == j:
            continue
        else:
            figure()
            scatter((glitches[:,i]),(glitches[:,j]),s=2)
            xlabel(dim[i])
            ylabel(dim[j])
            title(dim[i]+' vs. '+dim[j])
            xlim(min(glitches[:,i]),max(glitches[:,i]))
            ylim(min(glitches[:,j]),max(glitches[:,j]))
            savefig(snr_path + '/' + dim[i]+'vs'+dim[j]+'.png')
            close()

print 'Working..'
labels,max_k,centroids = gMeans(glitches,runs,snr_path)
#savetxt(str(ks_crit)+'_saved_labels.txt',saved_labels)                                                                                                       
# Use the webgen.py python script to generate an .html file for displaying the plots                                                                          
# and various other statistics from ksmeans.                                                                                                                  
            
ks = 0
num_k = max_k
webgen(ks,gps_start,gps_end,mean(num_k),std(num_k),dim,snr_low,snr_high,freq_low,freq_high,sci_time,g_found,new_path,max_k,srvName)

colors = rand(max_k+1,3)

# Plots the clustered parameters against each other for display on the .html page.                                                                            
             
print 'Plotting clusters...'
q = 0
j = 0
below = 0
greater_20_elem = []
elemCount = []
for i in range(max(labels)+1):
    if len(labels[labels == i]) < 20:
        below += 1
        elemCount.append(len(labels[labels == i]))
    else:
        greater_20_elem.append(i)
        elemCount.append(len(labels[labels == i]))
        continue
figure()
hist(elemCount)
xlabel('# of Elements in a cluster')
ylabel('Occurences')
savefig(snr_path + '/' + 'elementsPerCluster.png')
close()


print "post k found: " ,(max_k)

print shape(centroids),"Shape of centroids"
for l in range(len(dim)):
    for j in range(len(dim)):
        if l == j:
            continue
        else:
            figure()
            for u in greater_20_elem:
                if len(glitches[labels == u,j]) < 0:
                    continue
                else:
                    scatter((glitches[labels == u,l]),(glitches[labels == u,j]),s=10,c=colors[u],linewidths=0)
                    #scatter(centroids[labels == u,l],centroids[labels == u,j],s=15,c=[0,0,0],marker = 's')
            title(dim[l]+' vs. '+dim[j])
            xlabel(dim[l])
            ylabel(dim[j])
            xlim(min(glitches[:,l]),max(glitches[:,l]))
            ylim(min(glitches[:,j]),max(glitches[:,j]))
            #legend(loc=2,prop={'size':7})                                                                                                                                 
            savefig(cluster_path + dim[l]+'vs'+dim[j]+'clustered.png')
            close()
    q += 1


process = time.clock() - t0
print 'Process time: %0.2f secs'%process





print "Cluster Plot Locations: https://ldas-jobs.ligo-wa.caltech.edu"+web_path

from numpy import *
import matplotlib
from glitchparse import *
from gMeans import *
from pylab import *
from webgen import *
import commands, sys, time, os
from optparse import OptionParser
from clusterCompare import *
#from generate_test import generate_test


########################
########################
# Requires the following .py files to work: glitchparse.py, getGlitchFiles.py, ks_means.py, ksplit.py
# glitchparse.py and getGlitchFiles.py find the glitch files and parse them into a more accessible format
# ks_means.py and ksplit.py take the data from the glitch files and clusters them using the KSmeans splitting
# method for finding sets of clusters within data.
########################
######################## 

num_k = []
gps_start = '0000'
gps_end = '0000'
snr_low = 20
snr_high = 1000
freq_low = 50
freq_high = 10000
ks_crit = 0.05
runs = 1000

## This generates the glitch list with the snr and freq boundaries supplied above from a 
## set list of ~2 min segments that enclose a glitch injection
#generate_test(snr_low,snr_high,freq_low,freq_high)

sci_time = 3000
glitch_labels = []

## Loads the glitch parameters from the generated text file
glitches = loadtxt('test_list.txt',delimiter=' ')
g_found,param = shape(glitches)
obs = array(glitches)
#sci_time = 0000
#g_found = 0000
print shape(glitches)
glitch_shape = shape(glitches)


##Jitter##
#or l in range(glitch_shape[1]):
#012678
#l = 6
#    glitches[:,l] = glitches[:,l] + randn(glitch_shape[0])*0.005*max(glitches[:,l])

new_path = '/home/jkerriga/public_html/test'
snr_path = '/home/jkerriga/public_html/test/SNR'+str(snr_low)+'-'+str(snr_high)+'Freq'+str(freq_low)+'-'+str(freq_high)
cluster_path = snr_path+'/clustered/'

if os.path.exists(snr_path) == True:
    print 'Path exists.'
else:
    os.system('mkdir ' + str(new_path))
    os.system('mkdir ' + str(snr_path))
    os.system('mkdir ' + str(cluster_path))
    print 'Directory created.'

## Assign names to parameters
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

## Assign more detailed names to parameters, this should have the same index as above
dim = ['MS_Frequency','MS_SNR','MS_Bandwidth','MS_Q','Duration','Bandwidth','Cluster_nEvents','Cluster_Frequency_Average','Cluster_Peak_Frequency_Average','Initial_Peak_Time','Final_Peak_Time','Initial_Cluster_Frequency','Final_Cluster_Frequency']

figure()
plot(range(len(freq_av)),freq_av,'.')
xlabel('Time(s)')
ylabel('Freq')
savefig(new_path+'/freqintime.png')
close()

## Plots the glitch parameters against each other
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
            xlim(min(glitches[:,i]) - 0.1*max(glitches[:,i]),max(glitches[:,i]) + 0.1*max(glitches[:,i]))
            ylim(min(glitches[:,j]) - 0.1*max(glitches[:,j]),max(glitches[:,j]) + 0.1*max(glitches[:,j]))
            savefig(snr_path + '/' + dim[i]+'vs'+dim[j]+'.png')
            close()



## Runs ksmeans for n runs, this while loop will continue to for a run
## until all clusters found have more than 2 members, this is to
## prevent ksmeans from diverging to it assigning every glitch its
## own cluster. i.e. N clusters for N glitches
labels,ks,centroids = gMeans(glitches,runs)
num_k = ks
max_k = ks
colors = rand(max_k,3)
## Generates the .html page for viewing the glitch parameter and cluster plots
webgen(ks,gps_start,gps_end,mean(num_k),std(num_k),dim,snr_low,snr_high,freq_low,freq_high,sci_time,g_found,new_path,max_k)

print 'Plotting clusters...'

## Plots the clustered glitch parameters
q = 0
j = 0

for l in range(len(dim)):
    j = q
    for j in range(len(dim)):
        if l == j:
            continue
        else:
            figure()
            text_lab = 0
            for u in range(int(max_k)+1):
                if len(glitches[labels == u,j]) == 0:
                    continue
                elif len(glitches[labels == u,j]) < 12:
                    continue
                else:
                    text(centroids[u,l],centroids[u,j] + 0.1*max(centroids[u,j]),str(text_lab),fontsize=9)
                    scatter(obs[labels == u,l],obs[labels == u,j],s=6,c=colors[u],linewidths=0)
                    text_lab += 1
                    #scatter(centroids[u,l],centroids[u,j],s=15,c='k',marker = 's')
            title(dim[l]+' vs. '+dim[j])
            xlabel(dim[l])
            ylabel(dim[j])
            xlim(min(glitches[:,l]) - 0.1*max(glitches[:,l]),max(glitches[:,l]) + 0.1*max(glitches[:,l]))
            ylim(min(glitches[:,j]) - 0.1*max(glitches[:,j]),max(glitches[:,j]) + 0.1*max(glitches[:,j]))
            savefig(snr_path + '/clustered/' + dim[l]+'vs'+dim[j]+'clustered.png')
            close()
            

act_labels = loadtxt('/home/jkerriga/Clustering/Actual_labels.txt')
acc,clst_track = clusterCompare(obs,act_labels,labels)
print acc,clst_track

#for u in range(int(max_k)):
#    figure()
#    scatter((glitches[labels == u,0]),(glitches[labels == u,1]),s=10,c=colors[u],linewidths=0)
#    title('MS Freq vs. SNR')
#    xlabel('MS Freq')
#    ylabel('SNR')
#    savefig(snr_path + '/clustered/MSFreqSNR'+str(u)+'_clustered.png')
#    close()



#indx = [0,1,2,4,5,6,7]

#for h in indx:
#    figure()
#    hist(glitches[:,h],bins=30)
#    xlabel(str(dim[h]))
#    ylabel('# of occurences')
#    savefig(snr_path+'/'+dim[h]+'hist.png')
#    close()



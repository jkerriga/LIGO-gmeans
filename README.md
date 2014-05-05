LIGO-gmeans
===========

Frequentist g-means intended to work on LIGO data
To upload the LIGO-gmeans package for use on LIGO data you can reference the
globus-url-copy method here - https://wiki.ligo.org/LDG/GridToolsIntroduction

Descriptions for each .py file:
glitch_cluster.py - Calls the gMeans.py script and plots all output
gMeans.py - Drives the clustering process, this script is what runs the frequentist portion of gmeans
gSplit.py - Does the bifurcating of the observation space to cluster
gaussianClusterTest.py - Performs the Anderson-Darling test for gaussianity on a bifurcated cluster
kThreshold.py - Uses a set threshold number for neglecting clusters with less than a specified # of glitches
webgen.py - Builds a webpage for viewing output plots of glitches (needs a public_html directory in home directory)

clusterCompare.py - Compares % of correctly clustered observations (requires a dataset with known clusters)

getGlitchFiles.py - Retrieves the specified glitch files by GPS date-time (https://ldas-jobs.ligo-wa.caltech.edu/~detchar/S6/glitch/report/OmegaOnline.html)
glitchparse.py - Parses the retrieved glitches for use in the gmeans algorithm



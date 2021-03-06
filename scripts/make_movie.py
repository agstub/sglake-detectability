# This program creates a group of png images of the upper and lower surfaces
# over time. After running this, change to the 'pngs' directory and run the
# following bash script, where frames_per_sec is an integer (e.g., 50):
#
# ffmpeg -r frames_per_sec -f image2 -s 1920x1080 -i %01d.png -vcodec libx264 -pix_fmt yuv420p -vf scale=1280:-2 movie.mp4
#
# (This requires ffmpeg: https://ffmpeg.org/)

import sys
sys.path.insert(0, './source')

import matplotlib.pyplot as plt
import numpy as np
from geometry import interface, bed
from params import tol,t_final,Lngth,Hght,t_period,C
import subprocess
from scipy.misc import derivative
from scipy.interpolate import interp1d
import matplotlib as mpl

mpl.rcParams['xtick.major.size'] = 4
mpl.rcParams['xtick.major.width'] = 1
mpl.rcParams['xtick.minor.size'] = 4
mpl.rcParams['xtick.minor.width'] = 1
mpl.rcParams['ytick.major.size'] = 4
mpl.rcParams['ytick.major.width'] = 1
mpl.rcParams['ytick.minor.size'] = 4
mpl.rcParams['ytick.minor.width'] = 1

# Create directory for png's
bashCommand1 = "sudo mkdir pngs"
process1 = subprocess.Popen(bashCommand1.split(), stdout=subprocess.PIPE)
output, error = process1.communicate()

# Load relevant files
resultsname = 'results_t'+format(t_period/3.154e7,'.1f')+'_H'+format(Hght/1000.0,'.1f')+'_C'+str(int(np.floor(np.log10(C))))

Gamma_s = np.loadtxt(resultsname+'/Gamma_s')             # Lower surface
Gamma_h = np.loadtxt(resultsname+'/Gamma_h')             # Upper surface
x_left = np.loadtxt(resultsname+'/x_left')               # Left grounding line
x_right = np.loadtxt(resultsname+'/x_right')             # Right grounding line


# Create array for plotting
NX = np.shape(Gamma_s)[0]                                 # (Uniform) Grid spacing
NT = np.shape(Gamma_s)[1]                                 # Number of time steps
X = np.loadtxt(resultsname+'/X')                          # x-coordinate array
t = np.loadtxt(resultsname+'/t')
V = np.loadtxt(resultsname+'/lake_vol')


# Loop over time steps
for i in range(NT):

    plt.figure(figsize=(8,3))


    plt.title(r'$t=$'+format(t[i]/3.154e7,'.2f')+' yr',loc='left',fontsize=20)

    # Plot upper surface
    plt.plot(X/1000-0.5*Lngth/1000,Gamma_h[:,i]-0.99*Hght,color='royalblue',linewidth=1,label=r'$h$')

    # Plot ice, water, and bed domains; colored accordingly.
    p1 = plt.fill_between(X/1000-0.5*Lngth/1000,y1=Gamma_s[:,i], y2=Gamma_h[:,i]-0.99*Hght,facecolor='aliceblue',alpha=1.0)
    p2 = plt.fill_between(X/1000-0.5*Lngth/1000,bed(X),Gamma_s[:,i],facecolor='slateblue',alpha=0.5)
    p3 = plt.fill_between(X/1000-0.5*Lngth/1000,-18*np.ones(np.size(X)),bed(X),facecolor='burlywood',alpha=1.0)


    # Plot bed surface
    plt.plot(X/1000-0.5*Lngth/1000,bed(X),color='k',linewidth=1,label=r'$\beta$')

    plt.plot(X[(Gamma_s[:,i]-bed(X)>tol)]/1000-0.5*Lngth/1000,Gamma_s[:,i][(Gamma_s[:,i]-bed(X)>tol)],'o',color='crimson',markersize=1,label=r'$s>\beta$')


    # Plot grounding lines
    plt.plot(np.array([x_left[i]/1000-0.5*Lngth/1000]),np.array([np.min(bed(X))-0.5]),marker=r'^',color='crimson',linestyle='None',markersize=12)

    plt.plot(np.array([x_right[i]/1000-0.5*Lngth/1000]),np.array([np.min(bed(X))-0.5]),marker=r'^',markersize=12,color='crimson')



    # Label axes and save png:
    plt.xlabel(r'$x$ (km)',fontsize=20)
    plt.ylabel(r'$z$ (m)',fontsize=20)
    plt.yticks([-2,0,2,8,10,12],['-2','0','2',r'$h_0-2$',r'$h_0$',r'$h_0+2$'],fontsize=16)
    plt.xticks(fontsize=16)
    plt.xlim(-0.5*Lngth/1000,0.5*Lngth/1000)
    plt.ylim(-5,16)


    plt.savefig('pngs/'+str(i),bbox_inches='tight')
    plt.close()

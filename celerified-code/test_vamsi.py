from celery import Celery
app = Celery('test_vamsi', backend='mongodb://localhost/turkeycalltest', broker='mongodb://localhost/turkeycalltest')

'''
Test for Vamsi web interface
'''

import numpy as np
import pylab as pl
import scipy
import sys
import os
import pyfits

############################################################################################################################################################################################################
############################################################################################################################################################################################################
## few constants

fullsky_arcmin2 = 4*np.pi*(180.0*60/np.pi)**2
arcmin_to_radian = np.pi/(180.0*60.0)
pix_size_2048_arcmin = np.sqrt( 4.0*np.pi*(180*60/np.pi)**2 / (12*2048**2) )
pix_size_1024_arcmin = np.sqrt( 4.0*np.pi*(180*60/np.pi)**2 / (12*1024**2) ) 
seconds_per_year = 365.25*24*3600
############################################################################################################################################################################################################
############################################################################################################################################################################################################


##############
## SETUP COSMOLOGY
## e.g. 
params_fid = {}
params_fid['h'] = 70.0
params_fid['ombh2'] = 0.0226
params_fid['omch2'] = 0.114
params_fid['omnuh2'] = 0.001069 #100.0/93000
params_fid['omk'] = 0.001
params_fid['YHe'] = 0.24
params_fid['Neff'] = 3.04
params_fid['w'] = -1.0
params_fid['wa'] = 0.0
params_fid['tau'] = 0.09
params_fid['As'] = 2.46e-9
params_fid['ns'] = 0.96
params_fid['alphas'] = 0.0
params_fid['r'] = 0.1
params_fid['nT'] = - params_fid['r']/8
params_fid['A'] = 0.1 ## residuals amplitude @ ell= 1
params_fid['b'] = -0.8 ## ell dependence of the residuals
params_fid['k_scalar'] = 0.005
params_fid['k_tensor'] = 0.005

############################################################################################################################################################################################################
############################################################################################################################################################################################################

##############
## SETUP EXPERIMENTAL CONFIGURATIONS
## e.g. 
configurations = {}
configurations['COrE+'] = {}
configurations['COrE+']['freqs'] = [30.0, 60.0, 90.0, 150.0, 180.0, 220.0, 280.0, 320.0]
configurations['COrE+']['uKCMBarcmin'] = 10.0*np.ones(len(configurations['COrE+']['freqs'] ))
configurations['COrE+']['FWHM'] = 5.0*np.ones(len(configurations['COrE+']['freqs'] ))
configurations['COrE+']['fsky'] = 0.8
configurations['COrE+']['ell_min'] = 2
configurations['COrE+']['ell_max'] = 3000

configurations['LiteBIRD'] = {}
configurations['LiteBIRD']['freqs'] = [60.0, 78.0, 100.0, 140.0, 195.0, 280.0]
configurations['LiteBIRD']['uKCMBarcmin'] = [ 10.3, 6.5, 4.7, 3.7, 3.1, 3.8 ]
configurations['LiteBIRD']['FWHM'] = [75.0, 58.0, 45.0, 32.0, 24.0, 16.0]
configurations['LiteBIRD']['fsky'] = 0.7
configurations['LiteBIRD']['ell_min'] = 2
configurations['LiteBIRD']['ell_max'] = 500

configurations['Stage4'] = {}
configurations['Stage4']['freqs'] = [40.0, 90.0, 150.0, 220.0, 280.0]
configurations['Stage4']['uKCMBarcmin'] = [ 3.0, 1.5, 1.5, 5.0, 9.0 ]
configurations['Stage4']['FWHM'] = [ 11.0, 5.0, 3.0, 2.0, 1.5 ]
configurations['Stage4']['fsky'] = 0.5
configurations['Stage4']['ell_min'] = 10
configurations['Stage4']['ell_max'] = 3500

experiments = configurations.keys()

def BB_factor_computation(nu):
	cst = 56.8
	BB_factor = (nu/cst)**2*np.exp(nu/cst)/(np.exp(nu/cst)-1)**2
	return BB_factor

def Cl_res_computation( Nbolos, uKRJ_per_pix, freqs, spsp, Cl_dust, Cl_sync, Cl_dxs ):
	dB = np.sum(spsp)
	return dB

@app.task
def test(fsky, freqs, uKCMBarcmin, ell_max):

	## compute minimum multipole for each experiment
	ell_min = int( np.ceil(2.0 * np.sqrt(np.pi / fsky )))

	## computing uKRJ/pix for each experiment
	nfreqs = len( freqs )
	uKRJ_perpix = np.zeros(nfreqs)
	for f in range( nfreqs ):
		uKCMB_perpixel_f = uKCMBarcmin[f] * arcmin_to_radian#/ pix_size_2048_arcmin
		uKRJ_perpixel_f = uKCMB_perpixel_f*BB_factor_computation(  freqs[f] )
		uKRJ_perpix[f] = uKRJ_perpixel_f

	############################################################################################################################################################################################################
	############################################################################################################################################################################################################
	## Foregrounds 

	spsp = np.ones( (6,6) )

	########################################################################
	# load angular power spectra  #### will update with Planck power spectra @ 150GHz ! 
	ell = np.arange(ell_min, ell_max)
	Cl_dust = np.ones(ell.shape)
	Cl_sync = np.ones(ell.shape)
	Cl_dxs = np.ones(ell.shape)

	########################################################################
	########################################################################

	# assumed that nside=8 pixels over the sky have independent spectral parameters that have to be estimated
	npatch = int( fsky*12*8**2 )

	# compute noise, delta_beta and Clres from noise per channel in RJ
	ells=np.array(range(ell_min, ell_max+1))
	delta_betas = Cl_res_computation( np.ones(len( freqs )), uKRJ_perpix, freqs, spsp, Cl_dust, Cl_sync, Cl_dxs ) 

	############################################################################################################################################################################################################

	return delta_betas

if __name__ == "__main__":

	dB = test( 0.1, [1.0, 10.0, 100.0], [1.0, 10.0, 100.0], 3000)
	print '------------'
	print 'dB is ', dB
	print '------------'



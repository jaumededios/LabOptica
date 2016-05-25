import seaborn as sns #Some data analysis and nice plots [not necessary]
import matplotlib.pyplot as plt #Crucial to make the plots
import pandas as pd #Data import
import numpy as np #Deal with arrays of numbers
import uncertainties as uc #Propagate uncertainties
import uncertainties.unumpy as unp #Arrays with uncertainties
import scipy as scp #Science stuff! (regressions & so on)
import math #math basics (not really necesssary w/ numpy)

sns.set_context("notebook") #just some config for the plots
sns.set_style("ticks")

#Seamless integration of matplotlib with uncertainties
#It gets uncertainty arrays and uses them to make a scatter plot with errors
def _plt_error_scatter(x,y,target=None,*args, **kwargs):
    if target==None:
        target=plt
    presets={'marker':'o', 'ms':4, 'lw':2, 'mew':1, 'mfc':"white"}
    kwargs["xerr"]=unp.std_devs(x)
    kwargs["yerr"]=unp.std_devs(y)
    for key in presets:
        if not key in kwargs:
            kwargs[key]=presets[key]
    kwargs["linestyle"]="none"
    target.errorbar(unp.nominal_values(x),
                  unp.nominal_values(y),
                  *args,
                  **kwargs);

#Integration of the scipy curve fit with the uncertainties package
def _scp_error_curve_fit(f,x,y,*args, **kwargs):
    if not 'sigma' in kwargs:
        kwargs['sigma']=unp.std_devs(y)
    if not 'absolute_sigma' in kwargs:
        kwargs['absolute_sigma']=True
    result=scp.optimize.curve_fit(
                f,
                unp.nominal_values(x), 
                unp.nominal_values(y),
                *args, 
                **kwargs)
    return uc.correlated_values(*result)


#This is for the filled plots for continuous variables with errors
def _plt_error_regression(f,x,parameters=[], nsigma=1, linestyle={}, fillstyle={}, target=None):
    if target==None:
        target=plt;
    y=f(x,*parameters)
    ytop=unp.nominal_values(y)+nsigma*unp.std_devs(y)
    ybot=unp.nominal_values(y)-nsigma*unp.std_devs(y)
    y=unp.nominal_values(y)

    plt.plot(x,y,**linestyle)
    plt.fill_between(x,ybot,ytop,**fillstyle)

unp.n = unp.nominal_values
unp.s = unp.std_devs
scp.optimize.error_curve_fit=_scp_error_curve_fit
plt.errorScatter=_plt_error_scatter
plt.errorRegression=_plt_error_regression
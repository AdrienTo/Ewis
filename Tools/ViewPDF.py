import openturns as ot
from openturns.viewer import View

import numpy as np
from math import sqrt, sin, pi



def viewPDF (marginal, title=None, xTitle=None, yTitle=None, legend=None, outputFile=None ):
    PDF = marginal.drawPDF()
    if (title      != None): PDF.setTitle(title)
    if (xTitle     != None): PDF.setXTitle(xTitle)
    if (yTitle     != None): PDF.setYTitle(yTitle)
    if (legend     != None): PDF.setLegends(legend)
    if (outputFile != None): 
        View(PDF).save(outputFile)
    else :
        View (PDF)

def viewCDF (marginal, title=None, xTitle=None, yTitle= None, legend=None, outputFile=None):
    
    CDF = marginal.drawCDF()
    if (title      != None): CDF.setTitle(title)
    if (xTitle     != None): CDF.setXTitle(xTitle)
    if (yTitle     != None): CDF.setYTitle(yTitle)
    if (legend     != None): CDF.setLegends(legend)
    if (outputFile != None): 
        View(CDF).save(outputFile)
    else :
        View (CDF)  
    
        
def viewHisto (sample, name=None, title=None, xTitle=None, xmin=0, xmax=0, outputFile=None):
    
    histo=ot.VisualTest.DrawHistogram(sample)
    histo.setName(name)
    histo.setTitle(title)
    histo.setXTitle(xTitle)
    histo.setLegends('1')
    histo.setLegendPosition('topleft')
    histo.setLegendFontSize(6)
    BoundingBox = histo.getBoundingBox()
    histo.setBoundingBox([xmin, xmax, BoundingBox[2], BoundingBox[3]])
    View(histo).save(outputFile)

    
def viewEmpiricalCDF (sample, name=None, title=None, xTitle=None, yTitle= None,  xmin=0, xmax=0, outputFile=None):
    
    cdf=ot.VisualTest.DrawEmpiricalCDF(sample, xmin, xmax)
    cdf.setName(name)
    cdf.setTitle(title)
    cdf.setXTitle(xTitle)
    cdf.setYTitle(yTitle)
    cdf.setLegends('1')
    cdf.setLegendPosition('topleft')
    cdf.setLegendFontSize(6)
    View(cdf).save(outputFile)



def viewResults (sample, type, vmin, vmax, workdir):
    
    #Visualisation
    viewHisto        (sample, "Histogram "+ type, "Histogram "+ type, type, vmin, vmax, workdir+'/'+type+'Histogram.png')
    viewEmpiricalCDF (sample, "CDF "+ type, "CDF "+ type, type,"CDF", vmin, vmax,  workdir+'/'+type+'CDF.png')

    #Results

    #- Print results -#
    print "-------------------------------------------------------------------------------"
    print type + " \n"
    print "* ------ Deterministic analysis ------*"
    print " Min = % .2f" %sample.getMin()[0], "Max = % .2f" %sample.getMax()[0], "Delta = % .2f" %(sample.getMax()[0] - sample.getMin()[0])
    print "\n"
    print "* ------ Probabilistic analysis ------*"
    print " Quantile @ 50 = % .2f " %sample.computeQuantile(0.5) [0]
    print " Quantile @ 90 = % .2f " %sample.computeQuantile(0.90)[0]
    print " Quantile @ 99 = % .2f " %sample.computeQuantile(0.99)[0]
    print " Variance  = % .2f " %np.array(sample.computeCovariance())[0][0]
    print " Interquantile  (q(99,7) - q(0,3)) = % .2f " %(sample.computeQuantile(0.997)[0] - sample.computeQuantile(0.003)[0])
    print " 6-sigma = % .2f" %(sqrt(np.array(sample.computeCovariance())[0][0])*6)
    print "-------------------------------------------------------------------------------"

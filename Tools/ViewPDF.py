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

    
def viewCDF (sample, name=None, title=None, xTitle=None, yTitle= None,  xmin=0, xmax=0, outputFile=None):
    
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
    viewHisto (sample, "Histogram "+ type, "Histogram "+ type, type, vmin, vmax, workdir+'/'+type+'Histogram.png')
    viewCDF   (sample, "CDF "+ type, "CDF "+ type, type,"CDF", vmin, vmax,  workdir+'/'+type+'CDF.png')

    #Results

    #- Print results -#
    print "-------------------------------------------------------------------------------"
    print type + " \n"
    print "* ------ Deterministic analysis ------*"
    print type + " Min =", (sample.getMin())[0], "Max = ", sample.getMax()[0], "Delta = ", sample.getMax()[0] - sample.getMin()[0]
    print "\n"
    print "* ------ Probabilistic analysis ------*"
    print type + " Quantile @ 5% = ", sample.computeQuantile(0.05)[0], "Quantile @ 50% = ", sample.computeQuantile(0.5) [0],"Quantile @ 95% = ", sample.computeQuantile(0.95)[0]
    print type+": Variance =", np.array(sample.computeCovariance())[0][0], "6-sigma = ", 6*sqrt(np.array(sample.computeCovariance())[0][0])
    print type+": Interquantile (q(99,7%) - q(0,3%)) = ", (sample.computeQuantile(0.997)[0] - sample.computeQuantile(0.003)[0])
    print "-------------------------------------------------------------------------------"

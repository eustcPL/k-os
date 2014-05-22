# -*- coding: utf-8 -*-
# Author: xiao.wang@polytechnique.edu
# Date:   22 May, 2014
from lossFunction import * 
from pickingPositiveItem import *
from numericalInterest import *
import numpy

def k_os_AUC_loss():
    """
    1. initialise the model
    """
    X = preprocessData().getX()
    m = 2  # learning dimension 
    n = 4  # number of items 
    V = model(m,n).getV()
    
    """
    2. repeat
    until the error does not improve
    """
    epsilon  = 0.001
    lossFunc = lossFunction()
    nInterest = numericalInterest()
    
    previousLoss = lossFunc.AUCLoss(X,V)
    currentLoss = -1
    countIteration = 0
    while True:
        countIteration+=1
        if currentLoss != -1:
            previousLoss = currentLoss
            
        (u, d) = pickingPositiveItem(X,V)
        
        """
        pick a bar_d at random from D\Du
        """
        bar_Du = lossFunc.getBarDu(X, u)
        bar_d = numpy.random.choice(bar_Du)
        
        f_d_u = nInterest.f_d(d,u,X,V)
        f_bar_d_u = nInterest.f_d(bar_d, u, X, V)
        
        if (f_bar_d_u > f_d_u -1):
            """
            make a gradient step
            """
            alpha = 0.1
            V = lossFunc.SGD(X, V,u, d, bar_d, alpha)
            """
            Project weights to enforce constraints:
            ensure ||Vi|| <= C
            """
            C = 2
            V = lossFunc.constraintNorm(V, C)
        currentLoss = lossFunc.AUCLoss(X,V)

        if (numpy.abs(currentLoss - previousLoss)<epsilon):
            print "finish learning", countIteration
            print "total loss:", currentLoss
            break
        
    return (X, V)
#k_os_AUC_loss()
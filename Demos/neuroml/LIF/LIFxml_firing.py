# -*- coding: utf-8 -*-
## all SI units
########################################################################################
## Plot the membrane potential for a leaky integrate and fire neuron with current injection
## Author: Aditya Gilra
## Creation Date: 2012-06-08
## Modification Date: 2012-06-08
########################################################################################

import os
os.environ['NUMPTHREADS'] = '1'
import sys
sys.path.append('../../../python')

## simulation parameters
SIMDT = 5e-5 # seconds
PLOTDT = 5e-5 # seconds
RUNTIME = 2.0 # seconds
injectI = 1e-8#2.5e-12 # Amperes

## moose imports
import moose
from moose.neuroml import *
from moose.utils import * # has setupTable(), resetSim() etc
import math

## import numpy and matplotlib in matlab style commands
from pylab import *

def create_LIF():
    neuromlR = NeuroML()
    neuromlR.readNeuroMLFromFile('cells_channels/LIF.morph.xml')
    libcell = moose.Neuron('/library/LIF')
    LIFCellid = moose.copy(libcell,moose.Neutral('/cells'),'IF1')
    LIFCell = moose.Neuron(LIFCellid)
    return LIFCell

def run_LIF():
	## reset and run the simulation
	print "Reinit MOOSE."
	## from moose_utils.py sets clocks and resets
	resetSim(['/cells[0]'], SIMDT, PLOTDT, simmethod='ee')
	print "Running now..."
	moose.start(RUNTIME)

if __name__ == '__main__':
    IF1 = create_LIF()
    printCellTree(IF1)
    IF1Soma = moose.Compartment(IF1.path+'/soma_0')
    IF1Soma.inject = injectI
    IF1vmTable = setupTable("vmTableIF1",IF1Soma,'Vm')

    ## edge-detect the spikes using spike-gen (table does not have edge detect)
    ## IaF_spikegen is already present for compartments having IaF mechanisms
    spikeGen = moose.SpikeGen(IF1Soma.path+'/IaF_spikegen')
    table_path = moose.Neutral(IF1Soma.path+'/data').path
    IF1spikesTable = moose.Table(table_path+'/spikesTable')
    moose.connect(spikeGen,'spikeOut',IF1spikesTable,'input') ## spikeGen gives spiketimes

    run_LIF()
    print "Spiketimes :",IF1spikesTable.vector
    ## plot the membrane potential of the neuron
    timevec = arange(0.0,RUNTIME+PLOTDT/2.0,PLOTDT)
    ## Something is crazy! Why twice the number of table entries compared to time!!??
    figure(facecolor='w')
    print IF1vmTable
    plot(timevec, IF1vmTable.vector)
    show()

    ## At the end, some issue with Func (as per Subha) gives below or core dump error
    ## *** glibc detected *** python: corrupted double-linked list: 0x00000000038f9aa0 ***

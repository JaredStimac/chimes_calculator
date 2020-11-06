"""

	A simple usage example for computing system force, stress, and energy via 
	the serial_chimes_calculator python wrapper.

	Expects "libwrapper-C.so" in the same directory as this script. This file
	can be generated by typing "make all" in the directory containing this file
	
	Depends on wrapper_py.py from the chimes_serial_interface's api files

	Expects to be run with python version 3.X

	Run with: "python3 <this file> <parameter file> <coordinate file> <nlayers>

	Code Author: Rebecca K. Lindsey (2020)

"""

import os
import sys
import math

# Import ChIMES modules

chimes_module_path = os.path.abspath( os.getcwd() + "/../../api/")
if len(sys.argv) == 6:
	chimes_module_path = os.path.abspath(sys.argv[5])
sys.path.append(chimes_module_path)

import wrapper_py

# Initialize the ChIMES calculator

wrapper_py.chimes_wrapper = wrapper_py.init_chimes_wrapper("libwrapper-C.so")
wrapper_py.set_chimes()

# Read in the parameter and coordinate filename 

if (len(sys.argv) != 4) and (len(sys.argv) != 6):
	
	print( "ERROR: Wrong number of commandline args")
	print( "       Run with: python <this file> <parameter file> <xyz file> <nlayers>")
	print( "       Run with: python <this file> <parameter file> <xyz file> <nlayers>")
	exit()

param_file = sys.argv[1] # parameter file
coord_file = sys.argv[2] # coordinate file

rank = 0

#wrapper_py.init_chimes(sys.argv[1], int(sys.argv[3]), rank)
wrapper_py.init_chimes(sys.argv[1], rank)

# Read the coordinates, set up the force, stress, and energy vars

natoms  = None
lx      = None
ly      = None
lz      = None
atmtyps = []
xcrd    = []
ycrd    = []
zcrd    = []

ifstream = open(coord_file,'r')
natoms   = int(ifstream.readline())
cell_a       = ifstream.readline().split()
cell_b       = [float(cell_a[3]), float(cell_a[4]), float(cell_a[5])]
cell_c       = [float(cell_a[6]), float(cell_a[7]), float(cell_a[8])]
cell_a       = [float(cell_a[0]), float(cell_a[1]), float(cell_a[2])]

energy = 0.0
stress = [0.0]*9
fx     = [] 
fy     = []
fz     = []

for i in range(natoms):

	atmtyps.append(ifstream.readline().split())
	
	xcrd.append(float(atmtyps[-1][1]))
	ycrd.append(float(atmtyps[-1][2]))
	zcrd.append(float(atmtyps[-1][3]))
	
	atmtyps[-1] = atmtyps[-1][0]
	
	fx.append(0.0)
	fy.append(0.0)
	fz.append(0.0)

# Do the calculations

fx, fy, fz, stress, energy = wrapper_py.calculate_chimes(
                           natoms, 
			   xcrd, 
			   ycrd, 
			   zcrd, 
			   atmtyps, 
			   cell_a,
			   cell_b,
			   cell_c,
			   energy,
			   fx,
			   fy,
			   fz,
			   stress)

print ("Success!")
print ("Energy (kcal/mol)",energy)
print("Stress tensors (GPa): ")
print(stress[0]*6.9479)
print(stress[4]*6.9479)
print(stress[8]*6.9479)
print(stress[1]*6.9479)
print(stress[2]*6.9479)
print(stress[5]*6.9479)
print("Forces (kcal/mol/A): ")
for i in range(natoms):
	print(fx[i])
	print(fy[i])
	print(fz[i])

debug = 0

if len(sys.argv) == 6:
	debug = int(sys.argv[4])
	
if debug == 1:

	ofstream = open("debug.dat",'w')
	
	ofstream.write("{0:0.6f}\n".format(energy))
	ofstream.write("{0:0.6f}\n".format(stress[0]*6.9479))
	ofstream.write("{0:0.6f}\n".format(stress[4]*6.9479))
	ofstream.write("{0:0.6f}\n".format(stress[8]*6.9479))
	ofstream.write("{0:0.6f}\n".format(stress[1]*6.9479))
	ofstream.write("{0:0.6f}\n".format(stress[2]*6.9479))
	ofstream.write("{0:0.6f}\n".format(stress[5]*6.9479))
	for i in range(natoms):
		ofstream.write("{0:0.6e}\n{1:0.6e}\n{2:0.6e}\n".format(fx[i],fy[i],fz[i]))
	
	ofstream.close()

#!/usr/bin/env python

﻿import subprocess
import re
import argparse

maxInput = [400, 50] #default values to be used before an optimized value has been produced. These should be your best guess at a good value(probably in the middle of your range)
#The number of values in this list should be the number of parameters you will optimize, in order of optimization

parser = argparse.ArgumentParser()
parser.add_argument("-fpp", "--fpp", type=int, help="set argument fpp, the default is 600")
parser.add_argument("-a", "--arga", type=int, help="set argument a for a fixed value, the default is 6")
parser.add_argument("-fpprange", "--fpprange", type=str, help="set argument a for fpp range, formatted with 3 comma separated values: minimum range, maximum range, step")
parser.add_argument("-input1", "--input1", type=str, help="set input file 1")
parser.add_argument("-input2", "--input2", type=str, help="set input file 2")
parser.add_argument("-output1", "--output1", type=str, help="set output .fasta file")
parser.add_argument("-output2", "--output2", type=str, help="set output .priceq file")
parser.add_argument("-dbk", "--dbk", type=int, help="set argument dbk, the default is 50")
parser.add_argument("-dbkrange", "--dbkrange", type=int, help="set argument dbk, as a range of values to test, formatted as: minimum,maximum,step.")
parser.add_argument("-dbmax", "--dbmax", type=int, help="set argument dbmax, the default is 250")
parser.add_argument("-mol", "--mol", type=int, help="set argument mol, the default is 20.")
parser.add_argument("-option1", "--option1", type=str, help="Determine if you would like to find a maximum or minimum value to be find, input 1 for minimum, input 2 for maximum. Will find Maximum by default.")
parser.add_argument("-option2", "--option2", type=str, help="Determine the value you are trying to find Min/Max for. Input 1 for number of contigs, Input 2 for N50, Input 3 for largest contig length. Max Contig length is default.")

args = parser.parse_args()
if args.option1 == 1:
	print "Finding Minimum value for:"
else:
	print "Finding maximum value for:"
if args.option2 == 1:
	print " number of contigs"
if args.option2 == 2:
	print " N50"
else:
	print " max contig length"	

if args.fpprange:
	fpp_list = args.fpprange.split(',')
	minfpp = fpp_list[0]
	maxfpp = fpp_list[1] 
	fppstep = fpp_list[2]
	print "For argument fpp, the minimum value is: "+ str(minfpp) +", the maximum value is: "+ str(maxfpp) +", and the step is: "+ str(fppstep) +"."
else:
	if args.fpp:
		maxInput[0] = args.fpp
		minfpp = int(args.fpp)
		maxfpp = int(99999)
		fppstep = int(999999999)
	print "Fpp is "+ str(maxInput[0]) +"."
	minfpp = int(600)
	maxfpp = int(99999)
	fppstep = int(999999999)
	
if args.dbkrange:
	dbk_list = args.dbkrange.split(',')
	mindbk = dbk_list[0]
	maxdbk = dbk_list[1] 
	dbkstep = dbk_list[2]
	print "For argument dbkhe minimum value is: "+ str(mindbk) + ", the maximum value is: "+ str(maxdbk) +", and the step is: "+ str(dbkstep) +"."
else:
	if args.dbk:
		maxInput[1] = args.dbk
		mindbk = int(args.dbk)
		maxdbk = int(99999)
		dbkstep = int(999999999)
	print "Dbk is "+ str(maxInput[1]) +"."
	mindbk = int(50)
	maxdbk = int(99999)
	dbkstep = int(999999999)


FileInput1 = args.input1
print('File being read as first input: ')
print(FileInput1)
FileInput2 = args.input2
print(' File being read as second input: ')
print(FileInput2)
FileOutput1 = args.output1 
print(' Output .fasta file: ')
print(FileOutput1)
FileOutput2 = args.output2
print(' Output .priceq file: ')
print(FileOutput2)
if args.arga:
	ArgA = args.arga
else:
	ArgA = 6
if args.mol:
	ArgMol = args.mol
else:
	ArgMol = 20
if args.dbmax:
	ArgDbmax = args.dbmax
else:
	ArgDbmax = 250
print('Number of processors to be used: ')
print(ArgA)



rangeInput = []
#the 0(the first parameter to be optimized) spot in list rangeinput, to be iterated with j, this will be the range inputs(minimum, maximum, step) for the first parameter to be edited.
#Remember that the maximum value will not be reached ex: a range of 0,12,2 will produce values of 0,2,4,6,8, and 10. 12 (the maximum) will not be used.
rangeInput.append([int(minfpp),int(maxfpp),int(fppstep)])
#the 1 spot(second parameter to be optimized), also range inputs(min, max, step)
rangeInput.append([int(mindbk),int(maxdbk),int(dbkstep)])
#the 2 spot(third parameter to be optimized), range inputs(min,max,step)
#rangeInput.append([200,300,50])
#More inputs should be added in order until the number of lists(range parameters) added to 'rangeInput' is equal to the number of parameters you want to optimize
#rangeInput.append([10,30,5])

f = open('final_prog_data.txt', 'a')

for j in range(0,2,1): #The second number should be the number of values you want to optimize, this outer loop chooses the list in rangeInputs that will be read for optimization
	inputs = maxInput[:]
	d={}
#puts in range for i, using the particular parameter in the j loop(a list), and the range specified in the i loop(an integer)
	for i in range(rangeInput[j][0], rangeInput[j][1], rangeInput[j][2]):
		inputs[j] = i
#		run = 'echo 123455678892'+ str(FileOutput1) +' / 4 '+ str(FileInput1) +'/ '+ str(inputs[0]+inputs[1]+inputs[2])+' / 6/ '+ str(int(inputs[0])*int(inputs[1])*int(inputs[2])) +' '
		run = '/usr/local/Programs/bin/PriceTI -icf subset.fasta 1 1 2 -mol '+ str(ArgMol) +' -dbk ' + str(inputs[1]) + ' -dbmax '+ str(ArgDbmax) +' -fpp '+str(FileInput1) + ' ' +  str(FileInput2) + ' ' + str(inputs[0]) +' 90 -target 90 3 2 2 -rqf 95 0.998 0 14 -rqf 95 0.99 14 6 -rqf 95 0.9 20 10 -rqf 90 0.9 30 10 -rqf 80 0.6 40 20 -lenf 60 1 -lenf 70 5 -lenf 80 20 -reset 5 10 14 18 20 25 30 35 40 45 50 55 59 60 63 65 70 75 -nc 81 -nco 5 -a '+ str(ArgA) +' -o '+ str(FileOutput1) +' -o '+ str(FileOutput2) +' '
# This is the command you will be iterating over, and each paramater to be optimized should have the argument tag followed by the string addition of the input for that range. See next line for example
#Ex: run = '... -example ' + str(inputs[1]) + ' . . . '   Where -example is the argument tag (like -fpp or -dbmax) and [1] is the range to be used (1 is the second parameter to be optimized)
		result = subprocess.Popen(run, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell=True)
		out = result.stdout.read()
		err = result.stderr.read()
		print(repr(run))
		f.write('input: ')
		f.write(repr(i))
		f.write(', output: ')
		trimmed_out=out[-60:]
		output_list = trimmed_out.split('/')
#the next variable is called longest_contig_length, but based on user specification might actually represent the N50 or total number of contigs.
		if args.option2 == 1:
			longest_contig_length = output_list[-3]
		elif args.option2 == 2:
			longest_contig_length = output_list[-2]
		else:
			longest_contig_length = output_list[-1]

		untrimmed_contig_length= longest_contig_length.splitlines()
		trimmed_contig_length=untrimmed_contig_length[0]
		formatted_output = int(trimmed_contig_length.strip())
		f.write(repr(formatted_output))
		f.write('\n')
		d[i] = formatted_output
	f.write('\n')
	f.write(repr(d))
	if args.option1 == 1:
		f.write('Minimum Value is: ')
	else:	
		f.write('Maximum value is: ')
#Some of the folowing variables refer to the max contig length but may represent minimum values, or n50 values based on user specification. 
	local_max_output = max(d.values())
	f.write(repr(local_max_output))
	local_max_input = [max(d, key=d.get)]
	local_max_input_int=list()
	local_max_input_int=local_max_input[0]
	f.write('\n')
	if args.option1 == 1:
		f.write('Input for minimum value is: ')
	else:
		f.write('Input for maximum value is: ')

	f.write(repr(local_max_input_int))
	f.write('\n')
	f.write('\n')
	maxInput[j] = int(local_max_input_int)

f.write(repr(maxInput))
f.write('\n')

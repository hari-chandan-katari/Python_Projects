"""
		EE2703: Applied Programming Lab
		Assignment - 1
		Prof. Harishankar Ramachandran
		
			Done By:
			KATARI HARI CHANDAN
			EE19B032
"""

#We imported argv, exit functions from sys module.
from sys import argv, exit

#Rather than calling the strings as '.circuit' and'.end' we have written it in convinient form of a variable. 
Begin = '.circuit'
End = '.end'

#The length of argv array should be "2" because argv counts the number of arguments in the command line which should be 2 and the are .py file and .netlist file.
if len(argv) != 2:
	#Error statement is printed if length of argv array is not 2.
	print('\nError!! The Arguements you have written are incorrect, there should be exactly 2 arguements. \n The Command should be of form: python3 <code.py> <circuit.netlist>')
	exit()
elif argv[1].split('.')[1] != "netlist":
	#Error statement is printed if the 2nd arguement(argv[1]) is not .netlist file.
	print("Error!! Please make sure the filename ends with .netlist")
	exit()
else:
	try:
		with open(argv[1]) as f:
			lines = f.readlines()	#This reads all the lines in .netlist file and store them in an array named "lines".
			start = float('inf'); end = float('inf');
				
	# 2 variables start and end are given +inf values because, if the string .end occurs before .circuit, it should show an error message. TO ensure that initial values hould be large enough.
			
			i=0;	# This variable is defined to show an error message whenever .circuit word occurs more than once.
			for line in lines:              
				if Begin == line[:len(Begin)]:	#Makes sure .circuit word is there in the file and the the index is noted.
					start = lines.index(line)	#The index of the .circuit word is given to "start" variable.
					i = i+1		#The defined i is incremented and if it is greater than 1, it means .circuit word has occured more than once. Error message is printed.	
					if i>1:
						print("Error!! .circuit word is there more than once. Only 1 circuit can be implemented at a time.")
						exit()
				elif End == line[:len(End)]:		#Makes sure .end word is there in the file and the the index is noted.
					end = lines.index(line)	#The index of the .end word is given to "end" variable.
					           	
					break
                
			if start >= end:   #If start variable is greater than end variable, this implies .end appeared ahead of .circuit which is wrong. Error message is printed.           
				print('Invalid circuit definition. .circuit cannot be after .end in the netlist')
				exit(0)
			
			#All the documentation lines(starting with #) are removed and the remaining lines between .circuit and .end are printed in the reverse order of words and lines.
			for line in reversed([' '.join(reversed(line.split('#')[0].split())) for line in lines[start+1:end]]):
				print(line)                 

	except IOError:
		print('The file is invalid')
		exit()
		
"""
	The functions this Python Code can execute are:
	1. It reads a .netlist file and prints all the circuit descriptions in the reverse order of words and lines if Error statements are not printed.
	2. Error Statements are printed if:
		(i) .end appears ahead of .circuit
		(ii) .circuit or .end appear more than once.
		(iii) The Command line is not in the form python3 <code.py> <ckt.netlist>
		(iv) More than 2 aruguements are made in the command line.
"""

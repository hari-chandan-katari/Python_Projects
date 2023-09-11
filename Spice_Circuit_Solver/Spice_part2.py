"""
		EE2703: Applied Programming Lab
		Assignment - 2
		Prof. Harishankar Ramachandran
		
			Done By:
			KATARI HARI CHANDAN
			EE19B032
"""

import numpy as np
import sys
arg1=sys.argv[1]

#Opening the file and reading the lines
with open(arg1) as f:
	lines=f.readlines()
	circuit='.circuit'
	finish='.end'
	ac='.ac'
	start=-1;end=-2
	l=[]
	w=a=0
	ac_source=0

#Extracting the start and end of main circuit block
	for i in range(len(lines)): 
		k=(lines[i].split('#')[0]).strip()
		l.append(k)
		ac_num=0

		if k==circuit:
			start=i
		elif k==finish:
			end=i
		if ac in k:
			ac_source=1
			if k.split()[0]==ac:
				ac_num=i
				break
	if (start>=end or start<0):
		print ('Invalid circuit definition')
		exit()
	if ac_source==1 and ac_num==0:
		print("frequency is not given") 
		exit()
	freq=l[ac_num].split()[-1]

#Extracting the frequency value from the .ac command 
	if ac_source==1:
		if('e' in freq)==True:
			k=freq.find('e')
			w=int(freq[:k])*pow(10,int(freq[k+1:]))
		else:w=int(freq)
		print("Given circuit has AC Sources")

#Defining Classes
	class Passive:										
		def  __init__(self,name,n1,n2,value):
			self.n1=n1
			self.name=name
			self.n2=n2
			self.value=value
	class AC_Sources:
		def  __init__(self,name,n1,n2,typ,value,phase):
			self.n1=n1
			self.name=name
			self.n2=n2
			self.typ=typ
			self.value=value
			self.phase=phase
	class DC_Sources:
		def  __init__(self,name,n1,n2,typ,value):
			self.n1=n1
			self.name=name
			self.n2=n2
			self.typ=typ
			self.value=value

#Declaring Lists for all components
	R,L,C,V,N,I=([] for i in range(6))
	hash={}

#Organising all the components into  different Lists with instances to classes as elements
	for i in l[start+1:end]:
		p=i.split()
		f=p[-1]
	#Converting the values to decimal
		if('e' in p[-1])==True:
			k=f.find('e')
			k=float(f[:k])*pow(10,float(f[k+1:]))
		else:
			k=float(p[-1])
		p[-1]=k
		(c),*d=p
		y=c[1:]
		z=c[0:1]
	#Gathering all the nodes	
		if p[1] not in N:
			N.append(p[1])	
		if p[2] not in N:
			N.append(p[2])		
		if (z=='R'):
			R.append(Passive(*p))
		if ac_source!=1:		
			if (z=="V"):
				V.append(DC_Sources(*p))
			elif z=='I':
				I.append(DC_Sources(*p))
		if ac_source==1:
			if (z=="L"):
				L.append(Passive(*p))
			elif(z=='C'):
				C.append(Passive(*p))	
			elif (z=="V"):
				V.append(AC_Sources(*p))
			elif z=='I':
				I.append(AC_Sources(*p))
	
#Creating the Dictinary with all the nodes and voltage sources
	for i in N: 		
		if i!='GND':
			hash[i]=a
			a+=1
	p=len(hash)
	for i in V:
		hash[i.name]=p
		p+=1

#Creating the array using the dictionary
	A=np.zeros(len(hash),dtype='complex')	
	#For a particular node in dictionary 		
	for i in hash:
		if hash[i]<len(N)-1:
			S=np.zeros(len(hash),dtype='complex')	
				
		#Going through all resistors 
			for x in R:
				B=np.zeros(len(hash))
				f=float(x.value)
				if x.n1==i:			
					B[hash[i]]=1/f 
					try:B[hash[x.n2]]=-1/f
					except KeyError:pass
					S+=B
				elif x.n2==i:
					B[hash[i]]=1/f
					try:B[hash[x.n1]]=-1/f
					except KeyError:pass
					S+=B

		#Voltage sources
			for x in V:
				if x.n1==i:			
					B=np.zeros(len(hash))
					try:B[hash[x.name]]=-1
					except KeyError:pass
					S+=B
				elif x.n2==i:
					try:B[hash[x.name]]=1
					except KeyError:pass
					S+=B
			if ac_source==1:
			#Inductors	
				for x in L:
					B=np.zeros(len(hash),dtype='complex')
					l=float(x.value)
					if x.n1==i:
						B[hash[i]]=complex(0,-1/(w*l))
						try:B[hash[x.n2]]=complex(0,1/(w*l))
						except KeyError:pass
						S+=B
					elif x.n2==i:
						B[hash[i]]=complex(0,-1/(w*l))
						try:B[hash[x.n1]]=complex(0,1/(w*l))
						except KeyError:pass
						S+=B
	
			#Capacitors
				for x in C:
					B=np.zeros(len(hash),dtype='complex')
					d=float(x.value)
					if x.n1==i:
						B[hash[i]]=complex(0,w*d)
						try:B[hash[x.n2]]=complex(0,-w*d)
						except KeyError:pass
						S+=B
					elif x.n2==i:
						B[hash[i]]=complex(0,w*d)
						try:B[hash[x.n1]]=complex(0,-w*d)
						except KeyError:pass
						S+=B
					
			A=np.vstack((A,S))	
		else :	
			for k in V:
				if k.name==i :
					B=np.zeros(len(hash))
					try:B[hash[k.n1]]=1
					except:pass
					try:B[hash[k.n2]]=-1
					except:pass
					A=np.vstack((A,B))	
	A=np.delete(A,0,axis=0)

#Creating the B array 
	S,E=(np.zeros(len(hash),dtype='complex') for i in range(2))
	phase=0	
	for i in I:
		if ac_source==1:
			phase=complex(0,(i.phase*180)/np.pi)
		B=np.zeros(len(hash),dtype='complex')
		try:B[hash[i.n1]]=float(i.value)*np.exp(phase)/2
		except:pass
		try:B[hash[i.n2]]=-float(i.value)*np.exp(phase)/2
		except:pass
		S+=B
	for i in V:
		if ac_source==1:
			phase=complex(0,(i.phase*180)/np.pi)
		B=np.zeros(len(hash),dtype='complex')
		B[hash[i.name]]=float(i.value)*np.exp(phase)/2
		E+=B
	B=E+S	
	x = np.linalg.solve(A,B)
	k=0
	for i in hash:
		if hash[i]<len(N)-1:
			print("Node voltage at {} is {}".format(i,x[k]))
		else:
			print("Current through voltage source {} is {}".format(i,x[k]))
		k+=1


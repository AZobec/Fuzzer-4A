# -*- coding: utf-8 -*-
#!/usr/bin/python3

############ MODULE D'ITERATIONS ############
#Gestion des imports
from itertools import product
from optparse import OptionParser
import optparse
import imp
from modules import __requests__

#Creation de la fonction itérative qui va envoyer les résultats de l'itération dans un fichier (un dictionnaire gratos !!)
def to_file(destination,chars):
	_file = open(destination,"wb")
	print(">>> Renseigner la range voulue au format chiffre;chiffre")
	_range = input("")
	_range = _range.split(";")
	for length in range(int(_range[0]), int(_range[1])+1):
		#intégrer ici le multi-threading?? 
		list_fuzzing = product(chars, repeat=length)
		for fuzzing in list_fuzzing:
			print((''.join(fuzzing)))
			_file.write(bytes((''.join(fuzzing)),'UTF-8'))
			_file.write(bytes(("\n"),'UTF-8'))
	#On ferme proprement les fichier
	_file.close()

def to_url(url,chars):
	print(">>> Renseigner la range voulue au format chiffre;chiffre")
	_range = input("")
	_range = _range.split(";")
	print()
	print("#### DEBUT DU FUZZING URL ####")
	for length in range(int(_range[0]), int(_range[1])+1):
		#intégrer ici le multi-threading?? 
		list_fuzzing = product(chars, repeat=length)
		for fuzzing in list_fuzzing:
			#print((''.join(fuzzing)))
			url_tmp = url.replace("FUZZ", (''.join(fuzzing)))
			__requests__.if_page_exist(url_tmp)
	print("#### FIN DU FUZZING URL ####")

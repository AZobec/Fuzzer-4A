# -*- coding: utf-8 -*-
#!/usr/bin/python3

############ MODULE D'ITERATIONS ############
#Gestion des imports
from itertools import product
from optparse import OptionParser
import optparse
import imp
from modules import __requests__
from os import listdir
from os.path import isfile, join

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

def to_url_wordlist(url):
	wordlist = dict()
	wordlist["general_wl"] = "./wordlist/general"
	wordlist["vulns_wl"] = "./wordlist/vulns"
	#wordlist["injections_wl"] = "./wordlist/Injections"
	wordlist["webservicces_wl"] = "./wordlist/webservicces"
	for key in wordlist.keys():
		for txt_file in listdir(wordlist[key]):
			if isfile(join(wordlist[key],txt_file)):
				print ("#### DEBUT TEST WORDLIST "+txt_file+" ####")
				_file = open(wordlist[key]+"/"+txt_file)
				for line in _file.readlines():
					url_tmp = url.replace("FUZZ", line[:-1])
					__requests__.if_page_exist(url_tmp)
					#print(url_tmp)
				print ("#### FIN TEST WORDLIST "+txt_file+" ####")
				_file.close()


def to_url_bruteforce(url,chars):
	print(">>> Renseigner la range voulue au format chiffre;chiffre")
	_range = input("")
	_range = _range.split(";")
	print()
	print("#### DEBUT DU BRUTEFORCE URL ####")
	for length in range(int(_range[0]), int(_range[1])+1):
		#intégrer ici le multi-threading?? 
		list_fuzzing = product(chars, repeat=length)
		for fuzzing in list_fuzzing:
			#print((''.join(fuzzing)))
			url_tmp = url.replace("FUZZ", (''.join(fuzzing)))
			__requests__.if_page_exist(url_tmp)
	print("#### FIN DU BRUTEFORCE URL ####")


def to_post(url,post,chars):
	print(">>> Renseigner la range voulue au format chiffre;chiffre")
	_range = input("")
	_range = _range.split(";")
	list_fuzzing_deux = []
	print()
	print("#### DEBUT DU BRUTEFORCE POST METHOD ####")
	post_tmp = post
	for length in range(int(_range[0]), int(_range[1])+1):
		#intégrer ici le multi-threading?? 
		list_fuzzing = product(chars, repeat=length)
		list_fuzzing_deux = product(chars, repeat=length)

		if post.count("FUZZ") == 2:		
			for fuzzing in list_fuzzing:
				post_tmp = post.replace("FUZZ", (''.join(fuzzing)),1)
				for fuzzing_deux in list_fuzzing_deux:
					post_tmp_deux = post_tmp.replace("FUZZ", (''.join(fuzzing_deux)))
					list_fuzzing_deux = product(chars, repeat=length)
					__requests__.if_post(url,post_tmp_deux)
					print (post_tmp_deux)

	print("#### FIN DU BRUTEFORCE POST METHOD ####")


def __init__():
	print("Module Natif. Modifiez directement les fonctions du module __iterations__.py")
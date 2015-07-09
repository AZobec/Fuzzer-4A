#!/usr/bin/python3

#-----------------------------------#
#	Projet Python3 3I SI			#
#	Groupe : GRAU - ZOBEC 			#
#-----------------------------------#


#Le but de ce projet est de créer un fuzzer web modulable (ajout de modules personnels)
#il a pour fonctionnalités: fuzzing de méthodes POST, fuzzing d'URL, file disclosure, SQLi, xss?? , et une modularité qui permet d'importer ses propres modules

#Gestion des imports
from itertools import product
from optparse import OptionParser
import optparse
import socket
import sys
import imp
import requests
import os
from modules import __requests__
from modules import __iterations__

file_path = os.path.dirname(os.path.realpath(__file__))

def handle_module(called_module):
	try:
		if called_module+".py" in os.listdir(file_path+"/modules/"):
			mod = imp.load_source(called_module, file_path+"/modules/"+called_module+".py")
			mod.__init__()
		else:
			print ("Unimplemented function :"+called_module)
	except Exception as error:
		print ("Exception : "+str(error))


#on va demander au client la range qu'il veut taper, s'il veut faire que des minuscules ou pas, etc...
def menu():
	print("-_-_-_-_-_-Bienvenue dans le Fuzzer web-_-_-_-_-_-")
	print(">>> Quel type de données voulez-vous tenter d'injecter")
	print(">>> Tapez 1 pour : minuscules seulement")
	print(">>> Tapez 2 pour : MAJUSCULES seulement")
	print(">>> Tapez 3 pour : ch1ffr35 seulement")
	print(">>> Tapez 4 pour : minuscules + MAJUSCULES")
	print(">>> Tapez 5 pour : minuscules + MAJUSCULES + ch1ffr35 ")
	print(">>> Tapez 6 pour : minuscules + MAJUSCULES + ch1ffr35 + c@ractères spéci@ux")
	test_user = input("")
	if test_user == "1":
		return "abcdefghijklmnopqrstuvwxyz"
	if test_user == "2":
		return "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	if test_user == "3":
		return "0123456789"
	if test_user == "4":
		return "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
	if test_user == "5":
		return "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
	if test_user == "6":
		return "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#=!+-_ /:|"
#fin de la fonction menu



#Fin de la fonction iteration_mdp(destination):

#début du main
if __name__ == "__main__":
	
	arguments = dict()

	arguments["destination_file"] = ""
	arguments["dictionnaire"] = ""
	arguments["HOST"] = ""
	arguments["PORT"] = ""
	arguments["modules"] = ""	
	arguments["url"] = ""
	arguments["post"] = ""

	
	############ DEBUT GESTION DES ARGUMENTS ############

	parser = optparse.OptionParser()

	parser.add_option("-f", "--file", dest = 'dictionnaire', help = "Choix d'un dictionnaire", metavar = "FILE", default = False)
	parser.add_option("-H", "--host", dest = 'HOST', help = "Choix du serveur à attaquer", metavar = "SERVER", default = False)
	parser.add_option("-w", "--write", dest = 'destination_file', help = "Output des datas", metavar = "FILE", default = False)
	parser.add_option("-p", "--port", dest = 'port', help = "Choix du port", metavar = "PORT", default = False)
	parser.add_option("-i", "--import", dest = 'modules', help = "Modules à importer séparés par une virgule", metavar = "IMPORT", default = False)
	parser.add_option("-u", "--url", dest = 'url', help = "URL à cibler, avec FUZZ comme directory à injecter", metavar = "URL", default = False)
	parser.add_option("-P", "--POST", dest = 'post', help = "Méthode POST à injecter, avec FUZZ comme indication", metavar = "POST", default = False)
	
	options,args = parser.parse_args()

	if options.destination_file != False:
		arguments["destination_file"] = options.destination_file
	if options.dictionnaire != False:
		arguments["dictionnaire"] = options.dictionnaire
	if options.HOST != False :
		arguments["HOST"] = options.HOST
	if options.port != False:
		arguments["PORT"] = int(options.port)
	if options.modules != False:
		arguments["modules"] = options.modules
		if "," in arguments["modules"]:
				arguments["modules"] = arguments["modules"].split(",")
	if options.url != False:
		arguments["url"] = options.url
	if options.post != False:
		arguments["post"] = options.post

	############ FIN DE GESTION DES ARGUMENTS ###############

	######### Premier test : savoir si des arguments sont présents #########
	if len(sys.argv)==1:
		parser.print_help()
		exit()

	######### Seconde chose : afficher le niveau fuzzing en temrme de charset #########
	charset = menu() 

	###### TEST TO REMOVE ########
	if arguments["url"] != "":
		if "FUZZ" in arguments["url"]:
			__iterations__.to_url(arguments["url"],charset)
		else:
			print("Indiquer FUZZ dans l'URL à fuzzer")


	### 
	if arguments["modules"] != "":
		if isinstance(arguments["modules"], str):
			handle_module(arguments["modules"])
		else:
			for j in arguments["modules"]:
				handle_module(j)

	#on va maintenant tester chaque option qu'on a reçu et utiliser les fonctions en conséquence 
	if  arguments["destination_file"] != "":
		#Obtention du choix de l'utilisateur et donc du charset en conséquence
		iteration_mdp(arguments["destination_file"],charset)



#Fin du main

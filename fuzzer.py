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
def menu(test_user):
	if test_user == "1":
		print(">>> Niveau du bruteforce : min")
		return "abcdefghijklmnopqrstuvwxyz"
	if test_user == "2":
		print(">>> Niveau du bruteforce : maj")
		return "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	if test_user == "3":
		print(">>> Niveau du bruteforce : chiffres")
		return "0123456789"
	if test_user == "4":
		print(">>> Niveau du bruteforce : min + maj")
		return "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
	if test_user == "5":
		print(">>> Niveau du bruteforce : min + maj + chiffres")
		return "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
	if test_user == "6":
		print(">>> Niveau du bruteforce : min + maj + chiffres + special")
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
	arguments["level"] = ""

	
	############ DEBUT GESTION DES ARGUMENTS ############

	parser = optparse.OptionParser()

	parser.add_option("-f", "--file", dest = 'dictionnaire', help = "Choix d'un dictionnaire", metavar = "FILE", default = False)
	parser.add_option("-H", "--host", dest = 'HOST', help = "Choix du serveur à attaquer", metavar = "SERVER", default = False)
	parser.add_option("-w", "--write", dest = 'destination_file', help = "Output des datas", metavar = "FILE", default = False)
	parser.add_option("-p", "--port", dest = 'port', help = "Choix du port", metavar = "PORT", default = False)
	parser.add_option("-i", "--import", dest = 'modules', help = "Modules à importer séparés par une virgule", metavar = "IMPORT", default = False)
	parser.add_option("-u", "--url", dest = 'url', help = "URL à cibler, avec FUZZ comme directory à injecter", metavar = "URL", default = False)
	parser.add_option("-P", "--POST", dest = 'post', help = "Méthode POST à injecter, sans espace : user=FUZZ,pass=FUZZ", metavar = "POST", default = False)
	parser.add_option("-l", "--level", dest = 'level', help = "Level du bruteforcing(chars) (de 1 à 6) 0 pour false", metavar = "LEVEL", default = False)


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
	if options.level != False:
		arguments["level"] = options.level
	if options.level == "0":
		arguments["level"] = False
	if options.level == False:
		arguments["level"] = False

	############ FIN DE GESTION DES ARGUMENTS ###############

	######### Premier test : savoir si des arguments sont présents #########
	if len(sys.argv)==1:
		parser.print_help()
		exit()

	#Message de bienvenue : 
	print("___________                                             _____    _____   ")
	print("\_   _____/_ __________________ ___________            /  |  |  /  _  \  ")
	print(" |    __)|  |  \___   /\___   // __ \_  __ \  ______  /   |  |_/  /_\  \  ")
	print(" |     \ |  |  //    /  /    /\  ___/|  | \/ /_____/ /    ^   /    |    \ ")
	print(" \___  / |____//_____ \/_____ \\\\___  >__|            \____   |\____|__  / ")
	print("     \/              \/      \/    \/                     |__|        \/ 	")
	print()

	######### Seconde chose : afficher le niveau fuzzing en temrme de charset #########
	charset = menu(arguments["level"]) 

	###### IF URL IN ARGS : #######
	if arguments["url"] != "":
		if "FUZZ" in arguments["url"]:
			__iterations__.to_url_wordlist(arguments["url"])
			if arguments["level"] != False:
				__iterations__.to_url_bruteforce(arguments["url"],charset)
		#ici : la méthode post + url sans FUZZ d'URL pur
		elif arguments["post"] != "":
			__iterations__.to_post(arguments["url"],arguments["post"],charset)
		else:
			print("Usage : ./fuzzer.py -u http://foo.bar/FUZZ to fuzz url")
			print("Usage : ./fuzzer.py -u http://foo.bar/ --POST user=FUZZ,pass=FUZZ")
			exit()
			


	###### IF --IMPORT test des imports ######
	if arguments["modules"] != "":
		if isinstance(arguments["modules"], str):
			handle_module(arguments["modules"])
		else:
			for j in arguments["modules"]:
				handle_module(j)

	#on va maintenant tester chaque option qu'on a reçu et utiliser les fonctions en conséquence 
	if  arguments["destination_file"] != "":
		#Obtention du choix de l'utilisateur et donc du charset en conséquence
		__iterations__.to_file(arguments["destination_file"],charset)



#Fin du main

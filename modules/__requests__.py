# -*- coding: utf-8 -*-
#!/usr/bin/python3

############ MODULE DE TEST DE REQUETES ############
#Gestion des imports
import requests

# Test afin de savoir si la page existe bien
def if_page_exist(url):
	r = requests.get(url)
	if r.status_code == requests.codes.ok:
		print("Cette page existe : "+url)
		return 0
	else:
		return 1

def __init__():
	print("Merci de modifier directement les fonctions de ce module.")
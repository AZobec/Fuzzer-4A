# -*- coding: utf-8 -*-
#!/usr/bin/python3

############ MODULE DE TEST DE REQUETES ############
#Gestion des imports
import requests

# Test afin de savoir si la page existe bien
def if_page_exist(url):
	try:
		r = requests.get(url)
		if r.status_code == requests.codes.ok:
			print("Cette page existe : "+url)
			return 0
		else:
			return 1
	except requests.exceptions.Timeout:
		print(">>> Requete TimeOut")
	except requests.exceptions.TooManyRedirects:
		print(">>> TooManyRedirects")
	except requests.exceptions.RequestException as e:
		print (e)

def if_post(url,post):
	payload = dict()
	all_posts = post.split(",")
	for champ in all_posts:
		option, value= champ.split('=',1)
		payload[option]=value
	try:
		r = requests.post(url, data=payload)
		if r.status_code == requests.codes.ok:
			print("Cette page existe : "+url)
			return 0
		else:
			return 1
	except requests.exceptions.RequestException as e:
		print (e)

def __init__():
	print("Module Natif. Modifiez directement les fonctions du module __requests__.py")
# -*- coding: utf-8 -*-
#module de test de requests
import requests
def __init__():
	print(">>> Module de test du module requests")
	r = requests.get("http://zobec.fr/404")
	print(r.status_code)
	#print(r.text)
	if r.status_code == requests.codes.ok:
		print("OK")

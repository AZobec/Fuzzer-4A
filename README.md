# Fuzzer-4A

## Qu'est-ce que c'est ?
C'est le projet de Python de 4ASI2 de Fuzzer Web par :

- Alexandre GRAU
- Arnaud ZOBEC

## Qu'est-ce qu'il fait ?

- Directory discovery (wordlist)
- Directory discrover (bruteforce)
- Post data bruteforcing
- SQLi fuzzing ?

## Comment il fonctionne?

Il suffit de faire :
	
	git clone https://github.com/AZobec/Fuzzer-4A.git
	./fuzzer.py -h

### Options

	-h ou --help pour afficher les options
	-f ou --file=FILE pour choisir un dictionnaire en plus !
	-w ou --write=FILE pour écrire le dictionnaire utilisé (dico gratos)
	-p ou --port=PORT pour le choix du port
	-i ou --import=IMPORT pour importer un module présent dans /modules
	-u ou --url=URL URL à cibler. Insérer FUZZ pour l'endroit à fuzzer
			ex: http://foo.bar/FUZZ
	-P ou --POST=POST pour fuzzing de la méthode POST ex : -P user=FUZZ,pass=FUZZ
	-l ou --level=LEVELNB pour le level du bruteforcing (chars) de 0 (rien) à 6

# I-TRACING Exercice technique de recrutement

Dans le cadre d'une interview technique j'ai eu à travailler sur l'exercice décrit dans le document de référence N4255. Je vous remercie de prendre le temps de lire mon code.

## Installation

L’installation des librairies suivante est nécessaire pour le bon fonctionnement de ce programme.

```bash
pip install certstream
```

```bash
pip install requests
```

```bash
pip install levenshtein
```

## Utilisation

```bash
Lancer main.py
>>> Entrer le domaine a explorer : Vide par défaut
>>> Entrer le seuil de confiance AbuseIPDB 0-100 (Le plus bas le mieux) : 0 par défaut
>>> Entrer le seuil de confiance  
>>> Confirmer l'observation de données sur le terminal : Non par défaut
```

### Compréhension de la consigne
Pour protéger les utilisateurs et clients du site Pepito.com j'ai du concevoir un outil simple se servant du flux de données distribuer par certstream afin d'identifier les éventuels nom de domaines pouvant être une menace de typosquattage.

Nous devons déterminer leurs niveau de menace en fonction de leurs :
- ressemblance à notre nom de domaine
- réputation de certification ssl
- score AbuseIPDB

L'outil devrais donc signaler une alerte à chaque fois qu’un potentiel menace est détectée.

### Restriction

Dans le cadre de ce projet les restrictions principales sont l'usage du Python comme langage principale et l'utilisation de certstream et AbuseIPDB afin d'obtenir des scores de menace plus précis. Evidement pour des raisons d'intégrité et de transparence aucune intelligence artificielle n'a été utilisé pour cet exercice.

## Design

Cet outil interagit avec plusieurs API simultanément afin de pouvoir obtenir des résultats. Il est pratique de visualiser un cycle de fonctionnement afin d’identifier la forme du programme

[image] 

### Fichiers fournis

Les fichiers suivants sont fournis :
-  BaseClient.py : Interface servant à inplémenter AbuseIPDBClient en offrant la possibilité d'envoyer des requêtes.
- AbuseIPDBClient.py : Classe offrant la possibilité d'obtenir un score de confiance à partir d'une adresse IP.
- Logger.py : Classe permettant d'afficher les alertes potentiels de typosquating au besoin mais aussi principalement de sauvegarder en mémoire les résultats dans un fichier local.
- Main.py : Point d'entrée de notre programme.

### Fichiers ajoutés

Les fichiers suivants ont été ajoutés 

secrets.py : fichier contenant la variable api_key obtenue de AbuseIPDB afin de diminuer sa visibilité.

### Contrainte de développement et ajustements

Au cours du développement les contraintes suivantes ont attiré mon attention et que j'ai estimé importante dans le développement de l'outil

- Détermination du niveau de menace : Sans référence plus précise fournie dans le document de départ j'ai observé que chacun des paramètres nécessitait une étude afin de pouvoir lui attribuer un poids dans la détermination du niveau de menace. Pour la ressemblance de nom de domaine j'ai opté pour la méthode Levenshtein et de sa fonction ratio plutôt que distance. Ratio donnant un pourcentage de ressemblance alors que distance n'offre qu'une valeur fixe arbitraire.

```python
distance('cat', 'cattle')
3
ratio('cat', 'cattle')
0.6666666666666667
distance('cupcake', 'cakecup')
6
ratio('cupcake','cakecup')
0.5714285714285714
```
- Le seuil de confiance **AbuseIPDB** est une ressource limitée, j'ai eu à dépasser les 1000 requêtes offerte par jour a cause d'un mauvais filtrage de requêtes. En dehors du faite qu'il semble dépendre des avertissement d'utilisateurs il se peut qu'un site soit dans la liste blanche de **AbuseIPDB** et ainsi considéré comme digne de confiance malgré les avertissements des utilisateurs : *[Exemple](https://www.abuseipdb.com/check/162.216.150.198)*. Et dans le pire des cas, il se peut que **AbuseIPDB** n'ai pas encore de donnés sur le domaine ou que le domaine ne soit plus accessible.
- Et pour finir les certificats sont en bon nombre, en plus de **Let's Encript** un moyen supplémentaire d'obtenir une liste de certificats à éviter afin de les prendre en compte dans notre calcul de menace. N'étant pas un expert dans le domaine j'ai considéré qu'une ressemblance de 50%, un seul de confiance de plus de 20% et un certificat **Let's Encript** valait un point chacun, allant de 1 à 3, en passant par [LOW], [MEDIUM] et [HIGH].
* Pour ce qui est de **certstream**, il est très utile à partir du moment de son exécution mais il ne semble pas pouvoir donner des données antérieures à son moment d’exécution.
---
* Pour essayer de rendre l'outil un peu plus interactif j'ai eu a réfléchir à une liste de paramètre a entrer par l'utilisateur de l'outil lors de la recherche. Des arguments tel que le nom de domaine a explorer, le seuil de confiance et ressemblance minimale et aussi la possibilité d'afficher ou nom les résultats sur le terminal.

## Pistes d'améliorations
Au cours du développement j'ai collecté quelques idées d'implémentations bien que je n'ai pas pu tout implémenter et tester.

### Interface utilisateur et Base de données

Travaillant en Python et possédants une éventuelle grande quantité de données a conserver, une base de donnée PostgreSQL est recommandé avec Django.
Une interface utilisateur pourrait aisément guider des utilisateurs, proposer plus de paramètres de configuration pour la recherche de menace et améliorer la richesse et la visibilité des réponses à nos requêtes. Un compteur de requêtes AbuseIPDB m'aurait aussi aidé.

### Code Original fournis

Tel que proposé par la consigne j'ai eu à changer le code et ajouter les librairies suivantes :
- Socket : Afin de pouvoir obtenir une adresse IP au cas ou l'utilisateur entre un nom de domaine.
- json : afin d'avoir un accès plus simple aux données des réponses a nos requêtes.
- Lavenshtein : afin d'obtenir des méthodes pour calculer les ressemblances des noms de domaines.
- dateTime : Afin d'avoir des horaires sur les différentes sorties obtenues.


Au plaisir de pouvoir en discuter avec vous!

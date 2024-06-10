# main.py

from AbuseIPDBClient import AbuseIPDBClient
from Logger import Logger
import certstream

# importaiton de la librairie Levenshtein pour déterminer des ratios de ressemblance
from Levenshtein import ratio

# importation de datetime pour avoir un horaire sur les entrées
import datetime

# importation de la variable api_key
from secrets import api_key as key


def print_callback(message, context):
    global myDomain
    global logger
    Score = 0
    log = None
    if message["message_type"] == "heartbeat":
        return

    if message["message_type"] == "certificate_update":

        all_domains = message["data"]["leaf_cert"]["all_domains"]
        CA = message["data"]["leaf_cert"]["extensions"]["authorityInfoAccess"]

        if len(all_domains) == 0:
            domain = "NULL"
        else:
            domain = all_domains[0]
        # On supprime l'éventuel *. au début de certains domaines
        if domain.startswith("*."):
            domain = domain[2:]

        AbuseIPDBScore = AbuseIPDBClient("https://api.abuseipdb.com/api/v2/check", key)

        # On vérifie que notre nom de domaine est assez proche de celui qu'on vient de trouver
        if ratio(myDomain, domain) >= Ressemblance:
            Score += 1

            # On essaye d'obtenir un score AbuseIPDB
            if AbuseConfidence > 0:
                try:
                    if AbuseIPDBScore.check_reputation(domain=domain) >= AbuseConfidence and AbuseConfidence:
                        Score += 1
                except Exception as error:
                # handle the exception
                    if printLogs:
                        print(
                            f"An exception occurred with domain {domain}:".format(domain),
                            error,
                            )

            if "lernc" in CA:
                Score += 1

        if Score == 1:
            log = "LOG ::: [{}] // [LOW] Domain : {} | CA : {} \n".format(
                datetime.datetime.now().strftime("%m/%d/%y %H:%M:%S"),
                domain,
                message["data"]["leaf_cert"]["extensions"]["authorityInfoAccess"],
            )
        elif Score == 2:
            log = "LOG ::: [{}] // [Medium] Domain : {} | CA : \n{} ".format(
                datetime.datetime.now().strftime("%m/%d/%y %H:%M:%S"),
                domain,
                message["data"]["leaf_cert"]["extensions"]["authorityInfoAccess"],
            )
        elif Score == 3:
            log = "LOG ::: [{}] // [HIGH] Domain : {} | CA : \n{} ".format(
                datetime.datetime.now().strftime("%m/%d/%y %H:%M:%S"),
                domain,
                message["data"]["leaf_cert"]["extensions"]["authorityInfoAccess"],
            )
        if not log == None:
            logger.alert(message=log)


def main():
    certstream.listen_for_events(print_callback, url="wss://certstream.calidog.io/")


if __name__ == "__main__":

    myDomain = printLogs = ''
    AbuseConfidence = Ressemblance = -1

    while myDomain == '':
        myDomain = input(
            "Veuillez entrer un nom de domaine à explorer -> "
        )
    while not int(AbuseConfidence) >= 0 and int(AbuseConfidence) <= 100:
        try:
            AbuseConfidence = int(input(
            "Veuillez entrer le seuil de confiance AbuseIPDB 0-100 : (0 par defaut)"
            ))
        except:
            True
        
    while not int(Ressemblance) >= 0 and int(Ressemblance) <= 100:
        try:
            Ressemblance = int(input(
            "Veuillez entrer le degré de ressemblance  0-100 : (0 par defaut)"
            ))
        except:
            True

    Ressemblance = Ressemblance/100

    printLogs = input(
        "Voulez vous observer les entrées sur le terminal? (O/N): (N par défaut) -> "
        )
            
    if printLogs == "o" or printLogs == "O":
        printLogs = True
    else:
        printLogs = False

    logger = Logger(printLogs)

    main()

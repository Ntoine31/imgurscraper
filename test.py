import requests
import PIL
from alive_progress import alive_bar
import os
import threading

import cv2
original = cv2.imread("removed.png")

char_M = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
char_m = 'abcdefghijklmnopqrstuvwxyz'
char_d = '1234567890'

char = char_d+char_m
length = 7

logFile = open('log.txt','w')

count = len(char)
where = {}
for i in range(length):
    where[i] = 0
lastIndex = length - 1

def getImage(id):
    pic_url = 'https://i.imgur.com/'+id
    with open(id, 'wb') as handle:
        response = requests.get(pic_url, stream=True)
        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)

def checkNoExist(id):
    duplicate = original = cv2.imread(id)
    if original.shape == duplicate.shape:
        difference = cv2.subtract(original, duplicate)
        b, g, r = cv2.split(difference)
        if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
            return True
    return False

def updateWhere():
    for i in range(length-1,-1,-1):
        if where[i] == count:
            where[i] = 0
            if i-1 >= 0:
                where[i-1] += 1
                where[i] = 0
            else: 
                print('Done')
                exit()

def thread(id):
    getImage(id+'.png')
    removed = checkNoExist(id+'.png')
    if removed: os.remove(id+'.png')
    logFile.writelines(id + ' | REMOVED: ' + str(removed))
    os._exit(1)

def threadShit(id):
    pic_url = 'https://i.imgur.com/'+id
    with open(id, 'wb') as handle:
        response = requests.get(pic_url, stream=True)
        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)
    duplicate = original = cv2.imread(id)
    try:
        if original.shape == duplicate.shape:
            difference = cv2.subtract(original, duplicate)
            b, g, r = cv2.split(difference)
            if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
                os.remove(id)
    except:
        print('not ok:'+id)
    
            
    


with alive_bar(count**length) as progress:
    while True:
        #Compose the password
        id = ''
        for i in range(length):
            whereIndex =where[i]
            id += char[whereIndex]

        id += '.png'

        where[lastIndex] += 1

        if where[lastIndex] == count:
            updateWhere()

        thread=threading.Thread(target=threadShit,args=(id,))
        thread.start()
        
        progress()
    
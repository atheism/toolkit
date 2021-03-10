import os
import sys

def replacer(name):
    with open(name, "r+") as f:
        entry = f.read().replace('\n', '')
        print('read from file: ', entry)
        s = entry.split('_', 1)
        num = int(s[0]) + 100000
        nn = str(num) + '_' + s[1]
        print('write to file: ', nn)
        #f.seek(0)
        #f.write(nn)
        #f.truncate()
        f.close()

entries = os.listdir("tub")

for entry in entries:
    if entry.endswith('.jpg'):
        #print(entry)
        s = entry.split('_', 1)
        #print(int(s[0]) + 100000, s[1])
        num = int(s[0]) + 100000
        nn = str(num) + '_' + s[1]
        print(nn)
        #os.rename(entry, nn)
    if entry.endswith('.json'):
        replacer('tub/' + entry)
        s = entry.split('.', 1)
        t = s[0].split('_', 1)
        num = int(t[1]) + 100000
        nn = t[0] + '_' + str(num) + '.' + s[1]
        print(nn)
        #os.rename(entry, nn)

import sys,os.path

def getKey(_file):
    with open(_file,"r") as _File:
        filestring=_File.readline

def saveOVPNFile():
    pass



configPath = sys.argv[1]

fileOVPN='os.path.split(configPath)[1]'
print(os.path.split(configPath)[1])
from http.cookiejar import FileCookieJar
import sys,os.path
import platform
if platform.system()=='Windows':
    SEPT='\\'
else:
    SEPT='/'

BLOCKBEGIN='-----BEGIN'
BLOCKEND='-----END'

def getKey(_file):
    with open(_file,'r') as file:
        stage=0
        txt=''
        for line in file:
            if line.find(BLOCKBEGIN)!=-1:
                stage=1
                continue
            if line.find(BLOCKEND)!=-1:
                break
            if stage==1: txt+=line
        return(txt)    


configPath = sys.argv[1]

cName=os.path.split(configPath)[1].split('.')[0]
cPath=os.path.split(configPath)[0]

fileOVPN=cPath+SEPT+cName+'.OVPN'
fileCA=cPath+SEPT+'ca.crt'
fileTA=cPath+SEPT+'ta.key'
fileCERT=cPath+SEPT+cName+'.crt'
fileKEY=cPath+SEPT+cName+'.key'
fileCONF=cPath+SEPT+cName+'.conf'

configKEY='<ca>\n-----BEGIN CERTIFICATE-----\n'+getKey(fileCA)+'-----END CERTIFICATE-----\n</ca>\n'
configKEY+='<key>\n-----BEGIN PRIVATE KEY-----\n'+getKey(fileKEY)+'-----END PRIVATE KEY-----\n</key>\n'
configKEY+='<cert>\n-----BEGIN CERTIFICATE-----\n'+getKey(fileCERT)+'-----END CERTIFICATE-----\n</cert>\n'
configKEY+='<tls-auth>\n-----BEGIN OpenVPN Static key V1-----\n'+getKey(fileTA)+'-----END OpenVPN Static key V1-----\n</tls-auth>\n'

textOVPN=''
with open(fileCONF,'r') as file:
    for line in file:
        if line.find('ca ca.crt')!=-1:continue
        if line.find(f'cert {cName}.crt')!=-1:continue
        if line.find(f'key {cName}.key')!=-1:continue
        if line.find('tls-auth')!=-1:continue
        textOVPN+=line
textOVPN+="\nkey-direction 1\n\n"
textOVPN+=configKEY

#print(textOVPN)

with open(fileOVPN,'w') as file:
    file.write(textOVPN)
print('OVPN file writed.')
exit(0)
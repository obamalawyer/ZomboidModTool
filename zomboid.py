from urllib.parse import urlparse, parse_qs
import requests
from configobj import ConfigObj
import re
import argparse
import pathlib
import ruamel.yaml
from ruamel.yaml import YAML 

def args():
    parser = argparse.ArgumentParser(description="Project Zomboid Mod Adding Thing",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-d', '--docker', action='store_true', help='for docker hosting')
    group.add_argument('-n', '--native', action='store_true', help='for native hosting')
    parser.add_argument("config", help="Server config location")
    parser.add_argument("modlist", help="Modlist text file location")
    args = parser.parse_args()
    # print(args)
    configPath = args.config
    listPath = args.modlist
    if args.docker: servertype = 'docker'
    elif args.native: servertype = 'native'
    
    
    # print(f'args func listpath {listPath} and configpath {configPath}')
    return configPath, listPath, servertype

def getIds(url):
    r = requests.get(url)
    modName = re.findall(r"Mod ID: (.*)<\/", r.text)
    workshopId = urlparse(url).query
    return workshopId, modName

def getLists():
    configPath, listPath, servertype = args()
    # print(f'args func getList {listPath}')
    mods =  open(listPath, 'r')
    url = mods.readline()
    # print(listPath)

    workshopIdList = ""
    modNameList = ""
    
    while "https://steamcommunity.com/sharedfiles/filedetails/?id=" in url:
        workshopId, modName = getIds(url) 
        workshopIdList = workshopIdList + workshopId[3:] +';' 
        modNameList  = modNameList  + modName[0] +';'
        url = mods.readline()

    # print(f'Workshop Ids are {workshopIdList[:-1]} \nMod Ids are {modNameList [:-1]}')
    mods.close()
    return workshopIdList, modNameList
    

def writeToYaml():
    print('Editing yaml')
    configPath, listPath, servertype = args()
    # print(configPath)
    yaml = YAML()
    mf = pathlib.Path(configPath)
    doc = yaml.load(mf)
    workshopIdList, modNameList = getLists()
    # print(doc)
    readYaml = doc['services']['zomboid-dedicated-server']['environment']
    
    fullModnameList = 'MOD_NAMES=' + str(modNameList[:-1])
    fullWorkshopList = 'MOD_WORKSHOP_IDS=' + str(workshopIdList[:-1])


    x = [re.sub(r'MOD_NAMES=(.*)', str(fullModnameList), i) for i in readYaml]
    x = [re.sub(r'MOD_WORKSHOP_IDS=(.*)', str(fullWorkshopList), i) for i in x]
    index = 0

    while index < len(x):
        x[index] = ruamel.yaml.scalarstring.DoubleQuotedScalarString(x[index])
        index+=1
     # print(x)
    doc['services']['zomboid-dedicated-server']['environment'] = x

    yaml.dump(doc, mf)

def writeToNative():
    print('Editing ini')
    configPath, listPath, servertype = args()
    workshopIdList, modNameList = getLists()
    config = ConfigObj(configPath)
    # fullModnameList = 'MOD_NAMES=' + str(modNameList[:-1])
    # fullWorkshopList = 'MOD_WORKSHOP_IDS=' + str(workshopIdList[:-1])
    config['Mods'] = str(modNameList[:-1]) 
    config['WorkshopItems'] = str(workshopIdList[:-1])
    config.write()

def main():
    configPath, listPath, servertype = args()
    args()
    getLists()
    if servertype == 'docker': writeToYaml()
    elif servertype == 'native': writeToNative()
    print('Done')
        
        

main()
    
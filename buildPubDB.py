import re,sys
from PubDB import Pub

def getPubDB(file):
    lines = open(file,'r').readlines()
    
    pmatcher = re.compile('@(.*?){(.*?),')
    amatcher = re.compile('\s*(.*?)\s*=\s*[{"](.*?)["}]')
    ematcher = re.compile('\w*}\w*')
    
    pub = False
    pubs = []
    currPub = Pub()
    
    for line in lines:
        if not pub:
            # See if we're reading a publication
            for (type,ind) in pmatcher.findall(line):                
                pub = True
                currPub = Pub()
                currPub.setPubType(type)
                currPub.setIndex(ind)
        else:
            for (key,val) in amatcher.findall(line):                
                currPub.addEntry(key,val.replace('{','').replace('}',''))
                
            if ematcher.match(line):
                pubs.append(currPub)
                pub = False

    return pubs

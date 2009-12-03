from buildPubDB import getPubDB
import sys

name = sys.argv[1]
publoc = sys.argv[2]

def process(name,publoc):
    pubDB = getPubDB(publoc)

    years = []
    yearpubs = {}
    
    for pub in pubDB:
        if pub.hasKey('AUTHOR'):
            if pub.hasKey('YEAR') and pub.getEntry('AUTHOR').find(name) > -1:
                year = pub.getEntry('YEAR')
                if year in years:
                    ypubs = yearpubs[year]
                    ypubs.append(pub)
                else:
                    years.append(year)
                    tpubs = []
                    tpubs.append(pub)
                    yearpubs[year] = tpubs
        
    #This will reverse the sort
    years.sort(lambda x,y: int(y)-int(x) )
    
    #Also need to sort the pubs lists
    prettypubs = {}
    for year in years:
        pubs = yearpubs[year]
        
        pubs.sort(lambda x,y: x.getEntry('AUTHOR') < y.getEntry('AUTHOR'))
        prettypubs[year] = pubs
        
    #Build the super mapping
    mapping = ['templkeys','templvals']
    supermapping = {}
    supermapping['templkeys'] = years
    supermapping['templvals'] = prettypubs

    return years,prettypubs

(years,prettypubs) = process(name,publoc)

for year in years:
    print year
    print "<UL>"
    for pub in prettypubs[year]:
        print "<LI>" + pub.getSimpleWebRep() + "</LI>"
    print "</UL>"

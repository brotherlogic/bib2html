import sys

class Pub:
    
    def  __init__(self):
        self.pubType = ""
        self.keyMap = {}
        self.index = ""

    def getKeys(self):
        return self.keyMap
        
    def getPubType(self):
        return self.pubType
        
    def getBibTexRep(self):   
        ret = "@" + self.pubType + "{" + self.index + ",\n"
        for key in self.keyMap:
            ret += "\t" + key + "\t = {" + self.keyMap[key] + "},\n"
        ret += "}\n"
        
        return ret

    def hasLink(self,type):
        return self.getLink(type) != ""

    def getLink(self,type):
        if self.hasKey('FILE'):
            file_info = self.getEntry('FILE')
            print "LINK",file_info
            elems = file_info.split(':')
            if len(elems) == 3:
                if elems[2].lower() == type.lower():
                    return "/" + elems[1]

        return ""

    def getOrdering(self):
        if self.pubType == 'INPROCEEDINGS':
            return ['AUTHOR','YEAR','TITLE','EDITOR','BOOKTITLE','PAGES','DATE','MONTH','LOCATION']
        elif self.pubType == 'CONFERENCE':
            return ['AUTHOR','YEAR','TITLE','BOOKTITLE','LOCATION','DATE','MONTH']
        elif self.pubType == 'INCOLLECTION':
            return ['AUTHOR','YEAR','TITLE','EDITOR','BOOKTITLE','VOLUME','PAGES']
        elif self.pubType == 'ARTICLE':
            return ['AUTHOR','YEAR','TITLE','JOURNAL','VOLUME','NUMBER','PAGES']
        elif self.pubType == 'PHDTHESIS':
            return ['AUTHOR','YEAR','TITLE','SCHOOL']
        elif self.pubType == 'TECHREPORT':
            return ['AUTHOR','YEAR', 'TITLE','INSTITUTION','NUMBER']
        else:
            return ['AUTHOR','YEAR','TITLE','BOOKTITLE','PAGES']
        
    def getLinkOrdering(self):
        return ['PDF','POSTER','PRESENTATION','LINK']
        
    def getPrefix(self,key):
        if key == 'TITLE':
            return ' <B>'
        elif key == 'BOOKTITLE':
            if self.getPubType == 'INPROCEEDINGS':
                return ' <I> In: '
            elif self.getPubType == 'CONFERENCE':
                return ' <I> Presented At: '
            else:
                return ' <I>'
        elif key == 'LOCATION' or key == 'DATE' or key == 'MONTH' or key == 'VOLUME':
            return ', '
        elif key == 'EDITOR':
            return ' In: '
        elif key == 'JOURNAL' or key == 'INSTITUTION':
            return ' <I>'
        elif key == 'NUMBER' or key == 'YEAR':
            return ' ('
        elif key == 'SCHOOL':
            return ' <I>PhD Thesis</I>, '
        elif key == 'PAGES':
            return ', '
        else:
            return ''
        
    def getLinkPostfix(self):
        return ' '
    
    def getPostfix(self,key):
        if key == 'AUTHOR':
            return ' '
        elif key == 'TITLE':
            return '</B>.'
        elif key == 'BOOKTITLE' or key == 'JOURNAL' or key =='INSTITUTION':
            return '</I>'
        elif key == 'EDITOR':
            return ' (Eds.)'
        elif key == 'NUMBER' or key == 'YEAR':
            return ')'
        else:            
            return ''
        
    def setPubType(self,type):
        self.pubType = type
        
    def addEntry(self,key,value):
        self.keyMap[key.upper()] = value.strip()
        
    def getEntry(self,key):
        return self.keyMap[key]
    
    def getIndex(self):
        return self.index
    
    def setIndex(self,index):
        self.index = index
    
    def getSimpleWebRep(self):
        if 'PDF' in self.keyMap:
            return '<A HREF="' + self.keyMap['PDF'] + '">' + self.getOrderedWebRep() + "</a>"
        else:
            return self.getOrderedWebRep()
    
    def getWebRep(self,builder):
        if self.hasLink('PDF'):
            return '<A HREF="' + builder.addDownload(self.getLink('PDF')) + '">' + self.getOrderedWebRep() + "</A>"
        else:
            return self.getOrderedWebRep()

    def getWebRepNoLink(self):
        return self.getOrderedWebRep()
    
    def getOrderedWebRep(self):
        str = ""
        ordering = self.getOrdering()
        
        for i in range(len(ordering)):
            key = ordering[i]
            if key in self.keyMap:
                str += self.getPrefix(key) + self.addElement(key) + self.getPostfix(key)
        str += "."
        return str
    
    def addLinks(self):
        str = ""
        ordering = self.getLinkOrdering()
        
        for key in ordering:            
            if self.hasLink(key):
                str += '<A HREF="' + self.getLink(key) + '">[' + key + ']</A>'
        return str
        
    def addElement(self,key):
        if key == 'AUTHOR' or key == 'EDITOR':
            return self.makeWebAuthors(self.keyMap[key])
        elif key == 'PAGES' or key == 'DATE':
            return self.keyMap[key].replace('--','-')
        else:
            return self.tidy(self.keyMap[key])

    def tidy(self,str):
        return str.replace('\&','&')
        
    def getDefaultWebRep(self):
        str = self.makeWebAuthors(self.keyMap['AUTHOR']) + " "
        str += "<b>" + self.keyMap['TITLE'] + "</b>"
        
        return str

    def hasKey(self,key):
        return key in self.keyMap
    
    def makeWebAuthors(self,authors):
        elems = authors.split(' and ')

        str = ""
        if len(elems) == 1:
            str = self.initialise(elems[0])
        else:
            for i in range(len(elems)-2):
                str += self.initialise(elems[i]) + ", "
                
            str += self.initialise(elems[-2]) + " and " + self.initialise(elems[-1])


        return str
    
    def initialise(self,author):
        elems = author.split(', ')
        if len(elems) == 2:
            return elems[1][:1]    + ". " + elems[0]
        else:
            print elems
            print author
            sys.exit(1)
    
    

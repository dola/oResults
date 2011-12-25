#!/usr/bin/python
# -*- coding: utf-8 -*-

import codecs

class orReader:
    """imports orWareFiles and provides them in a JSON format."""
    
    keys = ['RESULTTYPE','HEATORLEG','UPTOLEG','CLASSKEY','CLASSFULL',
            'ISCLIQUE','NAME','FIRST','YOB','SEX','CLUB','GROUPNAME',
            'TOWN','NATION','WREID','CARDNR','STNR','REFPERS','REFHEAT',
            'REFGRP','RANK','RUNTIME','BEHIND','INFO','RESPERSIDX',
            'RESCARDIDX','SCHEDULED','STARTED','FINISHED','ISPREACT',
            'PRECLASS','PRERANK','PRERUNTIME','PREBEHIND','PREPERSIDX',
            'PRECARDIDX','ACTRANK','ACTRUNTIME','ACTBEHIND','ACTPERSIDX',
            'ACTCARDIDX','FOREIGNKEY']
    # terminator field omitted
    
    data = {}
    
    def __init__(self, filePath):
        """initializes the importer with the filePath of the file to import"""
        self._separator = ","
        self._ContinueAfterNewCat = False
        self.path = filePath
    
    def read(self, categories=[]):
        """reads an inputFile and imports all data returning a dictionary containing the data for each category"""
        f = codecs.open(self.path, "r", "ISO 8859-1")
        cat = ""
        
        for line in f:
            key = self._getCat(line, cat)
            value = self._trimLine(line)
            
            if (cat != key and (key in categories or categories == [])):
                cat = key
                self.data[cat] = []
                print("analizing category " + key)
                if (self._ContinueAfterNewCat):
                    continue
                
            if (not categories == [] and not cat in categories):
                continue
            
            fields = value.split(self._separator)
           
            tdict = {}
            for k, v in zip(self.keys, fields):
                tdict[k.lower()] = v.replace('"', "")
            self.data[cat].append(tdict)
    
    def _trimLine(self, line):
        """returns line with removed overhead"""
        try:
            return line.split("=")[1]
        except ValueError:
            return line
    
    def _getCat(self, line, oldCat):
        """extracts cat from one dataline"""
        key, value = line.split("=")
        return key;
    
    def prettyPrint(self):
        """does a prettyPrint of the imported data"""
        for cat in self.data:
            print("\n" + cat + " ({} competitors)".format(len(self.data[cat])))
            for l in self.data[cat]:
                print '{0[rank]:3s} {1:40s} {2:20s} {3:40s} {4:4s}'.format(l, l["first"] + l["name"], l["classkey"], l["club"], l["runtime"])

class startTimeReader(orReader):
    keys = ["StartNr","eCardNr","FamilyName","Firstname","YearOfBirth","Town","Club","StartTime"]

    def __init__(self, filePath):
        """initializes the importer with the filePath of the file to import"""
        orReader.__init__(self, filePath)
        self._separator = ";"
        self._ContinueAfterNewCat = True

    def _trimLine(self, line):
        """returns line with removed overhead"""
        return line
    
    def _getCat(self, line, oldCat):
        """extracts cat from one dataline"""
        fields = line.split(self._separator)
        if len(fields) == 5:
            return fields[0]
        else:
            return oldCat
        #return line.split(self._separator)[]

    def prettyPrint(self):
        """does a prettyPrint of the imported data"""
        for cat in self.data:
            print("\n" + cat + " ({} competitors)".format(len(self.data[cat])))
            for l in self.data[cat]:
                print '{0[rank]:3s} {1:40s} {2:20s} {3:40s} {4:4s}'.format(l, l["first"] + l["name"], l["classkey"], l["club"], l["runtime"])

if __name__ == "__main__":
    from export import HtmlExport, JSONExport
    import os
	
    reader = orReader("DBOResDataSingle-1.ore")
    reader.read([])
    e = HtmlExport(reader.data, os.path.join("D:","xampp","htdocs"))
    ##e.exportStartlist("")
    e.exportRanking("")
    
    j = JSONExport(reader.data)
    j.export("export.json")
# -*- coding: utf-8 -*-


import string
CODEC='utf-8'
isDebug=False
zhuanyiChar='\\'
charToZhuanYi={'\"':'"','\\':'\\','\b':'b','\f':'f','\n':'n','\r':'r','\t':'t','\u':'u'}
ignoreChar=[' ','\n','\t']
def dealZhuanyi(c):
    '''根据转意字符后面的字符，输出转意后的字符'''
    if c=='"': return '"'
    if c=='\\': return '\\'
    if c=='/':return '/'
    if c=='b':return '\b'
    if c=='f':return '\f'
    if c=='n':return '\n'
    if c=='r':return '\r'
    if c=='t':return '\t'
    raise ValueError,  "ERROR:dealZhuanyi(), not a zhuanyi char"
    return None

def getString(str):
    if isDebug: print "DEBUG:getString(",str,") - Begin"
    '''对于json字符串，返回str前面的string类型，并且返回string类型结束的索引。'''
    curIndex=0#只处理前面的空格，不处理后面的
    while str[curIndex] in ignoreChar: curIndex+=1
    if str[curIndex] != '"':
        raise ValueError, "Error: getString(), not a string:"+str
    curIndex+=1
    zhuanYiFlag=False
    resultStr=unicode("")
    end=0
    while curIndex<len(str):
        c=str[curIndex]
        i=curIndex
        curIndex+=1
        if zhuanYiFlag:
            zhuanYiFlag=False
            if c=='u':
                unistr=str[curIndex:curIndex+4]
                unistr='u"\\u'+unistr+'"'
                resultStr=resultStr+eval(unistr)
                curIndex+=4
            else:
                resultStr=resultStr+dealZhuanyi(c)
            continue
        if c==zhuanyiChar:
            zhuanYiFlag=True
            continue
        if i!=0 and c=='"':
            end=i
            break
        if i!=0:
            resultStr=resultStr+c
    
   #resultStr=resultStr.decode(CODEC)
    
    # not isinstance(resultStr,unicode): resultStr=unicode(resultStr)
    if isDebug:print "DEBUG:getString(",str,"):",resultStr,end+1
    return resultStr,curIndex

def getObject(str):
    if isDebug:print "DEBUG:getObject(",str,") - Begin"
    dic={}
    curIndex=0
    while str[curIndex] in ignoreChar: curIndex+=1
    if str[curIndex]!='{':
        raise ValueError, "Error: getObject(), not a Object:no {,:"+str
    curIndex+=1
    while str[curIndex] in ignoreChar: curIndex+=1
    if str[curIndex]=='}':
        return dic,curIndex+1
    while True:
        key,index=getString(str[curIndex:])
        curIndex+=index
        while str[curIndex] in ignoreChar: curIndex+=1
        if str[curIndex]!=':':
            raise ValueError,  "ERROR: getObject: have no ':',:"+str
        curIndex+=1
        value,index=getValue(str[curIndex:])
        curIndex+=index
        dic[key]=value
        while str[curIndex] in ignoreChar: curIndex+=1
        if str[curIndex]!=",":
            break
        curIndex+=1
    while str[curIndex] in ignoreChar: curIndex+=1
    if str[curIndex]!='}':
        raise ValueError,  "ERROR: getObject(): have no '}',:"+str
    return dic,curIndex+1

def getArray(str):
    if isDebug:print "DEBUG:getArray(",str,") - Begin"
    arr=[]
    curIndex=0
    while str[curIndex] in ignoreChar: curIndex+=1
    if str[curIndex]!='[':
        raise ValueError,  "ERROR: getArray(),:"+str
    curIndex+=1
    while str[curIndex] in ignoreChar: curIndex+=1
    if str[curIndex]==']':
        return arr,curIndex+1
    while True:
        value,index=getValue(str[curIndex:])
        arr.append(value)
        curIndex+=index
        while str[curIndex] in ignoreChar: curIndex+=1
        if str[curIndex]!=",":
            break
        while str[curIndex] in ignoreChar: curIndex+=1
        curIndex+=1
    while str[curIndex] in ignoreChar: curIndex+=1
    if str[curIndex]!=']':
        raise ValueError,  "ERROR: getArray(): have no ']',:"+str
    return arr,curIndex+1

def getNumber(str):
    if isDebug:print "DEBUG:getNumber(",str,") - Begin"
    curIndex=0
    beginIndex=0
    while str[beginIndex] in ignoreChar: beginIndex+=1
    isFloat=False
    while beginIndex+curIndex<len(str) and str[beginIndex+curIndex] in "+-0123456789.eE":
        if str[beginIndex+curIndex]=='.' : isFloat=True
        curIndex+=1
    if isFloat:
        number=float(str[beginIndex:beginIndex+curIndex])
        if number==float('inf'):
            raise ValueError,"number:"+str[beginIndex:beginIndex+curIndex]+" out of range range"
    else:
        number=int(str[beginIndex:beginIndex+curIndex])
    if isDebug:print "DEBUG:getNumber(",str,"):",number,beginIndex+curIndex
    return number,beginIndex+curIndex


def getKeywords(str):
    if isDebug:print "DEBUG:getKeywords(",str,") - Begin"
    curIndex=0
    while str[curIndex] in ignoreChar: curIndex+=1
    
    if str.find("true",curIndex,curIndex+4)!=-1:
        if isDebug:print "DEBUG:getKeywords(",str,")",True,curIndex+4
        return True,curIndex+4
    if str.find("false",curIndex,curIndex+5)!=-1:
        if isDebug:print "DEBUG:getKeywords(",str,")",False,curIndex+5
        return False,curIndex+5
    if str.find("null",curIndex,curIndex+4)!=-1:
        if isDebug:print "DEBUG:getKeywords(",str,")",None,curIndex+4
        return None,curIndex+4
    raise ValueError,  "ERROR:getKeywords():not a keyword,:"+str
    
    
def getValue(str):
    value=None
    curIndex=0
    while str[curIndex] in ignoreChar: curIndex+=1
    if str[curIndex]=='{':
        value,index=getObject(str[curIndex:])
        if isDebug: print "DEBUG:getValue(),getObject:",value,index
    elif str[curIndex]=='[':
        value,index=getArray(str[curIndex:])
        if isDebug:print "DEBUG:getValue(),getArray:",value,index
    elif str[curIndex]=='"':
        value,index=getString(str[curIndex:])
        if isDebug:print "DEBUG:getValue(),getString:",value,index
    elif str[curIndex] in "+-0123456789":
        value,index=getNumber(str[curIndex:])
        if isDebug:print "DEBUG:getValue(),getNumber:",value,index
    else:
        value,index=getKeywords(str[curIndex:])
        if isDebug:print "DEBUG:getValue(),getKeywords:",value,index
    return value,curIndex+index


def convertStringToJson(s):
    '''
    将字符串转换为JSON识别的字符串，
    如'a"bc',转换为'"a/"bc'
    '''
    if isDebug:print "DEBUG:convertStringToJson(",s,")-begin"
    strResult='"'
    for c in s:
        if c in charToZhuanYi.keys():
            strResult=strResult+"\\"+charToZhuanYi[c]
        else:
            strResult+=c
    strResult+="\""
    if isDebug:print "DEBUG:convertStringToJson(",s,"):",strResult
    return strResult

def convertListToJson(l):
    if isDebug:print "DEBUG:convertListToJson(",l,")-begin"
    strR="["
    if len(l)>0:
        for e in l:
            strR=strR+convertValueToJson(e)+','
        strR=strR[:-1]
    strR+=']'
    if isDebug:print "DEBUG:convertListToJson(",l,")",strR
    return strR

def convertDictToJson(d):
    if isDebug:print "DEBUG:convertDictToJson(",d,")-begin"
    strResult="{"
    if len(d)>0:
        for key in d.keys():
            strResult+=convertStringToJson(key)+":"+convertValueToJson(d[key])+","
        strResult=strResult[:-1]
    strResult+="}"
    if isDebug:print "DEBUG:convertDictToJson(",d,"):",strResult
    return strResult
    
def convertValueToJson(v):

    if isDebug:print "DEBUG:convertValueToJson(",v,")-begin",type(v)
    if v==True and isinstance(v,bool):     return 'true'
    if v==False and isinstance(v,bool):    return 'false'
    if v==None:     return 'null'

    
    if isinstance(v,int) or isinstance(v,float):        return unicode(v)
    if isinstance(v,unicode):                           return convertStringToJson(v)
    if isinstance(v,list):                              return convertListToJson(v)
    if isinstance(v,dict):                              return convertDictToJson(v)
    

    
    print "ERROR:convertValueToJson()"

def deepCopy(v):
    if not isinstance(v,list) and not isinstance(v,dict):
        if isinstance(v,str): return unicode(v,CODEC)
        else:return v
    if isinstance(v,list):
        resultList=[]
        for e in v:
            resultList.append(deepCopy(e))
        return resultList
    if isinstance(v,dict):
        resultDict={}
        for key in v.keys():
            resultDict[key]=deepCopy(v[key])
        return resultDict
if isDebug:
    print "deepCopy():"
    d={"a":"b","c":[100,200]}
    print id(d["c"])
    b=deepCopy(d)
    print id(b["c"])
    c=d
    print id(c["c"])
    print "----\n"

    
class JsonParser:
    'Json 解析'
    def __init__(self):
        self.dic={}
    def load(self,s):
        if isDebug:print "DEBUG:load(",s,")-begin"
        
        if not isinstance(s,unicode): s=s.decode(CODEC)
        
        if isDebug:print "DEBUG:load(",s,")-begin"
        #try:
        self.dic,num=getObject(s)
    def dump(self):
        if isDebug:print "DEBUG:dump(",self.dic,")-begin"
        return convertDictToJson(self.dic)
    def loadJson(self,f):
        if isDebug:print "DEBUG:loadJson(",f,")-begin"
        try:
            fp=open(f,'r')
        except IOError,args:
            raise IOError,'File operation error:'+f
        data=[line.strip() for line in fp.readlines()]
        fp.close
        s=""
        for e in data:
            s+=e
        JsonParser.load(self,s)
    def  dumpJson(self,f):
        if isDebug:print "DEBUG:dumpJson(",f,")-begin"
        try:
            fp=open(f,'w')
        except IOError,args:
            raise IOError,'File operation error:'+f
        s=JsonParser.dump(self)
        fp.write(s.encode(CODEC))
        fp.close
    def loadDict(self,d):
        for key in d.keys():
            if isinstance(key,str) or isinstance(key,unicode):
                if isinstance(key,str): key=unicode(key,CODEC)
                self.dic[key]=deepCopy(d[key])
    def dumpDict(self):
        newDic=deepCopy(self.dic)
        return newDic
    def __setitem__(self,key,value):
        self.dic[key]=deepCopy(value)
    def __getitem__ (self,key):
        return deepCopy(self.dic[key])
    def update(self,d):
        for key in d.keys():
            self.dic[key]=deepCopy(d[key])



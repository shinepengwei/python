# -*- coding: utf-8 -*-


import string
CODEC='utf-8'
isDebug=False
zhuanyiChar='\\'
charToZhuanYi={'\"':'"','\\':'\\','\b':'b','\f':'f','\n':'n','\r':'r','\t':'t'}
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
def dealIgnoreChar(string,curIndex):
    '解析文本时，当在value类型的前面和后面出现的空格、换行符和制表符，需要忽略'
    while string[curIndex] in ignoreChar: curIndex+=1#效率不高，可以改为set或者frozenset
    return curIndex
    
def getString(string):
    if isDebug: print "DEBUG:getString(",string,") - Begin"
    '''对于json字符串，返回string前面的string类型，并且返回string类型结束的索引。'''
    curIndex=0#只处理前面的空格，不处理后面的
    curIndex=dealIgnoreChar(string,curIndex)
    #while string[curIndex] in ignoreChar: curIndex+=1
    if string[curIndex] != '"':
        raise ValueError, "Error: getString(), not a string:"+string
    curIndex+=1
    zhuanYiFlag=False
    resultStr=unicode("")
    end=0
    while curIndex<len(string):##每次循环都计算一次string长度。
        c=string[curIndex]
        i=curIndex
        curIndex+=1
        if zhuanYiFlag:
            zhuanYiFlag=False
            if c=='u':
                unistr=string[curIndex:curIndex+4]
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
    if isDebug:print "DEBUG:getString(",string,"):",resultStr,end+1
    return resultStr,curIndex

def getObject(string):
    if isDebug:print "DEBUG:getObject(",string,") - Begin"
    dic={}
    curIndex=0
    curIndex=dealIgnoreChar(string,curIndex)
    if string[curIndex]!='{':
        raise ValueError, "Error: getObject(), not a Object:no {,:"+string
    curIndex+=1
    curIndex=dealIgnoreChar(string,curIndex)
    if string[curIndex]=='}':
        return dic,curIndex+1
    while True:
        key,index=getString(string[curIndex:])
        curIndex+=index
        curIndex=dealIgnoreChar(string,curIndex)
        if string[curIndex]!=':':
            raise ValueError,  "ERROR: getObject: have no ':',:"+string
        curIndex+=1
        value,index=getValue(string[curIndex:])
        curIndex+=index
        dic[key]=value
        curIndex=dealIgnoreChar(string,curIndex)
        if string[curIndex]!=",":
            break
        curIndex+=1
    curIndex=dealIgnoreChar(string,curIndex)
    if string[curIndex]!='}':
        raise ValueError,  "ERROR: getObject(): have no '}',:"+string
    return dic,curIndex+1

def getArray(string):
    if isDebug:print "DEBUG:getArray(",string,") - Begin"
    arr=[]
    curIndex=0
    curIndex=dealIgnoreChar(string,curIndex)
    if string[curIndex]!='[':
        raise ValueError,  "ERROR: getArray(),:"+string
    curIndex+=1
    curIndex=dealIgnoreChar(string,curIndex)
    if string[curIndex]==']':
        return arr,curIndex+1
    while True:
        value,index=getValue(string[curIndex:])
        arr.append(value)
        curIndex+=index
        curIndex=dealIgnoreChar(string,curIndex)
        if string[curIndex]!=",":
            break
        curIndex=dealIgnoreChar(string,curIndex)
        curIndex+=1
    curIndex=dealIgnoreChar(string,curIndex)
    if string[curIndex]!=']':
        raise ValueError,  "ERROR: getArray(): have no ']',:"+string
    return arr,curIndex+1

def getNumber(string):
    if isDebug:print "DEBUG:getNumber(",string,") - Begin"
    curIndex=0
    beginIndex=0
    curIndex=dealIgnoreChar(string,curIndex)
    isFloat=False
    while beginIndex+curIndex<len(string) and string[beginIndex+curIndex] in "+-0123456789.eE":
        if string[beginIndex+curIndex] in '.Ee' : isFloat=True
        curIndex+=1
    if isFloat:
        number=float(string[beginIndex:beginIndex+curIndex])
        if number==float('inf'):
            raise ValueError,"number:"+string[beginIndex:beginIndex+curIndex]+" out of range range"
    else:
        number=int(string[beginIndex:beginIndex+curIndex])
    if isDebug:print "DEBUG:getNumber(",string,"):",number,beginIndex+curIndex
    return number,beginIndex+curIndex


def getKeywords(string):
    if isDebug:print "DEBUG:getKeywords(",string,") - Begin"
    curIndex=0
    curIndex=dealIgnoreChar(string,curIndex)
    
    if string.find("true",curIndex,curIndex+4)!=-1:
        if isDebug:print "DEBUG:getKeywords(",string,")",True,curIndex+4
        return True,curIndex+4
    if string.find("false",curIndex,curIndex+5)!=-1:
        if isDebug:print "DEBUG:getKeywords(",string,")",False,curIndex+5
        return False,curIndex+5
    if string.find("null",curIndex,curIndex+4)!=-1:
        if isDebug:print "DEBUG:getKeywords(",string,")",None,curIndex+4
        return None,curIndex+4
    raise ValueError,  "ERROR:getKeywords():not a keyword,:"+string
    
    
def getValue(string):
    value=None
    curIndex=0
    curIndex=dealIgnoreChar(string,curIndex)
    if string[curIndex]=='{':
        value,index=getObject(string[curIndex:])
        if isDebug: print "DEBUG:getValue(),getObject:",value,index
    elif string[curIndex]=='[':
        value,index=getArray(string[curIndex:])
        if isDebug:print "DEBUG:getValue(),getArray:",value,index
    elif string[curIndex]=='"':
        value,index=getString(string[curIndex:])
        if isDebug:print "DEBUG:getValue(),getString:",value,index
    elif string[curIndex] in "+-0123456789":
        value,index=getNumber(string[curIndex:])
        if isDebug:print "DEBUG:getValue(),getNumber:",value,index
    else:
        value,index=getKeywords(string[curIndex:])
        if isDebug:print "DEBUG:getValue(),getKeywords:",value,index
    return value,curIndex+index


def convertStringToJson(s):
    '''
    将字符串转换为识别的字符串，
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
    '深拷贝 '   
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
def isValue(v):
    '判断python对象v是否可转为符合json格式的value值，用于更新类数据操作，当不符合格式时，不更新'
    if isinstance(v,str) or isinstance(v,unicode) or isinstance(v,int)\
       or isinstance(v,float)  or isinstance(v,bool)  or v==None:
        return True

    if isinstance(v,list):
        for e in v:
            if not isValue(e):
                return False
        return True
    if isinstance(v,dict):
        for key in v.keys():
            if not isValue(v[key]):
                return False
        return True


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
        if isValue(value):
            self.dic[key]=deepCopy(value)
    def __getitem__ (self,key):
        return deepCopy(self.dic[key])
    def update(self,d):
        for key in d.keys():
            if isValue(d[key]):
                self.dic[key]=deepCopy(d[key])

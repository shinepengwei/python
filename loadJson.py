# -*- coding: cp936 -*-

import string
CODEC='gb2312'
isDebug=True
zhuanyiChar='\\'
charToZhuanYi={'\"':'"','\\':'\\','\b':'b','\f':'f','\n':'n','\r':'r','\t':'t','\u':'u'}
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
    if c=='u':return '\u'
    print "ERROR:dealZhuanyi(), not a zhuanyi char"
    return None

def getString(str):
    if isDebug: print "DEBUG:getString(",str,") - Begin"
    '''对于json字符串，返回str前面的string类型，并且返回string类型结束的索引。'''
    curIndex=0#只处理前面的空格，不处理后面的
    while str[curIndex]==" ": curIndex+=1
    if str[curIndex] != '"':
        print "ERR: getString(), not a string"
    curIndex+=1
    zhuanYiFlag=False
    resultStr=""
    end=0
    while curIndex<len(str):
        c=str[curIndex]
        i=curIndex
        curIndex+=1
        if zhuanYiFlag:
            zhuanYiFlag=False
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
    
    resultStr=resultStr.decode(CODEC)
    
    # not isinstance(resultStr,unicode): resultStr=unicode(resultStr)
    if isDebug:print "DEBUG:getString(",str,"):",resultStr,end+1
    return resultStr,curIndex

def getObject(str):
    if isDebug:print "DEBUG:getObject(",str,") - Begin"
    dic={}
    curIndex=0
    while str[curIndex]==" ": curIndex+=1
    if str[curIndex]!='{':
        print "ERROR:no {"
    curIndex+=1
    while True:
        key,index=getString(str[curIndex:])
        curIndex+=index
        while str[curIndex]==" ": curIndex+=1
        if str[curIndex]!=':':
            print "ERROR: getObject: have no ':'"
        curIndex+=1
        value,index=getValue(str[curIndex:])
        curIndex+=index
        dic[key]=value
        while str[curIndex]==" ": curIndex+=1
        if str[curIndex]!=",":
            break
        curIndex+=1
    while str[curIndex]==" ": curIndex+=1
    if str[curIndex]!='}':
        print "ERROR: getObject(): have no '}'"
    return dic,curIndex+1

def getArray(str):
    if isDebug:print "DEBUG:getArray(",str,") - Begin"
    arr=[]
    curIndex=0
    while str[curIndex]==" ": curIndex+=1
    if str[curIndex]!='[':
        print "ERROR: getArray()"
    curIndex+=1
    while True:
        value,index=getValue(str[curIndex:])
        arr.append(value)
        curIndex+=index
        while str[curIndex]==" ": curIndex+=1
        if str[curIndex]!=",":
            break
        while str[curIndex]==" ": curIndex+=1
        curIndex+=1
    while str[curIndex]==" ": curIndex+=1
    if str[curIndex]!=']':
        print "ERROR: getArray(): have no ']'"
    return arr,curIndex+1

def getNumber(str):
    if isDebug:print "DEBUG:getNumber(",str,") - Begin"
    curIndex=0
    beginIndex=0
    while str[beginIndex]==" ": beginIndex+=1
    while beginIndex+curIndex<len(str) and str[beginIndex+curIndex] in "+-0123456789.eE":
        curIndex+=1
    number=string.atof(str[beginIndex:beginIndex+curIndex])
    if isDebug:print "DEBUG:getNumber(",str,"):",number,beginIndex+curIndex
    return number,beginIndex+curIndex
print getNumber("  234")
def getKeywords(str):
    if isDebug:print "DEBUG:getKeywords(",str,") - Begin"
    curIndex=0
    while str[curIndex]==" ": curIndex+=1
    
    if str.find("true",curIndex,curIndex+4)!=-1:
        if isDebug:print "DEBUG:getKeywords(",str,")",True,curIndex+4
        return True,curIndex+4
    if str.find("false",curIndex,curIndex+5)!=-1:
        if isDebug:print "DEBUG:getKeywords(",str,")",False,curIndex+5
        return False,curIndex+5
    if str.find("null",curIndex,curIndex+4)!=-1:
        if isDebug:print "DEBUG:getKeywords(",str,")",None,curIndex+4
        return None,curIndex+4
    if isDebug:print "ERROR:getKeywords():not a keyword"
    
    
def getValue(str):
    value=None
    curIndex=0
    while str[curIndex]==" ": curIndex+=1
    if str[curIndex]=='{':
        value,index=getObject(str)
        if isDebug: print "DEBUG:getValue(),getObject:",value,index
    elif str[curIndex]=='[':
        value,index=getArray(str)
        if isDebug:print "DEBUG:getValue(),getArray:",value,index
    elif str[curIndex]=='"':
        value,index=getString(str)
        if isDebug:print "DEBUG:getValue(),getString:",value,index
    elif str[curIndex] in "+-0123456789":
        value,index=getNumber(str)
        if isDebug:print "DEBUG:getValue(),getNumber:",value,index
    else:
        value,index=getKeywords(str)
        if isDebug:print "DEBUG:getValue(),getKeywords:",value,index
    return value,index


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
    for e in l:
        strR=strR+convertValueToJson(e)+','
    strR=strR[:-1]
    strR+=']'
    if isDebug:print "DEBUG:convertListToJson(",l,")",strR
    return strR

def convertDictToJson(d):
    if isDebug:print "DEBUG:convertDictToJson(",d,")-begin"
    strResult="{"
    for key in d.keys():
        strResult+=convertStringToJson(key)+":"+convertValueToJson(d[key])+","
    strResult=strResult[:-1]
    strResult+="}"
    if isDebug:print "DEBUG:convertDictToJson(",d,"):",strResult
    return strResult
    
def convertValueToJson(v):

    if isDebug:print "DEBUG:convertValueToJson(",v,")-begin",type(v)
    if v==True:     return 'true'
    if v==False:    return 'false'
    if v==None:     return 'null'

    
    if isinstance(v,int) or isinstance(v,float):        return unicode(v)
    if isinstance(v,unicode):                           return convertStringToJson(v)
    if isinstance(v,list):                              return convertListToJson(v)
    if isinstance(v,dict):                              return convertDictToJson(v)
    

    
    print "ERROR:convertValueToJson()"
    
class JsonParser:
    'Json 解析'
    def __init__(self):
        self.dic={}
    def load(self,s):
        if isDebug:print "DEBUG:load(",s,")-begin"
        self.dic,num=getObject(s)
    def dump(self):
        if isDebug:print "DEBUG:dump(",self.dic,")-begin"
        return convertDictToJson(self.dic)
    def loadJson(self,f):
        if isDebug:print "DEBUG:loadJson(",f,")-begin"
        fp=open(f,'r')
        print fp.encoding
        data=[line.strip() for line in fp.readlines()]
        fp.close
        print data
        s=""
        for e in data:
            s+=e
        print s
        JsonParser.load(self,s)

print len(' "s"')
print getString(' "s"')

print len('"s"')
print getString('"s"')

str4 =r'[1,3,"dd"]'
print getValue(str4)
str4 =r'[1,3, "dd" ]'
print getValue(str4)




   
str1='"我"'
print getString(str1)

str2=r'2334.55'
print getValue(str2)
str3=r"null"
print getValue(str3)
print "\n"
str4 =r'[1,3, "dd"]'
print getValue(str4)
print '\n'
str5 = r'{"a":   234,   "b":   null}'
print getObject(str5)

print '\n'
str = '{"中文"   :[   "1\\"\\r23","abc",   true,{"b":"ca"}],"b":null  }   '
print type(str)
dic,index=getObject(str)
print dic
print dic.keys()[0]

print "\n\n______________________________"
str="中文2"
print str
print str.decode(CODEC)
print unicode(str,CODEC)
print type(str.decode(CODEC))
#for i in range(1,len(str)):
    

str = '   {     "中文" : [   "1\\r23"    ,   "abc\\\\"     ,     true ,   {   "b"   :   "ca"   }   ]   ,   "b"   :   null}   '
a1 = JsonParser()
a1.loadJson("json.txt")
s=a1.dump()
print "a1.dump():",s
a1.load(str)
print "\n\n\na1.dump():"
print a1.dump()
str='cc\bc'
print str
print convertStringToJson(str)

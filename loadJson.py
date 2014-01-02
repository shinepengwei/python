# -*- coding: cp936 -*-
import string
isDebug=True
zhuanyiChar='\\'
def getString(str):
    if isDebug: print "DEBUG:getString(",str,") - Begin"
    '''对于json字符串，返回str前面的string类型，并且返回string类型结束的索引。'''
    if str[0] != '"':
        print "ERR: getString(), not a string"
    zhuanYiFlag=False
    end=0
    for i , c in enumerate(str):
        if zhuanYiFlag:
            zhuanYiFlag=False
            continue
        if c==zhuanyiChar:
            zhuanYiFlag=True
            continue
        if i!=0 and c=='"':
            end=i
            break
    if isDebug:print "DEBUG:getString(",str,"):",str[0:end+1],end+1
    return str[1:end],end+1
def getObject(str):
    if isDebug:print "DEBUG:getObject(",str,") - Begin"
    dic={}
    if str[0]!='{':
        print "ERROR:no {"
    curIndex=1
    while True:
        key,index=getString(str[curIndex:])
        curIndex+=index
        if str[curIndex]!=':':
            print "ERROR: getObject: have no ':'"
        curIndex+=1
        value,index=getValue(str[curIndex:])
        curIndex+=index
        dic[key]=value
        if str[curIndex]!=",":
            break
        curIndex+=1
    if str[curIndex]!='}':
        print "ERROR: getObject(): have no '}'"
    return dic,curIndex+1
def getArray(str):
    if isDebug:print "DEBUG:getArray(",str,") - Begin"
    arr=[]
    if str[0]!='[':
        print "ERROR: getArray()"
    curIndex=1
    while True:
        value,index=getValue(str[curIndex:])
        arr.append(value)
        curIndex+=index
        if str[curIndex]!=",":
            break
        curIndex+=1
    if str[curIndex]!=']':
        print "ERROR: getArray(): have no ']'"
    return arr,curIndex+1
def getNumber(str):
    if isDebug:print "DEBUG:getNumber(",str,") - Begin"
    curIndex=0
    while curIndex<len(str) and str[curIndex] in "+-0123456789.eE":
        curIndex+=1
    number=string.atof(str[:curIndex])
    if isDebug:print "DEBUG:getNumber(",str,"):",number,curIndex
    return number,curIndex
def getKeywords(str):
    if isDebug:print "DEBUG:getKeywords(",str,") - Begin"
    if str.find("true",0,4)!=-1:
        if isDebug:print "DEBUG:getKeywords(",str,")",True,4
        return True,4
    if str.find("false",0,4)!=-1:
        if isDebug:print "DEBUG:getKeywords(",str,")",False,5
        return False,5
    if str.find("null",0,4)!=-1:
        if isDebug:print "DEBUG:getKeywords(",str,")",None,4
        return None,4
    if isDebug:print "ERROR:getKeywords():not a keyword"
    
    
def getValue(str):
    value=None
    index=-1
    if str[0]=='{':
        value,index=getObject(str)
        if isDebug: print "DEBUG:getValue(),getObject:",value,index
    elif str[0]=='[':
        value,index=getArray(str)
        if isDebug:print "DEBUG:getValue(),getArray:",value,index
    elif str[0]=='"':
        value,index=getString(str)
        if isDebug:print "DEBUG:getValue(),getString:",value,index
    elif str[0] in "+-0123456789":
        value,index=getNumber(str)
        if isDebug:print "DEBUG:getValue(),getNumber:",value,index
    else:
        value,index=getKeywords(str)
        if isDebug:print "DEBUG:getValue(),getKeywords:",value,index
    return value,index
        
def load(str):
    length=len(str)
    dic=getObject(str)
    
     
str1=r'"\"f"kk'
print getString(str1)

str2=r'2334.55'
print getValue(str2)
str3=r"null"
print getValue(str3)
print "\n"
str4 =r'[1,3,"dd"]'
print getValue(str4)
print '\n'
str5 = r'{"a":234,"b":null}'
print getObject(str5)

print '\n'
str = r'{"a":[123,"a\"bc",true,{"b":"ca"}],"b":null}'
print getObject(str)
#for i in range(1,len(str)):
    


# -*- coding: utf-8 -*-

from JsonParser import JsonParser 
test_json_str=r'''
{
"root":
[
	"JSON Test Pattern pass1",
	{"object with 1 member":["array with 1 element"]},
	{},
	[],
	-42,
	true,
	false,
	null,
	{
	"chinese":"中文",
		"integer": 1234567890,
		"real": -9876.543210,
		"e": 0.123456789e-12,
		"E": 1.234567890E+34,
		"zero": 0,
		"one": 1,
		"space": " ",
		"quote": "\"",
		"backslash": "\\",
		"controls": "\b\f\n\r\t",
		"slash": "/ & \/",
		"alpha": "abcdefghijklmnopqrstuvwyz",
		"ALPHA": "ABCDEFGHIJKLMNOPQRSTUVWYZ",
		"digit": "0123456789",
		"special": "`1~!@#$%^&*()_+-={':[,]}|;.</>?",
		"hex": "\u0123\u4567\u89AB\uCDEF\uabcd\uef4A",
		"true": true,
		"false": false,
		"null": null,
		"array":[  ],
		"object":{  },
		"address": "50 St. James Street",
		"url": "http://www.JSON.org/",
		"comment": "// /* <!-- --",
		"# -- --> */": " ",
		" s p a c e d " :[1,2 , 3

			,

			4 , 5        ,          6           ,7        ],
		"compact": [1,2,3,4,5,6,7],
		"jsontext": "{\"object with 1 member\":[\"array with 1 element\"]}",
		"quotes": "&#34; \u0022 %22 0x22 034 &#x22;",
		"\/\\\"\uCAFE\uBABE\uAB98\uFCDE\ubcda\uef4A\b\f\n\r\t`1~!@#$%^&*()_+-=[]{}|;:',./<>?"
		: "A key can be any string"
	},
	0.5 ,98.6
	,
	99.44
	,

	1066


	,"rosebud"]
}'''


test_dict={u'root': [u'JSON Test Pattern pass1', {u'object with 1 member': [u'array with 1 element']}, {}, [], -42, True, False, None, {u'comment': u'// /* <!-- --', u'false': False, u'chinese': u'\u4e2d\u6587', u'backslash': u'\\', u'one': 1, u'quotes': u'&#34; " %22 0x22 034 &#x22;', u'zero': 0, u'alpha': u'abcdefghijklmnopqrstuvwyz', u'array': [], u'# -- --> */': u' ', u'special': u"`1~!@#$%^&*()_+-={':[,]}|;.</>?", u'compact': [1, 2, 3, 4, 5, 6, 7], u'null': None, u'space': u' ', u'hex': u'\u0123\u4567\u89ab\ucdef\uabcd\uef4a', u'controls': u'\x08\x0c\n\r\t', u'slash': u'/ & /', u'real': -9876.54321, u'digit': u'0123456789', u'E': 1.23456789e+34, u'quote': u'"', u'object': {}, u'/\\"\ucafe\ubabe\uab98\ufcde\ubcda\uef4a\x08\x0c\n\r\t`1~!@#$%^&*()_+-=[]{}|;:\',./<>?': u'A key can be any string', u'address': u'50 St. James Street', u'integer': 1234567890, u'true': True, u'e': 1.23456789e-13, u'url': u'http://www.JSON.org/', u'jsontext': u'{"object with 1 member":["array with 1 element"]}', u' s p a c e d ': [1, 2, 3, 4, 5, 6, 7], u'ALPHA': u'ABCDEFGHIJKLMNOPQRSTUVWYZ'}, 0.5, 98.6, 99.44, 1066, u'rosebud']}
file_path="data.txt"
a1 = JsonParser()
a2 = JsonParser()
a3 = JsonParser()

a1.load(test_json_str)
print 'a1.dump():\n',a1.dump()
d1=a1.dumpDict()
print 'd1:\n',d1

print 'test_dict:\n',test_dict
assert test_dict==d1

a2.loadDict(d1)
assert id(a2["root"])!=id(d1["root"])

a2.dumpJson(file_path)
a3.loadJson(file_path)
d3 = a3.dumpDict()
print 'd3:\n',d3
assert d1==d3

d4={"root":2,"a":3}
a3.update(d4)
a2["root"]=2
a2["a"]=3
print 'a3.dump():\n',a3.dump()
print 'a2.dump():\n',a2.dump()


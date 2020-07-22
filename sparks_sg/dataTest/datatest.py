
'''
this py. file show how to call a function with string var
'''

def aaa() :
    print "aaa"


def bbb():
    print "bbb"


flist = ["aaa", "bbb"]

for i in flist:
    eval(i)()
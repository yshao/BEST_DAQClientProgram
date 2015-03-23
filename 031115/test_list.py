a=['']+['a','b']
b=['']+['']
# a.remove()
print set(a)
c=list(set(b))
print c[0],len(c)
if c[0] == '' and len(c) == 1:
    print 'h'
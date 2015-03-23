import itertools
list1=['a','b','c','d']
list2=['x','y','o1']
list1=['X']
list2=['A','B']
if len(list1) < len(list2):
    combo=[zip(list1[0],x) for x in list2]
else:
    combo=[zip(x,list2) for x in itertools.permutations(list1,len(list2))]


### fliprule ###

### addrule ###

# print combo
# NumObjectRule()
# numdiff=f1.num - f2.num
# if numdiff > 0:
# elif numdiff == 0:
#     ""
# if numdiff < 0:
#     abs(numdiff)

#     f1.add(numdiff)

# for pairing in combo:
#     mea=0
#     for p in pairing:
#         mea=mea+analysis(p[0],p[1])

print combo
l=[]
l.append((1.2,('a','b')))
l.append((1.3,('a','b')))
l.append((1.1,('a','b')))

print l

print sorted(l)

from operator import itemgetter
# mylist = sorted(d, key=itemgetter('name', 'age'))


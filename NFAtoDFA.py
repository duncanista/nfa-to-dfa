import re
from collections import defaultdict
from itertools import chain, combinations

##Power set function taken from itertools recipes
def powerset(iterable):
    "list(powerset([1,2,3])) --> [(), (1,), (2,), (3,), (1,2), (1,3), (2,3), (1,2,3)]"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

nfaInput = "{(0,p,p),(0,p,q),(1,p,p),(0,q,r),(1,q,r),(0,r,s),(0,s,s),(1,s,s)}"

nfaInput = re.findall('\(([^)]+)',nfaInput)

transitionList = []
for transition in nfaInput:
    transitionList.append(transition.split(","))

##Creando la lista de Q para el NFA
nfaQ = [element for sublist in transitionList for element in sublist]
nfaQ = list(set(nfaQ))
if '0' in nfaQ:
    nfaQ.remove('0')
if '1' in nfaQ:
    nfaQ.remove('1')
if '_' in nfaQ:
    nfaQ.remove('_')
nfaQ.sort()

dfaQ = []
for q in powerset(nfaQ):
    dfaQ.append(list(q))


nfaDelta = defaultdict(list)
entry = ''
for entry,origin,target in transitionList:
    if entry == '0':
        index = 0
    elif entry == '1':
        index = 1
    else:
        entry = 2

    if origin not in nfaDelta:
        nfaDelta[origin] = [[],[]]

    nfaDelta[origin][index].append(target)

print(nfaDelta)

resultList = []

for q in dfaQ: #por cada subset de Q
    result = [q, [],[]]
    for state in q: #para cada Q del NFA en el subset de Q del DFA
        for i in nfaDelta[state][0]:
            result[1].append(i)
        for i in nfaDelta[state][1]:
            result[2].append(i)
        result[1] = list(set(result[1]))
        result[2] = list(set(result[2]))
        result[1].sort()
        result[2].sort()
    resultList.append(result)

formattedResult = [["Q", "0", "1"]]
for line in resultList:
    newLine = []
    for element in line:
        if element == []:
            new = "{/}"
        else:
            new = "{" + ", ".join(element) + "}"
        newLine.append(new)
    formattedResult.append(newLine)



frmt = '{:20}' + 2 * '{:20}'
for line in formattedResult:
    print(frmt.format(*line))

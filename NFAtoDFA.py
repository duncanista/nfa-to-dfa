# coding: utf-8
import re
from tkinter import *
from tkinter import filedialog
from collections import defaultdict
from itertools import chain, combinations

## Power set function taken from itertools recipes
def powerset(iterable):
    "list(powerset([1,2,3])) --> [(), (1), (2), (3), (1,2), (1,3), (2,3), (1,2,3)]"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

## Retrieve NFA given its transitions
def getTransitions(nfa):
    transitions = []
    for transition in nfa:
        transitions.append(transition.split(","))
    return transitions

## Get the NFA states
def getNFAStates(transitions):
    Q = [element for sublist in transitions for element in sublist]
    Q = list(set(Q))
    if '0' in Q:
        Q.remove('0')
    if '1' in Q:
        Q.remove('1')
    if '_' in Q:
        Q.remove('_')
    Q.sort()

    return Q

## Get the DFA final states given the NFA states
def getDFAStates(nfaQ):
    Q = []
    for q in powerset(nfaQ):
        Q.append(list(q))

    return Q

## NFA delta given its transitions
def getNFADelta(transitions):
    delta = defaultdict(list)
    for entry, origin, target in transitions:
        index = 0
        if entry == '0':
            index = 0
        elif entry == '1':
            index = 1

        if origin not in delta:
            delta[origin] = [[], []]

        delta[origin][index].append(target)

    return delta

## DFA delta given its states, and the NFA delta
def getDFADelta(Q, nfaDelta):
    delta = []

    # for every Q subset
    for q in Q:
        result = [q, [], []]
        # for every NFA Q in the subset of Q in the DFA
        for state in q:
            for i in nfaDelta[state][0]:
                result[1].append(i)
            for i in nfaDelta[state][1]:
                result[2].append(i)
            result[1] = list(set(result[1]))
            result[2] = list(set(result[2]))
            result[1].sort()
            result[2].sort()
        delta.append(result)

    return delta

## Set NFA final state as the last element thats being pointed in the raw input
def getNFAFinal(nfa):
    last = nfa[-1]
    last = last.split(",")[-1]
    return last

## Calculate the DFA final states by checking if the NFA final is in both zero and one from delta.
def getDFAFinal(final, delta):
    finalStates = []
    for state, zero, one  in delta:
        if final in zero and final in one:
            finalStates.append(state)
    return finalStates

def formatStates(Q):
    cardinality = len(Q[0])
    f = "\t"
    for q in Q:
        if len(q) > cardinality:
            f += "\n\t"
            cardinality = len(q)
        f += "{" + ", ".join(q) + "}, "
    f = f[:-2]
    return f

def formatDelta(delta):
    result = [["Q", "0", "1"]]
    for line in delta:
        newLine = []
        for element in line:
            if element == []:
                new = "{/}"
            else:
                new = "{" + ", ".join(element) + "}"
            newLine.append(new)
        result.append(newLine)

    return result

def getNFA(file):
    return re.findall('\(([^)]+)', file)

def getFile():
    path = filedialog.askopenfilename(filetypes=(("Text files", "*.txt"), ("all files", "*.*")))
    file = open(path, 'r').read()
    return file

def convert():
    global app
    file = getFile()
    nfaInput = getNFA(file)
    getNFAFinal(nfaInput)

    transitions = getTransitions(nfaInput)

    nfaQ = getNFAStates(transitions)
    nfaDelta = getNFADelta(transitions)
    nfaFinal = getNFAFinal(nfaInput)

    dfaQ = getDFAStates(nfaQ)
    dfaQo = nfaQ[0]
    dfaDelta = getDFADelta(dfaQ, nfaDelta)
    dfaFinal = getDFAFinal(nfaFinal, dfaDelta)
    dfaFormatDelta = formatDelta(dfaDelta)

    new = open('result.txt', 'w+')
    new.write("=" * 60)
    new.write("\nDefinición formal del DFA convertido.\n\nN = {Q, E, d, Qo, F} \n\n")
    new.write("Q = { \n" + formatStates(dfaQ) + "\n}\n\n")
    new.write("E = {0, 1}\n\n")
    new.write("Qo = " + dfaQo + "\n\n")
    new.write("F = { \n" + formatStates(dfaFinal) + "\n}\n\n")
    new.write("d = { \n")

    frmt = '{:20}' + 2 * '{:20}'
    for line in dfaFormatDelta:
        new.write("\t" + (frmt.format(*line)) + "\n")

    new.write("}")

    result = Label(app, text="Se creó un archivo con la definición formal.", font = ("Arial", 14))
    result.grid(pady=5, row=2, column=0)

def main():
    global app
    app = Tk()
    app.title("NFA to DFA application.")
    label = Label(app, text="Busque el archivo donde tiene su NFA y desea convertir a DFA.", font=("Arial", 14))
    button = Button(app, text="Seleccionar archivo...", command=convert)

    label.grid(pady=5, row=0, column=0)
    button.grid(pady=5, row=1, column=0)
    app.mainloop()

global app
main()





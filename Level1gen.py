import itertools
import random
import os
import json


### BLOCK FORMATS ###
strFormat = '<l>{}</l>'
boolFormatTrue = '<block s="reportBoolean"><l><bool>true</bool></l></block>'
boolFormatFalse = '<block s="reportBoolean"><l><bool>false</bool></l></block>'
emptyBoolFormat = '<bool>{}</bool>'

###HOF INPUT FORMATS###
emptyHOFfunc = "<script></script>"
notHOFfunc = '<autolambda><block s="reportNot"><l/></block></autolambda>'
andorOpformat = '<autolambda><block s="report{}"><block s="reportBoolean"><l><bool>{}</bool></l></block><l/></block></autolambda>'
boolHOFinputTrue = '<autolambda>' + boolFormatTrue + '</autolambda>'
boolHOFinputFalse = '<autolambda>' + boolFormatFalse + '</autolambda>'
andHOFfuncTrue = andorOpformat.format('And', 'true')
andHOFfuncFalse = andorOpformat.format('And', 'false')
orHOFfuncTrue = andorOpformat.format('Or', 'true')
orHOFfuncFalse = andorOpformat.format('Or', 'false')


##HOF TYPES

hoftypes = {"Map": ('"reportMap"', '"reifyReporter"'), "Keep":('"reportKeep"', '"reifyPredicate"') }

operations = [emptyHOFfunc,
              notHOFfunc,
              boolHOFinputFalse,
              boolHOFinputTrue,
              andHOFfuncFalse,
              andHOFfuncTrue,
              orHOFfuncFalse,
              orHOFfuncTrue]

bools = ['true', 'false']

'''
HOF Input Order
0: HOF 1
1: HOF 2
2: Operation
3-5: DATA inputs (booleans only)
#finaloutput = finalTemplate.format(notHOFfunc,boolHOFinput.format("true"), "true", "true", "true")
'''

with open("templates/mapTemplate.xml") as file:
	inputTemplate = file.read()

### GENERATING QUESTIONS ###

def generateQuestions():
    rawQuestions = []
    for typ in hoftypes:
        temp = [hoftypes[typ][0], hoftypes[typ][1]]
        otherlst = [operations[random.randint(0,7)],
                    bools[random.randint(0,1)],
                    bools[random.randint(0,1)],
                    bools[random.randint(0,1)]]
        empty = []
        for _ in range(len(otherlst)):
            empty.append(otherlst)
        rawResult = list(itertools.product(*empty))
        for result in rawResult:
            rawQuestions.append(temp + list(result))
    return rawQuestions

rawQuestions = generateQuestions()

#print("Number of Raw Questions: "+ str(len(rawQuestions)))

def pruneQuestions(lst):
    removes = []
    for question in lst:
        if question[2] not in operations:
            removes.append(question)
        if question[3] not in bools or question[4] not in bools or question[5] not in bools:
            removes.append(question)
    for item in removes:
        if item in lst:
            lst.remove(item)
    return lst

finalQuestions = pruneQuestions(rawQuestions)
#print("Number of pruned questions: " + str(len(finalQuestions)))

print("Number of questions generated: " + str(len(finalQuestions)))


'''
randomQuestion = finalQuestions[random.randint(0, 53)]
print(randomQuestion)

with open('return.xml', 'w') as object:
	output = inputTemplate.format(randomQuestion[0], 
                                  randomQuestion[1], 
                                  randomQuestion[2], 
                                  randomQuestion[3], 
                                  randomQuestion[4], 
                                  randomQuestion[5])
	object.write(output)
'''

def negate(lst):
    output = []
    for bool in lst:
        if bool == 'true':
            output.append('false')
        else:
            output.append('true')
    return output


###GENERATING ANSWERS###


def generateAnswers(lst):
    output = []
    for question in lst:
        answer = []
        if question[0] in hoftypes["Map"]:
            if question[2] == emptyHOFfunc:
                answer = question[3:]
                output.append([question, answer])
            elif question[2] == notHOFfunc:
                answer = negate(question[3:])
                output.append([question, answer])
            elif question[2] == boolHOFinputFalse:
                answer = ['false' for _ in range(3)]
                output.append([question, answer])
            elif question[2] == boolHOFinputTrue:
                answer = ['true' for _ in range(3)]
                output.append([question, answer])
            elif question[2] == andHOFfuncFalse:
                answer = ['false' for _ in range(3)]
                output.append([question, answer])
            elif question[2] == andHOFfuncTrue:
                answer = question[3:]
                output.append([question, answer])
            elif question[2] == orHOFfuncTrue:
                answer = ['true' for _ in range(3)]
                output.append([question, answer])
            elif question[2] == orHOFfuncFalse:
                answer = question[3:]
                output.append([question, answer])
        else:
            if question[2] == emptyHOFfunc:
                answer = []
                output.append([question, answer])
            elif question[2] == notHOFfunc:
                answer = [item for item in question[3:] if item == 'false']
                output.append([question, answer])
            elif question[2] == boolHOFinputFalse:
                answer = []
                output.append([question, answer])
            elif question[2] == boolHOFinputTrue:
                answer = question[3:]
                output.append([question, answer])
            elif question[2] == andHOFfuncFalse:
                answer = []
                output.append([question, answer])
            elif question[2] == andHOFfuncTrue:
                answer = [item for item in question[3:] if item == 'true']
                output.append([question, answer])
            elif question[2] == orHOFfuncTrue:
                answer = question[3:]
                output.append([question, answer])
            elif question[2] == orHOFfuncFalse:
                answer = [item for item in question[3:] if item == 'true']
                output.append([question, answer])
    return output


def answersdict(lst):
    output = {}
    count = 0
    for pair in lst:
        output["question" + str(count)] = pair
        count += 1
    return output

answers = generateAnswers(finalQuestions)
dict = answersdict(answers)



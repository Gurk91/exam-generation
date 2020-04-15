
import itertools
import random
import os
import json

with open("Q7XML.xml") as file:
	raw = file.read()

with open("mapTemplate.xml") as file2:
	finalTemplate = file2.read()



### BLOCK FORMATS ###
strFormat = '<l>{}</l>'
boolFormat = '<block s="reportBoolean"><l><bool>{}</bool></l></block>'

###HOF INPUT FORMATS###
emptyHOFfunc = "<script></script>"
notHOFfunc = '<autolambda><block s="reportNot"><l/></block></autolambda>'
boolHOFinput = '<autolambda>' + boolFormat + '</autolambda>'

'''
HOF Input Order
0-1 Map questions
2-4 DATA Array inputs (booleans only)
#finaloutput = finalTemplate.format(notHOFfunc,boolHOFinput.format("true"), "true", "true", "true")
'''


ops = [emptyHOFfunc, notHOFfunc, boolHOFinput]
boolStrs = [boolFormat.format("true"), boolFormat.format("false")]
bools = ["true", "false"]

templist = [ops[random.randint(0,2)],ops[random.randint(0,2)], bools[random.randint(0,1)], bools[random.randint(0,1)], bools[random.randint(0,1)]]

empty = []

for i in range(len(templist)):
	empty.append(templist)

rawResult = list(itertools.product(*empty))
print(len(rawResult))


def pruneBadQues(lst):
	removes = []
	for question in lst:
		if question[0] not in ops or question[1] not in ops:
			removes.append(question)
		if question[2] not in bools or question[3] not in bools or question[4] not in bools:
			removes.append(question)
	for item in removes:
		if item in lst:
			lst.remove(item)
	return lst

result = pruneBadQues(rawResult)
print(len(result))


sample = result[random.randint(0,107)]
print(sample)


with open('output.xml', 'w') as obj:
	finaloutput = finalTemplate.format(sample[0], sample[1], sample[2], sample[3], sample[4])
	obj.write(finaloutput)



##GENERATE ANSWERS




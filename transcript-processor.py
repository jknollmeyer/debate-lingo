# scrapes a raw transcript to get each candidates sentences
import operator

transcript = open("raw_transcript.txt", 'r')

candidateList = ["SANDERS", "CLINTON"]

speechList = dict()
wordDict = dict()
wordList = dict()
relFreqList = dict()
for candidate in candidateList:
    wordDict[candidate] = dict()
    speechList[candidate] = []
    wordList[candidate] = []
    relFreqList[candidate] = []


# speechList = {"SANDERS": [], "CLINTON": []}
# wordDict = {"SANDERS": {}, "CLINTON": {}}
# wordList = {"SANDERS": [], "CLINTON": []}
# relFreqList = {"SANDERS": [], "CLINTON": []}

totalDict = {}
totalWords = 0

for line in transcript.readlines():

    # check to see if the first word denotes a speaker
    firstWord = line.split(' ', 1)[0]

    if firstWord[-1] == ':':

        # indicate who is now speaking
        currentSpeaker = firstWord[:-1]
        line = line.split(' ', 1)[1]

    if currentSpeaker == "SANDERS" or currentSpeaker == "CLINTON":
        speechList[currentSpeaker].append(line.translate(None, ",.!?\n"))


candidateList = [x for x in speechList.keys() if x != "total"]
for candidate in candidateList:

    for sentence in speechList[candidate]:

        if sentence != '':
            for word in sentence.split(' '):
                if word.isspace():
                    pass
                elif word in wordDict[candidate].keys():
                    wordDict[candidate][word] += 1
                else:
                    wordDict[candidate][word] = 1

    # convert word dictionary to list of tuples so we can sort it
    wordList[candidate] = sorted(wordDict[candidate].items(),
                                 key=operator.itemgetter(1))
    for pair in wordList[candidate]:
        totalWords += pair[1]
        if pair[0] in totalDict.keys():
            totalDict[pair[0]] += pair[1]
        else:
            totalDict[pair[0]] = pair[1]


for candidate in candidateList:
    wordList[candidate][:] = [(x[0], x[1], float(x[1])/totalDict[x[0]])
                              for x in wordList[candidate]]
    wordList[candidate] = sorted(wordList[candidate],
                                 key=operator.itemgetter(1))

    wordList[candidate] = sorted(wordList[candidate],
                                 key=operator.itemgetter(2))

# wordList format: tuple(word, frequency, relfrequency, refrequency of total)
print "SANDERS"
for pair in wordList["SANDERS"]:
    if pair[1] > 5 and pair[2] > 0.8:
        print pair[0] + "  " + str(pair[1]) + " " + str(pair[2])

print "\n\n\n\nCLINTON"
for pair in wordList["CLINTON"]:
    if pair[1] > 5 and pair[2] > 0.8:
        print pair[0] + "  " + str(pair[1]) + " " + str(pair[2])

# scrapes a raw transcript to get each candidates sentences
import operator
import os
import sys

party = sys.argv[1]

if party == "dem":
    directory = "dem_transcripts"
    candidateList = ["SANDERS", "CLINTON", "O'MALLEY"]
if party == "gop":
    directory = "gop_transcripts"
    candidateList = ["BUSH", "CARSON", "CHRISTIE", "CRUZ", "KASICH", "TRUMP"]

# generator for transcript pieces
transcripts = (y
               for x in os.listdir(directory)
               for y in open(directory + '/' + x).readlines())
# in
wordDict = dict()
wordList = dict()
relFreqList = dict()
for candidate in candidateList:
    wordDict[candidate] = dict()
    wordList[candidate] = []
    relFreqList[candidate] = []

totalDict = {}
totalWords = 0

# read in all the lines from the transcript
for line in transcripts:

    # check to see if the first word denotes a speaker
    firstWord = line.split(' ', 1)[0]

    if len(firstWord) > 0 and firstWord[-1] == ':':

        # indicate who is now speaking
        currentSpeaker = firstWord[:-1]
        line = line.split(' ', 1)[1]

    # if the speaker is a candidate, tally the words in the sentence
    if currentSpeaker in candidateList:

        trimmedLine = line.translate(None, ",.!?\n").lower()

        for word in trimmedLine.split(' '):
            if word.isspace():
                pass
            elif word in wordDict[currentSpeaker].keys():
                wordDict[currentSpeaker][word] += 1
            else:
                wordDict[currentSpeaker][word] = 1

# convert the dicts into list of tuples so we can sort them
for candidate in candidateList:

    # convert word dictionary to list of tuples so we can sort it
    wordList[candidate] = sorted(wordDict[candidate].items(),
                                 key=operator.itemgetter(1))
    # tally all the occurences of words
    for pair in wordList[candidate]:
        totalWords += pair[1]
        if pair[0] in totalDict.keys():
            totalDict[pair[0]] += pair[1]
        else:
            totalDict[pair[0]] = pair[1]

# now that we have the total frequences, we generate the relative frequencies
for candidate in candidateList:
    wordList[candidate][:] = [(x[0], x[1], float(x[1])/totalDict[x[0]])
                              for x in wordList[candidate]]
    wordList[candidate] = sorted(wordList[candidate],
                                 key=operator.itemgetter(1))

    wordList[candidate] = sorted(wordList[candidate],
                                 key=operator.itemgetter(2))

# wordList format: tuple(word, frequency, relfrequency of total)

# go through each candidate and print out each candidate
for candidate in candidateList:
    print candidate
    for pair in wordList[candidate]:
        if pair[1] > 10 and pair[2] > 0.8:
            print pair[0] + "  " + str(pair[1]) + " " + str(pair[2])

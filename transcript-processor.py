# scrapes a raw transcript to get each candidates sentences
import operator
import os
import sys


# read in all the lines from the transcript
def transcript_to_candidate(transcripts, candidateList):
    wordDict = dict()

    for candidate in candidateList:
        wordDict[candidate] = dict()

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
    return wordDict


def sort_by_frequency(wordDict, candidateList):

    wordList = dict()
    totalWords = 0
    totalDict = {}
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

    return wordList, totalDict, totalWords

DEMOCRAT_CANDIDATES = ["SANDERS", "CLINTON", "O'MALLEY"]
GOP_CANDIDATES = ["BUSH", "CARSON", "CHRISTIE", "CRUZ", "KASICH", "TRUMP"]

party = sys.argv[1]

if party == "dem":
    directories = ["dem_transcripts"]
    candidateList = DEMOCRAT_CANDIDATES
if party == "gop":
    directories = ["gop_transcripts"]
    candidateList = GOP_CANDIDATES
if party == "all":
    directories = ["gop_transcripts", "dem_transcripts"]
    candidateList = DEMOCRAT_CANDIDATES + GOP_CANDIDATES

# generator for transcript pieces
transcripts = (transcript
               for directory in directories
               for fileName in os.listdir(directory)
               for transcript in open(directory + '/' + fileName).readlines())
# in
wordDict = dict()
wordList = dict()
relFreqList = dict()
for candidate in candidateList:
    wordList[candidate] = []
    relFreqList[candidate] = []

totalDict = {}
totalWords = 0

wordDict = transcript_to_candidate(transcripts, candidateList)

# if we're doing party vs. party, make some changes
if party == "all":
    wordDict["GOP"] = {}
    wordDict["DEM"] = {}

    for candidate in candidateList:
        if candidate in DEMOCRAT_CANDIDATES:
            currParty = "DEM"
        else:
            currParty = "GOP"
        for word in wordDict[candidate].keys():
            if word in wordDict[currParty].keys():
                wordDict[currParty][word] += wordDict[candidate][word]
            else:
                wordDict[currParty][word] = wordDict[candidate][word]
        del(wordDict[candidate])
    candidateList = ["GOP", "DEM"]

# convert dict into sorted list of tuples
wordList, totalDict, totalWords = sort_by_frequency(wordDict, candidateList)

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

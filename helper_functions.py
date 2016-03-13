# helper function for transcript processing
import operator


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

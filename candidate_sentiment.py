# scrapes raw transcripts to determine the overall sentiment of a candidate

import os
# import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from helper_functions import transcript_to_candidate_lines


def word_feats(words):
    return dict([(word, True) for word in words])


directories = ["gop_transcripts", "dem_transcripts"]
DEMOCRAT_CANDIDATES = ["CLINTON", "O'MALLEY", "SANDERS"]
GOP_CANDIDATES = ["BUSH", "CARSON", "CHRISTIE", "CRUZ", "KASICH", "TRUMP"]

candidateList = DEMOCRAT_CANDIDATES + GOP_CANDIDATES
transcripts = (transcript
               for directory in directories
               for fileName in os.listdir(directory)
               for transcript in open(directory + '/' + fileName).readlines())

lineList = transcript_to_candidate_lines(transcripts, candidateList)

negids = movie_reviews.fileids('neg')
posids = movie_reviews.fileids('pos')

negfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'neg')
            for f in negids]
posfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'pos')
            for f in posids]

trainfeats = negfeats + posfeats

classifier = NaiveBayesClassifier.train(trainfeats)
# print 'accuracy:', nltk.classify.util.accuracy(classifier, testfeats)
# classifier.show_most_informative_features()

sentimentCount = dict((candidate, {'pos': 0, 'neg': 0})
                      for candidate in candidateList)
print "candidate,party,positive_lines,negative_lines,positive %"
for candidate in candidateList:
    # print "Generating sentiment for " + candidate
    for line in lineList[candidate]:

        testingWordDict = {}
        for word in line:
            testingWordDict[word] = True

        prediction = classifier.classify(testingWordDict)
        sentimentCount[candidate][prediction] += 1
    if candidate in GOP_CANDIDATES:
        party = 'R'
    else:
        party = 'D'

    percentage = 100 * sentimentCount[candidate]['pos'] / \
        float(sentimentCount[candidate]['pos'] +
              sentimentCount[candidate]['neg'])

    print (candidate + ',' +
           party + ',' +
           str(sentimentCount[candidate]['pos']) + ',' +
           str(sentimentCount[candidate]['neg']) + ',' +
           "%0.1f") % percentage

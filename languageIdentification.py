#SCOTT BOMMARITO
#uniqname: zucchini
#ASSIGNMENT 1
#EECS 498 WN 2015

import re

#returns a map of unigrams to frequencies and a map of bigrams to frequencies
def trainBigramLanguageModel(training):
    unigrams = re.findall(".", training)
    bigrams = re.findall("..", training)
    uniFreq = {}
    biFreq = {}
    uniset = set(unigrams)
    biset = set(bigrams)
    for unigram in uniset:
        uniFreq[unigram] = unigrams.count(unigram)
    for bigram in biset:
        biFreq[bigram] = bigrams.count(bigram)
    return uniFreq, biFreq

#identify most likely language for a text given list of languages names, and maps of frequencies
def identifyLanguage(text, languages, uniFreq, biFreq):
    likely = float(0)
    index = 0
    for i in range(0, len(languages)):
        prob = float(1)
        charCount = len(uniFreq[i])
        for x in range(1, len(text)):
            bigram = text[x-1] + text[x]
            unigram = text[x]
            bigramFreq = 0
            unigramFreq = 0
            if bigram in biFreq[i]:
                bigramFreq = biFreq[i][bigram]
            if unigram in uniFreq[i]:
                unigramFreq = uniFreq[i][unigram]
            prob *= float(bigramFreq + 1) / float(unigramFreq + charCount)
        if (prob > likely):
            likely = prob
            index = i
    return languages[index]

def main(args):
    if len(args) != 2:
        print "incorrect command line arguments"
        return
    testfile = args[1]
    languageNames = ["English", "French", "Italian"]
    languageFiles = ["languageIdentification.data/training/" + language for language in languageNames]
    unigramMaps = []
    bigramMaps = []
    for filename in languageFiles:
        INFILE = open(filename)
        unimap, bimap = trainBigramLanguageModel(INFILE.read().strip())
        unigramMaps.append(unimap)
        bigramMaps.append(bimap)
    INFILE = open(testfile)
    SOLUTION = open("languageIdentification.data/solution")
    i = 1
    correct = 0
    for line in INFILE:
        text = line.strip()
        answer = str(i) + " " + identifyLanguage(text, languageNames, unigramMaps, bigramMaps)
        print answer
        i += 1
        if SOLUTION.readline() == answer + "\n":
            correct += 1
    INFILE.close()
    SOLUTION.close()
    print str(correct) + " / " + str(i - 1)
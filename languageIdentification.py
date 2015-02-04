import re

#returns list of tokens in a SGML-less text
def tokenizeTextNoDates(text):
    noNumberText = " ".join(re.split("[0-9]", text))
    tokens = re.split("[^\w]*", noNumberText)
    return tokens

#returns a map of unigrams to frequencies and a map of bigrams to frequencies
def trainBigramLanguageModel(training):
    tokens = tokenizeTextNoDates(training)
    unigrams = []
    bigrams = []
    for token in tokens:
        currentUnigrams = re.findall("\w", token)
        currentBigrams = re.findall("\w\w", token)
        for unigram in currentUnigrams:
            unigrams.append(unigram)
        for bigram in currentBigrams:
            bigrams.append(bigram)
    uniFreq = {}
    biFreq = {}
    uniset = set(unigrams)
    biset = set(bigrams)
    for unigram in uniset:
        uniFreq[unigram] = unigrams.count(unigram)
    for bigram in biset:
        biFreq[bigram] = bigrams.count(bigram)
    print "UNIFREQ: "
    print uniFreq
    print "BIFREQ: "
    print biFreq
    return uniFreq, biFreq

#identify most likely language for a text given list of languages names, and maps of frequencies
def identifyLanguage(text, languages, uniFreq, biFreq):
    likely = 0
    index = 0
    words = tokenizeTextNoDates(text)
    for i in range(0, len(languages) - 1):
        prob = 1
        charCount = len(uniFreq)
        for word in words:
            for x in range(1, len(word) - 1):
                bigram = word[x-1] + word[x]
                unigram = word[x]
                bigramFreq = 0
                unigramFreq = 0
                if bigram in biFreq[i]:
                    bigramFreq = biFreq[i][bigram]
                if unigram in uniFreq[i]:
                    unigramFreq = uniFreq[i][unigram]
                print "bigram is " + bigram
                print bigramFreq
                prob *= (bigramFreq + 1) / (unigramFreq + charCount)
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
    for line in INFILE:
        text = line.strip()
        print text + " " + identifyLanguage(text, languageNames, unigramMaps, bigramMaps)
    INFILE.close()

def runLang():
    main([",", "languageIdentification.data/test"])
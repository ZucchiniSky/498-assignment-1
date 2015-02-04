import re
from os import listdir
from os.path import isfile, join
from porterstemmer import PorterStemmer

stopwords = []

#generates the list of stopwords
def generateStopwords():
    INFILE = open("stopwords")
    for line in INFILE:
        stopwords.append(line.rstrip("\n"))
    INFILE.close()

#removes SGML tags from a text and replaces them with " "
def removeSGML(text):
    return " ".join(re.split("<.*?>", text))

#returns true if the word does not contain a "." and is at least one char long
def wordIsValid(word):
    return len(word) > 0 and not re.match(".*[.].*", word)

#returns list of tokens in a SGML-less text
def tokenizeText(text):
    dateReg = "(Jan|January|Feb|February|Mar|March|Apr|April|May|Jun|June|Jul|July|Aug|August|Sep|September|Oct|October|Nov|November|Dec|December|([01]?[0-9]))[ /]([0-2]?[0-9])[ ,/][1-9][0-9]*"
    dates = re.findall(dateReg, text)
    noDateText = " ".join(re.split(dateReg, text))
    noNumberText = " ".join(re.split("[0-9]", noDateText))
    tokens = re.split("[\s,;!?()/]*", noNumberText)
    tokens = filter(wordIsValid, tokens)
    for date in dates:
        tokens.append(date)
        print "FOUND DATE: " + date
    return tokens

#computes first - second
def listDiff(first, second):
    second = set(second)
    return [x for x in first if x not in second]

#removes stopwords from list of tokens
def removeStopwords(tokens):
    return listDiff(tokens, stopwords)

#stems a single word
def stemWord(str):
    stemmer = PorterStemmer()
    return stemmer.stem(str, 0, len(str)-1)

#stems a list of tokens
def stemWords(tokens):
    return [stemWord(token) for token in tokens]

#processes and tokenizes a file
def processFile(filename):
    INFILE = open(filename)
    text = INFILE.read()
    INFILE.close()
    text = removeSGML(text)
    tokens = tokenizeText(text)
    tokens = removeStopwords(tokens)
    return stemWords(tokens)

#used to sort a frequency list by highest frequency
def sortByFreq(x, y):
    return y[1] - x[1]

def main(args):
    if len(args) != 2:
        print "incorrect command line arguments"
    folder = args[1]
    files = [folder + filename for filename in listdir(folder) if isfile(join(folder, filename))]
    tokens = []
    generateStopwords()
    print "STOPWORDS ARE "
    print stopwords
    for filename in files:
        filetokens = processFile(filename)
        for token in filetokens:
            tokens.append(token)
    tokens = sorted(tokens)
    vocab = set(tokens)
    print "VOCAB IS "
    print vocab
    print "Words " + str(len(tokens))
    print "Vocabulary " + str(len(vocab))
    frequencies = []
    for word in vocab:
        frequencies.append([word, tokens.count(word)])
    print "Top 50 Words"
    frequencies = sorted(frequencies, cmp=sortByFreq)
    for i in range(0, 50):
        print str(frequencies[i][0]) + " " + str(frequencies[i][1])

def runToken():
    main([",", "cranfieldDocs/"])
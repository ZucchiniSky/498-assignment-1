import re
from os import listdir
from os.path import isfile, join
from porterstemmer import PorterStemmer

stopwords = []
dateMonth = "([jJ]an|[jJ]anuary|[fF]eb|[fF]ebruary|[mM]ar|[mM]arch|[aA]pr|[aA]pril|[mM]ay|[jJ]un|[jJ]une|[jJ]ul|[jJ]uly|[aA]ug|[aA]ugust|[sS]ep|[sS]eptember|[oO]ct|[oO]ctober|[nN]ov|[nN]ovember|[dD]ec|[dD]ecember|1[012]|0?[1-9])"
dateDay = "(0?[1-9]|[1-2][0-9]|3[0-1])"
dateYear = "[1-9][0-9]*"
dateReg = "(" + dateMonth + "[- ]" + dateDay + "[- ,]" + dateYear + ")"

#generates the list of stopwords
def generateStopwords():
    INFILE = open("stopwords")
    for line in INFILE:
        stopwords.append(line.strip())
    INFILE.close()

#removes SGML tags from a text and replaces them with " "
def removeSGML(text):
    return " ".join(re.split("<.*?>", text))

#returns true if the word does not contain a "." and is at least one char long
def wordIsValid(word):
    return len(word) > 0 and not re.match(".*[.].*", word)

#returns list of tokens in a SGML-less text
def tokenizeText(text):
    dates = re.findall(dateReg, text)
    noDateText = " ".join(re.split(dateReg, text))
    noNumberText = " ".join(re.split("[0-9]", noDateText))
    tokens = re.split("[\s,;!?()/]*", noNumberText)
    newTokens = []
    for token in tokens:
        if re.match(".*n't", token):
            print token
            newTokens.append("not")
            newTokens.append("".join(re.split(".*n't", token)))
            print "appended not and " + "".join(re.split(".*n't", token))
        elif re.match("let's", token):
            print token
            newTokens.append("us")
            newTokens.append("let")
            print "appended let us"
        elif re.match("I'm", token):
            print token
            newTokens.append("I")
            newTokens.append("am")
            print "appended I am"
        elif re.match(".*'re", token):
            print token
            newTokens.append("are")
            newTokens.append("".join(re.split(".*'re", token)))
            print "appended are and " + "".join(re.split(".*'re", token))
        elif re.match(".*'s", token):
            print token
            newTokens.append("is")
            newTokens.append("".join(re.split(".*'s", token)))
            newTokens.append("'s")
            print "appended 's and is and " + "".join(re.split(".*'s", token))
        elif re.match(".*'ve", token):
            print token
            newTokens.append("have")
            newTokens.append("".join(re.split(".*'ve", token)))
            print "appended have and " + "".join(re.split(".*'ve", token))
        elif re.match(".*'d", token):
            print token
            newTokens.append("did")
            newTokens.append("would")
            newTokens.append("had")
            newTokens.append("".join(re.split(".*'d", token)))
            print "appended did and would and had and " + "".join(re.split(".*'d", token))
        elif re.match(".*'ll", token):
            print token
            newTokens.append("will")
            newTokens.append("".join(re.split(".*'ll", token)))
            print "appended will and " + "".join(re.split(".*'ll", token))
        else:
            newTokens.append(token)
    tokens = newTokens
    tokens = filter(wordIsValid, tokens)
    for date in dates:
        tokens.append(date[0])
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
    vocab = set(tokens)
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
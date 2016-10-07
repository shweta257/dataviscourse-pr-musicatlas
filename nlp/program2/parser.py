import sys

grammarRules = {}
 
def readGrammar(grammarFileName):
    with open(grammarFileName) as f:
        for line in f:
            lineVals=line[:-1].split("->")
            left = lineVals[0].strip()
            right = lineVals[1].strip()
            if right not in grammarRules:
                grammarRules[right] = []     
            grammarRules[right].append(left)
    return

grammarFile = sys.argv[1]
sentenceFile = sys.argv[2]
readGrammar(grammarFile)
with open(sentenceFile) as f:
    for line in f:
        if len(line.strip()) == 0:
            continue
        print "\nPARSING SENTENCE:",line.strip(),""
        words = line.split(" ")
        matrix = [[[] for i in range(len(words))] for j in range(len(words))]
        for c, word in enumerate(words):
            word = word.strip()
            matrix[c][c] = grammarRules[word]
            for r in range(c-1, -1, -1):
                for s in range(r+1, c+1, 1):
                    for B in matrix[r][s - 1]:
                        for C in matrix[s][c]: 
                            key = B + " " + C
                            if key in grammarRules:
                                matrix[r][c].extend(grammarRules[key])

        sentenceCell = matrix[0][len(words)-1]
        parseCount = 0
        for grammar in sentenceCell:
            if grammar == 'S':
                parseCount += 1
        print "NUMBER OF PARSES FOUND:", parseCount
        print "CHART:"
        for i, row in enumerate(matrix):
            for j, cell in enumerate(row):
                if j < i:
                    continue
                if len(cell) == 0:
                    print "  chart[{},{}]".format(i+1,j+1) +": "+"-"
                else:
                    cell = sorted(cell)
                    curPosTags=[]
                    for grammar in cell:
                        curPosTags.append(grammar)
                    print "  chart[{},{}]".format(i+1,j+1) +": "+" ".join(curPosTags)
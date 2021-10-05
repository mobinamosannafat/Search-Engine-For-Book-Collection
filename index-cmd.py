# Program to biuld a dictionary of terms in 87 documents and perform boolean retrieval for input queries
import re
import os
import collections
import time

# This is the map where dictionary terms will be stored as keys and value will be posting list with position in the file
dictionary = {}
# This is the map of docId to input file name
docIdMap = {}


class index:
    def __init__(self, path):
        self.path = path
        pass

    def buildIndex(self): #doc

        docId = 1
        fileList = [f for f in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, f))]
        for eachFile in fileList:
            position = 1
            count = 0
            docIdMap[docId] = eachFile
            lines = [line.rstrip('\n') for line in open(self.path + "/" + eachFile)]

            for eachLine in lines:
                wordList = re.split('\W+', eachLine)

                while '' in wordList:
                    wordList.remove('')
                for word in wordList:
                    if (word.lower() in dictionary):
                        postingList = dictionary[word.lower()]
                        if (docId in postingList):
                            postingList[docId].append(position)
                            position = position + 1
                        else:
                            postingList[docId] = [position]
                            position = position + 1
                    else:
                        dictionary[word.lower()] = {docId: [position]}
                        position = position + 1
            docId = docId + 1

        length_dict = {key: len(value) for key, value in dictionary.items()}

    ############################
    def finalPrint(self, item):
        print("\n")
        print(" << Document name: " + docIdMap[item] +" >>")


    def and_query(self, query_terms):
        if len(query_terms) == 1:
            resultList = self.getPostingList(query_terms[0])
            if not resultList:
                print ("")
                printString = "Result for the Query : " + query_terms[0]
                print (printString)
                print ("0 documents returned as there is no match")
                return

            else:
                print ("")
                printString = "Result for the Query : " + query_terms[0]
                print (printString)
                print ("Total documents retrieved : " + str(len(resultList)))
                for items in resultList:
                    #print (docIdMap[items]) #
                    self.finalPrint(items)

        else:
            resultList = []
            for i in range(1, len(query_terms)):
                if (len(resultList) == 0):
                    resultList = self.mergePostingList(self.getPostingList(query_terms[0]),
                                                       self.getPostingList(query_terms[i]))
                else:
                    resultList = self.mergePostingList(resultList, self.getPostingList(query_terms[i]))
            print ("")
            printString = "Result for the Query(AND query) :"
            i = 1
            for keys in query_terms:
                if (i == len(query_terms)):
                    printString += " " + str(keys)
                else:
                    printString += " " + str(keys) + " AND"
                    i = i + 1

            print (printString)
            print ("Total documents retrieved : " + str(len(resultList)))
            for items in resultList:
                #print (docIdMap[items])
                self.finalPrint(items)

    def getPostingList(self, term):
        if (term in dictionary):
            postingList = dictionary[term]
            keysList = []
            for keys in postingList:
                keysList.append(keys)
            keysList.sort()
            # print keysList
            return keysList
        else:
            return None

    def mergePostingList(self, list1, list2):

        mergeResult = list(set(list1) & set(list2))
        mergeResult.sort()
        return mergeResult

    def saveTodict(self):
        # function to print the terms and posting list in the index
        fileobj = open("invertedIndex.txt", 'w')
        for key in dictionary:
            print (key + " --> " + str(dictionary[key]))
            fileobj.write(key + " --> " + str(dictionary[key]))
            fileobj.write("\n")
        fileobj.close()


def main():
    docCollectionPath = os.path.join("docs")
    query = input("Enter Query : ")
    indexObject = index(docCollectionPath)
    indexObject.buildIndex()

    wordList = re.split('\W+', query)

    while '' in wordList:
        wordList.remove('')

    wordsInLowerCase = []
    for word in wordList:
        wordsInLowerCase.append(word.lower())
    indexObject.and_query(wordsInLowerCase)

    cont = input("if you would like to see details, enter ""yes"" otherwise ""no"" : ")
    if (cont == "yes"): 
        print(" ############# Extra Information #############")
        print ("") #clear
        print ("Inverted Index :")#clear
        indexObject.print_dict()#clear
        print ("-------------------------------------------------------")

    else:
        print("Thank you for using this program")


if __name__ == '__main__':
    main()

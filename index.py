import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import re
import os
import collections
import time

# This is the map where dictionary terms will be stored 
# as keys and value will be posting list with position in the file
dictionary = {}
# This is the map of docId to input file name
docIdMap = {}
# This list will be used in printing the retrieved results to UI
data = []
# Specifying wich file to use as UI
ui,_ = loadUiType('mainwindow.ui')

# Class for UI functioning
class MainApp(QMainWindow, ui):

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.handleButtons()

    # Function that handles Search Button
    def handleButtons(self):
        # When button is bushed, "retResults" is called
        self.pushButton.clicked.connect(self.retResult)

    # Function to biuld the dictionary and posting lists AND 
    # perform boolean retrieval as well as showing results in UI
    def retResult(self):
        # set path to the documents's repository
        docCollectionPath = os.path.join("docs")
        # Reads the input query from search box
        query = self.lineEdit.text()
        self.label_2.setText("It may take while to find resualts , please be Patience")
        # Builds an object of type "index" and passes the documents's path to it
        indexObject = index(docCollectionPath)
        # Calls "buildIndex" in order to build the dictionary and posting lists
        indexObject.buildIndex()
        # Prints the inverted indexes to a file
        indexObject.saveTodict()
        # Split query by regular expression
        wordList = re.split('\W+', query)
        while '' in wordList:
            wordList.remove('')
        # Turns all the words to lowercase letters and appends them to the end of the new list
        wordsInLowerCase = []
        for word in wordList:
            wordsInLowerCase.append(word.lower())
        # Calls the "and_query" for the lowercase list
        docList = indexObject.and_query(wordsInLowerCase)
        # If the posting list of the query was empty, "No result is Printed on the screen"
        if not docList:
            self.label_2.setText("No result")
        else:
        # The docIds returned above are converted to a list of book names
            self.label_2.setText("RESULTS :")
            for i in range(len(docList)):
                data.append(docIdMap[docList[i]])
            # The book names are then printed in the Screen
            for j in range(len(data)):
                self.listWidget.addItem(data[j]) 

class index:
    def __init__(self, path):
        self.path = path
        pass

    # Function for building dictionary
    def buildIndex(self): #doc
        # Starts from the first document in the collection
        docId = 1
        # Gets all the files(books)
        fileList = [f for f in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, f))]
        # For each doc, starts from beginig and itterates through for adding new words to dictionary
        # OR just adding the position to the posting list
        for eachFile in fileList:
            position = 1
            count = 0
            docIdMap[docId] = eachFile
            # Reads document line by line
            lines = [line.rstrip('\n') for line in open(self.path + "/" + eachFile)]
            # Seperates words by space
            for eachLine in lines:
                wordList = re.split('\W+', eachLine)

                while '' in wordList:
                    wordList.remove('')
                # Lowercases all terms in order to store or search in dictionary
                for word in wordList:
                    # If the word exists in the dictionary
                    if (word.lower() in dictionary):
                        postingList = dictionary[word.lower()]
                        # If the docId is already in the posting list, it appends the position
                        if (docId in postingList):
                            postingList[docId].append(position)
                            position = position + 1
                        else:
                            # If the docId is not in the posting list, adds the Id and the position 
                            # of the word
                            postingList[docId] = [position]
                            position = position + 1
                    else:
                        # If the word has not been added to the dictionary before
                        # then it is added and a posting list is made for it
                        dictionary[word.lower()] = {docId: [position]}
                        position = position + 1
            # When the whole document has been scaned, it moves to the next doc in the collection
            docId = docId + 1
        #lengths = {key:len(value) for key,value in dictionary.iteritems()}
        length_dict = {key: len(value) for key, value in dictionary.items()}

    # This functions looks for the terms of the query in the dictionary 
    def and_query(self, query_terms):
        #print("in and query looking for words")
        # If the query contains only one word, calls "getPostingList" for that word
        if len(query_terms) == 1:
            resultList = self.getPostingList(query_terms[0])

        else:
        # If the query contains more than one word, finds the posting list of all the word
        # then merges the documents by calculating their AND for boolean retrieval
            resultList = []
            for i in range(1, len(query_terms)):
                if (len(resultList) == 0):
                    resultList = self.mergePostingList(self.getPostingList(query_terms[0]),
                                                       self.getPostingList(query_terms[i]))
                else:
                    resultList = self.mergePostingList(resultList, self.getPostingList(query_terms[i]))

        return resultList

    # Stores the docId in the posting list of the term and sorts them
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

    # Gets 2 listd as input and merges the list, sort it and return the final list
    def mergePostingList(self, list1, list2):
        try:
            mergeResult = list(set(list1) & set(list2))
            mergeResult.sort()
            return mergeResult
        except:
            print("No results!!!")


    def saveTodict(self):
        # function to print the terms and posting list in the index
        fileobj = open("invertedIndex.txt", 'w')
        for key in dictionary:
            #print (key + " --> " + str(dictionary[key]))
            fileobj.write(key + " --> " + str(dictionary[key]))
            fileobj.write("\n")
        fileobj.close()

def main():
    # This function starts the application allowing user to search
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()

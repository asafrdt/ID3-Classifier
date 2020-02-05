import copy
import csv
import operator
from tkinter import *
from tkinter import filedialog
import ctypes
from math import log
import tkinter as tk
class Node:
    def __init__(self, attr, parent, split, entropy, gain, dataSet, result,path):
        self.attribute = attr
        self.parent = parent
        self.nodes = []
        self.splitAtrribute = split
        self.classEntropy = entropy
        self.gain = gain
        self.dataSet = dataSet
        self.result = result
        self.path = None

    def __str__(self):
        return str(self.attribute, self.parent, self.nodes)
class Gui:
    def __init__(self, master):
        #title and place of the frame
        master.title("Data Mining Project")
        master.geometry("900x475")
        #create frames
        title = Frame(root)
        Path = Frame(root)
        Discretization = Frame(root)
        buttons = Frame(root)
        #frames places
        title.place(x=100, y=25)
        Path.place(x=5, y=100)
        Discretization.place(x=5, y=140)
        buttons.place(x=300, y=250)
        #buttos,labels and text fields
        self.LBLtitle = Label(title, text="Data Mining Project", font="Helvetica 15 bold", width=50)
        self.LBLtitle.pack()
        self.LBLPath = Label(Path, text="Directory Path", width=20)
        self.LBLPath.pack(side=LEFT)
        self.TXTpath = Entry(Path, width=80)
        self.TXTpath.pack(side=LEFT)
        # Browse button
        self.browse_button = Button(Path, text="Browse",command= self.browse)
        self.browse_button.pack()
        # Second Row
        self.lbl2 = Label(Discretization, text="Discretization Bin", width=20)
        self.lbl2.pack(side=LEFT)
        self.TXTDiscretization= Entry(Discretization, width=5)
        self.TXTDiscretization.pack(side=LEFT)
        # # Button Clean
        self.Clean_button = Button(buttons, text="Clean", width=30, command=self.clean)
        self.Clean_button.pack()
        # Button Discretization“
        self.Discretization_button = Button(buttons, text="Discretization", width=30,command=self.Discretization)
        self.Discretization_button.pack()
        # Button Build
        self.Build_button = Button(buttons, text="Build", width=30, command=self.build)
        self.Build_button.pack()
        # Button Classify“
        self.Classify_button = Button(buttons, text="Classify", width=30,command=self.classify)
        self.Classify_button.pack()
        # Button Accuracy““
        self.Accuracy_button = Button(buttons, text="Accuracy",width=30,command=self.Accuracy)
        self.Accuracy_button.pack()
        # Button Exit““
        self.Exit_button = Button(buttons, text="Exit", width=30,command=master.destroy)
        self.Exit_button.pack()

        self.Numeric_Attributes = {} # dictionary include: key- attribute,
        #                            value- dict of: key- avg of 2 numbers, value- gain of entropy
        self.Split_Dict = {}  # attributes and the col number of each
        self.Split_DictTest = {}
        self.Numeric_AttributesTest = {}
        self.Structure_Dict = {}
        self.classList = []
        self.classListTest = []
        self.Structure_DictTest = []
        self.Columns = 0
        self.bins = 0
        self.attributeCols = {}
        self.classEntropy = 0
        self.classEntropyTest =0
        self.MyFile = []
        self.MyfileTest = []
        self.roott = None
        self.rules =[]
    #Functions:
    # Functions:
    def classify(self):
        Bins = int(self.TXTDiscretization.get())
        if (self.CheckFolder()):
            train_path = self.TXTpath.get() + '/test_discretization_[#' + (str(Bins)) + '].csv'
            trainFile = open(self.TXTpath.get() + '/train.csv', 'r')
            rulesFile = open(self.TXTpath.get() + '/id3_rules_discretization_[#'+(str(Bins))+'].txt', 'r')
            StructureFile = open(self.TXTpath.get() + '/Structure.txt', 'r')
        else:
            return

        temprulesDict, rulesDict = {}, {}
        rulesList = []
        Columns, rules_counter, rulefound = 0, 0, 0

        testlist = self.read_Csv_Make_List(train_path)
        testlist[0].append('classify_class')  # new column for classification

        # find number of columns:
        for line in StructureFile:
            Columns = Columns + 1
        # create a Dict of rules
        for line in rulesFile:
            NewLine = line.strip('if')
            NewLine = NewLine.split()
            for i in range(0, len(NewLine)):
                NewLine[i] = NewLine[i].split('==')
                if (i % 2 == 0 and i != len(NewLine) - 1):
                    temprulesDict[NewLine[i][0]] = NewLine[i][1]
                elif (i == len(NewLine) - 1):
                    temprulesDict[NewLine[i][0]] = NewLine[i][1]
            rulesDict = copy.deepcopy(temprulesDict)
            rulesList.append(rulesDict)
            temprulesDict.clear()

        # Selection of classification according to the rules file
        for line in range(1, len(testlist)):
            for rule in range(0, rulesList.__len__()):
                for col in range(0, Columns - 1):
                    if testlist[0][col] in rulesList[rule].keys() and testlist[line][col] in rulesList[
                        rule].values():
                        rules_counter = rules_counter + 1
                    if (rules_counter == (rulesList[rule].__len__() - 1)):
                        testlist[line].append(rulesList[rule]['class'])
                        rulefound = 1
                        break
                rules_counter = 0
                if (rulefound):
                    rulefound = 0
                    break

        Bins = (self.TXTDiscretization.get())  # get number of bins from the GUI

        # create a new file after classifiction:
        with open('test_class_discretization_[#' + Bins + '].csv', mode='w', newline="\n") as train_file:
            train_writer = csv.writer(train_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for i in range(0, len(testlist)):
                train_writer.writerow(testlist[i])
        self.Mbox('', "Classifying the test-set is done!", 0)
    def Accuracy(self):
        Bins = (self.TXTDiscretization.get())

        if (self.CheckFolder()):
            testFile = self.TXTpath.get() + '/test_class_discretization_[#' + Bins + '].csv'
            trainFile = open(self.TXTpath.get() + '/train.csv', 'r')
            rulesFile = open(self.TXTpath.get() + '/id3_rules_discretization_[#'+str(Bins)+'].txt', 'r')
            StructureFile = open(self.TXTpath.get() + '/Structure.txt', 'r')
        else:
            return
        Columns, error = 0, 0
        errorlist = []
        testlist = self.read_Csv_Make_List(testFile)

        # find number of columns
        for line in StructureFile:
            Columns = Columns + 1

        # compare the old traget column with the new one and get numbers of errors and there id's.
        for line in range(1, len(testlist)):
            if (testlist[line][Columns] != testlist[line][Columns - 1]):
                error = error + 1
                errorlist.append(line + 1)

        if (errorlist == []):  # if there is a 100% accuaracy...
            errorlist.append("0 ID's classifyed as errors")

        # create a string for the Mbox:
        ErrorsId_Accuracy = "Errors ID's: {0}" \
                            ", accuracy: {1}%".format(errorlist, self.getaccuracy(error, len(testlist)))
        self.Mbox('', ErrorsId_Accuracy, 0)

        # create a new texy file with accuracy info:
        f = open("test_accuracy_discretization_[#" + Bins + "].txt", "w+")
        f.write(ErrorsId_Accuracy)
    def getaccuracy(self, errors, lines):
        return int((1 - (errors / lines)) * 100)
    def clean(self):
        CleanFlag = False
        counter = 0
        Columns = 0
        Structure_Dict,Value_Dict,Max_value_Dict,SumDict,emptydict = {},{},{},{},{}

        if (self.CheckFolder()):
            train_path = self.TXTpath.get() + '/train.csv'
            test_path = self.TXTpath.get() + '/test.csv'
            structure_path = self.TXTpath.get() + '/Structure.txt'
            trainFile = open(self.TXTpath.get() + '/train.csv', 'r')
            testFile = open(self.TXTpath.get() + '/test.csv', 'r')
            StructureFile = open(self.TXTpath.get() + '/Structure.txt', 'r')
        else:
            return
        # create Dictioanry from Structrefile and count number of columns
        for line in StructureFile:
            NewLine = line.strip('@ATTRIBUTE ')
            NewLine = NewLine.split()
            Structure_Dict[NewLine[0]] = NewLine[1]
            Columns = Columns + 1

        # Create list from train.csv file
        train_list = self.read_Csv_Make_List(train_path)
        test_list = self.read_Csv_Make_List(test_path)

        # if there is a emptey cell on class column, this part delete that line
        # and create a new file named Delete_empety_class_cells_rows.csv
        with open('train_clean.csv', mode='w', newline="\n") as train_file:
            train_writer = csv.writer(train_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for i in range(0, len(train_list)):
                if (train_list[i][Columns - 1] != ""):
                    train_writer.writerow(train_list[i])
                else:
                    CleanFlag = True

        # read from the new file (Delete_empety_class_cells_rows.csv) and create a list from it.
        train_list = self.read_Csv_Make_List('train_clean.csv')

        # check class column- how much different attributes it has, and how much time they appears.
        classList = Structure_Dict['class'].strip('{').strip('}').split(',')
        classDict = {}
        for class1 in classList:
            classDict[class1] = [0, 0]
        emptydict = copy.deepcopy(classDict)

        for key, value in Structure_Dict.items():
            if value != 'NUMERIC':  # than Find the attribute that appears most often and put it into a dictionary
                for i in range(1, len(train_list)):
                    if train_list[i][counter] != "":
                        if train_list[i][counter] not in Value_Dict:
                            Value_Dict[train_list[i][counter]] = 1
                        else:
                            Value_Dict[train_list[i][counter]] += 1
                    max_value = [(value, key) for key, value in Value_Dict.items()]
                    Max_value_Dict[key] = max(max_value)[1]
                Value_Dict.clear()
            if (value == 'NUMERIC'):
                for i in range(1, len(train_list)):
                    if train_list[i][counter] != "":
                        classDict[train_list[i][Columns-1]][0] +=1
                SumDict[key] = classDict
                for i in range(1, len(train_list)):
                    if train_list[i][counter] != "":
                        SumDict[key][train_list[i][Columns - 1]][1] += int(train_list[i][counter])
                for j in range(1, len(train_list)):
                    if train_list[j][counter] == "":
                        train_list[j][counter] = SumDict[key][train_list[j][Columns - 1]][1] / SumDict[key][train_list[j][Columns - 1]][0]
                        CleanFlag = True
                SumDict.clear()
                classDict = copy.deepcopy(emptydict)
            counter = counter + 1

        # fill in the emptey "cells" in the list with the most often attribute
        for j in range(0, Columns - 1):
            if train_list[0][j] in Max_value_Dict.keys():
                for i in range(1, len(train_list)):
                    if train_list[i][j] == "":
                        CleanFlag = True
                        train_list[i][j] = Max_value_Dict[train_list[0][j]]

        # create new file named "fillempteycells.csv and fill in the file with list without emptey cells
        with open('train_clean.csv', mode='w', newline="\n") as train_file:
            train_writer = csv.writer(train_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for i in range(0, len(train_list)):
                train_writer.writerow(train_list[i])

        # read the new file without emptrycells and create list from it:
        train_list = self.read_Csv_Make_List('train_clean.csv')
        self.cleantest()
        if CleanFlag:
            self.Mbox('', "Loading DataSet Done and Cleaning DataSet Done", 0)
        else:
            self.Mbox('', "Loading DataSet Done", 0)
    def cleantest(self):
        CleanFlag = False
        counter = 0
        Columns = 0
        Structure_Dict, Value_Dict, Max_value_Dict, SumDict, emptydict = {}, {}, {}, {}, {}

        if (self.CheckFolder()):
            train_path = self.TXTpath.get() + '/train.csv'
            test_path = self.TXTpath.get() + '/test.csv'
            structure_path = self.TXTpath.get() + '/Structure.txt'
            trainFile = open(self.TXTpath.get() + '/train.csv', 'r')
            testFile = open(self.TXTpath.get() + '/test.csv', 'r')
            StructureFile = open(self.TXTpath.get() + '/Structure.txt', 'r')
        else:
            return
        # create Dictioanry from Structrefile and count number of columns
        for line in StructureFile:
            NewLine = line.strip('@ATTRIBUTE ')
            NewLine = NewLine.split()
            Structure_Dict[NewLine[0]] = NewLine[1]
            Columns = Columns + 1

        # Create list from train.csv file
        train_list = self.read_Csv_Make_List(train_path)
        test_list = self.read_Csv_Make_List(test_path)

        # if there is a emptey cell on class column, this part delete that line
        # and create a new file named Delete_empety_class_cells_rows.csv
        with open('test_clean.csv', mode='w', newline="\n") as test_file:
            test_writer = csv.writer(test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for i in range(0, len(test_list)):
                if (test_list[i][Columns - 1] != ""):
                   test_writer.writerow(test_list[i])
                else:
                    CleanFlag = True

        # read from the new file (Delete_empety_class_cells_rows.csv) and create a list from it.
        test_list = self.read_Csv_Make_List('test_clean.csv')

        # check class column- how much different attributes it has, and how much time they appears.
        classList = Structure_Dict['class'].strip('{').strip('}').split(',')
        classDict = {}
        for class1 in classList:
            classDict[class1] = [0, 0]
        emptydict = copy.deepcopy(classDict)

        for key, value in Structure_Dict.items():
            if value != 'NUMERIC':  # than Find the attribute that appears most often and put it into a dictionary
                for i in range(1, len(test_list)):
                    if test_list[i][counter] != "":
                        if test_list[i][counter] not in Value_Dict:
                            Value_Dict[test_list[i][counter]] = 1
                        else:
                            Value_Dict[test_list[i][counter]] += 1
                    max_value = [(value, key) for key, value in Value_Dict.items()]
                    Max_value_Dict[key] = max(max_value)[1]
                Value_Dict.clear()
            if (value == 'NUMERIC'):
                for i in range(1, len(test_list)):
                    if test_list[i][counter] != "":
                        classDict[test_list[i][Columns - 1]][0] += 1
                SumDict[key] = classDict
                for i in range(1, len(test_list)):
                    if test_list[i][counter] != "":
                        SumDict[key][test_list[i][Columns - 1]][1] += int(test_list[i][counter])
                for j in range(1, len(test_list)):
                    if test_list[j][counter] == "":
                        test_list[j][counter] = SumDict[key][test_list[j][Columns - 1]][1] / \
                                                 SumDict[key][test_list[j][Columns - 1]][0]
                        CleanFlag = True
                SumDict.clear()
                classDict = copy.deepcopy(emptydict)
            counter = counter + 1

        # fill in the emptey "cells" in the list with the most often attribute
        for j in range(0, Columns - 1):
            if test_list[0][j] in Max_value_Dict.keys():
                for i in range(1, len(test_list)):
                    if test_list[i][j] == "":
                        CleanFlag = True
                        test_list[i][j] = Max_value_Dict[test_list[0][j]]

        # create new file named "fillempteycells.csv and fill in the file with list without emptey cells
        with open('test_clean.csv', mode='w', newline="\n") as train_file:
            test_writer = csv.writer(train_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for i in range(0, len(test_list)):
                test_writer.writerow(test_list[i])

        # read the new file without emptrycells and create list from it:
    def browse(self):
        self.DeletePathTextField()
        folderName = filedialog.askdirectory()
        self.TXTpath.insert(0, folderName)
        if (self.CheckFolder()):
            self.Mbox('','Folder opened successfully', 0)
    def DeletePathTextField(self):
        if self.TXTpath.get() != "":
            self.TXTpath.delete(0, END)
    def Mbox(self,title, text, style):
        return ctypes.windll.user32.MessageBoxW(0, text, title, style)
    def read_Csv_Make_List(self,path):
        read = csv.reader(open(path))
        return list(read)
    def CheckFolder(self):
        try:
            fo1 = open(self.TXTpath.get() + '/train.csv', 'r')
            fo2 = open(self.TXTpath.get() + '/test.csv', 'r')
            fo3 = open(self.TXTpath.get() + '/Structure.txt', 'r')
        except FileNotFoundError:
            self.Mbox('Error', 'Wrong folder! Choose the right folder and try again!', 0)
            self.DeletePathTextField()
            return False
        fo1.close()
        fo2.close()
        fo3.close()
        return True
    def Discretization(self):
        train_path = self.TXTpath.get() + '/train_clean.csv'
        structure_path = self.TXTpath.get() + '/Structure.txt'

        try:
            StructureFile = open(structure_path, 'r')
        except FileNotFoundError:
            self.Mbox('', 'Wrong folder! Choose the right folder and try again!', 0)
            return
        for line in StructureFile:
            NewLine = line.strip('@ATTRIBUTE')
            NewLine = NewLine.split()
            self.Structure_Dict[NewLine[0]] = NewLine[1]
            self.Columns += 1

        read = csv.reader(open(train_path))
        MyFile = list(read)
        Bins = int(self.TXTDiscretization.get())
        self.classList = self.Structure_Dict['class'].strip('{').strip('}').split(',')
        if Bins < len(self.classList):
            self.Mbox('', 'The number of bins smaller the the number of the classes! try again', 0)
            return
        self.bins = Bins
        i=0
        # dictionary of numeric attributes and their columns:
        for key in self.Structure_Dict:
            if self.Structure_Dict[key] == 'NUMERIC':
                self.Numeric_Attributes[key] = i
            i += 1

        # value: column of the attribute in train
        for key, value in self.Numeric_Attributes.items():
            Split_Dict1 = {}
            for i in range(1, len(MyFile)-1):
                avg = (float(MyFile[i][value]) + float(MyFile[i+1][value]))/2
                Split_Dict1[avg] = 0
            self.Split_Dict[MyFile[0][value]] = Split_Dict1
        print(self.Split_Dict)
        self.classEntropy = self.entropyForClass()
        binsDict = {}

        for key, value in self.Numeric_Attributes.items():
            help = {}
            maxAvgList = self.entropyForSplit(key, self.classEntropy)
            for i in range(len(maxAvgList)):
                help[i+1] = '<= %.2f' % (maxAvgList[i])
            binsDict[key] = help # bins dict- print the {'Height': {1: '<= 179.00', 2: '<= 190.00'}}
            print(binsDict)
            MyFile = self.numericToCategorial(key, maxAvgList, MyFile)
        self.MyFile = MyFile
        with open('train_discretization_[#'+(str(Bins))+'].csv', mode='w', newline="\n") as train_file:
            train_writer = csv.writer(train_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for i in range(0, len(MyFile)):
                if (MyFile[i][self.Columns - 1] != ""):
                    train_writer.writerow(MyFile[i])
        self.DiscretizationTest()
        self.Mbox('Discretization Status', 'Discretization DataSet Using %d Bins Done' % Bins, 0)

        self.attributeGain(binsDict)
    def DiscretizationTest(self):
        train_path = self.TXTpath.get() + '/test_clean.csv'
        structure_path = self.TXTpath.get() + '/Structure.txt'

        try:
            StructureFile = open(structure_path, 'r')
        except FileNotFoundError:
            self.Mbox('', 'Wrong folder! Choose the right folder and try again!', 0)
            return


        read = csv.reader(open(train_path))
        MyFile = list(read)
        Bins = int(self.TXTDiscretization.get())
        self.classListTest = self.Structure_Dict['class'].strip('{').strip('}').split(',')
        if Bins < len(self.classListTest):
            self.Mbox('', 'The number of bins smaller the the number of the classes! try again', 0)
            return
        self.bins = Bins
        i = 0
        # dictionary of numeric attributes and their columns:
        for key in self.Structure_Dict:
            if self.Structure_Dict[key] == 'NUMERIC':
                self.Numeric_AttributesTest[key] = i
            i += 1

        # value: column of the attribute in train
        for key, value in self.Numeric_AttributesTest.items():
            Split_Dict1 = {}
            for i in range(1, len(MyFile) - 1):
                avg = (float(MyFile[i][value]) + float(MyFile[i + 1][value])) / 2
                Split_Dict1[avg] = 0
            self.Split_DictTest[MyFile[0][value]] = Split_Dict1

        self.classEntropyTest = self.entropyForClassTest()
        binsDict = {}

        for key, value in self.Numeric_AttributesTest.items():
            help = {}
            maxAvgList = self.entropyForSplitTest(key, self.classEntropy)
            for i in range(len(maxAvgList)):
                help[i + 1] = '<= %.2f' % (maxAvgList[i])
            binsDict[key] = help
            MyFile = self.numericToCategorial(key, maxAvgList, MyFile)
        self.MyfileTest = MyFile
        with open('test_discretization_[#' + (str(Bins)) + '].csv', mode='w', newline="\n") as train_file:
            train_writer = csv.writer(train_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for i in range(0, len(MyFile)):
                if (MyFile[i][self.Columns - 1] != ""):
                    train_writer.writerow(MyFile[i])
    # calculate the entropy of all the file
    def entropyForClass(self):
        train_path = self.TXTpath.get() + '/train_clean.csv'
        read = csv.reader(open(train_path))
        MyFile = list(read)

        classDict = {}

        # classDict- dictionary of all the classes and 0 in value
        for class1 in self.classList:
            classDict[class1] = 0
        for i in range(1, len(MyFile)):
            classDict[MyFile[i][self.Columns - 1]] += 1

        entropy = 0
        for class1 in classDict:
            p = classDict[class1] / (len(MyFile) - 1)
            log1 = log(p, 2)
            entropy += p * log1
        return entropy * (-1)
    def entropyForClassTest(self):
        train_path = self.TXTpath.get() + '/test_clean.csv'
        read = csv.reader(open(train_path))
        MyFile = list(read)

        classDict = {}

        # classDict- dictionary of all the classes and 0 in value
        for class1 in self.classListTest:
            classDict[class1] = 0
        for i in range(1, len(MyFile)):
            classDict[MyFile[i][self.Columns - 1]] += 1

        entropy = 0
        for class1 in classDict:
            p = classDict[class1] / (len(MyFile) - 1)
            log1 = log(p, 2)
            entropy += p * log1
        return entropy * (-1)
    # returns binsList- list of the max averages for the partition to the bins
    def entropyForSplit(self, attribute, classEntropy):
        train_path = self.TXTpath.get() + '/train_clean.csv'

        read = csv.reader(open(train_path))
        MyFile = list(read)

        classList = self.Structure_Dict['class'].strip('{').strip('}').split(',')
        classDict = {}  # the value is list of <= avg in 0 index and > avg in 1 index
        for i in range(len(classList)):
            classDict[classList[i]] = [0, 0]

        # {'age': {51.0: {'yes': [0, 0], 'no': [0, 0]}-
        # Split_Dict.key-age(attribute), Split_Dict.value-51.0, Split_Dict.value.key- yes, Split_Dict.value,value-[0, 0]
        for key, value in self.Split_Dict.items():
            for k, v in dict(self.Split_Dict[key]).items():
                self.Split_Dict[key][k] = copy.deepcopy(classDict)

        attributeDict = {}
        for k, v in self.Split_Dict.items():
            if k == attribute:
                attributeDict = self.Split_Dict[k]

        for key, value in attributeDict.items():
            for i in range(1, len(MyFile)):

                if MyFile[i][self.Columns - 1] == 'yes':
                    if float(MyFile[i][self.Numeric_Attributes[attribute]]) <= key:
                        attributeDict[key]['yes'][0] = attributeDict[key]['yes'][0] + 1
                    else:
                        attributeDict[key]['yes'][1] += 1
                else:
                    if float(MyFile[i][self.Numeric_Attributes[attribute]]) <= key:
                        attributeDict[key]['no'][0] += 1
                    else:
                        attributeDict[key]['no'][1] += 1

        for key, value in attributeDict.items():
            sum1 = 0
            sum2 = 0
            # entropy1 is <=, entropy2 is >
            entropy1 = 0
            entropy2 = 0
            sumOfAll = 0
            for k, v in dict(attributeDict[key]).items():
                sum1 += attributeDict[key][k][0]
                sum2 += attributeDict[key][k][1]
                sumOfAll += sum1 + sum2

            for k, v in dict(attributeDict[key]).items():
                if attributeDict[key][k][0] == 0:
                    entropy1 += 0
                elif attributeDict[key][k][1] == 0:
                    entropy2 += 0
                else:
                    entropy1 += (attributeDict[key][k][0] / sum1) * log(attributeDict[key][k][0] / sum1, 2)
                    entropy2 += (attributeDict[key][k][1] / sum2) * log(attributeDict[key][k][1] / sum2, 2)
            entropy1 = entropy1 * (-1)
            entropy2 = entropy2 * (-1)
            info = (sum1 / sumOfAll) * entropy1 + (sum2 / sumOfAll) * entropy2
            attributeDict[key]['Gain'] = classEntropy - info
        GainList = []
        for key, value in attributeDict.items():
            GainList.append(attributeDict[key]['Gain'])
        maxGains = self.Nmaxelements(GainList)

        binslist = []
        for i in range(len(maxGains)):
            for key, value in attributeDict.items():
                if attributeDict[key]['Gain'] == maxGains[i] and maxGains[i] not in binslist:
                    binslist.append(key)
                    break
        return sorted(binslist)
    def entropyForSplitTest(self, attribute, classEntropy):
        train_path = self.TXTpath.get() + '/test_clean.csv'

        read = csv.reader(open(train_path))
        MyFile = list(read)

        classList = self.Structure_Dict['class'].strip('{').strip('}').split(',')
        classDict = {}  # the value is list of <= avg in 0 index and > avg in 1 index
        for i in range(len(classList)):
            classDict[classList[i]] = [0, 0]

        # {'age': {51.0: {'yes': [0, 0], 'no': [0, 0]}-
        # Split_Dict.key-age(attribute), Split_Dict.value-51.0, Split_Dict.value.key- yes, Split_Dict.value,value-[0, 0]
        for key, value in self.Split_DictTest.items():
            for k, v in dict(self.Split_DictTest[key]).items():
                self.Split_DictTest[key][k] = copy.deepcopy(classDict)

        attributeDict = {}
        for k, v in self.Split_DictTest.items():
            if k == attribute:
                attributeDict = self.Split_DictTest[k]

        for key, value in attributeDict.items():
            for i in range(1, len(MyFile)):

                if MyFile[i][self.Columns - 1] == 'yes':
                    if float(MyFile[i][self.Numeric_AttributesTest[attribute]]) <= key:
                        attributeDict[key]['yes'][0] = attributeDict[key]['yes'][0] + 1
                    else:
                        attributeDict[key]['yes'][1] += 1
                else:
                    if float(MyFile[i][self.Numeric_AttributesTest[attribute]]) <= key:
                        attributeDict[key]['no'][0] += 1
                    else:
                        attributeDict[key]['no'][1] += 1

        for key, value in attributeDict.items():
            sum1 = 0
            sum2 = 0
            # entropy1 is <=, entropy2 is >
            entropy1 = 0
            entropy2 = 0
            sumOfAll = 0
            for k, v in dict(attributeDict[key]).items():
                sum1 += attributeDict[key][k][0]
                sum2 += attributeDict[key][k][1]
                sumOfAll += sum1 + sum2

            for k, v in dict(attributeDict[key]).items():
                if attributeDict[key][k][0] == 0:
                    entropy1 += 0
                elif attributeDict[key][k][1] == 0:
                    entropy2 += 0
                else:
                    entropy1 += (attributeDict[key][k][0] / sum1) * log(attributeDict[key][k][0] / sum1, 2)
                    entropy2 += (attributeDict[key][k][1] / sum2) * log(attributeDict[key][k][1] / sum2, 2)
            entropy1 = entropy1 * (-1)
            entropy2 = entropy2 * (-1)
            info = (sum1 / sumOfAll) * entropy1 + (sum2 / sumOfAll) * entropy2
            attributeDict[key]['Gain'] = classEntropy - info
        GainList = []
        for key, value in attributeDict.items():
            GainList.append(attributeDict[key]['Gain'])
        maxGains = self.Nmaxelements(GainList)

        binslist = []
        for i in range(len(maxGains)):
            for key, value in attributeDict.items():
                if attributeDict[key]['Gain'] == maxGains[i] and maxGains[i] not in binslist:
                    binslist.append(key)
                    break
        return sorted(binslist)
    def Nmaxelements(self, list1):
        final_list = []
        for i in range(0, self.bins-1):
            max1 = 0
            for j in range(len(list1)):
                if list1[j] > max1 and list1[j] not in final_list:
                    max1 = list1[j]
            list1.remove(max1)
            final_list.append(max1)
        return final_list
    def numericToCategorial(self, attribute, gains, MyFile):
        # list of for each column of the numeric values for turn the to categorial
        attributeList = []
        for i in range(1, len(MyFile)):
            attributeList.append(MyFile[i][self.Numeric_Attributes[attribute]])
        attributeListHelp = copy.deepcopy(attributeList)

        # loop that check each round if the value smaller the the avg that choosen for thr bins
        for i in range(len(gains)):
            for j in range(len(attributeList)):
                if attributeList[j] != 'null' and float(attributeList[j]) <= gains[i]:
                    attributeListHelp[j] = i + 1
                    attributeList[j] = 'null'

        for j in range(len(attributeList)):
            if float(attributeListHelp[j]) > gains[len(gains) - 1]:
                attributeListHelp[j] = len(gains) + 1

        for i in range(1, len(MyFile)):
            MyFile[i][self.Numeric_Attributes[attribute]] = attributeListHelp[i - 1]

        return MyFile
    def numericToCategorialTest(self, attribute, gains, MyFile):
        # list of for each column of the numeric values for turn the to categorial
        attributeList = []
        for i in range(1, len(MyFile)):
            attributeList.append(MyFile[i][self.Numeric_AttributesTest[attribute]])
        attributeListHelp = copy.deepcopy(attributeList)

        # loop that check each round if the value smaller the the avg that choosen for thr bins
        for i in range(len(gains)):
            for j in range(len(attributeList)):
                if attributeList[j] != 'null' and float(attributeList[j]) <= gains[i]:
                    attributeListHelp[j] = i + 1
                    attributeList[j] = 'null'

        for j in range(len(attributeList)):
            if float(attributeListHelp[j]) > gains[len(gains) - 1]:
                attributeListHelp[j] = len(gains) + 1

        for i in range(1, len(MyFile)):
            MyFile[i][self.Numeric_AttributesTest[attribute]] = attributeListHelp[i - 1]

        return MyFile
    def attributeGain(self, binsDict):
        # convert the Structure_Dict to dictionary without NUMERIC
        for key, value in self.Structure_Dict.items():
            if self.Structure_Dict[key] == 'NUMERIC':
                self.Structure_Dict[key] = '{'
                for i in range(self.bins - 1):
                    self.Structure_Dict[key] += '%s,' % str(i + 1)
                self.Structure_Dict[key] += '%s}' % str(self.bins)
    def build(self):
        self.buildRec(None, self.MyFile)
        Bins = (self.TXTDiscretization.get())
        f = open("id3_rules_discretization_[#" + Bins + "].txt", "w+")
        self.Print(self.roott)
        self.CreateRulesFile(self.roott,f)
    def buildRec(self, parent, table):
        entropy = self.entropyForTree(table)
        print("------------entropy")
        print(entropy)
        if entropy == 0:
            return
        attribute = self.findTheMaxGain(table, entropy)
        print("---------att")
        print(attribute)
        gain = self.findGainsOfAttributes(table, entropy, attribute)
        splits = self.Structure_Dict[attribute].strip('{').strip('}').split(',')
        splitsDict = {}
        for i in range(len(splits)):
            splitsDict[splits[i]] = None
        # node = Node(attribute, parent, splits, entropy, gain, table, None,path
        node = Node(attribute, parent, splitsDict, entropy, gain, table, None,None)
        if parent != None:
            parent.nodes.append(node)
        if parent == None:
            self.roott = node
        col = 0
        # find the col number of the category:
        for i in range(len(table[0])):
            if table[0][i] == attribute:
                col = i
                break
        col = col - 1
        # send to the buildRec each branch:
        # for i in range(len(splits)):
        #     table1 = self.returnTableForSplit(table, splits[i], col)
        #     # entropy = self.entropyForTree(table)
        #     self.buildRec(node, table1)
        for key, value in dict(splitsDict).items():
            table1 = self.returnTableForSplit(table, key, col)
            if (self.entropyForTree(table1) == 0 and len(table1)!=1):
                splitsDict[key] = table1[1][len(table1[0])-1]
            self.buildRec(node,table1)
    def returnTableForSplit(self, table, split, col):
        help =[]
        j=1
        copyTable = copy.deepcopy(table[0])
        help.append(copyTable)
        del help[0][col+1]
        for i in range(1, len(table)):
            if str(table[i][col+1]) == str(split):
                copyTable = copy.deepcopy(table[i])
                help.append(copyTable)
                if str(split) in help[j]:
                    help[j].remove(str(split))
                elif int(split) in help[j]:
                    help[j].remove(int(split))
                # del help[j][col]
                j = j+1
        return help
    def findTheMaxGain(self, table, entropy):
        attributeGainsDict = {}
        attributeCols={}
        for i in range(len(table[0])):
            attributeCols[str(table[0][i])] = i
        for key, value in attributeCols.items():  # להכניס לרקורסיה
            if key != 'class':
                attributeGainsDict[key] = self.findGainsOfAttributes(table, entropy, key)
        max = 0
        for key, value in attributeGainsDict.items():
            print('attributeGainsDict: ', key, '- ', attributeGainsDict[key])
            if attributeGainsDict[key] > max:
                max = attributeGainsDict[key]
                attribute = key  # האטריביוט הסופי זה מה שיהיה בnode
        return attribute
    def findGainsOfAttributes(self, MyFile, classEntropy, attribute):
        tableForEntropy = []
        help =[attribute]
        attributeCols = {}
        for i in range(len(MyFile[0])):
            attributeCols[str(MyFile[0][i])] = i
        for i in range(len(self.classList)):
            help.append(self.classList[i])
        help.append('Entropy')

        tableForEntropy.append(help)
        categories = self.Structure_Dict[attribute].strip('{').strip('}').split(',')
        for i in range(len(categories)):
            help1 = []
            help1.append(categories[i])
            tableForEntropy.append(help1)

        for i in range(len(self.classList)):
            for j in range(1, len(tableForEntropy)):
                tableForEntropy[j].append(0)
        # calculate and add to tableForEntropy the number of yes, no in each category
        for i in range(len(self.classList)):
            for j in range(1, len(MyFile)):
                if MyFile[j][len(MyFile[0])-1] == self.classList[i]:
                    tableForEntropy[(categories.index(str(MyFile[j][attributeCols[attribute]])))+1][i + 1] += 1



        # calculate the entropy of each category in each attribute
        for i in range(1, len(tableForEntropy)):
            sum = 0
            entropy = 0
            for j in range(1, len(tableForEntropy[i])):
                sum += int(tableForEntropy[i][j])
            for j in range(1, len(tableForEntropy[i])):
                if tableForEntropy[i][j] == 0:
                    entropy += 0
                else:
                    entropy += (tableForEntropy[i][j]/sum)*log(tableForEntropy[i][j]/sum, 2)
            tableForEntropy[i].append((-1)*entropy)
            print('table for entropy:')
            print(tableForEntropy)
        info = 0
        for i in range(1, len(tableForEntropy)):
            sum = 0
            for j in range(1, len(tableForEntropy[i])-1):
                sum += tableForEntropy[i][j]
            info += (sum/(len(MyFile)-1))*tableForEntropy[i][len(tableForEntropy[i])-1]
        gain = classEntropy - info
        return gain
    def entropyForTree(self, MyFile):
        col = 0
        i = 0

        while MyFile[0][i] != 'class':
            col += 1
            i += 1
        classDict = {}
        # classDict- dictionary of all the classes and 0 in value
        for class1 in self.classList:
            classDict[class1] = 0
        for i in range(1, len(MyFile)):
            classDict[str(MyFile[i][col])] += 1
        entropy = 0
        for class1 in classDict:
            if len(MyFile) <= 1:
                return 0
            p = classDict[class1] / (len(MyFile) - 1)
            if p == 0:
                return 0
            log1 = log(p, 2)
            entropy += p * log1
        return entropy * (-1)
    def Print(self, roott):
        print(str(roott.attribute)+"->")
        print("(roott.nodes)---------", len(roott.nodes))
        print(roott.splitAtrribute)
        for k, v in dict(roott.splitAtrribute).items():
            if v != None:
                print('split: ', k, ' result: ', v)

        for i in range(len(roott.nodes)):
            self.Print((roott.nodes)[i])

    def CreateRulesFile(self,root,f):
        i=0
        if (root.parent==None):
            root.path = root.attribute
        else:
            if (root.path==None):
                root.path=""
            root.path = root.path+root.attribute
        for s, r in dict(root.splitAtrribute).items():
            if (r!=None):
                f.write("if "+str(root.path)+"=="+s+" than class=="+str(r)+"\n")
            else:
                root.nodes[i].path = str(root.path)+"=="+str(s)+" and "
                self.CreateRulesFile(root.nodes[i],f)
                i = i + 1
            # self.Print((roott.nodes)[i])

#Main
root = Tk()
g = Gui(root)
root.mainloop()
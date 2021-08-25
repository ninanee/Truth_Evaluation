# define operator
#For AND and OR. parsing until the first connnective symbol is reached.
#and the two variables around it can be identified
def forAndOrOperator(expression):

    if ('AND' in expression and 'OR' in expression):
        connectiveindex = min(expression.index('AND'), expression.index('OR'))
    elif ('AND' in expression):
        connectiveindex = expression.index('AND')
    else:
        connectiveindex = expression.index('OR')

    connective = expression[connectiveindex]

    leftValue = expression [connectiveindex - 1]
    rightValue = expression [connectiveindex + 1]
    leftValueBoolean = ('TRUE' in leftValue)
    rightValueBoolean = ('TRUE' in rightValue)

    if (connective == 'AND'):
        output = leftValueBoolean and rightValueBoolean
    elif (connective == 'OR'):
        output = leftValueBoolean or rightValueBoolean
    else:
        print("Error connnective: ", connective)
        exit()

    if (output):
        expression[connectiveindex - 1] = 'TRUE'
    else:
        expression[connectiveindex - 1] = 'FALSE'

    del expression[connectiveindex : connectiveindex + 2]

    return expression

#For NOT operator
def forNotOperator(variable):
    indexNot = variable.index('NOT')
    if (variable[indexNot + 1] == 'TRUE'):
        variable[indexNot + 1] = 'FALSE'
    else:
        variable[indexNot + 1] = 'TRUE'
    del variable[indexNot]

    return variable

#For IMPLY and EUQIAL
def forImplyEqualOperator(expression):
    if ('EQUAL' in expression and 'IMPLY' in expression):
        connectiveindex = min(expression.index('EQUAL'), expression.index('IMPLY'))
    elif ('EQUAL' in expression):
        connectiveindex = expression.index('EQUAL')
    else:
        connectiveindex = expression.index('IMPLY')

    connective = expression[connectiveindex]

    leftValue = expression[connectiveindex - 1]
    rightValue = expression[connectiveindex + 1]

    if (connective == 'EQUAL'):
        if (leftValue == rightValue):
            expression[connectiveindex - 1] = 'TRUE'
        else:
            expression[connectiveindex - 1] = 'FALSE'
    elif (connective == 'IMPLY'):
        if (leftValue == 'TRUE' and rightValue == 'FALSE'):
            expression[connectiveindex - 1] = 'FALSE'
        else:
            expression[connectiveindex - 1] = 'TRUE'
    else:
        print("Error connnective: ", connective)
        exit()

    del expression[connectiveindex : connectiveindex + 2]

    return expression

# handle the operators
def handingOperators(expression):

    if (len(expression) == 1):
        return expression

    while ('NOT' in expression):
        expression = forNotOperator(expression)

    while (('AND' in expression) or ('OR' in expression)):
        expression = forAndOrOperator(expression)

    while (('EQUAL' in expression) or ('IMPLY' in expression)):
        expression = forImplyEqualOperator(expression)

    return expression

#handling the bracket，until the first closing bracket is reached.
#findexIning the opening parenthesis preceding the closing one
def handingBrackets (expression):

    while (')' in expression):
        closeBrackets = expression.index(')')
        openBrackets = closeBrackets
        while (expression[openBrackets] != '('):
            openBrackets -= 1

        insideStatement = expression [openBrackets + 1 : closeBrackets]
        expression[openBrackets] = handingOperators(insideStatement)[0]
        del expression[openBrackets + 1 : closeBrackets + 1]

    return handingOperators(expression)

#Class for an object containing the name of the variable (P1, P2, etc.) and its value (True or False)
class propositionalVariables:
    def __init__(self, name, value):
        self.name = name
        self.value = value

#Parsing the propositional values entered by the user
def inputVariables (values):

    valList = []

    for i in range(len(values)):
        if (values[i] == '1' or values[i] == '0'):
            valList.append(values[i])
        else:
            print('Invalid input, we need to exit the program.')
            exit()

    #creating a list of objects of propositionalVariables class
    objectsList = []

    for i in range(len(valList)):
        objectsList.append(propositionalVariables(('P' + str(i + 1)), valList[i]))

    return objectsList

#Parsing the propositional sentence entered by the user
def truthValueInput (propVarList, statement):

    #splitting the input into values
    statement = statement.split()

    for i in range(len(propVarList)):
        while (propVarList[i].name in statement):
            indexIn = statement.index(propVarList[i].name)

            if (propVarList[i].value == '1'):
                statement[indexIn] = 'TRUE'
            else:
                statement[indexIn] = 'FALSE'

    return statement

#handling the propositional values entered by the user
#splitting the input into values
def getStatement(statement):
    statement = statement.split()

    return statement

#Get the number of variables
def getCount(values):
    valList = [] #handling the input and creating an array for values

    for i in range(len(values)):
        if(('P' in str(values[i])) & (values[i] not in valList) & (values[i] != 'IMPLY')):
            valList.append(values[i])

    count = len(valList)

    return count

#building the truth table
def truthTableConstruct (count, statement):

    rowNum = 2 ** count #The number of rows is determined.

    truthTableList = []

    for i in range(rowNum):
        #Converting the current number of row into a binary number and padding the binary number with as many 0-s as needed
        currNumInt = bin(i)[2:].zfill(rowNum)

        #Reversing the current number
        currNumStr = str(currNumInt)
        currNumStrLen = len(currNumStr)
        currNumSlicedStr = currNumStr[currNumStrLen::-1]

        intList = []
        objList = []

        #Putting all the values to a list
        for k in range (count):
            intList.append(currNumSlicedStr[k])

        #Creating a list of objects.
        for l in range(count):
            objList.append(propositionalVariables(('P' + str(l + 1)), intList[l]))
            print(objList[l].name, ' = ', objList[l].value)

        #Converting 0 and 1 to "True" or "False"
        this_statement = transform(objList, statement)

        #Parsing the statement to get the final value for the row
        this_output = handingBrackets(this_statement)

        print('-------------------------------------------')

        print('The truth value for row ', i, ' is ', this_output)
        print('-------------------------------------------')

        #Appending the row value to the final list of truth values
        truthTableList.append(this_output)

    return truthTableList

#Method to convert all 0-s and 1-s to "True" or "False"
def transform (objList, statement):
    #Processing this row and outputting its value.
    this_statement = statement.copy()
    for j in range (len(objList)):
        while (objList[j].name in this_statement):
            indexIn = this_statement.index(objList[j].name)

            if (objList[j].value == '1'):
                this_statement[indexIn] = 'TRUE'

            else:
                this_statement[indexIn] = 'FALSE'

    return this_statement

#Method to determine if all the row values are the same
def checkSame (truthTableList):
    first = truthTableList[0]
    for i in range(len(truthTableList)):
        if (truthTableList[i] != first):
            return False
    return True

#Method to determine if this is a Tautology, Contradiction or Contingency
def checkType (truthTableList):

    #Using method checkSame above
    checkSameBoo = checkSame (truthTableList)

    #If all the values in the list are the same, it is either Tautology or Contradiction
    if (checkSameBoo == True):
        if (truthTableList[0] == ['TRUE']):
                print('This sentence is Tautology')
        else:
                print('This sentence is Contradiction')
    else:
        print('This sentence is Contingency')

#For Q1
# main
print('This is for Question 1')
print('Please enter truth values for P1 P2..Pn')
print('1 for True and 0 for False without any spaces.')
print('Invalid input, like spaces the program will exit.')
question1 = input()
question1 = inputVariables(question1)

print('Please enter a sentence using P1 through P' + str(len(question1)))
print ('Please use NOT, AND, OR, IMPLY or EQUAL as operators only.')
print ('Please use whitespaces between variables and operators.')
print ('Invalid input, like spaces the program will exit.')
statement = input()
statement = truthValueInput(question1, statement)
output = handingBrackets(statement)
print('This statement is ', output)

# For Q2
print('This is for Q2')
print('Please enter a sentence using P1 through Pn.')
print ('Please use NOT, AND, OR, IMPLY or EQAL as operators. ')
print ('Please use bracket and whitespaces between variables n operators.')
statement = input()
statement = getStatement (statement)
variables_count = getCount(statement)
output = truthTableConstruct (variables_count, statement)
output = checkType(output)

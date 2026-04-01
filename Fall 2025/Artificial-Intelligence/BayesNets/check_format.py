import re
import sys

BASE_DIR = './'

values = {}
substitutions = {}

# Function to replace patterns in strings while preserving internal characters
# NOTE: Does not handle nested patterns with similar/repeating parts of the pattern (nested latex fractions for instance)
def replacePattern(string, pattern, replacementPattern) -> str:
    
    if len(pattern) == 0 or len(replacementPattern) == 0:
        print("PATTERN LENGTH 0")
        return string
    
    if len(pattern) != len(replacementPattern):
        print("PATTERN LENGTH MISMATCH")
        return string

    while True:
        indices = [0] * len(pattern)
        indices[0] = string.find(pattern[0])

        if indices[0] == -1:
            return string
        
        newString = string[0:indices[0]] + replacementPattern[0]
        
        for i in range(len(indices)):
            if i == 0:
                continue

            base = indices[i-1]
            offset = len(pattern[i-1])
            findIndex = base+offset
            indices[i] = string.find(pattern[i], findIndex)

            if indices[i] == -1:
                return string
        
            newString += string[findIndex:indices[i]] + replacementPattern[i]
    
        base = indices[-1]
        offset = len(pattern[-1])
        findIndex = base+offset
        string = newString + string[findIndex:]
        
        


def formatLine(line) -> str:
    # Make all lowercase
    formattedLine = line.casefold()

    # Remove/replace latex functions    
    formattedLine = formattedLine.replace("\\cdot", "*").replace("\\approx", '=')
    formattedLine = replacePattern(formattedLine, ["\\overline{", "}"], ["", "=f"])
    formattedLine = replacePattern(formattedLine, ["\\frac{", "}{", "}"], ["((", ")/(", "))"])

    # Only allow expeted characters in the string
    formattedLine = re.sub(r"[^ptfmwvhcu0-9.()=+*-/|]+", "", formattedLine)

    # Add space delimiters back in where expected
    formattedLine = formattedLine.replace("+", " + ")\
                                .replace("-", " - ")\
                                .replace("/", " / ")\
                                .replace("*", " * ")\
                                .replace(")p", ") * p")\
                                .replace("=", " = ")\
                                .replace(" = t", "=t")\
                                .replace(" = f", "=f")
    return formattedLine
    



def parseLine(line):
    
    formattedLine = formatLine(line)

    # Separate the LHS and RHS of the equation
    splitLine = formattedLine.split(r" = ")

    # If the equation is missing either side of the equation, do not continue processing the line
    if len(splitLine) < 2 or splitLine[0] == '' or splitLine[1] == '':
        print(f"INVALID LINE: {line.strip()}")
        return
    elif len(splitLine) > 2:
        print(f"WARNING: The line '{line.strip()}' has multiple equalities on it. The middle equalities are being ignored, so the autograder sees it as: {splitLine[0]} = {splitLine[-1]}.")

    # Determine if the line is a value assignment or a substitution for another expression of probabilities
    try:
        float(splitLine[-1])
        isValue = True
    except ValueError:
        isValue = False
    
    # Sort the line into the correct dict based on type of equation
    if isValue:
        values[splitLine[0]] = splitLine[-1]
    else:
        substitutions[splitLine[0]] = splitLine[-1]


def processFile(filepath, goalProbability=None):
    with open(filepath, 'r') as file:
        for line in file:
            parseLine(line)

    # Check Goal Probability
    if goalProbability != None:

        # Check for illegal characters
        illegalChars = re.findall(r"[^ptfmwvhcu0-9.()=+*-/|]+", goalProbability.casefold())
        if len(illegalChars) > 0:
            print(f"The following characters are not allowed in the goal probability: {illegalChars}")


        formattedGoalProbability = formatLine(goalProbability)

        # Ensure at least 1 valid variable used in the expression
        varsUsed = re.findall(r"[mwvhcu]+", formattedGoalProbability)
        if len(varsUsed) == 0:
            print("Goal Probability must use at least 1 variable (m, w, v, h, c, u)")

        # Ensure every variable has a T/F assignment in the goal expression
        missingEqualities = re.findall(r'[mwvhcu]+(?!=t|=f)', formattedGoalProbability)
        if len(missingEqualities) != 0:
            # Missing '=t' or '=f' on any variable in the expression
            print(f"Goal Probability is missing variable assignment on the following variables (ensure every variable has '=t' or '=f' after it): {missingEqualities}")


        # Ensure all probabilities are expanded to givens

        # Get the student's equation for the goal probability
        if formattedGoalProbability in substitutions:
            workingExpression = substitutions[formattedGoalProbability]

            # Follow the student's reasoning down to the lowest level, substituting more complex probabilities with simpler ones until no changes are made in a full pass
            isDirty = True
            while isDirty:

                isDirty = False

                # Find all probabilities we could substituting
                probabilities = re.findall(r"p\([mwvhcu=tf,|]+\)", workingExpression)
                
                # Try to substitute each found probability to an expression of simpler probabilities
                for probability in probabilities:
                    if probability in substitutions:
                        workingExpression = workingExpression.replace(probability, "( " + substitutions[probability] + " )")
                        isDirty = True


            ### Ensure the expanded form only uses givens and not higher-level expressions
            simplifiedProbabilities = set(re.findall(r"p\([mwvhcu=tf,|]+\)", workingExpression))
            print("\n\n The following are the simplified probabilities of the submission. Double check that they are all givens and not a higher-level expression. Make sure all expressions are expanded such that the final probability expressions are only the givens:")
            for expression in simplifiedProbabilities:
                print(expression)
            print()

        else:
            print("Goal Probability does not have a substitution/probability expression equivalence in the submission")



    # Ensure all probabilities used in substitutions have a value assigned to them in a separate statement
    noValueSet = set()
    for key in substitutions:
        if key not in values:
            noValueSet.add(key)

        probabilities = re.findall(r"p\([mwvhcu=tf,|]+\)", substitutions[key])
        for probability in probabilities:
            if probability not in values:
                noValueSet.add(probability)
    
    if len(noValueSet) != 0:
        print("The following probabilities do not have values assigned to them in the answer file:")
        for probability in noValueSet:
            print(probability)
        print()

    


# Run the checking program
if len(sys.argv) != 2 and len(sys.argv) != 3:
    print(f"Usage: python3 {sys.argv[0]} <input_file> '<optional:goal_probability_expression>'")
    sys.exit(1)
    
allowedSubmissionFiles = [f'part1_{i+1}.txt' for i in range(6)]

if sys.argv[1] not in allowedSubmissionFiles:
    print(f"{sys.argv[1]} is not an allowed submission file. The correct submission files follow 'part1_X.txt' format where X is the question number (1-6).")

if len(sys.argv) == 3:
    processFile(sys.argv[1], sys.argv[2])
else:
    processFile(sys.argv[1])
    
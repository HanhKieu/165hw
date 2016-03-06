def intChecker(inputString):
    if inputString.startswith('-') and inputString[1:].isdigit():
        return True
    elif inputString.isdigit():
        return True
    return False

def floatChecker(inputString):
    try:
        myValue = float(inputString)
    except ValueError:
        return False
    if myValue.is_integer():
        return False
    else:
        return True

def charChecker(inputString):
    return not(intChecker(inputString)) and not(floatChecker(inputString))
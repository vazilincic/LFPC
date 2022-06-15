# Function for partition
def parts(state):
    first = state[0]
    der = state.index('-')
    second = state[der + 1:]
    return first, second


# Checking if symbol is in map
def exists(key):
    if dict_of_rules.get(key) is not None:
        return True
    else:
        return False


# Recording rules
array_of_rules = []
print("Enter your rules: ")
while True:
    s = input()
    array_of_rules.append(s)
    print("One more?(n/no)")
    p = input()
    if p.lower() == 'n' or p.lower() == 'no':
        break

# Filling map with rules
dict_of_rules = {}
for rule in array_of_rules:
    f, s = parts(rule)

    if not exists(f):
        dict_of_rules[f] = []  # Creating array to save more than one word

    dict_of_rules[f].append(s)


# Algorithm for finding words
def replace(char): # Chars S, A, B and so on
    for rule in dict_of_rules.values():  # Here rule = [aP, asd] for example
        for j in range(len(rule)):
            if char in rule[j]:  # If char is in word
                ind = rule[j]  # ind is a string
                s = ind[:-1]  # cut off the last char
                arr_in_dict = len(dict_of_rules.get(char))
                for i in range(arr_in_dict):
                    rule.append(s + dict_of_rules.get(char)[i])  # creating word


# arr_reverse contains non-terminal symbols
arr_reverse = []
for ch in dict_of_rules.keys():
    arr_reverse.append(ch)

# it is necessary to reverse array for algorithm
for ch in arr_reverse[::-1]:
    replace(ch)

# For more results algorithm can be used 1 more time but no more than 2
for ch in arr_reverse[::-1]:
    replace(ch)


# Entering string
while True:
    choose = input("Do you want to enter string?(n/no) ")

    if choose.lower() == 'n' or choose.lower() == 'no':
        break

    word = input("Enter your string: ")
    if word in dict_of_rules.get('S') or dict_of_rules.get('P') or dict_of_rules.get('Q'):
        print("Accepted")
    else:
        print("Denied")

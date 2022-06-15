import pandas as pd


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


# finds all firsts of nonterminal
def first(nonterminal):
    firsts = set()
    for rule in dict_of_rules[nonterminal]:
        firsts.add(rule[0])

    firsts1 = set()

    for i in firsts:
        if i in dict_of_rules:
            for rule in dict_of_rules[i]:
                firsts1.add(rule[0])
        else:
            firsts1.add(i)
    firsts = firsts.union(firsts1)

    firsts1 = set()

    for i in firsts:
        if i in dict_of_rules:
            for rule in dict_of_rules[i]:
                firsts1.add(rule[0])
        else:
            firsts1.add(i)

    firsts = firsts.union(firsts1)
    return firsts


# finds all lasts of nonterminal
def last(nonterminal):
    lasts = set()
    for rule in dict_of_rules[nonterminal]:
        lasts.add(rule[-1])

    lasts1 = set()

    for i in lasts:
        if i in dict_of_rules:
            for rule in dict_of_rules[i]:
                lasts1.add(rule[-1])
        else:
            lasts1.add(i)
    lasts = lasts.union(lasts1)

    lasts1 = set()

    for i in lasts:
        if i in dict_of_rules:
            for rule in dict_of_rules[i]:
                lasts1.add(rule[-1])
        else:
            lasts1.add(i)

    lasts = lasts.union(lasts1)
    return lasts


# Equals rule(Ae -> A=e)
def equal_rule():
    array_of_equals = []
    for non in dict_of_rules:
        for rule in dict_of_rules[non]:
            if len(rule) > 1:
                for i in range(1, len(rule)):
                    new_string = rule[i - 1] + '=' + rule[i]
                    array_of_equals.append(new_string)
    return array_of_equals


# Terminal or nonterminal by nonterminal rule (aA or BA, a,B < First(A))
def t_or_n_by_non():
    smaller_rule = {}
    for non in dict_of_rules:
        for rule in dict_of_rules[non]:
            for i in range(1, len(rule)):
                if rule[i].isupper() and (rule[i - 1].islower() or rule[i - 1].isupper()):
                    smaller_rule[rule[i - 1]] = ['<']
                    smaller_rule[rule[i - 1]].append(first_last_table["First"][rule[i]])

    return smaller_rule


# Nonterminal by terminal rule (Ab, Last(A) > b)
def non_by_terminal():
    bigger_rule = {}
    for non in dict_of_rules:
        for rule in dict_of_rules[non]:
            for i in range(1, len(rule)):
                if rule[i].islower() and rule[i - 1].isupper():
                    variable = list(first_last_table["Last"][rule[i - 1]])[0]
                    if variable not in bigger_rule:
                        bigger_rule[variable] = ['>']
                        bigger_rule[variable].append(rule[i])
                    else:
                        bigger_rule[variable].append(rule[i])

    return bigger_rule


# Nonterminal by Nonterminal (AB, Last(A) > First(B))
# There is a problem with implementing this rule
"""
def non_by_non():
    bigger_rule = {}
    for non in dict_of_rules:
        for rule in dict_of_rules[non]:
            for i in range(1, len(rule)):
                if rule[i-1].isupper() and rule[i].isupper():
                    l = first_last_table["Last"][rule[i-1]]
                    bigger_rule[l] = ['>']
                    bigger_rule[l].append(first_last_table["First"][rule[i]])

    return bigger_rule
"""

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

non_terminals = set()
terminals = set()
for non in dict_of_rules:
    non_terminals.add(non)
    for rule in dict_of_rules[non]:
        for char in rule:
            if char.islower():
                terminals.add(char)

# All nons and terminals from rules
all_syms = non_terminals.union(terminals)
all_syms.add('$')
all_syms = sorted(all_syms)

# Creating first last table
first_last_table = {"First": {}, "Last": {}}

for rule in dict_of_rules:
    first_last_table["First"][rule] = set()
    first_last_table["Last"][rule] = set()

for rule in dict_of_rules:
    firsts = first(rule)
    lasts = last(rule)

    first_last_table["First"][rule] = firsts
    first_last_table["Last"][rule] = lasts

# Creating Simple Precedence Matrix
simple_precedence_matrix = {}
for non in all_syms:
    simple_precedence_matrix[non] = {}
    for non1 in all_syms:
        if non == '$' and non1 == '$':
            simple_precedence_matrix[non][non1] = ''
        elif non == '$':
            simple_precedence_matrix[non][non1] = '<'
        elif non1 == '$':
            simple_precedence_matrix[non][non1] = '>'
        else:
            simple_precedence_matrix[non][non1] = ''

# Putting into matrix '='
array = equal_rule()
for string in array:
    d = {string[2]: string[1]}
    simple_precedence_matrix[string[0]].update(d)

# Putting into matrix '<'
smaller_arr = t_or_n_by_non()
for line in smaller_arr:
    for symbol in smaller_arr[line]:
        if symbol == '<':
            pass
        else:
            for column in symbol:
                simple_precedence_matrix[line][column] = '<'

# Putting into matrix '>'
bigger_arr = non_by_terminal()
for line in bigger_arr:
    for symbol in bigger_arr[line]:
        if symbol == '>':
            pass
        else:
            for column in symbol:
                simple_precedence_matrix[line][column] = '>'

# Word Parsing
word = input("Enter the word: ")
new_string = ''
word += '$'
word = word[::-1]
word += '$'
word = word[::-1]
for i in range(1, len(word)):
    new_string += word[i - 1] + simple_precedence_matrix[word[i - 1]][word[i]]

new_string += '$'

print(new_string)

# Parsing Algorithm
while len(new_string) != 5 and new_string[2] != 'S':
    array_of_lits = [i for i, ltr in enumerate(new_string) if ltr == '<']  # finds all indexes of all '<'
    array_of_bigs = [i for i, ltr in enumerate(new_string) if ltr == '>']  # finds all indexes of all '>'
    minimum = 99
    a = 0
    b = 99
    for i in array_of_lits:
        for k in array_of_bigs:
            if minimum > k - i > 0 and i < k:
                minimum = abs(i - k)
                a, b = i, k

    if minimum == 2:
        character = new_string[a + 1:b]
        for non in non_terminals:
            for rule in dict_of_rules[non]:
                if rule == character:
                    new_string = list(new_string)
                    new_string[a] = simple_precedence_matrix[new_string[a - 1]][non]
                    new_string[a + 1] = non
                    new_string[b] = simple_precedence_matrix[non][new_string[b + 1]]
                    new_string = ''.join(new_string)
                    minimum = 99

    elif minimum == 4:
        line = new_string[a:b + 1]
        line2 = line.replace(line[2], '')
        new_string = new_string.replace(line, line2, 1)
        for non in non_terminals:
            for rule in dict_of_rules[non]:
                if rule == line2[1:3]:
                    new_string = list(new_string)
                    new_string[a] = simple_precedence_matrix[new_string[a - 1]][non]
                    new_string[a + 1:b - 1] = non
                    new_string[b - 2] = simple_precedence_matrix[non][new_string[b - 1]]
                    new_string = ''.join(new_string)
                    minimum = 99

    elif minimum == 6:
        line = new_string[a:b + 1]
        line2 = line.replace(line[2], '')
        new_string = new_string.replace(line, line2, 1)
        for non in non_terminals:
            for rule in dict_of_rules[non]:
                if rule == line2[1:4]:
                    new_string = list(new_string)
                    new_string[a] = simple_precedence_matrix[new_string[a - 1]][non]
                    new_string[a + 1:b - 2] = non
                    new_string[b - 4] = simple_precedence_matrix[non][new_string[b - 3]]
                    new_string = ''.join(new_string)
                    minimum = 99

    elif minimum == 8:
        line = new_string[a:b + 1]
        line2 = line.replace(line[2], '')
        new_string = new_string.replace(line, line2, 1)
        for non in non_terminals:
            for rule in dict_of_rules[non]:
                if rule == line2[1:5]:
                    new_string = list(new_string)
                    new_string[a] = simple_precedence_matrix[new_string[a - 1]][non]
                    new_string[a + 1:b - 3] = non
                    new_string[b - 6] = simple_precedence_matrix[non][new_string[b - 5]]
                    new_string = ''.join(new_string)
                    minimum = 99

    else:
        print("I think it is infinite loop! Your word is not accepted")
        break

    print(new_string)

else:
    print("Word is accepted")

df = pd.DataFrame(simple_precedence_matrix).T  # for pretty output of SPM
print(df)

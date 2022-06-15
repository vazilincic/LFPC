import pandas as pd

# Taking NFA input from User

nfa = {}
n = int(input("No. of states : "))  # Enter total no. of states
t = int(input("No. of transitions : "))  # Enter total no. of transitions/paths eg: a,b so input 2 for a,b,c input 3
for i in range(n):
    state = input("state name : ")  # Enter state name eg: A, B, C, ..etc
    nfa[state] = {}  # Creating a nested dictionary
    for j in range(t):
        path = input("path : ")  # Enter path eg : a or b in {a,b} 0 or 1 in {0,1}
        print("Enter end state from state {} travelling through path {} : ".format(state, path))
        reaching_state = [x for x in input().split()]  # Enter all the end states that
        nfa[state][path] = reaching_state  # Assigning the end states to the paths in dictionary

print("\nNFA :- \n")
print(nfa)  # Printing NFA
print("\nPrinting NFA table :- ")
nfa_table = pd.DataFrame(nfa)
print(nfa_table.transpose())

print("Enter final state of NFA : ")
nfa_final_state = [x for x in input().split()]  # Enter final state/states of NFA

dfa = {}  # dfa dictionary
nfa_keys = list(nfa.keys())  # all states in nfa
dfa[nfa_keys[0]] = nfa.get(nfa_keys[0])  # take the initial state
dfa_keys = list(dfa.keys())  # dfa states
all_states = dfa.get(nfa_keys[0]).values()  # all states from initial state
all_states = list(all_states)
in_transitions = {}  # just for simulate transitions
for i in all_states:
    try:  # because it can be absented states in paths
        dfa_keys = list(dfa.keys())
        if i[0] not in dfa_keys and i[0][::-1] not in dfa_keys:  # checks if state is not repeating
            for j in i[0]:
                transitions = list(nfa.get(j).keys())  # it is paths like a, b
                for k in transitions:
                    if k not in in_transitions:
                        in_transitions[k] = nfa.get(j).get(k)  # adding transition
                    else:
                        if len(nfa.get(j).get(k)) != 0:  # checks if it is not empty state
                            for char in nfa.get(j).get(k)[0]:  # it takes each char from state
                                if len(in_transitions[k]) == 0:  # symbol '^' will replace None
                                    in_transitions[k] = ['^']  # if transition is empty add '^'
                                    if char not in in_transitions[k][0]:
                                        in_transitions[k] = [in_transitions[k][0] + nfa.get(j).get(k)[0]]  # adding new state
                                        in_transitions[k] = [in_transitions[k][0].replace('^', '')]  # deleting '^'
                                else:
                                    if char not in in_transitions[k][0]:
                                        in_transitions[k] = [in_transitions[k][0] + nfa.get(j).get(k)[0]]
                                        in_transitions[k] = [in_transitions[k][0].replace('^', '')]
                        else:
                            continue

        else:
            continue

        dfa[i[0]] = in_transitions  # adding in dfa table new transitions
        arr_dfa = list(dfa.get(i[0]).values())  # it is all states from updated dfa
        for st in arr_dfa:
            if st not in all_states:
                all_states.append(st)  # if appear new state in dfa it goes to check
        in_transitions = {}  # resetting transitions

    except:
        continue

final_states = []
print(in_transitions)
dfa_table = pd.DataFrame(dfa)
print(dfa_table.transpose())
dfa_keys = list(dfa.keys())
for dk in dfa_keys:
    for fs in nfa_final_state:
        if (fs in dk or fs is dk) and fs not in final_states:  # finds final states
            final_states.append(dk)

print("Final States are: ", final_states[:])

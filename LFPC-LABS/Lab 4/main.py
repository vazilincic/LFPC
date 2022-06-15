rules = {"S" : {"aB", "bA", "A"}, "A" : {"B", "Sa", "bBA", "b"},
         "B" : {"b", "bS", "aD", "$"}, "D":{"AA"}, "C":{"Ba"}}

keys = list(rules.keys())


def check_for_epsilon(rules):
    is_epsilon = False
    epsilon = 0
    for key in keys:

        if "$" in rules[key]:
            is_epsilon = True
            epsilon = key
            rules[key].remove("$")

    return is_epsilon, epsilon


def count_of_eps(string, epsilon):
    count = 0
    for ch in string:
        if ch == epsilon:
            count += 1
    return count


def check_for_unit(rules):
    are_units = False
    unit_add = ''
    unit_from = ''
    for key in keys:
        for node in rules[key]:
            if len(node) == 1 and node.isupper():
                are_units = True
                unit_add = key
                unit_from = node
                rules[key].remove(node)
                return are_units, unit_add, unit_from
    return are_units, unit_add, unit_from


def is_unaccessible(rules, variable):
    unaccessible = True
    for check_in in keys:
        for node in rules[check_in]:
            if variable in node:
                unaccessible = False

    return unaccessible


is_eps, eps = check_for_epsilon(rules)
while is_eps:
    for k in keys:
        for node in rules[k].copy():
            if len(node) > 1 and eps in node and count_of_eps(node, eps) == 1:
                rules[k].add(node.replace(eps, ''))
            elif len(node) > 1 and eps in node and count_of_eps(node, eps) == 2:
                rules[k].add(node.replace(eps, '', 1))
                rules[k].add(node[::-1].replace(eps, '', 1)[::-1])
            elif len(node) == 1 and eps in node:
                rules[k].add(node.replace(eps, '$'))
                rules[k].remove(node)

    is_eps, eps = check_for_epsilon(rules)

are_units, unit_add, unit_from = check_for_unit(rules)
while are_units:
    for node in rules[unit_from]:
        rules[unit_add].add(node)

    are_units, unit_add, unit_from = check_for_unit(rules)


for k in keys:
    if is_unaccessible(rules, k):
        rules.pop(k, None)


keys = list(rules.keys())
substitution = {"a": "X1", "b": "X2", "X2B": "Y1"}
subs_keys = list(substitution.keys())

for key in keys:
    for node in rules[key]:
        if len(node) == 2 and not node.isupper() and not node.islower():
            for ch in node:
                if ch.islower():
                    new_node = node.replace(ch, substitution[ch])
                    rules[key].remove(node)
                    rules[key].add(new_node)
                    break
        elif len(node) == 3 and node[:2] not in substitution.values() and node[:2] in subs_keys:
            new_node = node.replace(node[:2], substitution[node[:2]])
            rules[key].remove(node)
            rules[key].add(new_node)

        elif len(node) == 3 and node[:2] not in substitution.values() and node[:2] not in subs_keys:
            new_node = node.replace(node[:2], substitution[node[0]] + node[1])
            new_node1 = new_node.replace(new_node[:3], substitution[new_node[:3]])
            rules[key].remove(node)
            rules[key].add(new_node1)


for k in substitution.keys():
    if k not in rules:
        rules[k] = {substitution.get(k)}
    elif k in rules:
        rules[k].add(substitution.get(k))

print(rules)

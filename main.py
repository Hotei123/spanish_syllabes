vowels = ['a', 'e', 'i', 'o', 'u']
single_consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'l', 'm', 'n', 'ñ', 'p', 'q', 'r', 's', 't', 'v', 'x', 'z']
syllabes = []

for c in single_consonants:
    for v in vowels:
        syllabe = c + v
        if syllabe.startswith('q'):
            if not (syllabe.endswith('e') or syllabe.endswith('i')):
                continue
            else:
                syllabe = syllabe[0] + 'u' + syllabe[1]
        if syllabe[0] in ['h', 'x', 'w', 'y',]:
            continue
        syllabes.append(syllabe)

syllabes.extend([str(i) for i in range(1, 10)])

print(syllabes)
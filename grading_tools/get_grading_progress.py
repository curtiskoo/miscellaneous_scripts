import os
from pprint import pprint
import re
import sys

path = sys.argv[1]
owd = os.getcwd()
os.chdir(path)
print(os.getcwd())
text = ''
#print(os.listdir())
dirs = list(filter(lambda x: os.path.isdir(x) and 'solution' not in x, os.listdir()))
#print(dirs)
print(len(dirs))


def get_grade(text, p=None):
    text = text.split('\n')
    if p != None:
        pprint(text)
        print('{}\n\n'.format('='*20))
    text = list(map(lambda x: x[x.find('#'):], text))
    text = list(filter(lambda x: x != '', text))
    # pprint(text)
    # regex = '#"(.+?)"'

    text2 = []
    acc = False
    grade = None
    for x in text:
        # find = re.findall(regex, x)
        if x[:1] == '#':
            find = x[1:]
            # print(find)
            f_index = find.find('"') + 1
            e_index = find.rfind('"')
            find = find[f_index:e_index]
            # print(find)
            if ';; *** GRADE: ' in find:
                try:
                    grade = find.split()[len(find.split()) - 1]
                    #print(text)
                except:
                    print(x, find.split(), len(find.split()))
                    raise IndexError
                text2.append(find)
                acc = True
                # print(grade)
                if p == None:
                    return grade
                    continue
            if find == '\\n':
                find = '\n'
            if acc == True:
                text2.append(find)

    # pprint(text2)
    #print('here')
    s = ''.join(text2)
    s = s.replace('\\"', '"')
    s = s.replace('\\', '@@##$$')
    s = s.split('\n')
    s = list(filter(lambda x: '@@##$$' not in x and '(#(struct' not in x, s))
    s = '\n'.join(s)
    print(s)


acc = 0
d = 0
dic = {}
for x in dirs:
    if os.path.isdir(x):
        text = open(os.path.join(x, os.listdir(x)[0])).read()
        # print(x)
        grade = get_grade(text)
        if len(sys.argv) > 2:
            if sys.argv[2] == x:
                print('Looking for: {}'.format(x))
                s = get_grade(text, True)
        if grade == None:
            grade = '0'
        if grade == '##':
            pass
        else:
            d += 1
        dic[x] = grade
        acc += 1
        # print(x, grade)
for x in sorted(dic.keys()):
    print(x, dic[x])

#if len(sys.argv) > 2:


print('{}/{} {}% Done'.format(d, acc, round(d / acc * 100, 2)))
os.chdir(owd)


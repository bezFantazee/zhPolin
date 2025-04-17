# функция для расчета значения выражения в постфиксной записи
def postfix_counting(a, b, c):
    steck=[]
    for i in range(len(pfix)):
        if pfix[i].isalpha():
            if pfix[i] == 'a':
                steck.append(a)
            if pfix[i] == 'b':
                steck.append(b)
            if pfix[i] == 'c':
                steck.append(c)
        #инверсия
        elif pfix[i] == '!':
            if steck[-1] == 1:
                steck[-1] = 0
            else:
                steck[-1] = 1
        elif pfix[i] in operations and pfix[i] != '!':
            #конъюнкция
            if pfix[i] == '*':
                res = steck[-1] * steck[-2]
            #дизъюнкция
            elif pfix[i] == '+':
                if steck[-1] == 1 or steck[-2] == 1:
                    res = 1
                else:
                    res = 0
            #импликация
            elif pfix[i] == '->':
                if steck[-2] == 1 and steck[-1] == 0:
                    res = 0
                else:
                    res = 1
            #эквивалентность
            elif pfix[i] == '==':
                if steck[-1] == steck[-2]:
                    res = 1
                else:
                    res = 0
            #исключающее или
            elif pfix[i]=='^':
                if steck[-1] == steck[-2]:
                    res = 0
                else:
                    res = 1
            #или-не
            elif pfix[i] == '|':
                if steck[-1] == 0 and steck[-2] == 0:
                    res = 1
                else:
                    res = 0
            #добавление результата
            steck.pop(-1)
            steck.pop(-1)
            steck.append(res)
    return steck[0]


#функция преобразования выражения в постфиксную запись
def postfix_not(infix_tok):
    brackets = ['(', ')']
    postfix_tok = []
    stack = []
    prev_type = 'op' #маркировка предыдущей операции

    for t in infix_tok:
        if t.isalpha():
            if prev_type == 'var':
                return ['WRONG']
            postfix_tok.append(t)
            prev_type = 'var'
        elif t in operations:
            if prev_type != 'var' and t != '!':
                return ['WRONG']
            if t == '!' and prev_type == 'var':
                return ['WRONG']
            while len(stack) > 0 and ((t == '!' and stack[-1]=='!')
                                    or (t == '*' and stack[-1] in operations[5:])
                                    or (t == '+' and stack[-1] in operations[4:])
                                    or (t == '->' and stack[-1] in operations[3:])
                                    or (t == '==' and stack[-1] in operations[2:])
                                    or (t == '^' and stack[-1] in operations[1:])
                                    or (t == '|' and stack[-1] in operations)):
                postfix_tok.append(stack.pop())
            stack.append(t)
            prev_type = 'op'

        elif t in brackets:
            if t == '(':
                if prev_type == 'var':
                    return ['WRONG']
                stack.append(t)
                prev_type = 'br'
            else:
                while len(stack) > 0 and stack[-1] != '(':
                    postfix_tok.append(stack.pop())
                if len(stack) == 0:
                    return ['WRONG']
                stack.pop()
        else:
            return ['WRONG']

    if prev_type != 'var':
        return ['WRONG']

    while len(stack) > 0:
        if stack[-1] == '(':
            return ['WRONG']
        postfix_tok.append(stack.pop())

    return postfix_tok


#функция для расчета полиндрома жигалкина
def calculateZhPolyn(ans):
    for i in range(1, 8):
        for j in range(8-i):
            res = ans[i-1][j] + ans[i-1][j+1]
            if res > 1:
                res = 0
            ans[i].append(res)
    for i in range(8):
        if ans[i][0] == 1:
            if matrix[0][i] == 1:
                zhPolyn.append('a')
            if matrix[1][i] == 1:
                zhPolyn.append('b')
            if matrix[2][i] == 1:
                zhPolyn.append('c')
            if matrix[0][i] == 0 and matrix[1][i] == 0 and matrix[2][i] == 0:
                zhPolyn.append('1')
            zhPolyn.append('^')
    zhPolyn.pop()


mas = input() #ввод выражения в качестве переменных должны выступать a, b, c
symbols = ['|', '==', '->', '+', '*', '(', ')', '!', '^', 'a', 'b', 'c']
for c in symbols:
    mas = mas.replace(c, ' '+c+' ')  #добавление пробелов

operations = ['|', '^', '==', '->', '+', '*', '!']
pfix = postfix_not(mas.split())

if len(pfix) == 1:  #проверка на наличие ошибки
    print(pfix[0])
else:
    matrix = [[0,0,0,0,1,1,1,1], [0,0,1,1,0,0,1,1], [0,1,0,1,0,1,0,1]] #значение переменных
    ans = []
    for i in range(8):
        ans.append([])
    #цикл для расчета значений в таблице истинности
    for j in range(len(matrix[0])):
        ans[0].append(postfix_counting(matrix[0][j], matrix[1][j], matrix[2][j]))

    print("Таблица истинности:\na | b | c | F")
    for i in range(len(matrix[0])):
        print(matrix[0][i], '|', matrix[1][i], '|', matrix[2][i], '|', ans[0][i])

    zhPolyn = []  #полиндром жигалкина
    calculateZhPolyn(ans)
    print(*zhPolyn)


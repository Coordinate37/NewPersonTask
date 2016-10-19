import re
import math
import sys

def CalPlusMinus(data, op_list):
    result = data[0]
    for i in range(len(op_list)):
        if op_list[i] == 'p':
            result += data[i+1]
        else:
            result -= data[i+1]

    return result

def CalMulDiv(data, op_list):
    result = float(data[0])
    for i in range(len(op_list)):
        if op_list[i] == '*':
            result *= data[i+1]
        else:
            try:
                result /= data[i+1]
            except ZeroDivisionError, e:
                print "Error:%s", e
                sys.exit()

    return result

def CalPow(data, op_list):
    result = float(data[0])
    for i in range(len(op_list)):
        if op_list[i] == '^':
            result = math.pow(result, data[i+1])
    
    return result

def CalSqrTri(data, op_list):
    result = float(data)
    for i in range(len(op_list)):
        if op_list[i] == 'v':
            result = math.sqrt(result)
        elif op_list[i] == 'sin':
            result = math.sin(result)
        else:
            result = math.cos(result)

    return result

def CalFac(data, op_list):
    result = float(data)
    if len(op_list) and result != int(result):
        return None
    for i in range(len(op_list)):
        result = math.factorial(result) 

    return result

def Calculate1(formula):  
    if formula.endswith("+") or formula.endswith("-"):
        return "Invalid formula"
    op_list = re.findall('!', formula)
    data = formula.replace('!', '')
    data = data.replace('+-', '-')
    data = data.replace('--', '')
    return CalFac(data, op_list)

def Calculate2(formula):
    if formula.endswith("sin") or formula.endswith("cos") or formula.endswith("v"):
        return "Invalid formula"
    op_list = re.findall('v|sin|cos', formula)
    data = re.sub('v|sin|cos', '', formula)
    data = Calculate1(data)
    if type(data) == type(''):
        return data
    return CalSqrTri(data, op_list)

def Calculate3(formula):
    op_list = re.findall('\^', formula)
    data = re.split('\^', formula)

    for i in range(len(data)):
        if data[i] == '':
            return "Invalid formula!"
        data[i] = Calculate2(data[i])
        if type(data[i]) == type(''):
            return data[i]

    return CalPow(data, op_list)

def Calculate4(formula):
    op_list = re.findall('[*/]', formula)
    data = re.split('[*/]', formula)

    for i in range(len(data)):
        if data[i] == '':
            return "Invalid formula!"
        data[i] = Calculate3(data[i])
        if type(data[i]) == type(''):
            return data[i]

    return CalMulDiv(data, op_list)

def Calculate5(formula):
    #print formula
    op_list = re.findall('[pm]', formula)
    data = re.split('[pm]', formula)
    #print data
    for i in range(len(data)):
        data[i] = Calculate4(data[i])
        if type(data[i]) == type(''):
            return data[i]

    return CalPlusMinus(data, op_list)

def ParseBracket(data_with_bracket):
    pi_value = repr(math.pi)
    data_with_bracket = data_with_bracket.replace('pi', pi_value)
    while data_with_bracket.count('(') > 0:
        first_right_bracket = data_with_bracket.index(')')
        left_bracket = data_with_bracket[0:first_right_bracket].rindex('(')
        data_in_bracket = data_with_bracket[left_bracket+1:first_right_bracket]
        m = re.search('[0-9!][+-][0-9scv+-]', data_in_bracket)
        while m is not None:
            op = m.group()
            if op[1] == '+':
                data_in_bracket = data_in_bracket.replace(op, op[0] + 'p' + op[2])
            else:
                data_in_bracket = data_in_bracket.replace(op, op[0] + 'm' + op[2])
            m = re.search('[0-9!][+-][0-9scv+-]', data_in_bracket)
        value = str(Calculate5(data_in_bracket))
        if not value.isdigit():
            return value

        data_with_bracket = data_with_bracket.replace(data_with_bracket[left_bracket:first_right_bracket+1], value)

    return Calculate5(data_with_bracket)

def main():
    while True:
        user_input = raw_input('>>>:').strip('*')
        user_input = user_input.replace(' ', '').strip('/')
        usre_input = user_input.replace('--', '+').strip('^')
        user_input = re.sub('\++', '+', user_input)
        user_input = re.sub('\*+', '*', user_input)
        user_input = re.sub('/+', '/', user_input)
        user_input = re.sub('\^+', '^', user_input)
        if len(user_input) == 0:
            continue
        user_input = '(' + user_input + ')'
        print ParseBracket(user_input)

if __name__ == '__main__':
    main()

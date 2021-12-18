import re

def checkEmail(email):
    regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    if(re.search(regex, email)):
        return True
    return False


def checkPhone(phone):
    regex = '^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]{9}$'
    if(re.search(regex, phone)):
        return True
    return False

def checkName(name):
    regex='^[^0-9_!¡?÷?¿/\\+=@#$%ˆ&*(){}|~<>;:[\]]{2,}$'
    if(re.search(regex, name)):
        if(len(name)>2):
            return True
    return False


def checkAge(age):
    regex = '^\d*$'
    if (re.search(regex, age)):
        a = int(age)

        if (a < 66 and a > 17):
            return True
    return False
# print(checkAge(""))
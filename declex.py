import sys
import re
buffer = ""
global state
state= 0
operators = r'[+\-*%<>=!&|!;,.[](){}]'
keyword_dict = {"break":'T_BREAK',"case":'T_CASE',"continue":'T_CONTINUE',"delete":'T_DELETE',"do":'T_DO',"else":'T_ELSE',"for":'T_FOR',"function":'T_FUNCTION',"if":'T_IF',"new":'T_NEW',"return":'T_RETURN',"bool":'T_BOOLTYPE',"void":'T_VOID',"while":'T_WHILE',"class":'T_CLASS',"const":'T_CONST',"extends":'T_EXTENDS',"implements":'T_IMPLEMENTS',"interface":'T_INTERFACE',"this":'T_THIS',"true":'T_TRUE',"false":'T_FALSE',"null":'T_NULL',"int":'T_INTTYPE',"double":'T_DOUBLE',"print":'T_PRINT', "extern":'T_EXTERN'}
operators_dict = {'+':"T_PLUS" ,  '-':"T_MINUS" , '*':"T_MULT" , '/':"T_DIV" , '%':"T_PER" ,'<':"T_GT" , '<=':"T_GEQ" ,  '>':"T_LT" , '>=':"T_LEQ" , '=':"T_ASSIGN" , '==':"T_EQ" , '!=':"T_NEQ" ,  '&&':"T_AND" ,  '||':"T_OR" , '!':"T_NOT" ,  ';':"T_SEMICOLON"  ,  '.':"T_DOT" ,  '[':"T_LSB" ,  ']':"T_RSB" ,  '(':"T_LPAREN",   ')':"T_RPAREN" , '{':"T_LCB" , '}':"T_RCB"}
state_token = ""
state_value = ""
out_buffer = ""
def state_0(position, state): #start
    global state_value
    global state_token
    global out_buffer
    state_token = ""
    state_value = ""
    if len(re.findall(r'[a-zA-Z]', buffer[position])) :
        state = 24
    elif len(re.findall(r'[0-9]', buffer[position])) :
        state = 1
    elif len(re.findall(r'[+\-*%<>=!&|!;,.[\](){}]', buffer[position])) :
        state = 10
    elif len(re.findall(r'/', buffer[position])) :
        state = 6
    elif len(re.findall(r'[\s\n\t]', buffer[position])) :
        state = 23
    elif len(re.findall(r'[\']', buffer[position])) :
        state = 16
    elif len(re.findall(r'[\"]', buffer[position])) :
        state = 13
    return position + 1, state
def state_1(position, state): #int
    global state_value
    global state_token
    global out_buffer
    state_token = "T_INTTYPE"
    state_value = state_value + str(buffer[position - 1])
    if len(re.findall(r'[^0-9.]', buffer[position])) :
        state = 0
        position -= 1
        out_buffer = out_buffer + state_token + " " + state_value + "\n"
    elif len(re.findall(r'"."', buffer[position])) :
        state = 2
    return position + 1, state

def state_2(position, state):
    global state_value
    global state_token
    global out_buffer
    state_token = "T_DOUBLETYPE"
    state_value = state_value + str(buffer[position- 1])
    if len(re.findall(r'[^0-9Ee]', buffer[position])) :
        state = 0
        position -= 1
        out_buffer = out_buffer + state_token + " " + state_value + "\n"
    elif len(re.findall(r'[Ee]', buffer[position])) :
        state = 3
    return position + 1, state

def state_3(position, state):
    global state_value
    global state_token
    global out_buffer
    state_token = "T_DOUBLETYPE"
    state_value = state_value + str(buffer[position- 1])
    if len(re.findall(r'[^+]', buffer[position])) :
        state = 0
        position -= 1
        out_buffer = out_buffer + state_token + " " + state_value + "\n"
    elif len(re.findall(r'[+]', buffer[position])) :
        state = 4
    return position + 1, state

def state_4(position, state):
    global state_value
    global state_token
    global out_buffer
    state_token = "T_DOUBLETYPE"
    state_value = state_value + str(buffer[position - 1])
    if len(re.findall(r'[^0-9]', buffer[position])):
        print("Error: expected int\n position:", position)
        out  = open("out", "w+")
        out.write(out_buffer)
        out.close()
        exit()
    elif len(re.findall(r'[0-9]', buffer[position])):
        state = 5
    return position + 1, state
def state_5(position, state):
    global state_value
    global state_token
    global out_buffer
    state_token = "T_DOUBLETYPE"
    state_value = state_value + str(buffer[position - 1])
    if len(re.findall(r'[^0-9]', buffer[position])):
        state = 0
        position -= 1
        out_buffer = out_buffer + state_token + " " + state_value + "\n"
    return position + 1, state
def state_6(position, state):
    global state_value
    global state_token
    global out_buffer
    state_token = "T_DIV"
    state_value = state_value + str(buffer[position - 1])
    if len(re.findall(r'[^*/]', buffer[position])):
        state = 0
        position -= 1
        out_buffer = out_buffer + state_token + " " + state_value + "\n"
    elif len(re.findall(r'[/]', buffer[position])):
        state = 7
    elif len(re.findall(r'[*]', buffer[position])):
        state = 8
    return position + 1, state
def state_7(position, state):
    global state_value
    global state_token
    global out_buffer
    state_token = "T_COMMENT"
    state_value = state_value + str(buffer[position - 1])
    if len(re.findall(r'[\n]', buffer[position])):
        state = 0
        out_buffer = out_buffer + state_token + " " + state_value + "\n"
    return position + 1, state
def state_8(position, state):
    global state_value
    global state_token
    global out_buffer
    state_token = "T_COMMENT"
    state_value = state_value + str(buffer[position - 1])
    if len(re.findall(r'[*]', buffer[position])):
        state = 9
    return position + 1, state
def state_9(position, state):
    global state_value
    global state_token
    global out_buffer
    state_token = "T_COMMENT"
    state_value = state_value + str(buffer[position - 1])
    if len(re.findall(r'[/]', buffer[position])):
        state = 0
        out_buffer = out_buffer + state_token + " " + state_value + "\n"
    elif len(re.findall(r'[^/]', buffer[position])):
        state = 8
    return position + 1, state
def state_10(position, state):
    global state_value
    global state_token
    global out_buffer
    state_value = state_value + str(buffer[position - 1])
    state_token = operators_dict[state_value]
    if len(re.findall(r'[^+&|]', buffer[position])):
        state = 0
        position -= 1
        out_buffer = out_buffer + state_token + " " + state_value + "\n"
    elif len(re.findall(r'[=&|]', buffer[position])):
        state = 11
    return position + 1, state
def state_11(position, state):
    global state_value
    global state_token
    global out_buffer
    state_value = state_value + str(buffer[position - 1])
    state_token = operators_dict[state_value]
    if len(re.findall(r'[!=><][=]|&&|[||]', state_value)):
        state = 0
        position -= 1
        out_buffer = out_buffer + state_token + " " + state_value + "\n"
    elif len(re.findall(r'[+\-*%<>!;,.[\](){}]', buffer[position])):
        state = 12

    return position + 1, state
def state_12(position, state):
        print("Error: wrong operator\n position:", position)
        out = open("out", "w+")
        out.write(out_buffer)
        out.close()
        exit()
def state_13(position, state):
    global state_value
    global state_token
    global out_buffer
    state_token = "T_STRINGCONSTANT"
    state_value = state_value + str(buffer[position - 1])
    if len(re.findall(r'[\n\\]"', buffer[position])):
        state = 15
    elif len(re.findall(r'["]', buffer[position])):
        state = 14
    return position + 1, state
def state_14(position, state):
    global state_value
    global state_token
    global out_buffer
    state_value = state_value + str(buffer[position - 1])
    state_token = "T_STRINGCONSTANT"
    if len(re.findall(r'[^\n\\"]', buffer[position])):
        state = 0
        position -= 1
        out_buffer = out_buffer + state_token + " " + state_value + "\n"
    elif len(re.findall(r'["]', buffer[position])):
        state = 15
    return position + 1, state
def state_15(position, state):
    print("Error: newline in string constant\n position:", position)
    out = open("out", "w+")
    out.write(out_buffer)
    out.close()
    exit()
def state_16(position, state):
    global state_value
    global state_token
    global out_buffer
    state_token = "T_CHARCONSTANT"
    state_value = state_value + str(buffer[position - 1])
    if len(re.findall(r'[\']', buffer[position])):
        state = 17
    elif len(re.findall(r'[\\]', buffer[position])):
        state = 18
    else:
        state = 20
    return position + 1, state
def state_17(position, state):
    print("Error: char constant has zero width\n position:", position)
    out = open("out", "w+")
    out.write(out_buffer)
    out.close()
    exit()
def state_18(position, state):
    global state_value
    global state_token
    global out_buffer
    state_token = "T_CHARCONSTANT"
    state_value = state_value + str(buffer[position - 1])
    if len(re.findall(r'[\']', buffer[position])):
        state = 19
    elif len(re.findall(r'[^\']', buffer[position])):
        state = 18
    return position + 1, state
def state_19(position, state):
    print("Error: unterminated char constant\n position:", position)
    out = open("out", "w+")
    out.write(out_buffer)
    out.close()
    exit()
def state_20(position, state):
    global state_value
    global state_token
    global out_buffer
    state_token = "T_CHARCONSTANT"
    state_value = state_value + str(buffer[position - 1])
    if len(re.findall(r'[\']', buffer[position])):
        state = 22
    elif len(re.findall(r'[^\']', buffer[position])):
        state = 21
    return position + 1, state
def state_21(position, state):
    print("Error: char constant length is greater than one\n position:", position)
    out = open("out", "w+")
    out.write(out_buffer)
    out.close()
    exit()
def state_22(position, state):
    global state_value
    global state_token
    global out_buffer
    state_value = state_value + str(buffer[position - 1])
    state_token = "T_CHARCONSTANT"
    if len(re.findall(r'[^\']', buffer[position])):
        state = 0
        position -= 1
        out_buffer = out_buffer + state_token + " " + state_value + "\n"
    return position + 1, state
def state_23(position, state):
    global state_value
    global state_token
    global out_buffer
    if buffer[position - 1] != '\n':
        state_value = state_value + str(buffer[position - 1])
    else:
        state_value = state_value + "\\" + "n"
    state_token = "T_WHITESPACE"
    if len(re.findall(r'[^\n\t\s]', buffer[position])):
        state = 0
        position -= 1
        out_buffer = out_buffer + state_token + " " + state_value + "\n"
    return position + 1, state
def state_24(position, state):
    global state_value
    global state_token
    global out_buffer
    state_value = state_value + str(buffer[position - 1])
    if state_value in keyword_dict:
        state_token = keyword_dict[state_value]
    else:
        state_token = "T_ID"
    if len(re.findall("[^A-Za-z0-9_]", buffer[position])):
        state = 0
        position -= 1
        out_buffer = out_buffer + state_token + " " + state_value + "\n"
    return position + 1, state


position = 0
if len(sys.argv) != 2:
    print("Too many or few arguements. \nLexer only need input file name")
    exit()
input_name = sys.argv[1]
input_code = open(input_name, "r")
buffer = input_code.read()
input_len = len(buffer)
while position < input_len:
    position , state= globals()["state_"+ str(state)](position, state)

out = open(input_name + ".out", "w+")
out.write(out_buffer)
out.close()
exit()





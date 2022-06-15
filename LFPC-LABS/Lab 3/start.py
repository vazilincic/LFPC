import Lexer

file=open("input.lex",'r')
text = file.readline()
while text!='':
    #print("\n",text)
    result, error = Lexer.run('<stdin>', text)
    if error: print(error.as_string())
    else:
        if len(result):
            for i in range (0,len(result)):
                print(result[i])
    text = file.readline()

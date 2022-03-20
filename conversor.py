import ply.lex as lex
import re
import sys

csv = open("test.csv", 'r')

# fstLine = csv.readline()
# header = re.split(',',fstLine)
# header[len(header)-1] = header[len(header)-1].replace('\n',"")
##tem aqui um '\n' no último elemento
# print(header)
#
# numeroDeArgumentos = len(header)
#
# ultima = r'(?:(.+))'
# teste = r'(?:(.+))'
# exp = r'(?:(.+),)'
#
#
# for i in range(numeroDeArgumentos-2):
#    exp = exp + teste
#
# exp = exp + ultima
# print(exp)


# p1 = re.compile(r'\w+')
#
#
# print(p1.search())
#
#
#
#
# p2 = re.compile(r'\d+,(([A-Za-zâí]+ ?)+,){2}(\d+,){4}\d+')

# for linha in csv.readlines():
# print(p2.match(linha).group())
# lineL = re.split(',',linha)
# print(lineL)


header = []

tokens = ["COMA", "LBEGIN", "LEND", "CONTENT"]

states = [("lista", "exclusive")]


# Apenas funciona dentro de uma lista? (estado lista)
# def t_lista_LBEGIN(t):
#    r'{'
#    t.lexer.push_state("lista")


# Listas
def t_ANY_LBEGIN(t):
    r'\w+{'
    t.lexer.push_state("lista")
    header.append(t.value)
    header.append([])
    print(t.value)


def t_lista_LEND(t):
    r'}'
    t.lexer.pop_state()


def t_lista_CONTENT(t):
    r'\d+'
    print(t.value)
    header[-1].append(t.value)
    print(header)


def t_lista_COMA(t):
    r','
    pass


# Conteúdo
def t_COMA(t):
    r','
    pass


def t_CONTENT(t):
    r'[\w \n]+'
    parametro = t.value
    header.append(parametro)
    print(parametro)
    # ver se o parâmetro é uma lista ou chama uma função
    # elif '::' in parametro:
    #    pass


# Erro
def t_ANY_error(t):
    print("ERROR : " + t.value)


lexer = lex.lex()

f = open("test.csv", 'r')
text = f.readline()
lexer.input(text)

for tok in lexer:
    pass

f.close()

import ply.lex as lex
import re


def getNome(a):
    a = a.replace('::', '')
    a = a.replace('\n', '')
    a = a.replace('{', '')
    a = '"' + a + '"'
    return a


csv = open("test.csv", 'r')

header = []

tokens = ["COMA", "LBEGIN", "LEND", "CONTENT", "FUNC"]

states = [("lista", "exclusive")]


# Listas
def t_ANY_LBEGIN(t):
    r'\w+{'
    t.lexer.push_state("lista")
    header.append(t.value)
    header.append([])


def t_FUNC(t):
    r'::\w+'
    header.append(t.value)


def t_lista_LEND(t):
    r'}'
    t.lexer.pop_state()


def t_lista_CONTENT(t):
    r'\d+'
    header[-1].append(t.value)


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
    parametro = parametro.replace('\n', '')
    header.append(parametro)


# Erro
def t_ANY_error(t):
    r'(.|\n)'
    print("ERROR : " + t.value)


lexer = lex.lex()

f = open("test.csv", 'r')
text = f.readlines()
lexer.input(text[0])

for tok in lexer:
    pass

print(header)

out = open("out.txt", 'x')
lista = ''

for line in text[1:]:

    i = 0  # Índice da lista do header
    j = 0  # Índice da lista que corresponde aos campos de uma linha de conteúdo
    out.write('{\n')
    final_string = ''

    lineL = re.split(',', line)
    print(lineL)

    # Para cada linha, ler o header e fazer as operações necessárias
    for elem in header:
        if type(elem) == list:
            # out.write('[')

            limite = int(elem[-1]) + j
            lista = lista + '['

            for x in range(j, limite):
                elemL = lineL[x]
                if elemL != '':
                    lista = lista + elemL
                    if x < (limite - 1):
                        if lineL[x + 1] != '':
                            lista = lista + ','

            j = limite
            lista = lista + ']\n'
            # out.write(lista)
            # out.write(']\n')

        else:  # É uma String
            if '{' in elem:
                # É uma Lista

                # A lista só é escrita para o json agora, pq sabemos que não será aplicada função à mesma
                out.write(lista)
                lista = ''

                print(str(header[i + 1]) + "Lista")
                nome_Lista = getNome(elem)
                lista = '\t' + nome_Lista + ': '
                # out.write('\t' + nome_Lista + ': ')

            elif '::' in elem:
                # É uma Função
                # Falta aqui aplicar a função à lista
                lista = ''

                print(str(header[i - 2]) + "Função")
                nome_Funcao = str(header[i - 2]) + '_' + elem
                nome_Funcao = getNome(nome_Funcao)
                out.write('\t' + nome_Funcao + ': \n')
            else:

                # A lista só é escrita para o json agora, pq sabemos que não será aplicada função à mesma
                out.write(lista)
                lista = ''

                # Apenas um Campo normal
                if elem == '':
                    # Aqui é um elemento da lista em falta, ou campo vazio
                    pass
                else:
                    campo = getNome(elem)
                    out.write('\t' + campo + ': ')
                    out.write(getNome(lineL[j]) + '\n')
                j = j + 1

        i = i + 1

    out.write('\n}')

# numeroDeArgumentos = len(header)
#
# ultima = r'(?:(.+))'
# exp = r'(?:(.+),)'
#
#
# for i in range(numeroDeArgumentos-2):
#    exp = exp + teste
#
# exp = exp + ultima
# print(exp)


# p1 = re.compile(r'\w+')
# print(p1.search())
# p2 = re.compile(r'\d+,(([A-Za-zâí]+ ?)+,){2}(\d+,){4}\d+')

# for linha in csv.readlines():
# print(p2.match(linha).group())
# lineL = re.split(',',linha)
# print(lineL)

f.close()

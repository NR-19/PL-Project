import sys
import ply.lex as lex
import re


def calculaFunc(list, nomeFunc):
    stringList = re.split(',', list)
    numberList = []

    for e in stringList:
        temp = re.search(r'\d+', e)
        if temp is not None:
            temp = temp.group()
            numberList.append(int(temp))

    nomeFunc = nomeFunc.replace("::", "")

    match nomeFunc:
        case "sum":
            ans = sum(numberList)
        case "average":
            ans = sum(numberList) / len(numberList)
        case "max":
            ans = max(numberList)
        case "min":
            ans = min(numberList)
        case "range":
            ans = abs(max(numberList) - min(numberList))
        case _:
            ans = 0
    return ans


def getNome(a):
    a = a.replace('::', '')
    a = a.replace('\n', '')
    a = a.replace('{', '')
    a = '"' + a + '"'
    return a


# Lista que contém os campos do header do csv
header = []

tokens = ["COMA", "LBEGIN", "LEND", "CONTENT", "FUNC"]

states = [("lista", "exclusive")]


# Listas
def t_LBEGIN(t):
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


def readCSV(csv,json):

    # Construir o lexer
    lexer = lex.lex()

    # Abrir o csv e ler a primeira linha (header)
    f = open(csv, 'r')
    lines = f.readlines()
    lexer.input(lines[0])

    for _ in lexer:
        pass

    print(header)
    out = open(json, 'w')

    linhasSize = len(lines[1:])

    out.write('[')
    lineCounter = 0

    for line in lines[1:]:

        lista = '' # String que corresponde à lista que será ou não imprimida no json
        i = 0  # Índice da lista do header
        j = 0  # Índice da lista que corresponde aos campos de uma linha de conteúdo
        sizeHeader = len(header)
        out.write('\n\t{\n')

        lineL = re.split(',', line)
        print(lineL)

        # Para cada linha, ler o header e fazer as operações necessárias
        for elem in header:

            if type(elem) == list:

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
                fechaLista = '\n'

                # Aqui vejo se é preciso pôr vírgula ou não
                if i < sizeHeader-1:
                    fechaLista = ',\n'

                lista = lista + ']' + fechaLista

            else:  # É uma String

                if '{' in elem:
                    # É uma Lista

                    # A lista só é escrita para o json agora, pq sabemos que não será aplicada função à mesma
                    out.write(lista)
                    lista = ''

                    nome_Lista = getNome(elem)
                    lista = '\t\t' + nome_Lista + ': '

                elif '::' in elem:
                    # É uma Função
                    # Falta aqui aplicar a função à lista

                    resultado = str(calculaFunc(lista, header[i]))

                    lista = ''

                    nome_Funcao = str(header[i - 2]) + '_' + elem

                    nome_Funcao = getNome(nome_Funcao)
                    out.write('\t\t' + nome_Funcao + ': ')
                    out.write(resultado)
                    # Aqui vejo se é preciso pôr vírgula ou não
                    if i < sizeHeader-1:
                        out.write(',\n')

                    else:
                        out.write('\n')

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
                        out.write('\t\t' + campo + ': ')
                        out.write(getNome(lineL[j]))

                        # Aqui ver se é preciso pôr vírgula ou não
                        if i < sizeHeader-1:
                            out.write(',\n')

                        else:
                            out.write('\n')

                    j = j + 1

            i = i + 1

        lineCounter = lineCounter + 1


        # Ver se é preciso ','
        fechaElemento = '\n\t}'
        if lineCounter<linhasSize:
            fechaElemento = fechaElemento + ','

        out.write(fechaElemento)

    out.write('\n]')

    f.close()
    out.close()


def main():

    # Lista de argumentos em que agrs[1] é o ficheiro csv (input) e args[2] é o json (ficheiro output)
    args = sys.argv[1:]

    readCSV(args[0],args[1])


if __name__ == "__main__":
    main()

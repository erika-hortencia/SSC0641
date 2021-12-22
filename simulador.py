import random

"""
Declaração das variáveis globais
"""
global msglen
global CRC
global msgbitlen
global tipoControle
global mensagem
global mensagemBit
global crc32
global porcentagemDeErros

msglen = 256
CRC = 32
msgbitlen = msglen * 8
mensagem = [0] * msglen
mensagemBit = [0] * (msgbitlen + CRC)
crc32 = [1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1]
############### Alterar os valores dessas variáveis para realizar os testes ###############
tipoControle = 2                        #Variável que determina o tipo de controle de erro a ser realizado 0=paridade par 1=paridade impar 2=CRC
porcentagemDeErros = 0                  #10%, 20%, 30%, ... 100%

"""
Fluxo principal do programa
"""
def main():
    print(' ')
    print('*************************************************************************')
    print('*******************         SIMULADOR INICIADO        *******************')
    print('*************************************************************************')
    print(' ')
    
    AplicacaoTransmissora()
    CamadaEnlaceDadosTransmissora(mensagemBit)
    MeioDeComunicacao(mensagemBit)
    CamadaDeEnlaceDeDadosReceptora(mensagemBit)
    CamadaDeAplicacaoReceptora(mensagemBit)

    return

"""
Recebe a mensagem a ser enviada e encaminha para a proxima camada
"""
def AplicacaoTransmissora():

    mensagem = input('=> Digite a mensagem a ser enviada: ')
    CamadaDeAplicacaoTransmissora(mensagem)

    return

"""
Recebe a mensagem e converte para bit
"""
def CamadaDeAplicacaoTransmissora(mensagem):
    print(' ')
    print(' ')
    ascii = i =  k = x = 0
    j = 7
    aux = [None] * 8

    #Conversão de char para bit
    while i < len(mensagem):
        #Conversão de char para int
        ascii = ord(mensagem[i])
        i += 1

        #Conversão int para bit
        while j > 0:
            aux[j] = ascii % 2
            ascii = ascii // 2

            j -= 1
        
        aux[0] = ascii
        j = 7

        #Transcrição para o vetor da mensagem em bits
        while x < 8:
            mensagemBit[k] = aux[x]

            k += 1
            x += 1
        
        x = 0

    return

"""
Chama a função de controle de erros
"""
def CamadaEnlaceDadosTransmissora(quadro):

    CamadaEnlaceDadosTransmissoraControleDeErro(quadro)

    return

"""
Encaminha para o tipo de controle de erro selecionado
"""
def CamadaEnlaceDadosTransmissoraControleDeErro(quadro):

    if tipoControle == 0:
        CamadaEnlaceDadosTransmissoraControleDeErroBitParidadePar(quadro)
    elif tipoControle == 1:
        CamadaEnlaceDadosTransmissoraControleDeErroBitParidadeImpar(quadro)
    elif tipoControle == 2:
        CamadaEnlaceDadosTransmissoraControleDeErroCRC(quadro)

    return


"""
Checa o numero de 1s no vetor, caso seja impar adiciona 1 ao final
"""
def CamadaEnlaceDadosTransmissoraControleDeErroBitParidadePar(quadro):
    sum = 0

    for i in range(msgbitlen):
        if(sum == 0 and quadro[i] == 0 or sum == 1 and quadro[i] == 1):
            sum = 0
        else:
            sum = 1
    quadro[msgbitlen] = sum

    return


"""
Checa o numero de 1s no vetor, caso seja par adiciona 1 ao final
"""
def CamadaEnlaceDadosTransmissoraControleDeErroBitParidadeImpar(quadro):
    sum = 1

    for i in range(msgbitlen):
        if(sum == 0 and quadro[i] == 0 or sum == 1 and quadro[i] == 1):
            sum = 0
        else:
            sum = 1
    quadro[msgbitlen] = sum

    return

"""
Utiliza o polinomio CRC-32 (IEEE 802)
"""
def CamadaEnlaceDadosTransmissoraControleDeErroCRC(quadro):
    quadroTemp = [0] * (msgbitlen+CRC)
    
    for i in range(msgbitlen + CRC):
        quadroTemp[i] = quadro[i]
    

    for i in range(msgbitlen):
        if quadroTemp[i] == 0:
            continue
        
        for j in range(CRC):
            if quadroTemp[i + j] == crc32[j]:
                quadroTemp[i + j] = 0
            else:
                quadroTemp[i + j] = 1

    for i in range(CRC):
        quadro[msgbitlen + i] = quadroTemp[msgbitlen + i]

    return

"""
Meio de comunicação
"""
def MeioDeComunicacao(fluxoBrutoDeBits):
    fluxoBrutoDeBitsPontoA = fluxoBrutoDeBits
    fluxoBrutoDeBitsPontoB = [0] * (msgbitlen + CRC)

    for i in range(msgbitlen + CRC):
        if random.randrange(0,100) >= porcentagemDeErros:   #Faz a probabilidade de erro
            fluxoBrutoDeBitsPontoB[i] += fluxoBrutoDeBitsPontoA[i]
        else: #Erro! Inverter (usa condição ternária)
            if not fluxoBrutoDeBitsPontoB[i]:
                fluxoBrutoDeBitsPontoA[i] = fluxoBrutoDeBitsPontoB[i] + 1
            else:
                fluxoBrutoDeBitsPontoA[i] = fluxoBrutoDeBitsPontoB[i] - 1
    
    return

"""
Recebe a mensagem do meio de comunicação e envia para a camada de cima
"""
def CamadaDeEnlaceDeDadosReceptora (quadro):

    CamadaEnlaceDadosReceptoraControleDeErro(quadro)

    return

"""
Encaminha a mensagem para o mesmo tipo de controle de erro utilizado na camada transmissora
"""
def CamadaEnlaceDadosReceptoraControleDeErro(quadro):

    if tipoControle == 0:
        CamadaEnlaceDadosReceptoraControleDeErroBitParidadePar(quadro)
    elif tipoControle == 1:
        CamadaEnlaceDadosReceptoraControleDeErroBitParidadeImpar(quadro)
    elif tipoControle == 2:
        CamadaEnlaceDadosReceptoraControleDeErroCRC(quadro)

    return


"""
Faz o check de erros
"""
def CamadaEnlaceDadosReceptoraControleDeErroBitParidadePar(quadro):

    sum = 0


    for i in range(msgbitlen + CRC):
        if(sum == 0 and quadro[i] == 0 or sum == 1 and quadro[i] == 1):
            sum = 0
        else:
            sum = 1
    
    if(sum):
        print('!!!!!!!!!!!!!!!!!!!!!ERRO NO RECEBIMENTO DA MENSAGEM!!!!!!!!!!!!!!!!!!!!!')
    else:
        print('Mensagem recebida com sucesso!')

    return


"""
Faz o check de erros
"""
def CamadaEnlaceDadosReceptoraControleDeErroBitParidadeImpar(quadro):
    
    sum = 1

   

    for i in range(msgbitlen + 1):
        if(sum == 0 and quadro[i] == 0 or sum == 1 and quadro[i] == 1):
            sum = 0
        else:
            sum = 1
    
    if(sum):
        print('!!!!!!!!!!!!!!!!!!!!!ERRO NO RECEBIMENTO DA MENSAGEM!!!!!!!!!!!!!!!!!!!!!')
    else:
        print('Mensagem recebida com sucesso!')

    return


"""
Faz o check de erros
"""
def CamadaEnlaceDadosReceptoraControleDeErroCRC(quadro):
    quadroTemp = [0] * (msgbitlen+CRC)
    errorFlag = 0
    
    for i in range(msgbitlen + CRC):
        quadroTemp[i] = quadro[i]
    

    for i in range(msgbitlen):
        if quadroTemp[i] == 0:
            continue
        
        for j in range(CRC):
            if quadroTemp[i + j] == crc32[j]:
                quadroTemp[i + j] = 0
            else:
                quadroTemp[i + j] = 1
    
    for i in range(CRC):
        if quadroTemp[msgbitlen + i] == 1:
            errorFlag = 1

            break

    if errorFlag:
        print('!!!!!!!!!!!!!!!!!!!!! ERRO: CODIGO CRC INVALIDO !!!!!!!!!!!!!!!!!!!!!')
    else:
        print('Mensagem recebida com sucesso!')

    return

"""
Converte a mensagem novamente para ascii e encaminha para a camada superior
"""
def CamadaDeAplicacaoReceptora(quadro):
    asciiTemp = 0
    i = j = 0
    tempmsg = []
    
    #Conversão de binario para char
    for i in range(len(mensagem)):
        
        #Conversão de binario para int
        for j in range(8):
            asciiTemp += pow(2, 7 - j) * quadro[((i * 8) + j)]

        #Conversão de int para char
        tempmsg.append(chr(asciiTemp))
        asciiTemp = 0

    str_char = "".join([str(int) for int in tempmsg])
    AclicacaoReceptora(str_char)
    return

"""
Exibe a mensagem recebida
"""
def AclicacaoReceptora(mensagem):
    print(' ')
    print(' ')
    print(' ')
    print('Mensagem recebida => ', mensagem)
    return




main()
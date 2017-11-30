#!/usr/bin/python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
from cProfile import run
from win32api import keybd_event
import string, os, sys, httplib
from datetime import date
from zipfile import ZipFile
import base64
import lxml
#from Demos.RegCreateKeyTransacted import keyname
from datetime import date
from lxml import etree, _elementpath
import gzip
import zipfile
import os
import subprocess

def gerar_reducaoZ():
    try:
        # Abre o arquivo desejado
        arquivoReducaoZ = open('teste.txt', 'r')
    except:
        print("Arquivo TXT de ReducaoZ não encontrado." )

    # Cria o elemento ReducaoZ
    reducaoZ = ET.Element("ReducaoZ", Versao="1.0")

    # Cria o subElemento Mensagem
    mensagem = ET.SubElement(reducaoZ, "Mensagem")

    # Cria o subElemento Signature
    #signature = ET.SubElement(reducaoZ, "Signature")

    # lê linha por linha e armazena em uma variavel
    # Estabelecimento

    linhasArquivo = arquivoReducaoZ.readlines()

    # Fecha a abertura do arquivo
    arquivoReducaoZ.close()
    temTotalizador = False
    pdv = 0
    loja = 0

    for linha in linhasArquivo:
        var = linha.split(" ; ")

        if (var[0] == "estabelecimento"):
            # Cria o submeelento Estabelecimento
            estabelecimento = ET.SubElement(mensagem, "Estabelecimento")

            # Cria os elementos do Estabelecimento
            ET.SubElement(estabelecimento, "Ie").text = var[1]
            ET.SubElement(estabelecimento, "Cnpj").text = var[2]
            ET.SubElement(estabelecimento, "NomeEmpresarial").text = var[3]

        elif (var[0] == "pafecf"):
            # Cria elemento PafEcf
            PafEcf = ET.SubElement(mensagem, "PafEcf")

            # Cria os elementos do PafEcf
            ET.SubElement(PafEcf, "NumeroCredenciamento").text = var[1]
            ET.SubElement(PafEcf, "NomeComercial").text = var[2]
            ET.SubElement(PafEcf, "Versao").text = var[3]
            ET.SubElement(PafEcf, "CnpjDesenvolvedor").text = var[4]
            ET.SubElement(PafEcf, "NomeEmpresarialDesenvolvedor").text = var[5]

        elif (var[0] == "ecf"):
            # Cria o elemento Ecf
            ecf = ET.SubElement(mensagem, "Ecf")

            # Cria os elementos do Ecf
            ET.SubElement(ecf, "NumeroCredenciamento").text = var[1]
            ET.SubElement(ecf, "NumeroFabricacao").text = var[2]
            ET.SubElement(ecf, "Tipo").text = var[3]
            ET.SubElement(ecf, "Marca").text = var[4]
            ET.SubElement(ecf, "Modelo").text = var[5]
            ET.SubElement(ecf, "Versao").text = var[6]
            ET.SubElement(ecf, "Caixa").text = var[7]

        elif (var[0] == "dadosZ"):
            # Cria o elemento DadosReducaoZ
            dadosReducaoZ = ET.SubElement(ecf, "DadosReducaoZ")

            # Cria os elementos do Ecf
            ET.SubElement(dadosReducaoZ, "DataReferencia").text = var[1]
            ET.SubElement(dadosReducaoZ, "DataHoraEmissao").text = var[2]
            ET.SubElement(dadosReducaoZ, "CRZ").text = var[3]
            ET.SubElement(dadosReducaoZ, "COO").text = var[4]
            ET.SubElement(dadosReducaoZ, "CRO").text = var[5]
            ET.SubElement(dadosReducaoZ, "VendaBrutaDiaria").text = var[6]
            ET.SubElement(dadosReducaoZ, "GT").text = var[7]

        elif (var[0] == "totalizadorParcial"):
            if (temTotalizador == False):
                # Cria o elemento TotalizadoresParciais
                totalizadoresParciais = ET.SubElement(dadosReducaoZ, "TotalizadoresParciais")
                temTotalizador = True

            # Cria o elemento TotalizadoresParcial
            totalizadorParcial = ET.SubElement(totalizadoresParciais, "TotalizadorParcial")

            # Cria os elementos do TotalizadoresParcial
            ET.SubElement(totalizadorParcial, "Nome").text = var[1]
            ET.SubElement(totalizadorParcial, "Valor").text = var[2]

        elif (var[0] == "produto"):

            # Cria o elemento ProdutosServiços
            produtosServicos = ET.SubElement(totalizadorParcial, "ProdutosServicos")

            tagProduto = ET.SubElement(produtosServicos, "Produto")
            # Cria os elementos do Produto
            ET.SubElement(tagProduto, "Descricao").text = var[1]
            ET.SubElement(tagProduto, "CodigoGTIN").text = var[2]
            ET.SubElement(tagProduto, "CodigoCEST").text = var[3]
            ET.SubElement(tagProduto, "CodigoNCMSH").text = var[4]
            ET.SubElement(tagProduto, "CodigoProprio").text = var[5]
            ET.SubElement(tagProduto, "Quantidade").text = var[6]
            ET.SubElement(tagProduto, "Unidade").text = var[7]
            ET.SubElement(tagProduto, "ValorDesconto").text = var[8]
            ET.SubElement(tagProduto, "ValorAcrescimo").text = var[9]
            ET.SubElement(tagProduto, "ValorTotalLiquido").text = var[10]
            ET.SubElement(tagProduto, "ValorCancelamento").text = var[11]

    # Cria o subElemento Signature
    signature = ET.SubElement(reducaoZ, "Signature", xmlns="http://www.w3.org/2000/09/xmldsig#")

    # Cria o subElemento SignedInfo
    signedinfo = ET.SubElement(signature, "SignedInfo")

    # Cria os elementos do SignedInfo
    ET.SubElement(signedinfo,"CanonicalizationMethod Algorithm='http://www.w3.org/TR/2001/REC-xml-c14n-20010315'")
    ET.SubElement(signedinfo,"SignatureMethod Algorithm='http://www.w3.org/2000/09/xmldsig#rsa-sha1'")
    # Cria o elemento ReferenceURI
    referenceuri = ET.SubElement(signedinfo, 'Reference', URI="")

    # Cria o subElemento Transforms
    transforms = ET.SubElement(referenceuri, "Transforms")

    # Cria os elementos do Transforms
    ET.SubElement(transforms, "Transform Algorithm='http://www.w3.org/2000/09/xmldsig#enveloped-signature'")
    ET.SubElement(transforms, "Transform Algorithm='http://www.w3.org/TR/2001/REC-xml-c14n-20010315'")

    # Cria os elementos do DigestMethod
    digestArquivo = open("digestValue.txt")
    # DigestValue
    digestvalueVar = digestArquivo.readline().split(" ; ")
    if (digestvalueVar[0] == "digestValue"):
        # Cria os elementos do DigestValue
        ET.SubElement(referenceuri, "DigestValue").text = digestvalueVar[1]

    # Fecha o arquivo DigestValue
    digestArquivo.close()

    signatureArquivo = open("signatureValue.txt")
    # SignatureValue
    signatureValueVar = signatureArquivo.readline().split(" ; ")
    if (signatureValueVar[0] == "signatureValue"):
        # Cria os elemento do SignatureValue
        signatureValue = ET.SubElement(signature, "SignatureValue").text = signatureValueVar[1]
    signatureArquivo.close()

    # Cria o elemento KeyInfo
    keyInfo = ET.SubElement(signature, "KeyInfo")

    # Cria o elemento X509Data
    x509Data = ET.SubElement(keyInfo, "X509Data")

    # Abre o arquivo X509 Certificate
    x509CertificateArquivo = open("x509.txt")
    # X509Certificate
    x509CertificateVar = x509CertificateArquivo.readline().split(" ; ")
    if (x509CertificateVar[0] == "x509Certificate"):
        # Cria os elementos do X509Certificate
        ET.SubElement(x509Data, "X509Certificate").text = x509CertificateVar[1]

    # Fecha o arquivo X509 Certificate
    x509CertificateArquivo.close()

    arquivo = ET.ElementTree(reducaoZ)

    arquivo.write("XMLReducaoZ.xml")
    print("Arquivo XML de ReducaoZ Gerado com sucesso")

    try:
        meuzip = ZipFile("XMLReducaoZ"+".zip", "a")
        meuzip.write("XMLReducaoZ.xml")
        meuzip.close()
        print("Arquivo de XML Zipado com sucesso")
    except:
        print("Esse arquivo já existe.")

def gerar_estoque():

    try:
        # Abre o arquivo desejado
        arquivoEstoque = open('estoque.txt', 'r')
    except:
        print("Arquivo TXT de Estoque não encontrado. ")

    # Cria o elemento ReducaoZ
    estoque = ET.Element("Estoque", Versao="1.0")

    # Cria o subElemento Mensagem
    mensagem = ET.SubElement(estoque, "Mensagem")

    # lê linha por linha e armazena em uma variavel
    # Estabelecimento

    linhasArquivo = arquivoEstoque.readlines()

    # Fecha a abertura do arquivo
    arquivoEstoque.close()
    temProdutos = False

    for linha in linhasArquivo:
        var = linha.split(" ; ")

        if (var[0] == "estabelecimento"):
            # Cria o submeelento Estabelecimento
            estabelecimento = ET.SubElement(mensagem, "Estabelecimento")

            # Cria os elementos do Estabelecimento
            ET.SubElement(estabelecimento, "Ie").text = var[1]
            ET.SubElement(estabelecimento, "Cnpj").text = var[2]
            ET.SubElement(estabelecimento, "NomeEmpresarial").text = var[3]

        elif (var[0] == "pafecf"):
            # Cria elemento PafEcf
            PafEcf = ET.SubElement(mensagem, "PafEcf")

            # Cria os elementos do PafEcf
            ET.SubElement(PafEcf, "NumeroCredenciamento").text = var[1]
            ET.SubElement(PafEcf, "NomeComercial").text = var[2]
            ET.SubElement(PafEcf, "Versao").text = var[3]
            ET.SubElement(PafEcf, "CnpjDesenvolvedor").text = var[4]
            ET.SubElement(PafEcf, "NomeEmpresarialDesenvolvedor").text = var[5]

        elif (var[0] == "dadosestoque"):
            # Cria o elemento DadosEstoque
            dadosEstoque = ET.SubElement(mensagem, "DadosEstoque")

            # Cria os elementos do Estoque
            ET.SubElement(dadosEstoque, "DataInicial").text = var[1]
            ET.SubElement(dadosEstoque, "DataFinal").text = var[2]

        elif (var[0] == "produto"):
            if(temProdutos == False):
                # Cria o elemento Produtos
                produtos = ET.SubElement(dadosEstoque, "Produtos")
                temProdutos = True

            #Cria o elemento Produto
            tagProduto = ET.SubElement(produtos, "Produto")
            # Cria os elementos do Produto
            ET.SubElement(tagProduto, "Descricao").text = var[1]
            ET.SubElement(tagProduto, "CodigoGTIN").text = var[2]
            ET.SubElement(tagProduto, "CodigoCEST").text = var[3]
            ET.SubElement(tagProduto, "CodigoNCMSH").text = var[4]
            ET.SubElement(tagProduto, "CodigoProprio").text = var[5]
            ET.SubElement(tagProduto, "Quantidade").text = var[6]
            ET.SubElement(tagProduto, "QuantidadeTotalAquisicao").text = var[7]
            ET.SubElement(tagProduto, "Unidade").text = var[8]
            ET.SubElement(tagProduto, "ValorUnitario").text = var[9]
            ET.SubElement(tagProduto, "ValorTotalAquisicao").text = var[10]
            ET.SubElement(tagProduto, "ValorTotalICMSDebitoFornecedor").text = var[11]
            ET.SubElement(tagProduto, "ValorBaseCalculoICMSST").text = var[12]
            ET.SubElement(tagProduto, "ValorTotalICMSST").text = var[13]
            ET.SubElement(tagProduto, "SituacaoTributaria").text = var[14]
            ET.SubElement(tagProduto, "Aliquota").text = var[15]
            ET.SubElement(tagProduto, "IsArredondado").text = var[16]
            ET.SubElement(tagProduto, "Ippt").text = var[17]
            ET.SubElement(tagProduto, "SituacaoEstoque").text = var[18]

    # Cria o subElemento Signature
    signature = ET.SubElement(estoque,'Signature', xmlns="http://www.w3.org/2000/09/xmldsig#")

    # Cria o subElemento SignedInfo
    signedinfo = ET.SubElement(signature, "SignedInfo")

    # Cria os elementos do SignedInfo
    ET.SubElement(signedinfo,"CanonicalizationMethod Algorithm='http://www.w3.org/TR/2001/REC-xml-c14n-20010315'")
    ET.SubElement(signedinfo,"SignatureMethod Algorithm='http://www.w3.org/2000/09/xmldsig#rsa-sha1'")
    # Cria o elemento ReferenceURI
    referenceuri = ET.SubElement(signedinfo, 'Reference', URI="")

    # Cria o subElemento Transforms
    transforms = ET.SubElement(referenceuri, "Transforms")

    # Cria os elementos do Transforms
    ET.SubElement(transforms, "Transform Algorithm='http://www.w3.org/2000/09/xmldsig#enveloped-signature'")
    ET.SubElement(transforms, "Transform Algorithm='http://www.w3.org/TR/2001/REC-xml-c14n-20010315'")

    # Cria os elementos do DigestMethod
    digestArquivo = open("digestValue.txt")
    # DigestValue
    digestvalueVar = digestArquivo.readline().split(" ; ")
    if (digestvalueVar[0] == "digestValue"):
        # Cria os elementos do DigestValue
        ET.SubElement(referenceuri, "DigestValue").text = digestvalueVar[1]

    # Fecha o arquivo DigestValue
    digestArquivo.close()

    signatureArquivo = open("signatureValue.txt")
    # SignatureValue
    signatureValueVar = signatureArquivo.readline().split(" ; ")
    if (signatureValueVar[0] == "signatureValue"):
        # Cria os elemento do SignatureValue
        signatureValue = ET.SubElement(signature, "SignatureValue").text = signatureValueVar[1]
    signatureArquivo.close()

    # Cria o elemento KeyInfo
    keyInfo = ET.SubElement(signature, "KeyInfo")

    # Cria o elemento X509Data
    x509Data = ET.SubElement(keyInfo, "X509Data")

    # Abre o arquivo X509 Certificate
    x509CertificateArquivo = open("x509.txt")
    # X509Certificate
    x509CertificateVar = x509CertificateArquivo.readline().split(" ; ")
    if (x509CertificateVar[0] == "x509Certificate"):
        # Cria os elementos do X509Certificate
        ET.SubElement(x509Data, "X509Certificate").text = x509CertificateVar[1]

    # Fecha o arquivo X509 Certificate
    x509CertificateArquivo.close()


    arquivo = ET.ElementTree(estoque)

    arquivo.write("XMLEstoque.xml")
    print("Arquivo XML de Estoque gerado com sucesso")

    try:
        meuzip = ZipFile("XMLEstoque"+".zip", "a")
        meuzip.write("XMLEstoque.xml")
        meuzip.close()
        print("Arquivo de Estoque Zipado com sucesso")
    except:
        print("Esse arquivo já existe.")


try:
    def main():
        print("Servico iniciado...")
        #gerar_estoque()
        #gerar_reducaoZ()
        #validarReducaZ()
        #validarEstoque()
        os.system("java -jar assinar.jar XMLReducaoZ.xml")
except Exception:
    print (Exception)

main()

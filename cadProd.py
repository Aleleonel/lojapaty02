from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import QDate, QTime, QDateTime, Qt
from PyQt5.QtWidgets import QMessageBox, QCompleter

import conexao

from reportlab.pdfgen import canvas

valor = 0


def gerar_pdf():
    cursor = conexao.banco.cursor()
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    y = 0
    pdf = canvas.Canvas("Lista de Produtos.pdf")
    pdf.setFont("Times-Bold", 18)
    pdf.drawString(200, 800, "Produtos: ")
    pdf.setFont("Times-Bold", 12)

    pdf.drawString(10, 750, "ID")
    pdf.drawString(50, 750, "CODIGO")
    pdf.drawString(110, 750, "PRODUTO")
    pdf.drawString(310, 750, "PREÇO")
    pdf.drawString(410, 750, "CATEGORIA")

    for i in range(0, len(dados_lidos)):
        y += 50
        pdf.drawString(10, 750 - y, str(dados_lidos[i][0]))
        pdf.drawString(50, 750 - y, str(dados_lidos[i][1]))
        pdf.drawString(110, 750 - y, str(dados_lidos[i][2]))
        pdf.drawString(310, 750 - y, str(dados_lidos[i][3]))
        pdf.drawString(410, 750 - y, str(dados_lidos[i][4]))

    pdf.save()
    global valor
    if not menu.progressBar.isVisible():
        menu.progressBar.show()
        while valor <= 100:
            valor += 0.0001
            menu.progressBar.setValue(valor)
    menu.progressBar.hide()
    valor = 0

    msg = QMessageBox()
    msg.setWindowTitle("Atenção")
    msg.setText("PDF Criado com Sucesso")
    msg.setIcon(QMessageBox.Information)
    msg.setDetailedText("Arquivo criado em meus documentos ")

    x = msg.exec_()


def edit_dados():
    linha = formulario_listprod.tableWidget.currentRow()

    cursor = conexao.banco.cursor()
    comando_SQL = "SELECT id FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]

    cursor.execute("SELECT * FROM produtos WHERE id =" + str(valor_id))
    produto = cursor.fetchall()
    formulario_editprod.show()

    formulario_editprod.ld_id.setText(str(produto[0][0]))
    formulario_editprod.ld_codigo.setText(str(produto[0][1]))
    formulario_editprod.ld_produto.setText(str(produto[0][2]))
    formulario_editprod.ld_preco.setText(str(produto[0][3]))
    formulario_editprod.ld_categoria.setText(str(produto[0][4]))


def salvar():
    linha = formulario_listprod.tableWidget.currentRow()

    cursor = conexao.banco.cursor()
    comando_SQL = "SELECT id FROM produtos"
    cursor.execute(comando_SQL)

    dados_lidos = cursor.fetchall()

    valor_id = dados_lidos[linha][0]

    cursor.execute("SELECT * FROM produtos WHERE id =" + str(valor_id))
    produto = cursor.fetchall()
    prod = formulario_editprod.ld_produto.text()
    prec = formulario_editprod.ld_preco.text()
    cat = formulario_editprod.ld_categoria.text()

    comando_SQL = "UPDATE produtos SET descricao = '" + prod + "', preco = '" \
                  + prec + "', categoria = '" + cat + "' WHERE id =" + str(valor_id)
    cursor.execute(comando_SQL)
    #
    conexao.banco.commit()
    formulario_editprod.close()


def excluir_dados():
    linha = formulario_listprod.tableWidget.currentRow()
    formulario_listprod.tableWidget.removeRow(linha)

    cursor = conexao.banco.cursor()
    comando_SQL = "SELECT id FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("DELETE FROM produtos WHERE id =" + str(valor_id))
    conexao.banco.commit()


def mostracadprod():
    formulario.show()


def GerarPedido():
    cursor = conexao.banco.cursor()
    comando_SQL = "SELECT codigo FROM pedidos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    cont = 0

    for i in range(len(dados_lidos)):
        if dados_lidos[i][1] == cont:
            print(cont)
        else:
            cont += 1
            print(cont)


def abrePedidoCaixa():
    """
    Abre o layout Pedido, escolhe o tipo de operação
    Insere data atual no pedido caixa
    :return:
    """
    # Mostra o layout
    formulario_caixa.show()

    # Lẽ a tapebela de tipo de operação
    cursor = conexao.banco.cursor()
    comando_SQL = "SELECT * FROM tipo_operacao"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    # Mostra as operações na ComboBox
    combo = [operacao for operacao in dados_lidos]
    for c in range(len(combo)):
        formulario_caixa.comboBox.addItems([combo[c][1]])

    # Chama a função que Tipo de Operação
    formulario_caixa.comboBox.activated.connect(tipoOperacao)

    # DATA DO PEDIDO
    d = QDate.currentDate()
    dataAtual = d.toString(Qt.ISODate)
    data = str(dataAtual)
    formulario_caixa.dtEdit.setText(data)


# Chamada pela função abrePedidoCaixa
def tipoOperacao(index):
    """
    Aqui vai ser devinido uma tabela temporaria
    que conterá os dados do pedido antes de serem
    salvos na tabela pedidos
    :param index:
    :return:
    """
    f = (formulario_caixa.comboBox.itemText(index))
    if f == 'ORÇAMENTO':
        print('orçamento')


rec = 0


def autoIncrement():
    global rec
    pStart = 1
    pInterval = 1
    if rec == 0:
        rec = pStart
    else:
        rec += pInterval
    return rec


def digitaItens():
    """
    Essa função agora gera uma tabela temporaria em memoria
    do tipo tabela de pedidos, e retorna os dados lidos para serem
    utilizados pela função "insereItens()"
    :return:
        dados_lidos
    """
    cursor = conexao.banco.cursor()
    comando_SQL = "CREATE TEMPORARY TABLE IF NOT EXISTS pedidos_temp " \
                  "(id INT AUTO_INCREMENT PRIMARY KEY," \
                  "codigo INT NOT NULL," \
                  "item VARCHAR(100) NOT NULL," \
                  "quantidade INT," \
                  "preco FLOAT," \
                  "sub_total FLOAT," \
                  "total FLOAT," \
                  "data DATETIME," \
                  "id_operacao INT" \
                  ") ENGINE MEMORY;"
    cursor.execute(comando_SQL)

    cursor = conexao.banco.cursor()
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    total = 0

    # DATA DO PEDIDO
    d = QDate.currentDate()
    dataAtual = d.toString(Qt.ISODate)
    data = str(dataAtual)

    numero = autoIncrement()
    # for i in range(0, 1000):
    #     numero += 1

    for i in range(len(dados_lidos)):
        if formulario_caixa.ProdutoItem.text() == dados_lidos[i][2]:
            prec = float(dados_lidos[i][3])
            quant = int(formulario_caixa.ldquantidade.text())
            sub_total = (quant * prec)
            total += sub_total

            cursor = conexao.banco.cursor()
            comando_SQL = "INSERT INTO pedidos_temp (codigo, item, quantidade, preco," \
                          "sub_total, Total, data, id_operacao" \
                          ")" \
                          "values (%s, %s, %s, %s, %s, %s, %s, %s)"
            dados = numero, (str(dados_lidos[i][2])), quant, prec, sub_total, total, str(data), 1
            cursor.execute(comando_SQL, dados)
            conexao.banco.commit()
            formulario_caixa.ProdutoItem.setText("")
            formulario_caixa.ldquantidade.setText("")

    cursor = conexao.banco.cursor()
    comando_SQL = "SELECT * FROM pedidos_temp"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    # mostra o resultado da tabela temporaria
    # print(dados_lidos)

    return dados_lidos


def insereItem():
    """
        Mostra os itens inseridos no grid
        e salva na tabela original (fazer ajustes)
    :return:
    """
    itens = digitaItens()

    # print(itens)

    formulario_caixa.tblw.setRowCount(len(itens))
    formulario_caixa.tblw.setColumnCount(7)

    for i in range(0, len(itens)):
        for j in range(0, 7):
            formulario_caixa.tblw.setItem(i, j, QtWidgets.QTableWidgetItem(str(itens[i][j])))

    # Copia os dados da tabela temporaria para a tabela original
    # cursor = conexao.banco.cursor()
    # comando_SQL = "INSERT INTO pedidos_temp (codigo, item, quantidade, preco, sub_total, Total, data, id_operacao)" \
    #               "SELECT codigo, item, quantidade, preco, sub_total, Total, data, id_operacao" \
    #               "FROM pedidos"
    # cursor.execute(comando_SQL)
    # conexao.banco.commit()


def abreCadastroCliente():
    formulario_cadclientes.show()

    # DATA DO CADASTRO
    d = QDate.currentDate()
    dataAtual = d.toString(Qt.ISODate)
    data = str(dataAtual)

    formulario_cadclientes.ldData.setText(data)

    return data


def abreCadastroEndereco():
    formulario_cadenderecos.show()

    # DATA DO CADASTRO
    d = QDate.currentDate()
    dataAtual = d.toString(Qt.ISODate)
    data = str(dataAtual)

    # formulario_cadenderecos.ldData.setText(data)

    return data


def cadastrarEndereco():
    rua = formulario_cadenderecos.ldrua.text()
    numero = formulario_cadenderecos.ldnumero.text()
    complemento = formulario_cadenderecos.ldcomplemento.text()
    bairro = formulario_cadenderecos.ldbairro.text()
    cidade = formulario_cadenderecos.ldcidade.text()
    cep = formulario_cadenderecos.ldcep.text()
    uf = formulario_cadenderecos.ldcep.text()

    cursor = conexao.banco.cursor()
    comando_SQL = "INSERT INTO endereco (rua, numero, complemento, bairro, cidade, cep, uf) " \
                  "values (%s, %s, %s, %s, %s,%s, %s)"
    dados = (rua, numero, complemento, bairro, cidade, cep, uf)
    cursor.execute(comando_SQL, dados)
    conexao.banco.commit()

    formulario_cadenderecos.ldrua.setText("")
    formulario_cadenderecos.ldnumero.setText("")
    formulario_cadenderecos.ldcomplemento.setText("")
    formulario_cadenderecos.ldbairro.setText("")
    formulario_cadenderecos.ldcidade.setText("")
    formulario_cadenderecos.ldcep.setText("")


def cadastrarCliente():

    data = abreCadastroCliente()

    nome = formulario_cadclientes.ldNome.text()
    cpf = formulario_cadclientes.ldcpf.text()
    rg = formulario_cadclientes.ldrg.text()
    email = formulario_cadclientes.ldemail.text()
    fone1 = formulario_cadclientes.ldfone1.text()
    fone2 = formulario_cadclientes.ldfone2.text()

    rua = formulario_cadclientes.ldrua.text()
    numero = formulario_cadclientes.ldnumero.text()
    complemento = formulario_cadclientes.ldcomplemento.text()
    bairro = formulario_cadclientes.ldbairro.text()
    cidade = formulario_cadclientes.ldcidade.text()
    cep = formulario_cadclientes.ldcep.text()
    uf = formulario_cadclientes.lduf.text()

    obs = formulario_cadclientes.textEdit.toPlainText()

    print(data, nome, obs)

    cursor = conexao.banco.cursor()
    comando_SQL = "INSERT INTO clientes (" \
                  "nome, dt_cadastro, observacao, cpf, rg, fone01, fone02, email, cep, endereco, numero," \
                  "bairro, complemento, cidade, uf) " \
                  "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s)"
    dados = (str(nome), data, str(obs), cpf, rg, fone1, fone2, email, cep, rua, numero, bairro, complemento, cidade, uf)
    cursor.execute(comando_SQL, dados)
    conexao.banco.commit()

    # limpando todos os campos
    formulario_cadclientes.ldNome.setText("")
    formulario_cadclientes.ldcpf.setText("")
    formulario_cadclientes.ldrg.setText("")
    formulario_cadclientes.ldrg.setText("")
    formulario_cadclientes.ldfone1.setText("")
    formulario_cadclientes.ldfone2.setText("")

    formulario_cadclientes.ldrua.setText("")
    formulario_cadclientes.ldnumero.setText("")
    formulario_cadclientes.ldcomplemento.setText("")
    formulario_cadclientes.ldbairro.setText("")
    formulario_cadclientes.ldcidade.setText("")
    formulario_cadclientes.ldcep.setText("")

    formulario_cadclientes.textEdit.setText("")


def listClientes():
    formulario_listcli.show()

    cursor = conexao.banco.cursor()
    comando_SQL = "SELECT * FROM clientes"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    formulario_listcli.tblwclientes.setRowCount(len(dados_lidos))
    formulario_listcli.tblwclientes.setColumnCount(15)

    for i in range(0, len(dados_lidos)):
        for j in range(0, 15):
            formulario_listcli.tblwclientes.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))


def cadastroProduto():
    codigo = formulario.ldCod.text()
    descricao = formulario.ldDesc.text()
    preco = formulario.ldPrec.text()
    Categoria = ""

    if formulario.rb01.isChecked():
        print("Categoria Unhas foi Selecionada")
        Categoria = "Unhas"

    elif formulario.rb02.isChecked():
        print("Categoria Maquiagens foi Selecionada")
        Categoria = "Maquiagens"

    elif formulario.rb03.isChecked():
        print("Categoria Pele foi Selecionada")
        Categoria = "Pele"

    elif formulario.rb04.isChecked():
        print("Categoria Cabelo foi Selecionada")
        Categoria = "Cabelo"

    cursor = conexao.banco.cursor()
    comando_SQL = "INSERT INTO produtos (codigo, descricao,preco,categoria) values (%s, %s, %s, %s)"
    dados = (str(codigo), str(descricao), str(preco), Categoria)
    cursor.execute(comando_SQL, dados)
    conexao.banco.commit()
    # limpando todos os campos
    formulario.ldCod.setText("")
    formulario.ldDesc.setText("")
    formulario.ldPrec.setText("")


def listaProd():
    formulario_listprod.show()

    cursor = conexao.banco.cursor()
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    formulario_listprod.tableWidget.setRowCount(len(dados_lidos))
    formulario_listprod.tableWidget.setColumnCount(5)

    for i in range(0, len(dados_lidos)):
        for j in range(0, 5):
            formulario_listprod.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))


app = QtWidgets.QApplication([])

menu = uic.loadUi("menuPrincipal.ui")
formulario = uic.loadUi("cadProd.ui")
formulario_listprod = uic.loadUi("listprod.ui")
formulario_listcli = uic.loadUi("listCli.ui")
formulario_editprod = uic.loadUi("editprod.ui")
formulario_caixa = uic.loadUi("ctrlCaixa.ui")
formulario_cadclientes = uic.loadUi("cadCli.ui")
formulario_cadenderecos = uic.loadUi("cadEnd.ui")

menu.actionCadastrar.triggered.connect(mostracadprod)
menu.actionCadClientes.triggered.connect(abreCadastroCliente)
menu.actionEnderecos.triggered.connect(abreCadastroEndereco)
menu.actionListProd.triggered.connect(listaProd)
menu.actionGeraPdf.triggered.connect(gerar_pdf)
menu.actioncaixa.triggered.connect(abrePedidoCaixa)

formulario.btnCadastrar.clicked.connect(cadastroProduto)
formulario.btnListar.clicked.connect(listaProd)
formulario_listprod.btn_pdf.clicked.connect(gerar_pdf)

formulario_listprod.btnDel.clicked.connect(excluir_dados)
formulario_listprod.btnEditar.clicked.connect(edit_dados)
formulario_editprod.btnSalvarEdit.clicked.connect(salvar)

formulario_caixa.btnInsere.clicked.connect(insereItem)
formulario_caixa.btngerar.clicked.connect(digitaItens)

formulario_cadclientes.btnCadastrar.clicked.connect(cadastrarCliente)
formulario_cadclientes.btnlistar.clicked.connect(listClientes)
formulario_cadenderecos.btnCadEnder.clicked.connect(cadastrarEndereco)

menu.show()
menu.progressBar.hide()
app.exec()

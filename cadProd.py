from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import QDate, QTime, QDateTime, Qt
from PyQt5.QtWidgets import QMessageBox

from datetime import date, datetime

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


def selecionaProduto():
    formulario_caixa.show()

    cursor = conexao.banco.cursor()
    comando_SQL = "SELECT * FROM tipo_operacao"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    combo = [numero for numero in dados_lidos]
    print(combo)

    for c in range(len(combo)):
        formulario_caixa.comboBox.addItems([combo[c][1]])

    # formulario_caixa.comboBox2.activated.connect(insereItem)

    # DATA DO PEDIDO
    d = QDate.currentDate()
    dataAtual = d.toString(Qt.ISODate)
    data = str(dataAtual)
    formulario_caixa.dtEdit.setText(data)
    # formulario_caixa.comboBox.addItems(["Pedido", "Balcão", "Orçamento"])
    # formulario_caixa.comboBox.addItems([combo[0][2]])


def insereItem():
    cursor = conexao.banco.cursor()
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    itens = preparaItem()
    item = [item for item in itens]

    print(item)

    # for i in range(len(dados_lidos)):
    #     if formulario_caixa.ProdutoItem.text() == dados_lidos[i][2]:
    #         itens_pedido["item"] = (dados_lidos[i][2])
    #         itens_pedido["preco"] = (dados_lidos[i][3])
    #
    #
    # formulario_caixa.tblw.setRowCount(len(dados_lidos))
    # formulario_caixa.tblw.setColumnCount(4)
    # formulario_caixa.ProdutoItem.setText("")
    #
    # for i in range(1):
    #     for j in range(0, 1):
    #         formulario_caixa.tblw.setItem(i, j, QtWidgets.QTableWidgetItem(str(item[0])))
    #         formulario_caixa.tblw.setItem(i, j + 2, QtWidgets.QTableWidgetItem(str(item[1])))


def preparaItem():
    """
    Essa função armazena os itens digidados e
    guarda em uma dicionario dentro de uma lista
    :return:
    """
    cursor = conexao.banco.cursor()
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    itens_pedido = {}
    item = []
    for i in range(len(dados_lidos)):
        if formulario_caixa.ProdutoItem.text() == dados_lidos[i][2]:
            itens_pedido["item"] = (dados_lidos[i][2])
            itens_pedido["preco"] = (dados_lidos[i][3])

            item.append(itens_pedido)
    return item


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
formulario_editprod = uic.loadUi("editprod.ui")
formulario_caixa = uic.loadUi("ctrlCaixa.ui")

menu.actionCadastrar.triggered.connect(mostracadprod)
menu.actionListProd.triggered.connect(listaProd)
menu.actionGeraPdf.triggered.connect(gerar_pdf)
menu.actioncaixa.triggered.connect(selecionaProduto)

formulario.btnCadastrar.clicked.connect(cadastroProduto)
formulario.btnListar.clicked.connect(listaProd)
formulario_listprod.btn_pdf.clicked.connect(gerar_pdf)

formulario_listprod.btnDel.clicked.connect(excluir_dados)
formulario_listprod.btnEditar.clicked.connect(edit_dados)
formulario_editprod.btnSalvarEdit.clicked.connect(salvar)
formulario_caixa.btnInsere.clicked.connect(insereItem)
formulario_caixa.btngerar.clicked.connect(preparaItem)

menu.show()
menu.progressBar.hide()
app.exec()

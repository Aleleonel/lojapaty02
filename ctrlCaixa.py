from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox

import conexao


def selecionaProduto():
    cursor = conexao.banco.cursor()
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    ctrlCaixa.comboBox>add()
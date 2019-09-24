from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout, QLabel, QLineEdit, QMessageBox, QPushButton, QTextEdit, QVBoxLayout, QWidget,QDialog
from PyQt5.QtWidgets import QApplication, QTextBrowser, QTableWidget,QTableView
from PyQt5.QtGui import QStandardItemModel,QStandardItem
import sys
import prettytable
import os
import configparser
import pyhdb

class hdb_query(QDialog):
    def __init__(self):
        super(hdb_query,self).__init__()
        # self.cursor = cursor
        self.HDB_tab_name = ''
        self.HDB_IP = ''
        self.HDB_PORT = ''
        self.HDB_account = ''
        self.HDB_pwd = ''

        self.model = QStandardItemModel()
        self.headerlist = ['TABLE_NAME','COLUMN_NAME','POSITION','DATA_TYPE_NAME','LENGTH','SCALE','COMMENTS']
        self.model.setHorizontalHeaderLabels(self.headerlist)

        HDB_tab_name = QLabel("Table Name: ")
        self.tabline = QLineEdit()
        self.tabline.setReadOnly(False)

        self.HDB_result_table = QTableView(self)


        self.get_result = QPushButton("执行")
        self.get_result.show()
        self.get_result.clicked.connect(self.get_result_set)

        buttonLayout1 = QVBoxLayout()
        buttonLayout1.addWidget(self.get_result)

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.tabline, 0, 0, Qt.AlignTop)
        mainLayout.addWidget(self.HDB_result_table,2,0,Qt.AlignTop)
        mainLayout.addLayout(buttonLayout1, 0, 1)
        # QMessageBox.information(self,"test","real test")
        self.setLayout(mainLayout)
        self.setWindowTitle("HANA Assist")
        self.setFixedHeight(200)
        self.setFixedWidth(800)

    def get_conf(self):
        if  os.path.exists('conf.conf'):
            cf = configparser.ConfigParser()
            cf.read('conf.conf')
            self.HDB_IP = cf.get('dev','IP')
            self.HDB_PORT = cf.get('dev','PORT')
            self.HDB_account = cf.get('dev','User')
            self.HDB_pwd = cf.get('dev','PWD')
        else:
            error_msg = "没有已保存的配置项"
            QMessageBox.information(self, "errer_message", error_msg)

    def get_result_set(self):
        self.get_conf()
        str_sql_prefix = "SELECT DISTINCT TABLE_NAME, COLUMN_NAME, POSITION, DATA_TYPE_NAME, LENGTH, SCALE, COMMENTS \
        FROM SYS.TABLE_COLUMNS WHERE TABLE_NAME = "
        str_sql = str_sql_prefix + "'" + str(self.tabline.text()) + "'" + "ORDER BY POSITION"
        try:
            dbcon = pyhdb.connect(
                host=self.HDB_IP,
                port=self.HDB_PORT,
                user=self.HDB_account,
                password=self.HDB_pwd
            )
            cursor = dbcon.cursor()
            print(cursor)
            cursor.execute(str_sql)
        except:
            if cursor.connection == '':
                error_msg = "光标出错"
                QMessageBox.information(self, "error_msg", error_msg)
                self.HDB_result_output.setText(str_sql)
            else:
                error_msg = "SQL执行出错"
                QMessageBox.information(self,"error_msg",error_msg)
                self.HDB_result_output.setText(str_sql)
        else:
            res = cursor.fetchall()
            for i in range(len(res)):
                for j in range(len(res[i])):
                    self.model.setItem(i,j,QStandardItem(str(res[i][j])))
            self.HDB_result_table.setModel(self.model)
            # self.HDB_result_output.setText(res[1][1])  # 在指定的区域显示提示信息

if __name__ == '__main__':
    app = QApplication(sys.argv)
    logon = hdb_query()
    logon.show()
    sys.exit(app.exec())

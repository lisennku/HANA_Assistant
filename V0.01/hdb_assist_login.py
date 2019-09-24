from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout, QLabel, QLineEdit, QMessageBox, QPushButton, QTextEdit, QVBoxLayout, QWidget,QDialog
import sys
from PyQt5.QtWidgets import QApplication
import pyhdb
import re
import hdb_assist_querywindow as qy
import os
import configparser


class Assist_Log_On(QWidget):
    def __init__(self):
        super(Assist_Log_On,self).__init__()
        self.HDB_IP = ''
        self.HDB_PORT = ''
        self.HDB_account = ''
        self.HDB_pwd = ''

        #输入HANA 数据库 连接信息
        HDB_IP_Lable = QLabel("IP: ")
        self.ipline = QLineEdit()
        self.ipline.setReadOnly(False)

        HDB_PORT_Lable = QLabel("PORT: ")
        self.portline = QLineEdit()
        self.portline.setReadOnly(False)

        HDB_ACT_Lable = QLabel("ACCOUNT: ")
        self.actline = QLineEdit()
        self.actline.setReadOnly(False)

        HDB_PWD_Lable = QLabel("PWD: ")
        self.pwdline = QLineEdit()
        self.pwdline.setReadOnly(False)

        # 按钮
        self.TestButton = QPushButton("测试连接")
        self.TestButton.show()
        self.TestButton.clicked.connect(self.test_con)

        self.FillConfButton = QPushButton("获取配置")
        self.FillConfButton.show()
        self.FillConfButton.clicked.connect(self.get_conf)

        self.SaveConButton = QPushButton("保存连接信息")
        self.SaveConButton.hide()
        self.SaveConButton.clicked.connect(self.save_conf)

        self.ConfirmButton = QPushButton("登录")
        self.ConfirmButton.hide()
        # self.ConfirmButton.clicked.connect(self.log_on)

        buttonLayout1 = QVBoxLayout()
        buttonLayout1.addWidget(self.TestButton)
        buttonLayout1.addWidget(self.FillConfButton)
        buttonLayout1.addWidget(self.SaveConButton)
        buttonLayout1.addWidget(self.ConfirmButton)
        #buttonLayout1.addStretch()

        #显示 Lable和输入框
        mainLayout = QGridLayout()
        mainLayout.addWidget(HDB_IP_Lable, 0, 0)
        mainLayout.addWidget(self.ipline, 0, 1)
        mainLayout.addWidget(HDB_PORT_Lable, 1, 0,Qt.AlignTop)
        mainLayout.addWidget(self.portline, 1, 1,Qt.AlignTop)
        mainLayout.addWidget(HDB_ACT_Lable, 2, 0,Qt.AlignTop)
        mainLayout.addWidget(self.actline, 2, 1,Qt.AlignTop)
        mainLayout.addWidget(HDB_PWD_Lable, 3, 0,Qt.AlignTop)
        mainLayout.addWidget(self.pwdline, 3, 1,Qt.AlignTop)
        mainLayout.addLayout(buttonLayout1, 1, 2)
        self.setLayout(mainLayout)
        self.setWindowTitle("HANA Assist")
        self.setFixedHeight(200)
        self.setFixedWidth(400)

    def save_conf(self):
        conf_file = open('conf.conf','w+')
        conf_file.write('[dev]')
        conf_file.writelines(['\nIP = ',self.HDB_IP])
        conf_file.writelines(['\nPort = ', self.HDB_PORT])
        conf_file.writelines(['\nUser = ', self.HDB_account])
        conf_file.writelines(['\nPWD = ', self.HDB_pwd])
        conf_file.close()
        error_msg = "已保存"
        QMessageBox.information(self,"error_msg",error_msg)

    def get_conf(self):
        if  os.path.exists('conf.conf'):
            cf = configparser.ConfigParser()
            cf.read('conf.conf')
            self.HDB_IP = cf.get('dev','IP')
            self.HDB_PORT = cf.get('dev','PORT')
            self.HDB_account = cf.get('dev','User')
            self.HDB_pwd = cf.get('dev','PWD')
            self.ipline.setText(self.HDB_IP)
            self.portline.setText(self.HDB_PORT)
            self.actline.setText(self.HDB_account)
            self.pwdline.setText(self.HDB_pwd)
        else:
            error_msg = "没有已保存的配置项"
            QMessageBox.information(self, "errer_message", error_msg)



    def test_con(self):
        if self.HDB_pwd + self.HDB_account + self.HDB_PORT +self.HDB_IP == '':
            self.HDB_IP = self.ipline.text()
            self.HDB_PORT = self.portline.text()
            self.HDB_account = self.actline.text()
            self.HDB_pwd = self.pwdline.text()
        if self.char_legal('IP',self.HDB_IP) & self.char_legal('PORT',self.HDB_PORT):
            try:
                dbcon = pyhdb.connect(
                    host = self.HDB_IP,
                    port = self.HDB_PORT,
                    user = self.HDB_account,
                    password = self.HDB_pwd
                                      )
            except:
                error_msg = "连接数据库发生意外"
                QMessageBox.information(self,"errer_message",error_msg)
                return False
            else:
                dbcon.close()
                self.save_conf()
                error_msg = "成功连接数据库"
                self.SaveConButton.show()
                self.ConfirmButton.show()
                QMessageBox.information(self,"errer_message",error_msg)
                return True
        else:
            QMessageBox.information(self,"errer_message","连接字符串有误")
            return False


    def char_legal(self,check_type,char):
        if check_type.upper() == 'IP':
            if re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", char):
                return True
            else:
                return False
        elif check_type.upper() == 'PORT':
            if re.match(r"[0-9]{5}", char):
                return True
            else:
                return False
        else:
            return False

    def get_cursor(self):
        if self.HDB_pwd + self.HDB_account + self.HDB_PORT +self.HDB_IP == '':
            self.HDB_IP = self.ipline.text()
            self.HDB_PORT = self.portline.text()
            self.HDB_account = self.actline.text()
            self.HDB_pwd = self.pwdline.text()
        try:
            dbcon = pyhdb.connect(
                host=self.HDB_IP,
                port=self.HDB_PORT,
                user=self.HDB_account,
                password=self.HDB_pwd
                                 )
        except:
            return False
        else:
            cursor = dbcon.cursor()
            return cursor()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    logon = Assist_Log_On()
    logon.show()

    query = qy.hdb_query()
    logon.ConfirmButton.clicked.connect(query.show)
    sys.exit(app.exec())

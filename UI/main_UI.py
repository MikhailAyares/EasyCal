import sys
import time
import sqlite3

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QStackedWidget, QMessageBox, QDialog
from Signup import Signup_Window
from Login import Ui_Form as Login_Window
from Prelogin import Prelogin_Window
from Home import Home_Window
from User_database import Register,login,get_data


class Prelogin(QMainWindow):
    
    def __init__(self,manager):
        super().__init__()
        self.prelogwin = Prelogin_Window()
        self.prelogwin.setupUi(self)
        
        self.manager = manager
        
        self.prelogwin.tombolYES.clicked.connect(self.yes_clicked)
        self.prelogwin.tombolNO.clicked.connect(self.no_clicked)
        
    def yes_clicked(self):
        self.manager.show_login()
    
    def no_clicked(self):
        callsignup = Signup(self.manager)
        callsignup.exec_()
        

class Login(QWidget):
    
    def __init__(self, manager):
        super().__init__()
        self.logwin = Login_Window()
        self.logwin.setupUi(self)
        
        self.manager = manager
        
        self.logwin.Enterbutton.clicked.connect(self.Enter_Clicked)
        self.logwin.backbutton.clicked.connect(self.back_clicked) 
        
    def Enter_Clicked(self):
        print("pp")
        username = self.logwin.inputNamauser.text()
        password = self.logwin.inputPassword.text()
        self.manager.show_home()
        
        '''msg_box = QMessageBox()
        
        if not username or not password:
            msg_box.warning(self, "Error", "Mohon isi username dan password.")
            return
        elif login(username,password):
            self.logwin.progress()
            self.manager.show_home()
        else:
            msg_box.critical(self, "Login Gagal", "Username atau Password salah.")'''
         
    def back_clicked(self):
        self.manager.show_prelogin()    
    
class Signup(QDialog):
    
    def __init__(self, manager):
        super().__init__()
        self.signwin = Signup_Window()
        self.signwin.setupUi(self)
        
        self.manager = manager
        
        self.signwin.Backbutton.clicked.connect(self.back_clicked)
        self.signwin.Savedatabutton.clicked.connect(self.save_clicked)
        
        self.gender = None
        self.signwin.Malebutton.clicked.connect(lambda: self.button_clicked("Male"))
        self.signwin.Femalebutton.clicked.connect(lambda: self.button_clicked("Female"))
            
    def button_clicked(self, gender):
        self.gender = gender
        
        if gender == "Male":
         self.signwin.Malebutton.setStyleSheet("background-color: lightblue;") 
         self.signwin.Femalebutton.setStyleSheet("background-color: rgb(255, 255, 255);")
        
        else:
         self.signwin.Malebutton.setStyleSheet("background-color: rgb(255, 255, 255);")
         self.signwin.Femalebutton.setStyleSheet("background-color: lightcoral;") 
         
    def back_clicked(self):
        self.close()
    
    def save_clicked(self):
        
        username = self.signwin.InputNamauser.text().strip()
        password = self.signwin.InputPassword.text()
        gender = self.gender
        Age_User = self.signwin.InputAgeuser.value()
        BB_User = self.signwin.InputBBuser.value()
        TB_User = self.signwin.InputTBuser.value()
        Target_BB = self.signwin.InputTBuser.value()      
        
        msg_box = QMessageBox()     

        if not username or not password or Age_User == 0 or BB_User == 0 or TB_User == 0 or Target_BB == 0:
            msg_box.warning(self, "Failed", "Silahkan lengkapi semua data. Pastikan angka tidak 0.")
        elif Register(username, password, Age_User, BB_User,TB_User,Target_BB):
            msg_box.information(self, "Sucess", "Data berhasil disimpan")
        else:
            msg_box.critical(self, "Failed", "Data user sudah tersedia")      
    
                
class Home(QMainWindow):
    
    def __init__(self, manager):
        super().__init__()
        self.homewin = Home_Window()
        self.homewin.setupUi(self)
        
        self.homewin.LogoutButton.clicked.connect(self.back_clicked)
        self.homewin.FoodlogButton.clicked.connect(lambda:print("foodlog"))
        self.homewin.progress.clicked.connect(lambda:print("progress"))
                
        self.manager = manager
        
    #def show_food_log():
    
    #def show_progress():
        
    def back_clicked(self):
        self.manager.show_login()    
            
class Mainapp(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EasyCal")
        self.setFixedSize(1056, 820)

        self.prelogin = Prelogin(self)
        self.login = Login(self)
        self.signup = Signup(self)
        self.home = Home(self)
                
        self.stackwidget = QStackedWidget()
        self.setCentralWidget(self.stackwidget)
        
        self.show_prelogin()        
        
        self.stackwidget.addWidget(self.prelogin)  
        self.stackwidget.addWidget(self.login)       
        self.stackwidget.addWidget(self.home)  
    
    def show_prelogin(self):
        self.stackwidget.setCurrentWidget(self.prelogin)
    def show_login(self):
        self.stackwidget.setCurrentWidget(self.login)
    def show_home(self):  
        self.stackwidget.setCurrentWidget(self.home)
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Mainapp()
    window.show()
    sys.exit(app.exec_())
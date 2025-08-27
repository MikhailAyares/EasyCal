import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QStackedWidget, QMessageBox, QDialog
from Signup import Signup_Window
from Login import Ui_Form as Login_Window
from Prelogin import Prelogin_Window
from Home import Home_Window
from User_database import Register,login,get_data
from Progress import Ui_MainWindow as Progress_Window
from Foodlog import Ui_MainWindow as Foodlog_Window
from addmanual import Ui_Addmanual as Addmanual_Window


class Prelogin(QMainWindow):
    
    def __init__(self,manager):
        super().__init__()
        self.prelogwin = Prelogin_Window()
        self.prelogwin.setupUi(self)
        
        self.manager = manager
        
        self.prelogwin.tombolYES.clicked.connect(lambda: self.manager.show_login())
        self.prelogwin.tombolNO.clicked.connect(self.no_clicked)
    
    def no_clicked(self):
        callsignup = Signup(self.manager)
        callsignup.exec_()
        

class Login(QWidget):
    
    def __init__(self, manager):
        super().__init__()
        self.logwin = Login_Window()
        self.logwin.setupUi(self)
        
        self.manager = manager
        
        self.logwin.Enterbutton.clicked.connect(lambda: self.manager.show_home())
        self.logwin.backbutton.clicked.connect(lambda: self.manager.show_prelogin()) 
        
    def Enter_Clicked(self,username):
        print("pp")
        username = self.logwin.inputNamauser.text()
        password = self.logwin.inputPassword.text()
        
        msg_box = QMessageBox()
        
        if not username or not password:
            msg_box.warning(self, "Error", "Mohon isi username dan password.")
            return
        elif login(username,password):
            
            self.logwin.progress()
            self.manager.show_home()
        else:
            msg_box.critical(self, "Login Gagal", "Username atau Password salah.")
    
    
class Signup(QDialog):
    
    def __init__(self, manager):
        super().__init__()
        self.signwin = Signup_Window()
        self.signwin.setupUi(self)
        
        self.manager = manager
        
        self.signwin.Backbutton.clicked.connect(lambda: self.close())
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
            
class Addmanual(QDialog):
    
    def __init__(self, manager):
        super().__init__()
        self.addmanualwin = Addmanual_Window()
        self.addmanualwin.setupUi(self)
        
        self.manager = manager
                
class Home(QMainWindow):
    
    def __init__(self, manager):
        super().__init__()
        self.homewin = Home_Window()
        self.homewin.setupUi(self)
        
        self.homewin.LogoutButton.clicked.connect(lambda: self.manager.show_login() )
        self.homewin.FoodlogButton.clicked.connect(lambda: self.manager.show_foodlog())
        self.homewin.progress.clicked.connect(lambda:self.manager.show_progress())
                
        self.manager = manager
        
    def display_data(self,username):
        
        display = get_data(username)
        
        if display:
            self.homewin.DisplayNameLabel.setText(display['username'])
            self.homewin.DisplayAgeLabel.setText(str(display['age']))
            self.homewin.DisplayHeightLabel.setText(str(display['height']))
            self.homewin.DisplayWeightLabel.setText(str(display['weight']))
            
class Foodlog(QMainWindow):
    
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.foodlogwin = Foodlog_Window()
        self.foodlogwin.setupUi(self)
        
        self.foodlogwin.home.clicked.connect(lambda: self.manager.show_home())
        self.foodlogwin.progress.clicked.connect(lambda: self.manager.show_progress())
        self.foodlogwin.addmanual_button.clicked.connect(self.show_addmanual)
        
    def show_addmanual(self):
        calladdmanual = Addmanual(self.manager)
        calladdmanual.exec_()
        
class Progress(QMainWindow):
    
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.progresswin = Progress_Window()
        self.progresswin.setupUi(self)
        
        self.progresswin.home_button.clicked.connect(lambda: self.manager.show_home())
        self.progresswin.foodlog_button.clicked.connect(lambda: self.manager.show_foodlog())
        
class Mainapp(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EasyCal")
        self.setFixedSize(1056, 820)

        self.prelogin = Prelogin(self)
        self.login = Login(self)
        self.signup = Signup(self)
        self.home = Home(self)
        self.progress = Progress(self)
        self.foodlog = Foodlog(self)
        self.addmanualmenu = Addmanual(self)
                
        self.stackwidget = QStackedWidget()
        self.setCentralWidget(self.stackwidget)
        
        self.show_prelogin()        
        
        self.stackwidget.addWidget(self.prelogin)  
        self.stackwidget.addWidget(self.login)       
        self.stackwidget.addWidget(self.home) 
        self.stackwidget.addWidget(self.foodlog)  
        self.stackwidget.addWidget(self.progress)  
    
    def show_prelogin(self):
        self.stackwidget.setCurrentWidget(self.prelogin)
    def show_login(self):
        self.stackwidget.setCurrentWidget(self.login)
    def show_home(self):  
        self.stackwidget.setCurrentWidget(self.home)
    def show_foodlog(self):  
        self.stackwidget.setCurrentWidget(self.foodlog)
    def show_progress(self):  
        self.stackwidget.setCurrentWidget(self.progress)
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Mainapp()
    window.show()
    sys.exit(app.exec_())
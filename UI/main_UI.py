import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QStackedWidget, QMessageBox, QDialog
from Signup import Signup_Window
from Login import Ui_Form as Login_Window
from Prelogin import Prelogin_Window
from Home import Home_Window
from User_database import Register, login, get_data
from Progress import Ui_MainWindow as Progress_Window
from Foodlog import Ui_MainWindow as Foodlog_Window
from addmanual import Ui_Addmanual as Addmanual_Window

class Prelogin(QMainWindow):
    def __init__(self, manager):
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
        self.logwin.Enterbutton.clicked.connect(self.enter_clicked) 
        self.logwin.backbutton.clicked.connect(self.back_clicked) 
        
    def back_clicked(self):
        self.manager.show_prelogin()
        self.clear_fields()

    def clear_fields(self):
        self.logwin.inputNamauser.clear()
        self.logwin.inputPassword.clear()
        self.logwin.LoadingBar.setValue(0)
        
    def enter_clicked(self):
        username = self.logwin.inputNamauser.text().strip()
        password = self.logwin.inputPassword.text()
        
        msg_box = QMessageBox()
        
        if not username or not password:
            msg_box.warning(self, "Error", "Mohon isi username dan password.")
            return
        
        if login(username, password):
            self.logwin.progress()
            self.manager.show_home(username)
        else:
            msg_box.critical(self, "Login Gagal", "Username atau Password salah.")
    
class Signup(QDialog):
    def __init__(self, manager):
        super().__init__()
        self.signwin = Signup_Window()
        self.signwin.setupUi(self)
        self.manager = manager
        self.signwin.Backbutton.clicked.connect(self.close)
        self.signwin.Savedatabutton.clicked.connect(self.save_clicked)
        
        self.gender = None 
        self.signwin.Malebutton.clicked.connect(lambda: self.gender_button_clicked("Male"))
        self.signwin.Femalebutton.clicked.connect(lambda: self.gender_button_clicked("Female"))
            
    def gender_button_clicked(self, gender):
        self.gender = gender
        if gender == "Male":
           self.signwin.Malebutton.setStyleSheet("background-color: lightblue; border: 1px solid #ccc; border-radius: 5px; font: 10pt 'Segoe UI';") 
           self.signwin.Femalebutton.setStyleSheet("background-color: white; border: 1px solid #ccc; border-radius: 5px; font: 10pt 'Segoe UI';")
        else:
           self.signwin.Malebutton.setStyleSheet("background-color: white; border: 1px solid #ccc; border-radius: 5px; font: 10pt 'Segoe UI';")
           self.signwin.Femalebutton.setStyleSheet("background-color: lightcoral; border: 1px solid #ccc; border-radius: 5px; font: 10pt 'Segoe UI';") 
    
    def save_clicked(self):

        username = self.signwin.InputNamauser.text().strip()
        password = self.signwin.InputPassword.text()
        gender = self.gender
        age_user = self.signwin.InputAgeuser.value()
        start_weight = self.signwin.InputBBuser.value()
        height = self.signwin.InputTBuser.value()
        goal_weight = self.signwin.InputTargetBB.value()
        
        
        activity_map = {"Sedentary": 1, "Light": 2, "Moderate": 3, "Very active": 4}
        activity_level = activity_map.get(self.signwin.ActivityBox.currentText())

        weekly_goal_map = {"0.25 kg/week": 0.25, "0.5 kg/week": 0.5, "1.0 kg/week": 1.0}
        weekly_goal = weekly_goal_map.get(self.signwin.WeeklyBox.currentText())
        
        msg_box = QMessageBox()

        if not all([username, password, gender, age_user, start_weight, height, goal_weight]):
            msg_box.warning(self, "Gagal", "Silakan lengkapi semua data. Pastikan nilai numerik tidak 0.")
            return

        if Register(username, password, age_user, gender, start_weight, goal_weight, activity_level, weekly_goal, height):
            msg_box.information(self, "Sukses", "Data berhasil disimpan. Silakan login.")
            self.accept() 
        else:
            msg_box.critical(self, "Gagal", "Username ini sudah terdaftar.")

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
        self.manager = manager
        
        self.homewin.LogoutButton.clicked.connect(self.logout_clicked)
        self.homewin.FoodlogButton.clicked.connect(lambda: self.manager.show_foodlog())
        self.homewin.progress.clicked.connect(lambda: self.manager.show_progress())
    
    def logout_clicked(self):
        self.manager.show_login()
        self.clear_display_data()

    def clear_display_data(self):
        self.homewin.DisplayNameLabel.clear()
        self.homewin.DisplayAgeLabel.clear()
        self.homewin.DisplayGenderLabel.clear()
        self.homewin.DisplayHeightLabel.clear()
        self.homewin.DisplayWeightLabel.clear()
        self.homewin.DisplayWeightLabel2.clear() 
        self.homewin.DisplayWeightLabel3.clear() 

    def display_data(self, username):
        user_data = get_data(username)
        
        if user_data:
            self.homewin.DisplayNameLabel.setText(user_data['username'])
            self.homewin.DisplayAgeLabel.setText(str(user_data['age']))
            self.homewin.DisplayGenderLabel.setText(user_data['gender'])
            self.homewin.DisplayHeightLabel.setText(str(user_data['height']))
            self.homewin.DisplayWeightLabel.setText(str(user_data['current_weight']))
            self.homewin.DisplayWeightLabel2.setText(str(user_data['start_weight']))
            self.homewin.DisplayWeightLabel3.setText(str(user_data['goal_weight']))
        else:
            self.clear_display_data()
            QMessageBox.critical(self, "Error", f"Tidak dapat memuat data untuk pengguna: {username}")
            
class Foodlog(QMainWindow):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.foodlogwin = Foodlog_Window()
        self.foodlogwin.setupUi(self)
        self.foodlogwin.home.clicked.connect(lambda: self.manager.show_home(self.manager.current_user))
        self.foodlogwin.progress.clicked.connect(lambda: self.manager.show_progress())
        self.foodlogwin.addmanual.clicked.connect(self.show_addmanual)
        
    def show_addmanual(self):
        calladdmanual = Addmanual(self.manager)
        calladdmanual.exec_()
        
class Progress(QMainWindow):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.progresswin = Progress_Window()
        self.progresswin.setupUi(self)
        self.progresswin.home_button.clicked.connect(lambda: self.manager.show_home(self.manager.current_user))
        self.progresswin.foodlog_button.clicked.connect(lambda: self.manager.show_foodlog())
        
class Mainapp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EasyCal")
        self.setFixedSize(1056, 820)

        self.current_user = None

        self.prelogin = Prelogin(self)
        self.login = Login(self)
        self.home = Home(self)
        self.progress = Progress(self)
        self.foodlog = Foodlog(self)
              
        self.stackwidget = QStackedWidget()
        self.setCentralWidget(self.stackwidget)
        
        self.stackwidget.addWidget(self.prelogin)
        self.stackwidget.addWidget(self.login)
        self.stackwidget.addWidget(self.home)
        self.stackwidget.addWidget(self.foodlog)
        self.stackwidget.addWidget(self.progress)
        
        self.show_prelogin()

    def show_prelogin(self):
        self.stackwidget.setCurrentWidget(self.prelogin)
        
    def show_login(self):
        self.login.clear_fields() 
        self.stackwidget.setCurrentWidget(self.login)
        
    def show_home(self, username):
        self.current_user = username 
        self.home.display_data(self.current_user) 
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


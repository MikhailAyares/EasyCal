import sys
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QStackedWidget, QMessageBox, QDialog

# Import kelas UI dari file masing-masing
from Signup import Signup_Window
from Login import Ui_Form
from Prelogin import Prelogin_Window
from Home import Home_Window

# Import file database yang baru kita buat
import database

class Login(QWidget):
    def __init__(self, manager):
        super().__init__()
        self.logwin = Ui_Form()
        self.logwin.setupUi(self)
        
        self.manager = manager
        self.logwin.Enterbutton.clicked.connect(self.enter_clicked)
        self.logwin.backbutton.clicked.connect(self.back_clicked) 
        
    def enter_clicked(self):
        username = self.logwin.inputNamauser.text().strip()
        password = self.logwin.inputPassword.text()

        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Username dan Password tidak boleh kosong.")
            return

        # Memeriksa kredensial ke database
        if database.check_user_credentials(username, password):
            # Jika valid, pindah ke halaman home dan kirim username
            self.manager.show_home(username)
        else:
            # Jika tidak valid, tampilkan pesan error
            QMessageBox.critical(self, "Login Gagal", "Username atau Password salah.")

    def back_clicked(self):
        # Menutup window manager (seluruh aplikasi login/home)
        self.manager.close()

class Signup(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.signwin = Signup_Window()
        self.signwin.setupUi(self)
        
        self.signwin.Backbutton.clicked.connect(self.back_clicked)
        self.signwin.Savedatabutton.clicked.connect(self.save_clicked)
        
    def back_clicked(self):
        self.close()
    
    def save_clicked(self):
        username = self.signwin.InputNamauser.text().strip()
        password = self.signwin.InputPassword.text()
        age = self.signwin.InputAgeuser.value()
        weight = self.signwin.InputBBuser.value() # Seharusnya ini berat badan (BB)
        height = self.signwin.InputTBuser.value() # Seharusnya ini tinggi badan (TB)
        target_weight = self.signwin.InputTargetBB.value()

        # Validasi input tidak boleh kosong
        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Username dan Password tidak boleh kosong.")
            return

        # Memasukkan data ke database
        if database.insert_user_data(username, password, age, weight, height, target_weight):
            QMessageBox.information(self, "Sukses", "Akun berhasil dibuat! Silakan login.")
            self.close() # Menutup dialog signup jika berhasil
        else:
            QMessageBox.critical(self, "Error", "Username sudah digunakan. Silakan pilih username lain.")

class Home(QWidget):
    def __init__(self, manager):
        super().__init__()
        self.homewin = Home_Window()
        self.homewin.setupUi(self)
        
        self.manager = manager
        self.homewin.LogoutButton.clicked.connect(self.logout_clicked)
        
    def load_user_data(self, username):
        """Fungsi ini dipanggil untuk memuat dan menampilkan data user."""
        user_data = database.get_user_data(username)
        
        if user_data:
            # Mengisi semua label dengan data dari database
            # str() digunakan untuk mengubah angka menjadi teks agar bisa ditampilkan di QLabel
            self.homewin.DisplayNameLabel.setText(user_data['username'])
            self.homewin.DisplayAgeLabel.setText(str(user_data['age']))
            self.homewin.DisplayHeightLabel.setText(str(user_data['height']))
            self.homewin.DisplayWeightLabel.setText(str(user_data['weight']))
            
            # Mengisi label progress berat badan
            self.homewin.DisplayWeightLabel2.setText(str(user_data['weight'])) # Berat awal
            self.homewin.DisplayWeightLabel3.setText(str(user_data['target_weight'])) # Target berat
            
    '''def clear_user_data(self):
        """Membersihkan data user saat logout."""
        self.homewin.DisplayNameLabel.clear()
        self.homewin.DisplayAgeLabel.clear()
        self.homewin.DisplayHeightLabel.clear()
        self.homewin.DisplayWeightLabel.clear()
        self.homewin.DisplayWeightLabel2.clear()
        self.homewin.DisplayWeightLabel3.clear()

    def logout_clicked(self):
        self.clear_user_data() # Membersihkan data di halaman home
        self.manager.show_login() # Kembali ke halaman login'''
            
class WindowManager(QMainWindow):
    def __init__(self):
        super().__init__()

        self.stackwidget = QStackedWidget()
        self.setCentralWidget(self.stackwidget)

        # Membuat instance halaman
        self.login_page = Login(self)
        self.home_page = Home(self)

        # Menambahkan halaman ke stack
        self.stackwidget.addWidget(self.login_page)
        self.stackwidget.addWidget(self.home_page)
        
        self.show_login()

    def show_login(self):
        self.setWindowTitle("Login")
        self.setFixedSize(410, 410) # Mengatur ukuran window agar pas
        self.stackwidget.setCurrentWidget(self.login_page)

    def show_home(self, username):
        """Menerima username dan memuat data sebelum menampilkan halaman home."""
        self.setWindowTitle("Home")
        self.setFixedSize(720, 820) # Mengatur ukuran window agar pas
        self.home_page.load_user_data(username) # Memanggil fungsi untuk memuat data
        self.stackwidget.setCurrentWidget(self.home_page)
        
class Mainapp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.prelogwin = Prelogin_Window()
        self.prelogwin.setupUi(self)
        self.setWindowTitle("Welcome")
        self.setFixedSize(900, 700)
        
        self.prelogwin.tombolYES.clicked.connect(self.yes_clicked)
        self.prelogwin.tombolNO.clicked.connect(self.no_clicked)
        
    def yes_clicked(self):
        # Membuat instance WindowManager yang akan menangani login dan home
        self.window_manager = WindowManager()
        self.window_manager.show()
        self.hide() # Sembunyikan jendela prelogin

    def no_clicked(self):
        signup_dialog = Signup(self)
        signup_dialog.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Inisialisasi database saat aplikasi pertama kali dijalankan
    database.init_db()
    
    window = Mainapp()
    window.show()
    sys.exit(app.exec_())

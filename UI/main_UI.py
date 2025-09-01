import sys
from datetime import date, datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QStackedWidget, QMessageBox, QDialog, QVBoxLayout, QTableWidgetItem
from PyQt5.QtGui import QIcon
from Signup import Signup_Window
from Login import Ui_Form as Login_Window
from Prelogin import Prelogin_Window
from Home import Home_Window
from User_database import Register, login, update_data, get_data, update_calories, get_calories, add_meal_log, get_meal_logs_by_date, get_calorie_history, get_weight_history, get_latest_target_calories, save_target_calories
from Progress import Ui_MainWindow as Progress_Window
from Foodlog import Ui_MainWindow as Foodlog_Window
from Addmanual import Ui_Addmanual as Addmanual_Window
from searchfood import Ui_searchfood as searchfood_Window
import calories_formula
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from Updatedata import Ui_Form as Update_Window
import numpy as np

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.fig = Figure(figsize=(6, 3), dpi=75)
        self.axes = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.setParent(parent)
        self.updateGeometry()

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
        
        
        activity_map = {"Sedentary (no exercise)": "Sedentary", "Light (1-3 times/week)": "Light", "Moderate (4-5 times/week)": "Moderate", "Very active(6-7 times/week)": "Very active"}
        activity_level = activity_map.get(self.signwin.ActivityBox.currentText())

        weekly_goal_map = {"0.25 kg/week": 0.25, "0.5 kg/week": 0.5, "1.0 kg/week": 1.0}
        weekly_goal = weekly_goal_map.get(self.signwin.WeeklyBox.currentText())
        
        msg_box = QMessageBox()

        if not all([username, password, gender, age_user, start_weight, height, goal_weight]):
            msg_box.warning(self, "Gagal", "Silakan lengkapi semua data. Pastikan nilai numerik tidak 0.")
            return

        if Register(username, password, age_user, gender, start_weight, goal_weight, activity_level, weekly_goal, height):
            bmr = calories_formula.bmr_calculate(age_user, gender, start_weight, height)
            calories_min = calories_formula.calories_min(bmr, activity_level)
            calories_deficit = calories_formula.calories_deficit(calories_min, weekly_goal)
            target_calories = calories_formula.calories_target(calories_min, calories_deficit, goal_weight, start_weight)
            save_target_calories(username, target_calories)
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

        self.addmanualwin.insercalories.setMaximum(9999.99)
        self.addmanualwin.insertprotein.setMaximum(9999.99)
        self.addmanualwin.insertfat.setMaximum(9999.99)
        self.addmanualwin.insercarbs.setMaximum(9999.99)
        self.addmanualwin.insertportion.setMaximum(9999.99)

        self.addmanualwin.save.clicked.connect(self.accept)
        self.addmanualwin.cancel.clicked.connect(self.reject)
    
    def get_data(self):
        return {
            "name": self.addmanualwin.insertname.text(),
            "calories": self.addmanualwin.insercalories.value(),
            "protein": self.addmanualwin.insertprotein.value(),
            "fat": self.addmanualwin.insertfat.value(),
            "carbs": self.addmanualwin.insercarbs.value(),
            "portion": self.addmanualwin.insertportion.value()
        }

class searchfood(QDialog):
    def __init__(self, manager):
        super().__init__()
        self.searchfoodwin = searchfood_Window()
        self.searchfoodwin.setupUi(self)
        self.manager = manager

        self.searchfoodwin.pushButton_4.clicked.disconnect()
        self.searchfoodwin.pushButton_4.clicked.connect(self.accept)

    def get_picked_items(self):
        return self.searchfoodwin.picked_item

    def get_food_details(self, food_name):
        cursor = self.searchfoodwin.cursor
        cursor.execute("SELECT calories, proteins, fat, carbohydrate FROM nutrisi WHERE name = ?", (food_name,))
        result = cursor.fetchone()
        if result:
            return {
                "calories": result[0],
                "proteins": result[1],
                "fat": result[2],
                "carbs": result[3]
            }
        return None
    
class UpdateData(QDialog):
    def __init__(self, manager):
        super().__init__()
        self.updatewin = Update_Window()
        self.updatewin.setupUi(self)
        self.manager = manager

        
        self.updatewin.pushButton.clicked.connect(self.save_clicked)
        self.updatewin.cancel.clicked.connect(self.close)
    
    def save_clicked(self):
        username=self.manager.current_user
        current_weight = self.updatewin.currentweight_2.value()
        target_weight = self.updatewin.targetweight_2.value()
        activity_map = {"Sedentary (no exercise)": "Sedentary", "Light (1-3 times/week)": "Light", "Moderate (4-5 times/week)": "Moderate", "Very active(6-7 times/week)": "Very active"}
        activity_level = activity_map.get(self.updatewin.activity.currentText())
 
        msg_box = QMessageBox()

        if update_data(username, current_weight, target_weight, activity_level):
            msg_box.information(self, "Sukses", "Update data berhasil.")
            self.accept()

        else:
            msg_box.critical(self, "Gagal", "Update data belum berhasil.")






                
class Home(QMainWindow):
    def __init__(self, manager):
        super().__init__()
        self.homewin = Home_Window()
        self.homewin.setupUi(self)
        self.manager = manager
        
        self.homewin.LogoutButton.clicked.connect(self.logout_clicked)
        self.homewin.FoodlogButton.clicked.connect(lambda: self.manager.show_foodlog())
        self.homewin.progress.clicked.connect(lambda: self.manager.show_progress())
        self.homewin.update_weight.clicked.connect(lambda: self.manager.updatedata.exec_())
    
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
        self.homewin.DisplayBreakfastLabel.setText("0")
        self.homewin.DisplayLunchLabel.setText("0")
        self.homewin.DisplayDinnerLabel.setText("0")
        self.homewin.CaloriBar.setValue(0)

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
            
            today_str = date.today().strftime('%Y-%m-%d')
            calories_data = get_calories(username, today_str)
            
            if calories_data:
                bfast = calories_data.get('breakfast_cal', 0)
                lunch = calories_data.get('lunch_cal', 0)
                dinner = calories_data.get('dinner_cal', 0)
                total = calories_data.get('total_cal', 0)
                
                self.homewin.DisplayBreakfastLabel.setText(str(int(bfast)))
                self.homewin.DisplayLunchLabel.setText(str(int(lunch)))
                self.homewin.DisplayDinnerLabel.setText(str(int(dinner)))
                self.homewin.CaloriBar.setValue(int(total))
            else:
                self.homewin.DisplayBreakfastLabel.setText("0")
                self.homewin.DisplayLunchLabel.setText("0")
                self.homewin.DisplayDinnerLabel.setText("0")
                self.homewin.CaloriBar.setValue(0)
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
        self.foodlogwin.searchfood.clicked.connect(self.show_searchfood)
        
    def load_and_display_meals(self):
        if not self.manager.current_user:
            return

        today_str = date.today().strftime('%Y-%m-%d')
        meal_logs = get_meal_logs_by_date(self.manager.current_user, today_str)
        
        table = self.foodlogwin.table
        table.setRowCount(0)
        
        calories_data = get_calories(self.manager.current_user, today_str)
        total_calories_consumed = 0
        total_protein = 0
        total_fat = 0
        total_carbs = 0

        for row_num, meal in enumerate(meal_logs):
            table.insertRow(row_num)
            
            total_calories_consumed += meal.get('calories', 0)
            total_protein += meal.get('protein', 0)
            total_fat += meal.get('fat', 0)
            total_carbs += meal.get('carbs', 0)

            log_time = datetime.strptime(meal['log_time'], '%Y-%m-%d %H:%M:%S').strftime('%H:%M')
            calories = f"{meal['calories']:.1f}"
            protein = f"{meal['protein']:.1f}"
            fat = f"{meal['fat']:.1f}"
            carbs = f"{meal['carbs']:.1f}"
            portion = f"{meal['portion']:.1f} gr"
            
            table.setItem(row_num, 0, QTableWidgetItem(meal['meal_name']))
            table.setItem(row_num, 1, QTableWidgetItem(log_time))
            table.setItem(row_num, 2, QTableWidgetItem(calories))
            table.setItem(row_num, 3, QTableWidgetItem(protein))
            table.setItem(row_num, 4, QTableWidgetItem(fat))
            table.setItem(row_num, 5, QTableWidgetItem(carbs))
            table.setItem(row_num, 6, QTableWidgetItem(portion))
        
        target_cal = calories_data.get('target_cal', 2000) if calories_data else 2000
        remaining_cal = target_cal - total_calories_consumed
        
        self.foodlogwin.calorie_2.setText(f"{int(total_calories_consumed)} cal") 
        self.foodlogwin.calorie_3.setText(f"{int(target_cal)} cal")
        self.foodlogwin.calorie.setText(f"{int(remaining_cal)} cal")
        
        self.foodlogwin.proteingram.setText(f"{total_protein:.1f} gr")
        self.foodlogwin.carbsgram.setText(f"{total_carbs:.1f} gr")
        self.foodlogwin.fatgram.setText(f"{total_fat:.1f} gr")

    def show_addmanual(self):
        calladdmanual = Addmanual(self.manager)
        if calladdmanual.exec_() == QDialog.Accepted:
            data = calladdmanual.get_data()
            if not data['name'] or data['portion'] == 0:
                QMessageBox.warning(self, "Input tidak lengkap", "nama makanan dan porsi jangan kosong.")
                return

            add_meal_log(
                username=self.manager.current_user,
                meal_name=data['name'],
                calories=data['calories'],
                protein=data['protein'],
                fat=data['fat'],
                carbs=data['carbs'],
                portion=data['portion']
            )
            self.load_and_display_meals()
    
    def show_searchfood(self):
        callsearchfood = searchfood(self.manager)
        callsearchfood = searchfood(self.manager)
        if callsearchfood.exec_() == QDialog.Accepted:
            picked_items = callsearchfood.get_picked_items()
            
            for name, portion in picked_items.items():
                food_details = callsearchfood.get_food_details(name)
                if food_details:
                    multiplier = portion / 100.0
                    calories = food_details['calories'] * multiplier
                    protein = food_details['proteins'] * multiplier
                    fat = food_details['fat'] * multiplier
                    carbs = food_details['carbs'] * multiplier
                    
                    add_meal_log(
                        username=self.manager.current_user,
                        meal_name=name,
                        calories=calories,
                        protein=protein,
                        fat=fat,
                        carbs=carbs,
                        portion=portion
                    )
            self.load_and_display_meals()
        
class Progress(QMainWindow):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.progresswin = Progress_Window()
        self.progresswin.setupUi(self)
        self.progresswin.home_button.clicked.connect(lambda: self.manager.show_home(self.manager.current_user))
        self.progresswin.foodlog_button.clicked.connect(lambda: self.manager.show_foodlog())
        self.setup_graphs(None, None, None) 

    def load_user_data(self, username):
        print(f"Loading progress data for user: {username}")
        user_data = get_data(username)
        if not user_data:
            self.show_no_data_message()
            return

        weight_data = get_weight_history(username)
        calorie_data = get_calorie_history(username)

        start_weight = float(user_data.get('start_weight', 0))
        current_weight = float(user_data.get('current_weight', 0))
        goal_weight = float(user_data.get('goal_weight', 0))

        target_calories = get_latest_target_calories(username)
        
        self.update_progress(start_weight, current_weight, goal_weight)
        self.predict_goal_achievement(start_weight, goal_weight, current_weight, calorie_data, target_calories)
        self.setup_graphs(weight_data, calorie_data, target_calories)

    def add_canvas_to_placeholder(self, placeholder, canvas):
        if placeholder.layout() is not None:
            while placeholder.layout().count():
                child = placeholder.layout().takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
        else:
            layout = QVBoxLayout()
            placeholder.setLayout(layout)

        placeholder.layout().addWidget(canvas)

    def setup_graphs(self, weight_data, calorie_data, target_calories):
        if self.progresswin.weight_graph_placeholder:
            weight_canvas = MplCanvas()
            self.plot_weight_graph(weight_canvas, weight_data)
            self.add_canvas_to_placeholder(self.progresswin.weight_graph_placeholder, weight_canvas)
            
        if self.progresswin.calories_graph_placeholder:
            calories_canvas = MplCanvas()
            self.plot_calories_graph(calories_canvas, calorie_data, target_calories)
            self.add_canvas_to_placeholder(self.progresswin.calories_graph_placeholder, calories_canvas)
        
    def plot_weight_graph(self, canvas, weight_data):
        ax = canvas.axes
        ax.cla()

        if weight_data:
            days = range(1, len(weight_data) + 1)
            
            ax.set_facecolor('#f8f8f8') 
            
            ax.plot(days, weight_data, marker='o', linestyle='-', color='#6495ED', linewidth=2, markersize=7)
            
            ax.set_title("Your Weight Journey", fontsize=14, fontweight='bold', color='#333333', fontname='Segoe UI')
            ax.set_ylabel("Weight (kg)", fontsize=11, color='#555555', fontname='Segoe UI')
            
            ax.grid(True, linestyle='--', alpha=0.6, color='#CCCCCC')
            
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color('#BBBBBB')
            ax.spines['bottom'].set_color('#BBBBBB')
            
            ax.tick_params(axis='x', labelsize=9, colors='#666666')
            ax.tick_params(axis='y', labelsize=9, colors='#666666')

            ax.set_xticks(days)
            ax.set_xticklabels([f"Day {d}" for d in days], rotation=45, ha='right', fontsize=8) 

        else:
            ax.text(0.5, 0.5, "Not enough data to show.", horizontalalignment='center',
                     verticalalignment='center', transform=ax.transAxes, fontsize=12, color='#888888')
            ax.set_xticks([])
            ax.set_yticks([])

        canvas.fig.tight_layout(pad=1)

    def plot_calories_graph(self, canvas, calorie_data, target_calories):
        ax = canvas.axes
        ax.cla()

        if calorie_data and target_calories:
            days = range(1, len(calorie_data) + 1)
            
            ax.set_facecolor('#f8f8f8') 

            colors = []
            for calorie in calorie_data:
                if calorie > target_calories:
                    colors.append('#E74C3C')
                elif calorie < target_calories:
                    colors.append('#F39C12')
                else:
                    colors.append('#2ECC71')

            ax.bar(days, calorie_data, color=colors, width=0.7, edgecolor='white', linewidth=0.8)
            
            ax.set_title("Your Daily Calorie Intake", fontsize=14, fontweight='bold', color='#333333', fontname='Segoe UI')
            ax.set_ylabel("Calories (kcal)", fontsize=11, color='#555555', fontname='Segoe UI')
            
            ax.grid(axis='y', linestyle='--', alpha=0.6, color='#CCCCCC')
            ax.grid(axis='x', visible=False)
            
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color('#BBBBBB')
            ax.spines['bottom'].set_color('#BBBBBB')
            
            ax.tick_params(axis='x', labelsize=9, colors='#666666')
            ax.tick_params(axis='y', labelsize=9, colors='#666666')

            ax.set_xticks(days)
            ax.set_xticklabels([f"Day {d}" for d in days], rotation=45, ha='right', fontsize=8)

        else:
            ax.text(0.5, 0.5, "No data to show.", horizontalalignment='center',
                     verticalalignment='center', transform=ax.transAxes, fontsize=12, color='#888888')
            ax.set_xticks([])
            ax.set_yticks([])

        canvas.fig.tight_layout(pad=1)

    def update_progress(self, start_weight, current_weight, goal_weight):
        self.progresswin.start_label.setStyleSheet("font-weight: bold;")
        self.progresswin.start_label.setText(f"{start_weight:.1f} kg")
        self.progresswin.current_label.setStyleSheet("color: limegreen; font-weight: bold;")
        self.progresswin.current_label.setText(f"{current_weight:.1f} kg")
        self.progresswin.goal_label.setStyleSheet("font-weight: bold;")
        self.progresswin.goal_label.setText(f"{goal_weight:.1f} kg")

        try:
            total_progress_needed = start_weight - goal_weight
            current_progress = start_weight - current_weight
            progress_percentage = (current_progress / total_progress_needed) * 100
            
            progress_percentage = max(0, min(100, progress_percentage))

            self.progresswin.progress_bar.setValue(int(progress_percentage))
            
            self.progresswin.percentage_label.setText(f"{int(progress_percentage)}%")
            
        except (ZeroDivisionError, TypeError):
            self.progresswin.progress_bar.setValue(0)
            self.progresswin.percentage_label.setText("N/A")
            
    def predict_goal_achievement(self, start_weight, goal_weight, current_weight, calorie_data, target_calories):
        avg_intake = np.mean(calorie_data)
        kcal_per_kg = 7700

        if goal_weight < start_weight:
            daily_deficit = target_calories - avg_intake
            
            if current_weight <= goal_weight:
                self.progresswin.days_to_goal_label.setText("Goal Achieved!")

            elif daily_deficit > 0: 
                weight_to_lose = current_weight - goal_weight
                total_kcal_to_lose = weight_to_lose * kcal_per_kg
                days_needed = total_kcal_to_lose / daily_deficit
                self.progresswin.days_to_goal_label.setText(f"{int(days_needed)} days")
            else:
                self.progresswin.days_to_goal_label.setText("Increase deficit to lose weight")

        elif goal_weight > start_weight:
            daily_surplus = avg_intake - target_calories

            if current_weight >= goal_weight:
                self.progresswin.days_to_goal_label.setText("Goal Achieved!")

            elif daily_surplus > 0: 
                weight_to_gain = goal_weight - current_weight
                total_kcal_to_gain = weight_to_gain * kcal_per_kg
                days_needed = total_kcal_to_gain / daily_surplus
                self.progresswin.days_to_goal_label.setText(f"{int(days_needed)} days")
            else:
                self.progresswin.days_to_goal_label.setText("Increase surplus to gain weight")

    def show_no_data_message(self):
        self.progresswin.start_label.setText("...")
        self.progresswin.current_label.setText("...")
        self.progresswin.goal_label.setText("...")
        self.progresswin.progress_bar.setValue(0)
        self.progresswin.percentage_label.setText("N/A")
        self.progresswin.days_to_goal_label.setText("No data")
        
class Mainapp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("Logokecil.png"))
        self.setWindowTitle("EasyCal")
        self.setFixedSize(1056, 820)

        self.current_user = None

        self.prelogin = Prelogin(self)
        self.login = Login(self)
        self.home = Home(self)
        self.progress = Progress(self)
        self.foodlog = Foodlog(self)
        self.addmanualmenu = Addmanual(self)
        self.searchfoodmenu = searchfood(self)
        self.updatedata = UpdateData(self)
            
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
        self.progress.load_user_data(self.current_user) 
        self.stackwidget.setCurrentWidget(self.home)
        
    def show_foodlog(self):
        self.foodlog.load_and_display_meals()
        self.stackwidget.setCurrentWidget(self.foodlog)

    def show_progress(self):
        self.stackwidget.setCurrentWidget(self.progress)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Mainapp()
    window.show()
    sys.exit(app.exec_())


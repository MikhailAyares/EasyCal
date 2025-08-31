import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QPushButton, QGraphicsDropShadowEffect, QLabel, QProgressBar, QFrame, QVBoxLayout, QWidget, QSizePolicy
from PyQt5 import uic
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QCursor, QColor, QIcon
import datetime
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

class MplCanvas(FigureCanvas):
    """
    A custom Matplotlib canvas class to be embedded in a PyQt5 UI.
    """
    def __init__(self, parent=None):
        # Create a new figure and axes with a reasonable default size
        self.fig = Figure(figsize=(6, 3), dpi=75)
        self.axes = self.fig.add_subplot(111)
        
        # Initialize the canvas with the figure
        super(MplCanvas, self).__init__(self.fig)
        
        # Set the canvas parent and size policy
        self.setParent(parent)
        self.updateGeometry()

# Main window class for your application
class Progress(QMainWindow):
    def __init__(self, start_weight=None, current_weight=None, goal_weight=None, weight_data=None, 
                 calorie_data=None, start_date=None, target_weeks=None, target_calories=None):
        super(Progress, self).__init__()

        # Load the UI from the .ui file.
        # This will automatically create attributes for your widgets
        # based on their objectName from Qt Designer.
        uic.loadUi("progress.ui", self)
        
        # Check if we have data to work with
        if start_weight and current_weight and goal_weight:
            # Update the labels and graphs with the provided data
            self.update_progress(float(start_weight), float(current_weight), float(goal_weight))
            self.predict_goal_achievement(start_weight, goal_weight, current_weight, calorie_data, target_calories)
        else:
            # If no data is provided, show a message on the UI
            self.show_no_data_message()
            
        # Setup the graphs, passing the historical data
        self.setup_graphs(weight_data, calorie_data, target_calories)

        self.home_button.clicked.connect(self.go_to_home)
        self.foodlog_button.clicked.connect(self.go_to_foodlog)
        self.logout_button.clicked.connect(self.logout)

    def go_to_home(self):
        self.close()

    def go_to_foodlog(self):
        self.close()

    def logout(self):
        self.close()

    def add_canvas_to_placeholder(self, placeholder, canvas):
        layout = QVBoxLayout(placeholder)
        layout.addWidget(canvas)

    def setup_graphs(self, weight_data, calorie_data, target_calories):
        """
        Sets up the Matplotlib canvases and adds them to the UI.
        """
        # Set up the weight progress graph
        if self.weight_graph_placeholder:
            # Pass the placeholder widget as the parent to the canvas
            weight_canvas = MplCanvas()
            self.plot_weight_graph(weight_canvas, weight_data)
            self.add_canvas_to_placeholder(self.weight_graph_placeholder, weight_canvas)
            
        # Set up the calories intake graph
        if self.calories_graph_placeholder:
            # Pass the placeholder widget as the parent to the canvas
            calories_canvas = MplCanvas()
            self.plot_calories_graph(calories_canvas, calorie_data, target_calories)
            self.add_canvas_to_placeholder(self.calories_graph_placeholder, calories_canvas)
        
    def plot_weight_graph(self, canvas, weight_data):
        ax = canvas.axes
        ax.cla() # Clear any previous plot

        if weight_data and len(weight_data) > 1:
            # Data from user input
            days = range(1, len(weight_data) + 1)
            
            # --- Casual Styling Changes for Weight Graph ---
            # Set a lighter background color for the plot area
            ax.set_facecolor('#f8f8f8') 
            
            # Use a friendly blue color for the line
            ax.plot(days, weight_data, marker='o', linestyle='-', color='#6495ED', linewidth=2, markersize=7)
            
            # Casual font and title styling
            ax.set_title("Your Weight Journey", fontsize=14, fontweight='bold', color='#333333', fontname='Segoe UI')
            ax.set_ylabel("Weight (kg)", fontsize=11, color='#555555', fontname='Segoe UI')
            #ax.set_xlabel("Day", fontsize=11, color='#555555', fontname='Segoe UI')
            
            # Customize gridlines to be lighter and less intrusive
            ax.grid(True, linestyle='--', alpha=0.6, color='#CCCCCC')
            
            # Make the plot border (spines) lighter or invisible
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color('#BBBBBB')
            ax.spines['bottom'].set_color('#BBBBBB')
            
            # Customize tick labels for better readability
            ax.tick_params(axis='x', labelsize=9, colors='#666666')
            ax.tick_params(axis='y', labelsize=9, colors='#666666')

            # Ensure x-axis shows appropriate labels for all days
            ax.set_xticks(days)
            ax.set_xticklabels([f"Day {d}" for d in days], rotation=45, ha='right', fontsize=8) # Rotate for long labels

        else:
            ax.text(0.5, 0.5, "Not enough data to show.", horizontalalignment='center',
                     verticalalignment='center', transform=ax.transAxes, fontsize=12, color='#888888')
            ax.set_xticks([])
            ax.set_yticks([])

        canvas.fig.tight_layout(pad=1) # Add more padding

    def plot_calories_graph(self, canvas, calorie_data, target_calories):
        ax = canvas.axes
        ax.cla() # Clear any previous plot

        if calorie_data and target_calories:
            days = range(1, len(calorie_data) + 1)
            
            # --- Casual Styling Changes for Calorie Graph ---
            ax.set_facecolor('#f8f8f8') 

            colors = []
            for calorie in calorie_data:
                if calorie > target_calories:
                    colors.append('#E74C3C') # Softer red for "Above Target"
                elif calorie < target_calories:
                    colors.append('#F39C12') # Softer orange for "Below Target"
                else:
                    colors.append('#2ECC71') # Green for "Within Target"

            # Plot the bar chart with adjusted width and edge color
            ax.bar(days, calorie_data, color=colors, width=0.7, edgecolor='white', linewidth=0.8)
            
            ax.set_title("Your Daily Calorie Intake", fontsize=14, fontweight='bold', color='#333333', fontname='Segoe UI')
            ax.set_ylabel("Calories (kcal)", fontsize=11, color='#555555', fontname='Segoe UI')
            #ax.set_xlabel("Day", fontsize=11, color='#555555', fontname='Segoe UI')
            
            # Only horizontal gridlines for bars, lighter
            ax.grid(axis='y', linestyle='--', alpha=0.6, color='#CCCCCC')
            ax.grid(axis='x', visible=False) # Hide vertical gridlines for bars
            
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
        """
        Calculates and updates the UI elements based on weight data.
        """
        # The 'self.start_label' and other widget variables
        # are automatically created by uic.loadUi()
        self.start_label.setText(f"{start_weight:.1f} kg")
        self.current_label.setText(f"{current_weight:.1f} kg")
        self.goal_label.setText(f"{goal_weight:.1f} kg")

        # Calculate progress percentage
        try:
            total_progress_needed = start_weight - goal_weight
            current_progress = start_weight - current_weight
            progress_percentage = (current_progress / total_progress_needed) * 100
            
            # Clamp the percentage to be between 0 and 100
            progress_percentage = max(0, min(100, progress_percentage))

            # Update the QProgressBar value
            self.progress_bar.setValue(int(progress_percentage))
            
            # Update the percentage label
            self.percentage_label.setText(f"{int(progress_percentage)}%")
            
        except (ZeroDivisionError, TypeError):
            # Handle cases where the goal and start weights are the same,
            # or data is invalid.
            self.progress_bar.setValue(0)
            self.percentage_label.setText("N/A")
            
    # --- NEW: Universal Prediction Algorithm Method ---
    def predict_goal_achievement(self, start_weight, goal_weight, current_weight, calorie_data, target_calories):
        """
        Predicts time to goal for both weight loss and gain using a pre-calculated TDEE.
        """
        # Step 2: Calculate user's average calorie intake
        avg_intake = np.mean(calorie_data)
        kcal_per_kg = 7700 # Approx. kcal in 1 kg of body weight

        # --- Branching Logic: Is the goal to lose or gain weight? ---
        
        # SCENARIO 1: WEIGHT LOSS GOAL
        if goal_weight < start_weight:
            daily_deficit = target_calories - avg_intake
            
            if current_weight <= goal_weight:
                self.days_to_goal_label.setText("Goal Achieved!")

            # Check if user is actually in a deficit
            elif daily_deficit > 0: 
                weight_to_lose = current_weight - goal_weight
                total_kcal_to_lose = weight_to_lose * kcal_per_kg
                days_needed = total_kcal_to_lose / daily_deficit
                self.days_to_goal_label.setText(f"{int(days_needed)} days")
            else:
                self.days_to_goal_label.setText("Increase deficit to lose weight")

        # SCENARIO 2: WEIGHT GAIN GOAL
        elif goal_weight > start_weight:
            daily_surplus = avg_intake - target_calories

            if current_weight >= goal_weight:
                self.days_to_goal_label.setText("Goal Achieved!")

            # Check if user is actually in a surplus
            elif daily_surplus > 0: 
                weight_to_gain = goal_weight - current_weight
                total_kcal_to_gain = weight_to_gain * kcal_per_kg
                days_needed = total_kcal_to_gain / daily_surplus
                self.days_to_goal_label.setText(f"{int(days_needed)} days")
            else:
                self.days_to_goal_label.setText("Increase surplus to gain weight")

    def show_no_data_message(self):
        """
        Displays a message on the UI when no data is provided for calculation.
        """
        self.start_label.setText("...")
        self.current_label.setText("...")
        self.goal_label.setText("...")
        self.progress_bar.setValue(0)
        self.percentage_label.setText("N/A")
        self.days_to_goal_label.setText("No data")

def main():
    """
    Main function to run the application.
    """
    app = QApplication(sys.argv)
    
    # --- HERE IS WHERE YOU WOULD INPUT YOUR TEST DATA ---
    # For a real application, these values would come from a database or file.
    # We will use lists to simulate that.
    start = 75.7
    current = 77
    goal = 80
    
    # Simulate a list of daily weight readings from the user
    weight_data = [
    85.0, 84.8, 84.9, 84.5, 84.2, 84.3, 83.9, 83.7, 83.8, 83.4,
    83.1, 83.2, 82.9, 82.7, 82.8, 82.5, 82.6, 82.3, 82.2, 82.1]
    
    # Simulate a list of daily calorie intake from the user
    calorie_data = [
    2250, 2100, 2300, 1950, 2050, 2150, 2200, 1900, 2000, 2250,
    2100, 1980, 2350, 2050, 2120, 1950, 2200, 2080, 2150, 1990,]
    
    target_calories = 2000

    # Pass the variables to your Progress class
    window = Progress(
        start_weight=start,
        current_weight=current, 
        goal_weight=goal,
        weight_data=weight_data,
        calorie_data=calorie_data,
        target_calories=target_calories
    )
    
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
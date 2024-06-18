import sys

import psutil
import pyqtgraph as pg
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QLabel,
                             QMainWindow, QPushButton, QStackedWidget,
                             QTableWidget, QTableWidgetItem, QVBoxLayout,
                             QWidget)


class HomeWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        self.system_info_cpu = QLabel()
        self.system_info_cpu.setStyleSheet("color: white; font-size: 18px;")
        layout.addWidget(self.system_info_cpu)

        # Add graph widgets
        self.cpu_graph = pg.PlotWidget()
        self.cpu_graph.setLabel('left', 'CPU Usage (%)')
        layout.addWidget(self.cpu_graph)

        self.system_info_ram = QLabel()
        self.system_info_ram.setStyleSheet("color: white; font-size: 18px;")
        layout.addWidget(self.system_info_ram)

        self.ram_graph = pg.PlotWidget()
        self.ram_graph.setLabel('left', 'RAM Usage (%)')
        layout.addWidget(self.ram_graph)

        self.cpu_data = []
        self.ram_data = []
        self.time_data = []
        self.max_points = 100

        self.cpu_curve = self.cpu_graph.plot(pen='y')
        self.ram_curve = self.ram_graph.plot(pen='y')

        # Adjust graph sizes
        self.cpu_graph.setFixedHeight(200)
        self.ram_graph.setFixedHeight(200)

        # Match colors with the theme
        self.cpu_graph.setBackground('#1e1e2e')  # Set background color
        self.cpu_curve.setPen(pg.mkPen(color='#f5c2e7', width=2))  # Set pen color

        self.ram_graph.setBackground('#1e1e2e')  # Set background color
        self.ram_curve.setPen(pg.mkPen(color='#f5c2e7', width=2))  # Set pen color

        

        self.cpu_graph.setYRange(0, 100, padding=0)
        self.ram_graph.setYRange(0, 100, padding=0)

        # Hide the axes
        self.cpu_graph.showAxis('left', False)
        self.cpu_graph.showAxis('bottom', False)
        self.ram_graph.showAxis('left', False)
        self.ram_graph.showAxis('bottom', False)

        # Add a border around the plot
        self.cpu_graph.setStyleSheet("border: 1px solid #d9e0ee;")
        self.ram_graph.setStyleSheet("border: 1px solid #d9e0ee;")

        # Disable the auto-resize icon
        self.cpu_graph.setMenuEnabled(False)
        self.ram_graph.setMenuEnabled(False)
 

        self.cpu_graph.setMouseEnabled(x=False, y=False)
        self.ram_graph.setMouseEnabled(x=False, y=False)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_system_info)
        self.timer.start(1000)  # Update every second

    def update_system_info(self):
        cpu_usage = psutil.cpu_percent(interval=None)
        memory_info = psutil.virtual_memory()
        ram_usage = memory_info.percent

        self.system_info_cpu.setText(f"CPU Usage: {cpu_usage}%")
        self.system_info_ram.setText(f"Memory Usage: {ram_usage}%")

        self.cpu_data.append(cpu_usage)
        self.ram_data.append(ram_usage)
        if len(self.time_data) == 0:
            self.time_data.append(0)
        else:
            self.time_data.append(self.time_data[-1] + 1)

        if len(self.cpu_data) > self.max_points:
            self.cpu_data.pop(0)
            self.ram_data.pop(0)
            self.time_data.pop(0)

        self.cpu_curve.setData(self.time_data, self.cpu_data)
        self.ram_curve.setData(self.time_data, self.ram_data)

class TasksWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(['Name', 'PID', 'CPU', 'Memory', 'Status'])
        layout.addWidget(self.tableWidget)
        
        self.update_process_list()

    def update_process_list(self):
        self.tableWidget.setRowCount(0)
        processes = {}
        for process in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
            name = process.info['name']
            if process.info['pid'] < 1000:  # Assuming system processes have PID < 1000
                name = "SYSTEM"
            if name not in processes:
                processes[name] = {
                    'pid': process.info['pid'],
                    'cpu_percent': process.info['cpu_percent'],
                    'memory_percent': process.info['memory_percent'],
                    'status': process.info['status'],
                    'count': 1
                }
            else:
                processes[name]['cpu_percent'] += process.info['cpu_percent']
                processes[name]['memory_percent'] += process.info['memory_percent']
                processes[name]['count'] += 1

        for name, info in processes.items():
            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)
            self.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(f"{name} ({info['count']})"))
            self.tableWidget.setItem(rowPosition, 1, QTableWidgetItem(str(info['pid'])))
            self.tableWidget.setItem(rowPosition, 2, QTableWidgetItem(f"{info['cpu_percent']:.2f}%"))
            self.tableWidget.setItem(rowPosition, 3, QTableWidgetItem(f"{info['memory_percent']:.2f}%"))
            self.tableWidget.setItem(rowPosition, 4, QTableWidgetItem(info['status']))

class TaskMancer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('TaskMancer')
        self.setGeometry(100, 100, 800, 600)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.mainLayout = QVBoxLayout()
        self.centralWidget.setLayout(self.mainLayout)

        self.menuBar = QHBoxLayout()
        self.mainLayout.addLayout(self.menuBar)

        self.stack = QStackedWidget(self)
        self.mainLayout.addWidget(self.stack)

        self.homeWidget = HomeWidget()
        self.tasksWidget = TasksWidget()
        
        self.stack.addWidget(self.homeWidget)
        self.stack.addWidget(self.tasksWidget)

        self.createMenu()
        self.apply_theme()

    def createMenu(self):
        homeButton = QPushButton('Home')
        homeButton.clicked.connect(lambda: self.stack.setCurrentWidget(self.homeWidget))
        self.menuBar.addWidget(homeButton)
        
        tasksButton = QPushButton('Tasks')
        tasksButton.clicked.connect(lambda: self.stack.setCurrentWidget(self.tasksWidget))
        self.menuBar.addWidget(tasksButton)
        
        # Add more buttons and functionalities as needed
        self.menuBar.addStretch()

    def apply_theme(self):
        with open('themes/catppuccin.qss', 'r') as f:
            self.setStyleSheet(f.read())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = TaskMancer()
    window.show()
    sys.exit(app.exec_())

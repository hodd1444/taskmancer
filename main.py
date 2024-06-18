import sys
import psutil
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem

class TaskMancer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('TaskMancer')
        self.setGeometry(100, 100, 800, 600)
        
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(['PID', 'Name', 'CPU', 'Memory', 'Status'])
        self.setCentralWidget(self.tableWidget)
        
        self.update_process_list()
        
        self.apply_theme()

    def update_process_list(self):
        self.tableWidget.setRowCount(0)
        for process in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)
            self.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(str(process.info['pid'])))
            self.tableWidget.setItem(rowPosition, 1, QTableWidgetItem(process.info['name']))
            self.tableWidget.setItem(rowPosition, 2, QTableWidgetItem(str(process.info['cpu_percent'])))
            self.tableWidget.setItem(rowPosition, 3, QTableWidgetItem(str(process.info['memory_percent'])))
            self.tableWidget.setItem(rowPosition, 4, QTableWidgetItem(process.info['status']))

    def apply_theme(self):
        with open('themes/catppuccin.qss', 'r') as f:
            self.setStyleSheet(f.read())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TaskMancer()
    ex.show()
    sys.exit(app.exec_())


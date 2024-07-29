import json, datetime, sys

print("Expenses Program")


class Expenses:
    def __init__(self):
        self.expense_data = self.read_file()
        self.ask_method()
        self.save_to_file("expense.json")

    def add_expense(self, Title, Expense):
        for title, exp in self.expense_data.items():
            if title == Title:
                print(f"Error: Expense with the same title already exists: {title}")
                return
        self.date_added = datetime.datetime.now().strftime("%Y-%m-%d")
        dictts = {
            Title: {"Expense": Expense, "date_added": self.date_added},
        }
        self.expense_data.update(dictts)

    def delete_expense(self, title):
        if title in self.expense_data:
            del self.expense_data[title]
            print(f"Expense '{title}' deleted successfully.")
        else:
            print(f"Error: Expense with the title '{title}' does not exist.")

    def update_expense(self, title, new_expense, new_title):
        if title in self.expense_data:
            self.delete_expense(title)
            self.add_expense(new_title, new_expense)
        else:
            print(f"Error: Expense with the title '{title}' does not exist.")

    def get_expense(self, title):
        if title in self.expense_data:
            return self.expense_data[title]
        else:
            print(f"Error: Expense with the title '{title}' does not exist.")

    def save_to_file(self, filename):
        with open(filename, "w") as f:
            json.dump(self.expense_data, f, indent=4)

    def read_file(self, filename="expense.json") -> dict:
        with open(filename, "r") as f:
            data = json.load(f)
        return data
        # print(f"File '{filename}' loaded successfully.")

    def ask_method(self):
        import os

        # os.system("cls")
        print("Choose an option:")
        print("1. Add Expense")
        print("2. Delete Expense")
        print("3. Update Expense")
        print("4. Get Expense")
        print("5. Exit")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            os.system("cls")
            title = input("Enter expense title: ")
            expense = float(input("Enter expense amount: "))
            self.add_expense(title, expense)
            self.save_to_file("expense.json")
            self.ask_method()
        elif choice == 2:
            os.system("cls")
            title = input("Enter expense title to delete: ")
            self.delete_expense(title)
            self.save_to_file("expense.json")
            self.ask_method()

        elif choice == 3:
            os.system("cls")
            title = input("Enter expense title to update: ")
            new_expense = float(input("Enter new expense amount: "))
            new_title = input("Enter new expense title: ")
            self.update_expense(title, new_expense, new_title)
            self.save_to_file("expense.json")
            self.ask_method()

        elif choice == 4:
            os.system("cls")
            title = input("Enter expense title to get: ")
            expense = self.get_expense(title)
            print(f"Expense '{title}': {expense['Expense']}")
            self.ask_method()

        elif choice == 5:
            os.system("cls")
            print("Exiting the program...")
            sys.exit()


if __name__ == "__main__":
    expenses = Expenses()

exit()
import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView


class YouTubeBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Browser")
        self.setGeometry(100, 100, 1200, 800)

        self.browser = QWebEngineView()
        self.browser.setUrl(
            QUrl("C:/Users/Black/OneDrive/Desktop/Rent Recorder/htmlfile.html")
        )
        self.browser.loadFinished.connect(self.on_load_finished)

        self.setCentralWidget(self.browser)

    def on_load_finished(self, success):
        if not success:
            QMessageBox.critical(self, "Load Error", "Failed to load the webpage.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("YouTube Browser")

    window = YouTubeBrowser()
    window.show()

    sys.exit(app.exec_())

exit()
import json, os
import ast

# import module
# import sys, cv2, datetime, win32gui, win32con, random
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import qt_material, sys
from home import Ui_MainWindow


class Person:
    def __init__(
        self,
        Serial_Number,
        NIC,
        Rent,
        Rentel_Name,
        Due_Date,
        Received_Rent,
        Balance_Rent,
        Electric_Bill,
        Electricity_Meter_Number,
        Electricity_Account_Number,
        Consumer_Number,
        Electricity_Meter_Name,
        Gas_Costumer_Number,
        Gas_Meter_Number,
    ):
        # is_empty = os.path.getsize("persondata.json") == 0
        # print(is_empty)
        # if is_empty == False:
        #     with open("persondata.json", "r") as json_file:
        #         data_dict = json.load(json_file)
        # print(data_dict)

        dictionary = self.to_dictionary(
            Serial_Number,
            NIC,
            Rent,
            Rentel_Name,
            Due_Date,
            Received_Rent,
            Balance_Rent,
            Electric_Bill,
            Electricity_Meter_Number,
            Electricity_Account_Number,
            Consumer_Number,
            Electricity_Meter_Name,
            Gas_Costumer_Number,
            Gas_Meter_Number,
        )

        is_empty = os.path.getsize("persondata.json") == 0
        print(is_empty)
        with open("persondata.json", "r") as json_file:
            data_dict = json.load(json_file)
        strdata_dict = str(data_dict).replace("}}", "},")
        strdata_dict += str(dictionary)
        strdata_dict = strdata_dict.replace(",{", ",")
        data_dict = ast.literal_eval(strdata_dict)
        print(strdata_dict)
        self.to_json("persondata.json", data_dict)

        # data_dict.update(dictionary)
        # dictionary = dict(d, dictionary)

    # Create A function that converts the dictionary to a json file containing that dictionary
    def to_json(self, file_path, dictionary):

        with open(file_path, "w") as f:
            json.dump(dictionary, f, indent=4)

    # Create A function that takes values then converts it to a dictionary
    def to_dictionary(
        self,
        Serial_Number,
        NIC,
        Rent,
        Rentel_Name,
        Due_Date,
        Received_Rent,
        Balance_Rent,
        Electric_Bill,
        Electricity_Meter_Number,
        Electricity_Account_Number,
        Consumer_Number,
        Electricity_Meter_Name,
        Gas_Costumer_Number,
        Gas_Meter_Number,
    ):
        dictionary = {
            f"{Rentel_Name}": {
                "Serial_Number": Serial_Number,
                "NIC": NIC,
                "Rent": Rent,
                "Rentel_Name": Rentel_Name,
                "Due_Date": Due_Date,
                "Received_Rent": Received_Rent,
                "Balance_Rent": Balance_Rent,
                "Electric_Bill": Electric_Bill,
                "Electricity_Meter_Number": Electricity_Meter_Number,
                "Electricity_Account_Number": Electricity_Account_Number,
                "Consumer_Number": Consumer_Number,
                "Electricity_Meter_Name": Electricity_Meter_Name,
                "Gas_Costumer_Number": Gas_Costumer_Number,
                "Gas_Meter_Number": Gas_Meter_Number,
            }
        }
        return dictionary


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        width = QDesktopWidget().width()
        height = QDesktopWidget().height()
        self.homeui = Ui_MainWindow()
        # self.KK_Moosa_Plot_no_72ui.setupUi(self)
        # self.homeui.KK_Moosa_Plot_no_72.clicked.connect(
        #     self.change_ui
        # )
        self.setting = QSettings("Rent Recorder", "Theme")

        try:
            qt_material.apply_stylesheet(self, self.setting.value("themeName"))
        except:
            pass
        self.homeui.setupUi(self)
        self.homeui.Add_Person_btn.clicked.connect(self.Add_Person_func)
        self.homeui.dark_amber.changed.connect(self.Theme_Change)
        self.homeui.actiondark_blue.changed.connect(self.Theme_Change)
        self.homeui.actiondark_cyan.changed.connect(self.Theme_Change)
        self.homeui.actiondark_lightgreen.changed.connect(self.Theme_Change)
        self.homeui.actiondark_medical.changed.connect(self.Theme_Change)
        self.homeui.actiondark_pink.changed.connect(self.Theme_Change)
        self.homeui.actionlight_blue_500.changed.connect(self.Theme_Change)
        self.homeui.actionlight_cyan.changed.connect(self.Theme_Change)
        self.homeui.actionlight_cyan_500.changed.connect(self.Theme_Change)
        self.homeui.actionlight_lightgreen.changed.connect(self.Theme_Change)
        self.homeui.actionlight_lightgreen_500.changed.connect(self.Theme_Change)
        self.homeui.actionlight_orange.changed.connect(self.Theme_Change)
        self.homeui.actionlight_pink.changed.connect(self.Theme_Change)
        self.homeui.actionlight_pink_500.changed.connect(self.Theme_Change)
        self.homeui.actionlight_purple.changed.connect(self.Theme_Change)
        self.homeui.actionlight_purple_500.changed.connect(self.Theme_Change)
        self.homeui.actionlight_red.changed.connect(self.Theme_Change)
        self.homeui.actionlight_red_500.changed.connect(self.Theme_Change)
        self.homeui.actionlight_teal.changed.connect(self.Theme_Change)
        self.homeui.actionlight_teal_500.changed.connect(self.Theme_Change)
        self.homeui.actionlight_yellow.changed.connect(self.Theme_Change)
        self.homeui.actiondark_purple.changed.connect(self.Theme_Change)
        self.homeui.actiondark_red.changed.connect(self.Theme_Change)
        self.homeui.actiondark_teal.changed.connect(self.Theme_Change)
        self.homeui.actiondark_yellow.changed.connect(self.Theme_Change)
        self.homeui.actionlight_amber.changed.connect(self.Theme_Change)
        self.homeui.actionlight_blue.changed.connect(self.Theme_Change)
        self.homeui.actionlight_blue_500.changed.connect(self.Theme_Change)
        self.homeui.label_2.mousePressEvent = self.test
        # qt_material.apply_stylesheet(self, qt_material.list_themes()[-18])
        # savedself.themeName = self.setting.value("self.themeName")
        # print(savedself.themeName)
        print(qt_material.list_themes())
        self.themeName = ""

    def test(self, event):
        print("This is a test", event.pos())

    def Add_Person_func(self):
        print("Adding new person...")
        # TODO: Implement adding new person logic here
        Person(
            self.homeui.Serial_Number.text(),
            self.homeui.NIC.text(),
            self.homeui.Rent.text(),
            self.homeui.Rentel_Name.text(),
            self.homeui.Due_Date.text(),
            self.homeui.Received_Rent.text(),
            self.homeui.Balance_Rent.text(),
            self.homeui.Electric_Bill.text(),
            self.homeui.Electricity_Meter_Number.text(),
            self.homeui.Electricity_Account_Number.text(),
            self.homeui.Consumer_Number.text(),
            self.homeui.Electricity_Meter_Name.text(),
            self.homeui.Gas_Costumer_Number.text(),
            self.homeui.Gas_Meter_Number.text(),
        )

    def Theme_Change(self):
        if self.homeui.dark_amber.isChecked():
            qt_material.apply_stylesheet(self, self.homeui.dark_amber.text() + ".xml")
            self.homeui.dark_amber.setChecked(False)
            self.themeName = f"{self.homeui.dark_amber.text()}" + ".xml"

        elif self.homeui.actiondark_blue.isChecked():
            qt_material.apply_stylesheet(
                self, self.homeui.actiondark_blue.text() + ".xml"
            )
            self.homeui.actiondark_blue.setChecked(False)
            self.themeName = f"{self.homeui.actiondark_blue.text()}" + ".xml"

        elif self.homeui.actiondark_cyan.isChecked():
            qt_material.apply_stylesheet(
                self, self.homeui.actiondark_cyan.text() + ".xml"
            )
            self.homeui.actiondark_cyan.setChecked(False)
            self.themeName = f"{self.homeui.actiondark_cyan.text()}" + ".xml"

        elif self.homeui.actiondark_lightgreen.isChecked():
            qt_material.apply_stylesheet(
                self, self.homeui.actiondark_lightgreen.text() + ".xml"
            )
            self.homeui.actiondark_lightgreen.setChecked(False)
            self.themeName = self.homeui.actiondark_lightgreen.text() + ".xml"

        elif self.homeui.actiondark_medical.isChecked():
            qt_material.apply_stylesheet(
                self, self.homeui.actiondark_medical.text() + ".xml"
            )
            self.homeui.actiondark_medical.setChecked(False)
            self.themeName = self.homeui.actiondark_blue.text() + ".xml"

        elif self.homeui.actiondark_pink.isChecked():
            qt_material.apply_stylesheet(
                self, self.homeui.actiondark_pink.text() + ".xml"
            )
            self.homeui.actiondark_pink.setChecked(False)
            self.themeName = self.homeui.actiondark_pink.text() + ".xml"

        elif self.homeui.actionlight_blue_500.isChecked():
            qt_material.apply_stylesheet(
                self, self.homeui.actionlight_blue_500.text() + ".xml"
            )
            self.homeui.actionlight_blue_500.setChecked(False)
            self.themeName = self.homeui.actionlight_blue_500.text() + ".xml"

        elif self.homeui.actionlight_cyan.isChecked():
            qt_material.apply_stylesheet(
                self, self.homeui.actionlight_cyan.text() + ".xml"
            )
            self.homeui.actionlight_cyan.setChecked(False)
            self.themeName = self.homeui.actionlight_cyan.text() + ".xml"

        elif self.homeui.actionlight_cyan_500.isChecked():
            qt_material.apply_stylesheet(
                self, self.homeui.actionlight_cyan_500.text() + ".xml"
            )
            self.homeui.actionlight_cyan_500.setChecked(False)
            self.themeName = self.homeui.actionlight_cyan_500.text() + ".xml"

        elif self.homeui.actionlight_lightgreen.isChecked():
            qt_material.apply_stylesheet(
                self, self.homeui.actionlight_lightgreen.text() + ".xml"
            )
            self.homeui.actionlight_lightgreen.setChecked(False)
            self.themeName = self.homeui.actionlight_lightgreen.text() + ".xml"

        elif self.homeui.actionlight_lightgreen_500.isChecked():
            qt_material.apply_stylesheet(
                self, self.homeui.actionlight_lightgreen_500.text() + ".xml"
            )
            self.homeui.actionlight_lightgreen_500.setChecked(False)
            self.themeName = self.homeui.actionlight_lightgreen_500.text() + ".xml"

        elif self.homeui.actionlight_orange.isChecked():
            qt_material.apply_stylesheet(
                self, self.homeui.actionlight_orange.text() + ".xml"
            )
            self.homeui.actionlight_orange.setChecked(False)
            self.themeName = self.homeui.actionlight_orange.text() + ".xml"

        elif self.homeui.actionlight_pink.isChecked():
            qt_material.apply_stylesheet(
                self, self.homeui.actionlight_pink.text() + ".xml"
            )
            self.homeui.actionlight_pink.setChecked(False)
            self.themeName = self.homeui.actionlight_pink.text() + ".xml"

        elif self.homeui.actionlight_pink_500.isChecked():
            qt_material.apply_stylesheet(
                self, self.homeui.actionlight_pink_500.text() + ".xml"
            )
            self.homeui.actionlight_pink_500.setChecked(False)
            self.themeName = self.homeui.actionlight_pink_500.text() + ".xml"

        elif self.homeui.actionlight_purple.isChecked():
            qt_material.apply_stylesheet(
                self, self.homeui.actionlight_purple.text() + ".xml"
            )
            self.homeui.actionlight_purple.setChecked(False)
            self.themeName = self.homeui.actionlight_purple.text() + ".xml"

        elif self.homeui.actionlight_purple_500.isChecked():

            qt_material.apply_stylesheet(
                self, self.homeui.actionlight_purple_500.text() + ".xml"
            )
            self.homeui.actionlight_purple_500.setChecked(False)
            self.themeName = self.homeui.actionlight_purple_500.text() + ".xml"

        elif self.homeui.actionlight_red.isChecked():
            qt_material.apply_stylesheet(
                self, self.homeui.actionlight_red.text() + ".xml"
            )
            self.homeui.actionlight_red.setChecked(False)
            self.themeName = self.homeui.actionlight_red.text() + ".xml"

        elif self.homeui.actionlight_red_500.isChecked():
            qt_material.apply_stylesheet(
                self, self.homeui.actionlight_red_500.text() + ".xml"
            )
            self.homeui.actionlight_red_500.setChecked(False)
            self.themeName = self.homeui.actionlight_red_500.text() + ".xml"

        elif self.homeui.actionlight_teal.isChecked():
            qt_material.apply_stylesheet(
                self, self.homeui.actionlight_teal.text() + ".xml"
            )

            self.homeui.actionlight_teal.setChecked(False)
            self.themeName = self.homeui.actionlight_teal.text() + ".xml"

        elif self.homeui.actionlight_teal_500.isChecked():
            qt_material.apply_stylesheet(
                self, self.homeui.actionlight_teal_500.text() + ".xml"
            )
            self.homeui.actionlight_teal_500.setChecked(False)
            self.themeName = self.homeui.actionlight_teal_500.text() + ".xml"

        elif self.homeui.actionlight_yellow.isChecked():
            qt_material.apply_stylesheet(
                self, self.homeui.actionlight_yellow.text() + ".xml"
            )
            self.homeui.actionlight_yellow.setChecked(False)
            self.themeName = self.homeui.actionlight_yellow.text() + ".xml"

        elif self.homeui.actiondark_purple.isChecked():
            qt_material.apply_stylesheet(
                self, self.homeui.actiondark_purple.text() + ".xml"
            )
            self.homeui.actiondark_purple.setChecked(False)
            self.themeName = self.homeui.actiondark_purple.text() + ".xml"

        elif self.homeui.actiondark_red.isChecked():
            qt_material.apply_stylesheet(
                self, self.homeui.actiondark_red.text() + ".xml"
            )
            self.homeui.actiondark_red.setChecked(False)
            self.themeName = self.homeui.actiondark_red.text() + ".xml"

        elif self.homeui.actiondark_teal.isChecked():
            qt_material.apply_stylesheet(
                self, self.homeui.actiondark_teal.text() + ".xml"
            )
            self.homeui.actiondark_teal.setChecked(False)
            self.themeName = self.homeui.actiondark_teal.text() + ".xml"

        elif self.homeui.actiondark_yellow.isChecked():
            qt_material.apply_stylesheet(
                self, self.homeui.actiondark_yellow.text() + ".xml"
            )
            self.homeui.actiondark_yellow.setChecked(False)
            self.themeName = self.homeui.actiondark_yellow.text() + ".xml"

        elif self.homeui.actionlight_amber.isChecked():
            qt_material.apply_stylesheet(
                self, self.homeui.actionlight_amber.text() + ".xml"
            )
            self.homeui.actionlight_amber.setChecked(False)
            self.themeName = self.homeui.actionlight_amber.text() + ".xml"

        elif self.homeui.actionlight_blue.isChecked():
            qt_material.apply_stylesheet(
                self, self.homeui.actionlight_blue.text() + ".xml"
            )
            self.homeui.actionlight_blue.setChecked(False)
            self.themeName = self.homeui.actionlight_blue.text() + ".xml"

        elif self.homeui.actionlight_blue_500.isChecked():
            qt_material.apply_stylesheet(
                self, self.homeui.actionlight_blue_500.text() + ".xml"
            )
            self.homeui.actionlight_blue_500.setChecked(False)
            self.themeName = self.homeui.actionlight_blue_500.text() + ".xml"

    def closeEvent(self, event):
        self.setting.setValue("themeName", self.themeName)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    app.exec_()

# import openpyxl
# from openpyxl.utils import get_column_letter
# from datetime import datetime


# def extract_data():
#     # Create a new.xlsx file
#     wb = openpyxl.Workbook()
#     ws = wb.active

#     # Write data to cells
#     ws["A1"] = "Hello Qt!"
#     ws["A2"] = 12345
#     ws["A3"] = "=44+33"
#     ws["A4"] = True
#     ws["A5"] = "http://qt-project.org"
#     ws["A6"] = datetime(2013, 12, 27)
#     ws["A7"] = datetime(2013, 12, 27, 6, 30)
#     ws["K17"] = "hooo"

#     # Save the file
#     wb.save("XLSX\\extractdata.xlsx")

#     # Load the file
#     wb = openpyxl.load_workbook("XLSX\\extractdata.xlsx")
#     ws = wb.active

#     # Read data from cells
#     print("extractdata.xlsx - Reading cells")
#     print(list(ws.values))
#     print(ws["A1"].value)
#     print(ws["A2"].value)
#     print(ws["A3"].value)
#     print(ws["A4"].value)
#     print(ws["A5"].value)
#     print(ws["A6"].value)
#     print(ws["A7"].value)
#     print(ws["K17"].value)

#     # Read data from cells using iteration
#     print("extractdata.xlsx - Iterating over cells")
#     for row in range(1, 10):
#         cell = ws[get_column_letter(1) + str(row)]
#         if cell.value is not None:
#             print(cell.value)


# if __name__ == "__main__":
#     extract_data()

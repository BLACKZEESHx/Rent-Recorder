import os, sqlite3, datetime
import pandas as pd
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import qt_material, sys
from home import Ui_MainWindow
from openpyxl import load_workbook
from openpyxl.styles import PatternFill, Font
from KK_Moosa_Plot_no_72 import Ui_Form
from plyer import notification

class Expenses:
    def __init__(self):
        self.conn = sqlite3.connect("expense.db")
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS expenses
                         (title TEXT PRIMARY KEY, expense REAL, date_added TEXT)""")
        self.conn.commit()

    def add_expense(self, Title, Expense):
        self.cursor.execute("INSERT INTO expenses VALUES (?,?,?)", (Title, Expense, datetime.datetime.now().strftime("%Y-%m-%d")))
        self.conn.commit()

    def delete_expense(self, title):
        self.cursor.execute("DELETE FROM expenses WHERE title =?", (title,))
        self.conn.commit()

    def update_expense(self, title, new_expense, new_title):
        self.delete_expense(title)
        self.add_expense(new_title, new_expense)

    def get_expense(self, title):
        self.cursor.execute("SELECT * FROM expenses WHERE title =?", (title,))
        return self.cursor.fetchone()
    
    def get_all_expenses(self):
        self.cursor.execute("SELECT * FROM expenses")
        return self.cursor.fetchall()

class Personed:
    def __init__(self):
        self.current_month, self.previous_month = self.get_current_and_previous_month()
        self.setup_directories()
        self.setup_database()

    def get_current_and_previous_month(self):
        today = datetime.date.today()
        current_month = today.strftime("%B_%Y")
        first_day_of_current_month = today.replace(day=1)
        last_day_of_previous_month = first_day_of_current_month - datetime.timedelta(days=1)
        previous_month = last_day_of_previous_month.strftime("%B_%Y")
        return current_month, previous_month

    def setup_directories(self):
        os.makedirs(f"data/{self.current_month}", exist_ok=True)
        previous_month_dir = f"data/{self.previous_month}"
        if not os.path.exists(previous_month_dir):
            os.makedirs(previous_month_dir)

    def setup_database(self):
        self.conn = sqlite3.connect(f"data/{self.current_month}/persondata.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS persondata (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Serial_Number TEXT,
                NIC TEXT,
                Rent REAL,
                Rentel_Name TEXT,
                Due_Date TEXT,
                Received_Rent REAL,
                Balance_Rent REAL,
                Electric_Bill REAL,
                Electricity_Meter_Number TEXT,
                Electricity_Account_Number TEXT,
                Consumer_Number TEXT,
                Electricity_Meter_Name TEXT,
                Gas_Costumer_Number TEXT,
                Gas_Meter_Number TEXT,
                Advance_Amount REAL,
                Building TEXT,
                Gas_Bill REAL,
                Date_Added TEXT,
                is_paid TEXT
            )
        """)
        self.conn.commit()

    def insert_data(self, data):
        self.cursor.execute("""
            INSERT INTO persondata (
                Serial_Number, NIC, Rent, Rentel_Name, Due_Date, Received_Rent,
                Balance_Rent, Electric_Bill, Electricity_Meter_Number,
                Electricity_Account_Number, Consumer_Number, Electricity_Meter_Name,
                Gas_Costumer_Number, Gas_Meter_Number, Advance_Amount, Building,
                Gas_Bill, Date_Added, is_paid
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, data)
        self.conn.commit()

    def update_person(self, rentel_name, **kwargs):
        set_clause = ", ".join(f"{key} = ?" for key in kwargs.keys())
        values = list(kwargs.values()) + [rentel_name]
        self.cursor.execute(f"UPDATE persondata SET {set_clause} WHERE Rentel_Name = ?", values)
        self.conn.commit()

    def get_all_persons(self):
        self.cursor.execute("SELECT * FROM persondata")
        return self.cursor.fetchall()

    def get_person_by_name(self, rentel_name):
        self.cursor.execute("SELECT * FROM persondata WHERE Rentel_Name = ?", (rentel_name,))
        return self.cursor.fetchone()

    def get_persons_by_building(self, building):
        self.cursor.execute("SELECT * FROM persondata WHERE Building = ?", (building,))
        return self.cursor.fetchall()

    def __del__(self):
        self.conn.close()

class XLSX(QMainWindow):
    def __init__(self):
        super().__init__()
        self.homeui = Ui_MainWindow()
        self.Expense_Sys = Expenses()
        self.Person_Sys = Personed()
        self.homeui.setupUi(self)
        self.homeui.Tab_window.currentChanged.connect(self.taber)
        self.SetupUI()
        self.homeui.action.triggered.connect(self.add_building)
        self.homeui.action_2.triggered.connect(self.remove_building)
        self.homeui.add_exp_btn.clicked.connect(self.add_exp_method)
        self.read_buildings_file()
        self.homeui.Electric_Bill.clicked.connect(self.electric_bill_method)
        self.homeui.Gas_Bill.clicked.connect(self.gas_bill_method)
        self.homeui.buildingcombobox.currentTextChanged.connect(self.Add_Building_dialog)
        self.homeui.menuPrint.triggered.connect(lambda: os.system("print " + f"RentData.xlsx"))
        
        self.setting = QSettings("Rent Recorder", "Theme")
        try:
            qt_material.apply_stylesheet(self, self.setting.value("themeName"))
        except:
            qt_material.apply_stylesheet(self, "light_teal_500.xml")
        self.setStyleSheet(self.styleSheet() + '*{font: 22pt "Cascadia Code";}')

        self.homeui.Add_Person_btn.clicked.connect(self.Add_Person_func)
        self.homeui.menuConvert_To_Excel.mousePressEvent = self.convert_to_excel

        # Theme change connections...

        self.homeui.searchedit.returnPressed.connect(self.search)

        self.themeName = ""
        self.searchtimer = QTimer(self.homeui.searchedit)
        self.searchtimer.timeout.connect(self.setupui_search)
        self.searchtimer.start(1000)
        self.setStyleSheet(self.styleSheet() + '*{font: 11pt "Cascadia Code";}')

    def add_exp_method(self):
        title = self.homeui.title_lineedit.text()
        amount = self.homeui.exp_amount_lineedit.text()
        self.Expense_Sys.add_expense(title, int(amount))
        self.taber(2)

    def add_building(self):
        dialog = QDialog(self)
        add_building_line_edit = QLineEdit(dialog)
        add_building_line_edit.returnPressed.connect(lambda _="", name=add_building_line_edit: self.Add_Building(name))
        add_building_line_edit.setPlaceholderText("Enter Building Name")
        add_building_line_edit.move(10, 10)
        dialog.setWindowTitle("Add Building")
        add_building_line_edit.show()
        dialog.exec_()

    def read_buildings_file(self):
        index = self.homeui.buildingcombobox.currentIndex()
        self.homeui.buildingcombobox.clear()
        buildings = []
        with open("buildings.txt", "r") as file_building:
            buildings = file_building.readlines()
        for building in buildings:
            self.homeui.buildingcombobox.addItem(building.strip())
        self.homeui.buildingcombobox.setCurrentIndex(index)
        index = self.homeui.buildingcombo_2.currentIndex()

        self.homeui.buildingcombo_2.clear()
        
        buildings = []
        with open("buildings.txt", "r") as file_building:
            buildings = file_building.readlines()
        for building in buildings:
                self.homeui.buildingcombo_2.addItem(building.strip())
    
    def Add_Building_dialog(self, n):
        if n == "Show All Building":
            pass
        else:
            for i in reversed(range(self.homeui.scrollAreaWidgetContents.layout().count())):
                widget_to_remove = self.homeui.scrollAreaWidgetContents.layout().itemAt(i).widget()
                if type(widget_to_remove).__name__ == "QLabel":
                    continue
                if widget_to_remove is not None:
                    widget_to_remove.setParent(None)
            for person in self.Person_Sys.get_persons_by_building(n):
                self.person_layout = QWidget()
                self.person_widget = QGridLayout(self.person_layout)
                self.person_info = QLabel(f"Rental Name: {person[4]}\nSerial No.:{person[1]}\nBuilding:{person[16]} ")
                self.Received_Rent = QLabel(f"Received Rent:{person[6]}\nRent:{person[3]}\nBalance:{person[7]}")
                self.Electric_Bill = QPushButton(f"{person[8]}")
                self.Gas_Bill = QPushButton(f"{person[17]}")
                self.Gas_Bill.clicked.connect(lambda _, p=person: self.show_person_data(p))
                self.Electric_Bill.clicked.connect(lambda _, p=person: self.show_person_data(p))
                self.person_widget.addWidget(self.person_info, 0, 0, 9,1)
                self.person_widget.addWidget(self.Received_Rent, 0, 1, 9,1)
                self.person_widget.addWidget(self.Electric_Bill, 0, 2, 2,1)
                self.person_widget.addWidget(self.Gas_Bill, 2, 2, 2,1)
                self.homeui.scrollAreaWidgetContents.layout().addWidget(self.person_layout)
                if person[8] == "Electric Bill is not paid":
                    self.Gas_Bill.setStyleSheet(self.Gas_Bill.styleSheet() + "background-color: red;")
                elif person[8] == "Electric Bill is paid":
                    self.Electric_Bill.setStyleSheet(self.Electric_Bill.styleSheet() + "background-color: green;")

                if person[17] =="Gas Bill is not paid":
                    self.Gas_Bill.setStyleSheet(self.Gas_Bill.styleSheet() + "background-color: red;")
                elif person[17] == "Gas Bill is paid":
                    self.Electric_Bill.setStyleSheet(self.Electric_Bill.styleSheet() + "background-color: green;")

    def Add_Building(self, name: QLineEdit):
        with open("buildings.txt", "a") as file_building:
            file_building.write(name.text() + "\n")
        print(name.text())
        
    def taber(self, n):
        if n == 2:
            self.delete_widget(self.homeui.scrollAreaWidgetContents_expense)
            data = self.Expense_Sys.get_all_expenses()
            for expense in data:
                self.expense_title = QPushButton(f"{expense[0]}: RS.{expense[1]} Date Added:{expense[2]}")
                self.homeui.scrollAreaWidgetContents_expense.layout().addWidget(self.expense_title)
    def delete_widget(self, widget):
        for i in reversed(range(widget.layout().count())):
            widget_to_remove = widget.layout().itemAt(i).widget()
            if widget_to_remove is not None:
                widget_to_remove.setParent(None)
                
    def setupui_search(self):
        if self.homeui.buildingcombobox.currentText() == "Show All Building":
            if self.homeui.searchedit.text() == "":
                for i in reversed(range(self.homeui.scrollAreaWidgetContents.layout().count())):
                    widget_to_remove = self.homeui.scrollAreaWidgetContents.layout().itemAt(i).widget()
                    if widget_to_remove is not None:
                        widget_to_remove.setParent(None)

                self.SetupUI()
        elif self.homeui.buildingcombobox.currentText() != "Show All Building" :
            self.read_buildings_file()

    def search(self):
        search_text = self.homeui.searchedit.text()
        
        persons = self.Person_Sys.get_all_persons()

        if search_text:
            for person in persons:
                if search_text.lower() in person[4].lower() or search_text.lower() in person[1] or search_text.lower() in person[2] or search_text.lower() in person[5]:
                    for i in reversed(range(self.homeui.scrollAreaWidgetContents.layout().count())):
                        widget_to_remove = self.homeui.scrollAreaWidgetContents.layout().itemAt(i).widget()
                        if widget_to_remove is not None:
                            widget_to_remove.setParent(None)
                    layout = self.homeui.scrollAreaWidgetContents.layout()

                    for i, value in enumerate(person):
                        label = QLabel(f"<h2>{self.Person_Sys.cursor.description[i][0]}:</h2><h3>{value}</h3>")
                        label.mousePressEvent = lambda _, p=person: self.show_person_data(p)
                        label.setStyleSheet(label.styleSheet()+ "*{background-color: #F2F3F3;}")
                        layout.addWidget(label)                        

                    self.SetupUI()
                    break
            else:
                QMessageBox.information(self, "Search Result", "No rental found with the given data")
        try:
            qt_material.apply_stylesheet(self, self.setting.value("themeName"))
        except:
            qt_material.apply_stylesheet(self, "light_teal_500.xml")
        self.setStyleSheet(self.styleSheet() + '*{font: 11pt "Cascadia Code";}')

    def convert_to_excel(self, e):
        try:
            persons = self.Person_Sys.get_all_persons()
            df = pd.DataFrame(persons, columns=[desc[0] for desc in self.Person_Sys.cursor.description])
            excel_path = "RentData.xlsx"
            df.to_excel(excel_path, index=False)

            wb = load_workbook(excel_path)
            ws = wb.active

            header_fill = PatternFill(start_color="FFC0CB", end_color="FFC0CB", fill_type="solid")
            header_font = Font(size=16, bold=True)

            for cell in ws[1]:
                cell.fill = header_fill
                cell.font = header_font
                ws.column_dimensions[cell.column_letter].width = 20

            wb.save(excel_path)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export data: {str(e)}")
        try:
            qt_material.apply_stylesheet(self, self.setting.value("themeName"))
        except:
            qt_material.apply_stylesheet(self, "light_teal_500.xml")
        self.setStyleSheet(self.styleSheet() + '*{font: 11pt "Cascadia Code";}')

    def Add_Person_func(self):
        data = (
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
            self.homeui.Advance_Amount.text(),
            self.homeui.buildingcombo_2.currentText(),
            self.homeui.Gas_Bill.text(),
            datetime.date.today().strftime("%Y-%m-%d"),
            "no"
        )
        self.Person_Sys.insert_data(data)
        for i in reversed(range(self.homeui.scrollAreaWidgetContents.layout().count())):
            widget_to_remove = self.homeui.scrollAreaWidgetContents.layout().itemAt(i).widget()
            if widget_to_remove is not None:
                widget_to_remove.setParent(None)
        self.SetupUI()
        try:
            qt_material.apply_stylesheet(self, self.setting.value("themeName"))
        except:
            qt_material.apply_stylesheet(self, "light_teal_500.xml")
        self.setStyleSheet(self.styleSheet() + '*{font: 11pt "Cascadia Code";}')

    def SetupUI(self):
        if self.homeui.buildingcombobox.currentText() == "Show All Building":
            persons = self.Person_Sys.get_all_persons()

            for person in persons:
                self.person_layout = QWidget()
                self.person_layout.setObjectName("person_layout")
                self.person_widget = QGridLayout(self.person_layout)
                self.person_info = QLabel(f"Rental Name: {person[4]}\nSerial No.:{person[1]}\nBuilding:{person[16]} ")
                self.Received_Rent = QLabel(f"Received Rent:{person[6]}\nRent:{person[3]}\nBalance:{person[7]}")
                self.Electric_Bill = QPushButton(f"{person[8]}")
                self.Gas_Bill = QPushButton(f"{person[17]}")
                self.Electric_Bill.setObjectName("ebill")
                self.person_layout.setStyleSheet("QWidget#person_layout{border-radius: 50px; padding: 1.5em; border: 3px dotted white;};")
                self.Electric_Bill.setStyleSheet("QPushButton#ebill{margin-top: 50px;}")

                self.Gas_Bill.clicked.connect(lambda _, p=person: self.show_person_data(p))
                self.Electric_Bill.clicked.connect(lambda _, p=person: self.show_person_data(p))

                self.person_widget.addWidget(self.person_info, 0, 0, 9,1)
                self.person_widget.addWidget(self.Received_Rent, 0, 1, 9,1)
                self.person_widget.addWidget(self.Electric_Bill, 0, 2, 3,1)
                self.person_widget.addWidget(self.Gas_Bill, 3, 2, 3,1)
                self.homeui.scrollAreaWidgetContents.layout().addWidget(self.person_layout)

                if person[19] == "yes" and int(person[6]) < int(person[3]):
                    if int(person[6]) != 0:
                        sumed = int(person[3]) - int(person[6])
                        self.Person_Sys.update_person(person[4], Balance_Rent=sumed)

                if int(person[6]) < int(person[3]) and person[19] == "no":
                    if int(person[6]) != 0:
                        sumed = int(person[7]) - int(person[6])
                        self.Person_Sys.update_person(person[4], Balance_Rent=sumed, Received_Rent=0)
            
                if int(person[6]) > int(person[3]):
                    if int(person[7]) != 0:
                        sumed = int(person[6]) - int(person[3])
                        sumed2 = int(person[7]) - sumed
                        self.Person_Sys.update_person(person[4], Balance_Rent=sumed2, Received_Rent=0)
                            
                if person[5] == str(datetime.datetime.now().day):
                    if not int(person[6]) >= int(person[3]):
                        self.payment_info_widget = QWidget()
                        self.payment_info_widget.setStyleSheet("QWidget{border-radius: 50px; padding: 0.5em; background-color: rgba(255, 0, 0, 128);}; color: white;")
                        self.payment_info_layout = QVBoxLayout(self.payment_info_widget)
                        self.payment_info_label = QLabel(f"Payment Reminder: It's {person[5]}th and {person[4]} didn't pay the rent.")
                        self.payment_info_layout.addWidget(self.payment_info_label)
                        self.homeui.scrollAreaWidgetContents.layout().addWidget(self.payment_info_widget)
        
    def show_person_data(self, person):
        form = Ui_Form()
        widget = QDialog(self)
        form.setupUi(widget)
        
        for i, value in enumerate(person):
            person_widget = QLabel(f" <h2>{self.Person_Sys.cursor.description[i][0]}:</h2><h3>{value}</h3>")
            form.scrollAreaWidgetContents.layout().addWidget(person_widget)
        
        form.Serial_Number_3.setText(str(person[1]))
        form.NIC_3.setText(str(person[2]))
        form.Rent_3.setText(str(person[3]))
        form.Rentel_Name_3.setText(str(person[4]))
        form.Due_Date_3.setText(str(person[5]))
        form.Received_Rent_3.setText(str(person[6]))
        form.Balance_Rent_3.setText(str(person[7]))
        form.Electric_Bill_3.setText(str(person[8]))
        form.Electricity_Meter_Number_3.setText(str(person[9]))
        form.Electricity_Account_Number_3.setText(str(person[10]))
        form.Consumer_Number_3.setText(str(person[11]))
        form.Electricity_Meter_Name_3.setText(str(person[12]))
        form.Gas_Costumer_Number_3.setText(str(person[13]))
        form.Gas_Meter_Number_3.setText(str(person[14]))
        form.Advance_Amount_3.setText(str(person[15]))   
        form.Gas_Bill_3.setText(str(person[17]))
        form.Building_3.setText(str(person[16]))            
        widget.setWindowTitle(str(person[4]))
        form.Gas_Bill_3.clicked.connect(lambda _, f=form: self.gas_bill_3_method(f))
        form.Electric_Bill_3.clicked.connect(lambda _, f=form: self.electric_bill_3_method(f))
        form.Add_Person_btn_3.clicked.connect(lambda _, f=form: self.update_person_in_database(f))
        
        widget.exec_()
        try:
            qt_material.apply_stylesheet(widget, self.setting.value("themeName"))
        except:
            qt_material.apply_stylesheet(widget, "light_teal.xml")

        try:
            qt_material.apply_stylesheet(self, self.setting.value("themeName"))
        except:
            qt_material.apply_stylesheet(self, "light_teal_500.xml")
        self.setStyleSheet(self.styleSheet() + '*{font: 11pt "Cascadia Code";}')

    def update_person_in_database(self, form):
        person_data = {
            "Serial_Number": form.Serial_Number_3.text(),
            "NIC": form.NIC_3.text(),
            "Rent": form.Rent_3.text(),
            "Rentel_Name": form.Rentel_Name_3.text(),
            "Due_Date": form.Due_Date_3.text(),
            "Received_Rent": form.Received_Rent_3.text(),
            "Balance_Rent": form.Balance_Rent_3.text(),
            "Electric_Bill": form.Electric_Bill_3.text(),
            "Gas_Bill": form.Gas_Bill_3.text(),
            "Electricity_Meter_Number": form.Electricity_Meter_Number_3.text(),
            "Electricity_Account_Number": form.Electricity_Account_Number_3.text(),
            "Consumer_Number": form.Consumer_Number_3.text(),
            "Electricity_Meter_Name": form.Electricity_Meter_Name_3.text(),
            "Gas_Costumer_Number": form.Gas_Costumer_Number_3.text(),
            "Gas_Meter_Number": form.Gas_Meter_Number_3.text(),
            "Advance_Amount": form.Advance_Amount_3.text(),
            "Building": form.Building_3.text(),
        }

        self.Person_Sys.update_person(person_data["Rentel_Name"], **person_data)
        print("Person data updated successfully!")

    def closeEvent(self, event):
        self.setting.setValue("themeName", self.themeName)
        self.convert_to_excel(event)

    def remove_building(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Remove Building")
        line_edit = QLineEdit(dialog)
        line_edit.setPlaceholderText("Building Name To Remove...")
        line_edit.returnPressed.connect(lambda _="", n=line_edit.text():self.remove_building_name(n))
        dialog.exec_()

    def remove_building_name(self, name):
        if not name:
            pass
        with open('buildings.txt', 'r') as file:
            lines = file.readlines()

        word_to_remove = name
        print(name + "sd")

        new_lines = []
        for line in lines:
            new_line = ' '.join([word for word in line.split() if word != word_to_remove])
            new_lines.append(new_line + "\n")

        with open('buildings.txt', 'w') as file:
            file.writelines(new_lines)

    def electric_bill_method(self):
        if self.homeui.Electric_Bill.isChecked():
            print("Yes", self.homeui.Electric_Bill.isChecked())
            self.homeui.Electric_Bill.setText("Electric Bill is paid")
            self.homeui.Electric_Bill.setStyleSheet(self.homeui.Electric_Bill.styleSheet() + "background-color: green;")
        else: 
            print("No", self.homeui.Electric_Bill.isChecked())
            self.homeui.Electric_Bill.setText("Electric Bill is not paid")
            self.homeui.Electric_Bill.setStyleSheet(self.homeui.Electric_Bill.styleSheet() + "background-color: red;")

    def gas_bill_method(self):
        if self.homeui.Gas_Bill.isChecked():
            print("Yes", self.homeui.Gas_Bill.isChecked())
            self.homeui.Gas_Bill.setText("Gas Bill is paid")
            self.homeui.Gas_Bill.setStyleSheet(self.homeui.Gas_Bill.styleSheet() + "background-color: green;")
        else: 
            print("No", self.homeui.Gas_Bill.isChecked())
            self.homeui.Gas_Bill.setText("Gas Bill is not paid")
            self.homeui.Gas_Bill.setStyleSheet(self.homeui.Gas_Bill.styleSheet() + "background-color: red;")

    def electric_bill_3_method(self, form):
        if form.Electric_Bill_3.isChecked():
            print("Yes", form.Electric_Bill_3.isChecked())
            form.Electric_Bill_3.setText("Electric Bill is paid")
            form.Electric_Bill_3.setStyleSheet(form.Electric_Bill_3.styleSheet() + "background-color: green;")
        else: 
            print("No", form.Electric_Bill_3.isChecked())
            form.Electric_Bill_3.setText("Electric Bill is not paid")
            form.Electric_Bill_3.setStyleSheet(form.Electric_Bill_3.styleSheet() + "background-color: red;")

    def gas_bill_3_method(self, form):
        if form.Gas_Bill_3.isChecked():
            print("Yes", form.Gas_Bill_3.isChecked())
            form.Gas_Bill_3.setText("Gas Bill is paid")
            form.Gas_Bill_3.setStyleSheet(form.Gas_Bill_3.styleSheet() + "background-color: green;")
        else: 
            print("No", form.Gas_Bill_3.isChecked())
            form.Gas_Bill_3.setText("Gas Bill is not paid")
            form.Gas_Bill_3.setStyleSheet(form.Gas_Bill_3.styleSheet() + "background-color: red;")

def main():
    app = QApplication(sys.argv)
    window = XLSX()
    window.showMaximized()
    app.exec_()

main()

# Summary is a class that use other methods to calculate the total rent, balance and recieving amounts of given json file.
import json


class Summary:
    def __init__(self, filename):
        self.filename = filename
        self.json: dict = self.read_json()
        # print(self.read_json())
        self.total_rent = self.calculate_total_rent()

    def read_json(self) -> dict:
        with open(self.filename, "r") as file:
            data = json.load(file)
        return data

    def calculate_total_rent(self) -> int:
        total_rent = 0
        total_balance = 0
        total_recieving_amounts = 0
        for person, person_data in self.json.items():
            for key, value in person_data.items():
                if key == "Rent":
                    print(
                        {
                            person: {
                                "Rent": person_data["Rent"],
                                "Balance_Rent": person_data["Balance_Rent"],
                                "Received_Rent": person_data["Received_Rent"],
                            }
                        }
                    )
                    total_rent += int(value)
                    # print(int(value))
                elif key == "Balance_Rent":
                    total_balance += int(value)

                elif key == "Received_Rent":
                    total_recieving_amounts += int(value)
                    # total_rent -= int(value)

        total_rent -= int(total_recieving_amounts)
        return {
            "Total_Rent": total_rent,
            "Balance Rent": total_balance,
            "Received_Rent": total_recieving_amounts,
        }

if __name__ == "__main__":
    summary = Summary(r"C:\Users\Black\OneDrive\Desktop\Rent Recorder\data\July_2024\persondata.json")
    print(f"Total rent: {summary.total_rent}")
    # Add more methods to calculate balance and recieving amounts here.
    # For example, balance = total_rent - total_recieving_amounts, etc.
    # print(f"Balance: {summary.calculate_balance()}")
    # print(f"Total recieving amounts: {summary.calculate_total_recieving_amounts()}")
    # etc.

exit()
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
)
import sys
import openpyxl

path = "Rent sheet  JUNE(AutoRecovered).xlsx"
workbook = openpyxl.load_workbook(path)
sheet = workbook.active


def replace_at_index(tup, index, value):
    return tup[:index] + (value,) + tup[index + 1 :]


class Main(QWidget):
    def __init__(self):
        super(Main, self).__init__()
        self.setWindowTitle("Load Excel data to QTableWidget")

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.table_widget = QTableWidget()
        layout.addWidget(self.table_widget)
        add_person = QPushButton("Add Person")
        layout.addWidget(add_person)

        add_person.clicked.connect(self.add_person)

        self.load_data(sheet)

    def add_person(self):
        # global sheet, workbook, path
        sheet.append(["person", "name"])
        workbook.save("person.xlsx")
        path2 = "person.xlsx"
        workbook2 = openpyxl.load_workbook(path2)
        sheet2 = workbook2.active
        self.load_data(sheet2)

    def load_data(self, sheet):

        self.table_widget.setRowCount(sheet.max_row)
        self.table_widget.setColumnCount(sheet.max_column)

        list_values = list(sheet.values)
        self.table_widget.setHorizontalHeaderLabels(list_values[0])

        row_index = 0
        for value_tuple in list_values[1:]:
            col_index = 0
            for value in value_tuple:
                self.table_widget.setItem(
                    row_index, col_index, QTableWidgetItem(str(value))
                )
                col_index += 1
            row_index += 1


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main()
    window.showMaximized()
    app.exec_()

# data={
# houseno,
# rent,
# rentalname,
# due,
# recivdata,
# balancerent,
# elecbill,
# gassbil,
# Nic,
# advancebill,
# gasmeterno,
# gascostumerno,
# electmetername,
# electmeterno,
# electacountno,
# consumerno,
# }

# allmonthshistry

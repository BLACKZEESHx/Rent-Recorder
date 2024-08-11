import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.Qt3DCore import *
from PyQt5.Qt3DExtras import Qt3DWindow, QOrbitCameraController, QPhongMaterial
from PyQt5.Qt3DRender import QMesh
from PyQt5.QtGui import QColor, QVector3D


class MainWindow(Qt3DWindow):
    def __init__(self):
        super().__init__()
        self.defaultFrameGraph().setClearColor(QColor(255, 255, 255))
        self.rootEntity = QEntity()

        # Camera
        self.camera = self.camera()
        self.camera.lens().setPerspectiveProjection(45.0, 16.0 / 9.0, 0.1, 1000.0)
        self.camera.setPosition(QVector3D(0, 0, 20))
        self.camera.setViewCenter(QVector3D(0, 0, 0))

        # For camera controls
        self.camController = QOrbitCameraController(self.rootEntity)
        # self.camController.setLinearSpeed(50)
        self.camController.setLookSpeed(180)
        self.camController.setCamera(self.camera)

        # Load 3D model
        self.modelEntity = QEntity(self.rootEntity)
        self.mesh = QMesh()
        self.mesh.setSource(
            QUrl.fromLocalFile("scene.gltf")
        )  # Replace 'model.obj' with your model file path
        self.material = QPhongMaterial()
        self.material.setDiffuse(QColor(255, 255, 255))  # White color

        self.transform = QTransform()
        self.modelEntity.addComponent(self.mesh)
        self.modelEntity.addComponent(self.material)
        self.modelEntity.addComponent(self.transform)

        # Set root entity
        self.setRootEntity(self.rootEntity)


app = QApplication(sys.argv)
view = MainWindow()
container = QWidget.createWindowContainer(view)
screenSize = view.screen().size()
container.setMinimumSize(200, 100)
container.setMaximumSize(screenSize)

# Show window
container.show()
sys.exit(app.exec_())


exit()
import sys

import sqlite3
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QFormLayout,
)


class TenantDatabase:
    def __init__(self, db_name="property_management.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute(
                """CREATE TABLE IF NOT EXISTS Tenants (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    serial_number TEXT,
                                    nic TEXT,
                                    rent REAL,
                                    rental_name TEXT,
                                    due_date TEXT,
                                    received_rent REAL,
                                    balance_rent REAL,
                                    electric_bill REAL,
                                    gas_bill REAL,
                                    electricity_meter_number TEXT,
                                    electricity_account_number TEXT,
                                    consumer_number TEXT,
                                    electricity_meter_name TEXT,
                                    gas_customer_number TEXT,
                                    gas_meter_number TEXT,
                                    advance_amount REAL,
                                    building TEXT)"""
            )

            self.conn.execute(
                """CREATE TABLE IF NOT EXISTS RentHistory (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    tenant_id INTEGER,
                                    date TEXT,
                                    rent REAL,
                                    received_rent REAL,
                                    balance_rent REAL,
                                    FOREIGN KEY (tenant_id) REFERENCES Tenants(id))"""
            )

    def add_tenant(self, tenant_data):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(
                """INSERT INTO Tenants (serial_number, nic, rent, rental_name, due_date, received_rent, balance_rent, electric_bill, gas_bill, electricity_meter_number, electricity_account_number, consumer_number, electricity_meter_name, gas_customer_number, gas_meter_number, advance_amount, building)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                tenant_data,
            )
            return cursor.lastrowid

    def add_rent_history(self, tenant_id, history_data):
        with self.conn:
            self.conn.execute(
                """INSERT INTO RentHistory (tenant_id, date, rent, received_rent, balance_rent)
                                 VALUES (?, ?, ?, ?, ?)""",
                (tenant_id, *history_data),
            )

    def get_tenants(self):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM Tenants")
            return cursor.fetchall()


class PropertyManagementApp(QMainWindow):
    def __init__(self, tenant_db):
        super().__init__()
        self.tenant_db = tenant_db
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Property Management System")
        self.setGeometry(100, 100, 600, 400)

        widget = QWidget()
        layout = QVBoxLayout()

        form_layout = QFormLayout()
        self.serial_number_input = QLineEdit()
        self.rental_name_input = QLineEdit()
        self.nic_input = QLineEdit()
        self.rent_input = QLineEdit()
        self.due_date_input = QLineEdit()
        self.received_rent_input = QLineEdit()
        self.balance_rent_input = QLineEdit()
        self.electric_bill_input = QLineEdit()
        self.gas_bill_input = QLineEdit()
        self.electricity_meter_number_input = QLineEdit()
        self.electricity_account_number_input = QLineEdit()
        self.consumer_number_input = QLineEdit()
        self.electricity_meter_name_input = QLineEdit()
        self.gas_customer_number_input = QLineEdit()
        self.gas_meter_number_input = QLineEdit()
        self.advance_amount_input = QLineEdit()
        self.building_input = QLineEdit()

        form_layout.addRow("Serial Number:", self.serial_number_input)
        form_layout.addRow("Rental Name:", self.rental_name_input)
        form_layout.addRow("NIC:", self.nic_input)
        form_layout.addRow("Rent:", self.rent_input)
        form_layout.addRow("Due Date:", self.due_date_input)
        form_layout.addRow("Received Rent:", self.received_rent_input)
        form_layout.addRow("Balance Rent:", self.balance_rent_input)
        form_layout.addRow("Electric Bill:", self.electric_bill_input)
        form_layout.addRow("Gas Bill:", self.gas_bill_input)
        form_layout.addRow(
            "Electricity Meter Number:", self.electricity_meter_number_input
        )
        form_layout.addRow(
            "Electricity Account Number:", self.electricity_account_number_input
        )
        form_layout.addRow("Consumer Number:", self.consumer_number_input)
        form_layout.addRow("Electricity Meter Name:", self.electricity_meter_name_input)
        form_layout.addRow("Gas Customer Number:", self.gas_customer_number_input)
        form_layout.addRow("Gas Meter Number:", self.gas_meter_number_input)
        form_layout.addRow("Advance Amount:", self.advance_amount_input)
        form_layout.addRow("Building:", self.building_input)

        layout.addLayout(form_layout)

        self.submit_btn = QPushButton("Add Tenant")
        self.submit_btn.clicked.connect(self.add_tenant)
        layout.addWidget(self.submit_btn)

        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def add_tenant(self):
        tenant_data = (
            self.serial_number_input.text(),
            self.nic_input.text(),
            float(self.rent_input.text()),
            self.rental_name_input.text(),
            self.due_date_input.text(),
            float(self.received_rent_input.text()),
            float(self.balance_rent_input.text()),
            float(self.electric_bill_input.text()),
            float(self.gas_bill_input.text()),
            self.electricity_meter_number_input.text(),
            self.electricity_account_number_input.text(),
            self.consumer_number_input.text(),
            self.electricity_meter_name_input.text(),
            self.gas_customer_number_input.text(),
            self.gas_meter_number_input.text(),
            float(self.advance_amount_input.text()),
            self.building_input.text(),
        )

        tenant_id = self.tenant_db.add_tenant(tenant_data)
        history_data = (
            self.due_date_input.text(),
            float(self.rent_input.text()),
            float(self.received_rent_input.text()),
            float(self.balance_rent_input.text()),
        )
        self.tenant_db.add_rent_history(tenant_id, history_data)

        print(f"Tenant {tenant_data[3]} added with ID {tenant_id}")


if __name__ == "__main__":
    tenant_db = TenantDatabase()
    app = QApplication(sys.argv)
    mainWin = PropertyManagementApp(tenant_db)
    mainWin.show()
    sys.exit(app.exec_())

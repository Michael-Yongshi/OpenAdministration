import sys
import logging

from tkinter import dialog
from venv import create
from numpy import double

from PyQt6.QtCore import (
    QSettings,
    QDate,
    Qt,
    )

from PyQt6.QtWidgets import (
    QApplication,
    QCalendarWidget,
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QGridLayout,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QSpinBox,
    QComboBox,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    )

from PyQt6.QtGui import (
    QAction,
    QIcon,
    QDoubleValidator,
    )

from darktheme.widget_template_pyqt6 import (
    DarkPalette,
    QBorderlessFrame,
    QBorderedWidget,
    QClickLabel,
)

from sqlitemanager import handler
from sqlitemanager.objects import Database

from src.helpers import calc_invoice_total, calc_invoice_vat, get_database_info, get_date_range, get_columns, get_records, check_tables, create_records

class QMainApplication(QApplication):
    """A Dark styled application."""
    def __init__(self, *__args):
        super().__init__(*__args)
        
        self.setStyle("Fusion")
        self.setPalette(DarkPalette())   

class MainWindow (QMainWindow):
    """The main window that everything runs in"""
    def __init__(self):
        super().__init__()

        # Some window settings
        self.setWindowTitle('Administration')

        # create empty settings of the main window
        self.settings = QSettings("Michael-Yongshi", "Administration")

        # connect to database
        self.db = None

        # set menu bar
        bar = self.menuBar()

        file_menu = bar.addMenu('File')

        create_action = QAction('Create', self)
        create_action.setToolTip('Create a new administration')
        create_action.triggered.connect(self.create_administration)
        file_menu.addAction(create_action)

        open_action = QAction('Open', self)
        open_action.setToolTip('Choose an existing <b>administration</b>')
        # open_action.triggered.connect(self.choose_administration)
        # file_menu.addAction(open_action)

        save_action = QAction('Save', self)
        save_action.setShortcut("Ctrl+S")
        save_action.setToolTip('Save current <b>administration</b>')
        # save_action.triggered.connect(self.save_administration)
        # file_menu.addAction(save_action)

        close_action = QAction('Close', self)
        close_action.setToolTip('Close <b>administration</b>')
        # close_action.triggered.connect(self.close_administration)
        # file_menu.addAction(close_action)

        quit_action = QAction('Quit', self)
        quit_action.setToolTip('Quit')
        quit_action.triggered.connect(QApplication.instance().quit)
        # file_menu.addAction(quit_action)

        self.initUI()

    def initUI(self):
       
        # save window settings (size and position)
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())

        # update nested widget
        if self.db == None:
            self.nested_widget = QBorderedWidget()
        else:
            self.nested_widget = self.set_nested_widget()
        self.setCentralWidget(self.nested_widget)

        # Restore window settings (size and position)
        self.restoreGeometry(self.settings.value("geometry", bytes("", "utf-8")))
        self.restoreState(self.settings.value("windowState", bytes("", "utf-8")))
        self.show()

    def set_nested_widget(self):

        # top navigation
        tabs = QTabWidget()

        tabs.addTab(WidgetOverview(self), "Overview")
        tabs.addTab(WidgetPurchases(self), "Purchases")
        tabs.addTab(WidgetSales(self), "Sales")
        tabs.addTab(WidgetTransactions(self), "Transactions")

        tabs.addTab(WidgetSystem(self), "System")

        return tabs

    def create_administration(self):

        # TODO , create a database at path of your choice
        self.db = Database(filename="administration")
        check_tables(db=self.db)

        # restart ui to force changes
        self.initUI()

class WidgetOverview(QBorderedWidget):
    def __init__(self, mainwindow):
        super().__init__()

        self.mainwindow = mainwindow

        sysbox = QVBoxLayout()
        topbox = QHBoxLayout()

        self.year_select = QLineEdit()
        self.year_select.setText('2022')
        topbox.addWidget(self.year_select)

        self.quarter_select = QComboBox()
        self.quarter_select.addItems(['All','Q1', 'Q2', 'Q3', 'Q4'])
        topbox.addWidget(self.quarter_select)

        topwidget = QBorderedWidget()
        topwidget.setLayout(topbox)

        sysbox.addWidget(topwidget)

        tabs = QTabWidget()

        tabs.addTab(self.set_profit_widget(), "Profit & Loss")
        tabs.addTab(self.set_balance_widget(), "Balance")
        tabs.addTab(self.set_liquidity_widget(), "Liquidity")

        sysbox.addWidget(tabs)

        self.setLayout(sysbox)

    def set_profit_widget(self):

        profitwidget = QBorderedWidget()
        layout = QVBoxLayout()

        # get total costs per category per year per quarter
        # conditional read with where statement
        tablename = 'purchases'

        daterange = get_date_range(self.year_select, self.quarter_select)
        daterangewidget = QLabel(str(daterange))
        layout.addWidget(daterangewidget)

        query = f"SELECT category, Sum(Amount) FROM {tablename} WHERE date BETWEEN {daterange[0]} AND {daterange[1]} GROUP BY category"
        result = self.mainwindow.db.execute_query(query)

        logging.info(f"query result = {result}")

        profitwidget.setLayout(layout)
        return profitwidget

    def set_balance_widget(self):

        balancewidget = QBorderedWidget()

        return balancewidget

    def set_liquidity_widget(self):

        liquidwidget = QBorderedWidget()

        return liquidwidget

class WidgetPurchases(QBorderedWidget):
    def __init__(self, mainwindow):
        super().__init__()
        
        self.mainwindow = mainwindow
        self.tablename = 'purchases'

        sysbox = QVBoxLayout()

        tabs = QTabWidget()

        tabs.addTab(self.set_view_widget(), "View invoices")
        tabs.addTab(self.set_add_widget(), "Add invoice")
        tabs.addTab(self.set_import_widget(), "Import")

        sysbox.addWidget(tabs)

        self.setLayout(sysbox)

    def set_view_widget(self):

        widget = QBorderedWidget()

        sysbox = QVBoxLayout()

        table = QTableWidget(self)

        records = handler.get_records(db=self.mainwindow.db, table_name=self.tablename)
        logging.info(f"records: {records}")

        # only fetch columns seperately from the database if returned records is an empty list
        if records == []:
            columns = handler.get_table_column_names(db=self.mainwindow.db, table_selection=self.tablename)
        # else get columns just from the first record returned
        else:
            columns = records[0].columns

        table.setHorizontalHeaderLabels(columns)
        table.setColumnCount(len(columns))
        table.setRowCount(10)

        # Iterate over rows and columns to fill the Table widget
        row = 0
        for record in records:
            col = 0
            for value in record.values:
                cell = QTableWidgetItem(str(value))
                table.setItem(row, col, cell)
                col += 1
            row += 1

        sysbox.addWidget(table)

        widget.setLayout(sysbox)

        return widget

    def set_add_widget(self):

        dialogwidget = QPurchaseDialog(mainwindow=self.mainwindow)

        return dialogwidget

    def set_import_widget(self):

        widget = QBorderedWidget()

        return widget

    def add_purchase_invoice(self):
        """Add new purchase invoice"""

class QPurchaseDialog(QDialog):
    def __init__(self, mainwindow):
        super().__init__()

        self.mainwindow = mainwindow

        # create form
        self.formGroupBox = QGroupBox("Form layout")

        formlayout = QFormLayout()

        self.catform = QComboBox()
        category_records = handler.get_records(db=self.mainwindow.db, table_name="purchase_categories")
        logging.info(category_records)

        categories = []
        for category_record in category_records:
            categories += [category_record.dict["name"]]
        logging.info(categories)

        self.catform.addItems(categories)
        formlayout.addRow(QLabel("Category:"), self.catform)

        self.suppform = QLineEdit()
        formlayout.addRow(QLabel("Supplier:"), self.suppform)

        self.idform = QLineEdit()
        formlayout.addRow(QLabel("Invoice Id:"), self.idform)

        self.dateform = QCalendarWidget()
        formlayout.addRow(QLabel("Invoice date:"), self.dateform)

        self.amountform = QLineEdit()
        self.amountform.setValidator(QDoubleValidator())
        self.amountform.textChanged.connect(self.on_change)
        formlayout.addRow(QLabel("Amount:"), self.amountform)

        # TODO, make vat form dynamic with extra VAT type table
        self.vatform = QComboBox()
        self.vatform.addItems(["21", "6", "0"])
        self.vatform.setEditable(True)
        self.vatform.currentTextChanged.connect(self.on_change)
        formlayout.addRow(QLabel("VAT %:"), self.vatform)

        self.vatamountform = QLabel()
        formlayout.addRow(QLabel("VAT Amount:"), self.vatamountform)

        self.totalform = QLabel()
        formlayout.addRow(QLabel("Total Amount:"), self.totalform)

        self.paidform = QCheckBox()
        formlayout.addRow(QLabel("Paid:"), self.paidform)

        self.formGroupBox.setLayout(formlayout)

        # add buttons
        self.buttonbox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttonbox.accepted.connect(self.accept)
        self.buttonbox.rejected.connect(self.reject)

        # set to layout of main widget
        mainlayout = QVBoxLayout()
        mainlayout.addWidget(self.formGroupBox)
        mainlayout.addWidget(self.buttonbox)
        self.setLayout(mainlayout)
    
    def on_change(self):
        if self.vatform.currentText() == "" or self.amountform.text() == "":
            self.vatamountform.setText("")
            self.totalform.setText("")
        else:
            self.vatamountform.setText(str(calc_invoice_vat(
                float(self.vatform.currentText()), float(self.amountform.text())
                )))
            self.totalform.setText(str(calc_invoice_total(
                float(self.vatform.currentText()), float(self.amountform.text())
                )))

    def accept(self):
        
        record = {
            "id": self.idform.text(), 
            "category": self.catform.currentText(), 
            "supplier": self.suppform.text(), 
            "date": self.dateform.selectedDate().toString('yyyyMMdd'), 
            "amount": self.amountform.text(), 
            "vat_type": self.vatform.currentText(),
            "vat": self.vatamountform.text(), 
            "isPaid": self.paidform.checkState(),
        }
        logging.info(f"Created new invoice: {record}")

        handler.create_records(db=self.mainwindow.db, table_name="purchases", records=[record])

        self.idform.setText("")
        self.amountform.setText("")

        self.mainwindow.initUI()

    def reject(self):

        self.dateform.setSelectedDate(QDate.currentDate())
        self.suppform.setText("")
        self.idform.setText("")
        self.amountform.setText("")

class WidgetSales(QBorderedWidget):
    def __init__(self, mainwindow):
        super().__init__()

class WidgetTransactions(QBorderedWidget):
    def __init__(self, mainwindow):
        super().__init__()

class WidgetSystem(QBorderedWidget):
    def __init__(self, mainwindow):
        super().__init__()
        
        self.mainwindow = mainwindow
        
        sysbox = QGridLayout()
        
        label = QClickLabel()
        label.setText(get_database_info(db=self.mainwindow.db))
        sysbox.addWidget(label, 0, 0)

        self.setToolTip("database")
        self.setLayout(sysbox)

def run():
    global app
    app = QMainApplication(sys.argv)
    global main
    main = MainWindow()
    sys.exit(app.exec())

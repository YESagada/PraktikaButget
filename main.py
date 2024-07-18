import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, \
    QPushButton, QHBoxLayout, QInputDialog, QFileDialog, QLabel, QTabWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class BudgetApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Budget Manager')
        self.setGeometry(100, 100, 800, 600)

        # Stylesheet for the entire application
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QTableWidget {
                border: 1px solid #d4d4d4;
                font-size: 14px;
                background-color: #ffffff;
            }
            QHeaderView::section {
                background-color: #e0e0e0;
                padding: 4px;
                font-size: 14px;
                border: 1px solid #d4d4d4;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px;
                font-size: 14px;
                border: none;
                border-radius: 4px;
                margin: 2px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLabel {
                font-size: 16px;
                font-weight: bold;
                margin: 4px;
            }
            QMenuBar {
                background-color: #f0f0f0;
                font-size: 14px;
            }
            QMenu {
                background-color: #f0f0f0;
            }
            QAction {
                font-size: 14px;
            }
            QTabWidget::pane {
                border: 1px solid #d4d4d4;
            }
            QTabBar::tab {
                background: #e0e0e0;
                border: 1px solid #d4d4d4;
                padding: 10px;
                font-size: 14px;
            }
            QTabBar::tab:selected {
                background: #ffffff;
                margin-bottom: -1px;
            }
        """)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        viewMenu = menubar.addMenu('View')

        importAction = QAction('Import', self)
        importAction.triggered.connect(self.importData)
        exportAction = QAction('Export', self)
        exportAction.triggered.connect(self.exportData)
        exitAction = QAction('Exit', self)

        fileMenu.addAction(importAction)
        fileMenu.addAction(exportAction)
        fileMenu.addAction(exitAction)

        self.tabs = QTabWidget()
        self.expensesTab = QWidget()
        self.incomeTab = QWidget()

        self.tabs.addTab(self.expensesTab, "Expenses")
        self.tabs.addTab(self.incomeTab, "Income")

        self.expensesTable = QTableWidget()
        self.expensesTable.setColumnCount(4)
        self.expensesTable.setHorizontalHeaderLabels(["Date", "Category", "Description", "Amount"])
        self.expensesTable.horizontalHeader().setStretchLastSection(True)

        self.incomeTable = QTableWidget()
        self.incomeTable.setColumnCount(4)
        self.incomeTable.setHorizontalHeaderLabels(["Date", "Category", "Description", "Amount"])
        self.incomeTable.horizontalHeader().setStretchLastSection(True)

        addExpenseButton = QPushButton('Add Expense')
        addExpenseButton.clicked.connect(self.addExpenseEntry)

        deleteExpenseButton = QPushButton('Delete Expense')
        deleteExpenseButton.clicked.connect(self.deleteExpenseEntry)

        addIncomeButton = QPushButton('Add Income')
        addIncomeButton.clicked.connect(self.addIncomeEntry)

        deleteIncomeButton = QPushButton('Delete Income')
        deleteIncomeButton.clicked.connect(self.deleteIncomeEntry)

        expenseButtonLayout = QHBoxLayout()
        expenseButtonLayout.addWidget(addExpenseButton)
        expenseButtonLayout.addWidget(deleteExpenseButton)

        incomeButtonLayout = QHBoxLayout()
        incomeButtonLayout.addWidget(addIncomeButton)
        incomeButtonLayout.addWidget(deleteIncomeButton)

        expenseLayout = QVBoxLayout()
        expenseLayout.addWidget(self.expensesTable)
        expenseLayout.addLayout(expenseButtonLayout)

        incomeLayout = QVBoxLayout()
        incomeLayout.addWidget(self.incomeTable)
        incomeLayout.addLayout(incomeButtonLayout)

        self.expensesTab.setLayout(expenseLayout)
        self.incomeTab.setLayout(incomeLayout)

        totalExpensesLabel = QLabel('Total Expenses: $0.00')
        totalIncomeLabel = QLabel('Total Income: $0.00')

        centralWidget = QWidget()
        layout = QVBoxLayout(centralWidget)
        layout.addWidget(self.tabs)
        layout.addWidget(totalExpensesLabel)
        layout.addWidget(totalIncomeLabel)

        self.setCentralWidget(centralWidget)

        exitAction.triggered.connect(self.close)

        self.totalExpensesLabel = totalExpensesLabel
        self.totalIncomeLabel = totalIncomeLabel

        self.show()

    def addExpenseEntry(self):
        rowPosition = self.expensesTable.rowCount()
        self.expensesTable.insertRow(rowPosition)

        date, ok = QInputDialog.getText(self, 'Date Input', 'Enter date:')
        if ok:
            self.expensesTable.setItem(rowPosition, 0, QTableWidgetItem(date))

        category, ok = QInputDialog.getText(self, 'Category Input', 'Enter category:')
        if ok:
            self.expensesTable.setItem(rowPosition, 1, QTableWidgetItem(category))

        description, ok = QInputDialog.getText(self, 'Description Input', 'Enter description:')
        if ok:
            self.expensesTable.setItem(rowPosition, 2, QTableWidgetItem(description))

        amount, ok = QInputDialog.getText(self, 'Amount Input', 'Enter amount:')
        if ok:
            self.expensesTable.setItem(rowPosition, 3, QTableWidgetItem(amount))

        self.updateTotals()

    def deleteExpenseEntry(self):
        row = self.expensesTable.currentRow()
        self.expensesTable.removeRow(row)

        self.updateTotals()

    def addIncomeEntry(self):
        rowPosition = self.incomeTable.rowCount()
        self.incomeTable.insertRow(rowPosition)

        date, ok = QInputDialog.getText(self, 'Date Input', 'Enter date:')
        if ok:
            self.incomeTable.setItem(rowPosition, 0, QTableWidgetItem(date))

        category, ok = QInputDialog.getText(self, 'Category Input', 'Enter category:')
        if ok:
            self.incomeTable.setItem(rowPosition, 1, QTableWidgetItem(category))

        description, ok = QInputDialog.getText(self, 'Description Input', 'Enter description:')
        if ok:
            self.incomeTable.setItem(rowPosition, 2, QTableWidgetItem(description))

        amount, ok = QInputDialog.getText(self, 'Amount Input', 'Enter amount:')
        if ok:
            self.incomeTable.setItem(rowPosition, 3, QTableWidgetItem(amount))

        self.updateTotals()

    def deleteIncomeEntry(self):
        row = self.incomeTable.currentRow()
        self.incomeTable.removeRow(row)

        self.updateTotals()

    def importData(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Import CSV", "", "CSV Files (*.csv)", options=options)
        if fileName:
            data = pd.read_csv(fileName)
            if not data.empty:
                self.expensesTable.setRowCount(0)
                self.incomeTable.setRowCount(0)
                for i, row in data.iterrows():
                    if row["Amount"] < 0:
                        self.expensesTable.insertRow(self.expensesTable.rowCount())
                        self.expensesTable.setItem(self.expensesTable.rowCount() - 1, 0, QTableWidgetItem(row["Date"]))
                        self.expensesTable.setItem(self.expensesTable.rowCount() - 1, 1, QTableWidgetItem(row["Category"]))
                        self.expensesTable.setItem(self.expensesTable.rowCount() - 1, 2, QTableWidgetItem(row["Description"]))
                        self.expensesTable.setItem(self.expensesTable.rowCount() - 1, 3, QTableWidgetItem(str(row["Amount"])))
                    else:
                        self.incomeTable.insertRow(self.incomeTable.rowCount())
                        self.incomeTable.setItem(self.incomeTable.rowCount() - 1, 0, QTableWidgetItem(row["Date"]))
                        self.incomeTable.setItem(self.incomeTable.rowCount() - 1, 1, QTableWidgetItem(row["Category"]))
                        self.incomeTable.setItem(self.incomeTable.rowCount() - 1, 2, QTableWidgetItem(row["Description"]))
                        self.incomeTable.setItem(self.incomeTable.rowCount() - 1, 3, QTableWidgetItem(str(row["Amount"])))

                self.updateTotals()

    def exportData(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "Export CSV", "", "CSV Files (*.csv)", options=options)
        if fileName:
            expenseData = []
            incomeData = []

            for row in range(self.expensesTable.rowCount()):
                rowData = []
                for col in range(self.expensesTable.columnCount()):
                    item = self.expensesTable.item(row, col)
                    if item:
                        rowData.append(item.text())
                    else:
                        rowData.append('')
                expenseData.append(rowData)

            for row in range(self.incomeTable.rowCount()):
                rowData = []
                for col in range(self.incomeTable.columnCount()):
                    item = self.incomeTable.item(row, col)
                    if item:
                        rowData.append(item.text())
                    else:
                        rowData.append('')
                incomeData.append(rowData)

            expenses_df = pd.DataFrame(expenseData, columns=["Date", "Category", "Description", "Amount"])
            income_df = pd.DataFrame(incomeData, columns=["Date", "Category", "Description", "Amount"])

            combined_df = pd.concat([expenses_df, income_df])
            combined_df.to_csv(fileName, index=False)

    def updateTotals(self):
        totalExpenses = 0.0
        totalIncome = 0.0

        for row in range(self.expensesTable.rowCount()):
            amountItem = self.expensesTable.item(row, 3)
            if amountItem:
                try:
                    amount = float(amountItem.text())
                    totalExpenses += amount
                except ValueError:
                    pass

        for row in range(self.incomeTable.rowCount()):
            amountItem = self.incomeTable.item(row, 3)
            if amountItem:
                try:
                    amount = float(amountItem.text())
                    totalIncome += amount
                except ValueError:
                    pass

        self.totalExpensesLabel.setText(f'Total Expenses: ${totalExpenses:.2f}')
        self.totalIncomeLabel.setText(f'Total Income: ${totalIncome:.2f}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BudgetApp()
    sys.exit(app.exec_())


"""
Created on Thu Jul  6 19:19:52 2023

@author: Bhavesh Soni
"""




from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog, QHeaderView, QTableWidgetItem, QApplication, QMainWindow, QTreeView, QPushButton, QTextEdit, QWidget
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QFont
from PyQt5.QtCore import Qt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

from ramp import User, Appliance, UseCase, get_day_type
import pandas as pd
from openpyxl import load_workbook
from openpyxl.worksheet.cell_range import CellRange

import matplotlib
import matplotlib.pyplot as plt

import os
from contextlib import redirect_stdout, redirect_stderr
from io import StringIO
import sys
import shutil

from PyQt5 import QtCore, QtGui, QtWidgets



# Will Show Errors and Messege in MessegeBox
class QTextEditLogger(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)  # Set read-only mode

        # Set size and read-only mode
        self.setFixedSize(1850, 200)  # Adjust the size according to your needs
        self.setReadOnly(True)

        font = QFont()
        font.setPointSize(10)
        self.setFont(font)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

    def write(self, message):
        self.append(message)
        



# Main Window Class
class Ui_MainWindow(QtWidgets.QMainWindow):
       
    
    
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        uic.loadUi('RAMP.ui', self)

        # Initialize the QTextEditLogger
        self.log_textedit = QTextEditLogger(self.console_1)
        sys.stdout = self.log_textedit
        sys.stderr = self.log_textedit
        
        # Initialize the rest of your setup here
        self.setupUi(self)



    def setupUi(self, MainWindow):


        self.use_case = None
        self.selected_users = []


        # Keep All applaince widget hidden initially
        for i in range(1, 31):
            getattr(self, f'widget_{i}').hide()

        
        
        # Set default 'Whole Week' for combo box for each Applainces (RAMP Lite)
        for i in range(1, 31):
            getattr(self, f'wd_we_comboBox_{i}').setCurrentIndex(2)
        
        

        
        # Set widgets disabled at initial stage (RAMP LIte)
        self.start_dateEdit_1.setEnabled(False)
        self.ndays_spinBox_1.setEnabled(False)
        self.set_title_lineEdit_1.setEnabled(False)
        self.simulate_pushButton_1.setEnabled(False)     
        self.scrollArea.setEnabled(False)
        self.console_1.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.console_1.setMinimumSize(200, 200) 
     
        # PushButtons connected to functions (RAMP Lite)
        #
        self.save_image_pushButton.clicked.connect(self.save_figure_lite)
        self.generate_pushButton_1.clicked.connect(self.generate_plots_lite)
        self.save_csv_pushButton.clicked.connect(self.save_as_csv_lite)
        self.simulate_pushButton_1.clicked.connect(self.ramplite_simulation) 
       
        # Create a Group of Timestamp Radio buttons
        radio_button_group = QtWidgets.QButtonGroup()
        radio_button_group.addButton(self.Minute_radioButton_1)
        radio_button_group.addButton(self.FifteenMinute_radioButton_1)
        radio_button_group.addButton(self.Hourly_radioButton_1)
        radio_button_group.addButton(self.Daily_radioButton_1)
        radio_button_group.addButton(self.Monthly_radioButton_1)
        radio_button_group.addButton(self.barchart_radioButton_1)
        

        # Enable radio buttons on simulate button press
        def enable_timestamp_Group_radio_buttons(enable=True):
            for button in radio_button_group.buttons():
                button.setEnabled(enable)

        # Disable the radio buttons initially
        enable_timestamp_Group_radio_buttons(False)
        # Connect simulate button press to enabling the radio buttons
        self.simulate_pushButton_1.clicked.connect(lambda: enable_timestamp_Group_radio_buttons(True))
        


        # Assuming you have appliancename_lineEdit_1 to appliancename_lineEdit_30
        self.appliancename_lineEdits = [getattr(self, f'appliancename_lineEdit_{i}') for i in range(1, 31)]
        # Connect signal to slot
        for lineEdit in self.appliancename_lineEdits:
            lineEdit.textChanged.connect(self.handle_appliancename_change)

        
        # Function to handle changes in user name
        def handle_username_change():
            if self.user_name_lineEdit_1.text():
                self.scrollArea.setEnabled(True)
            else:
                self.scrollArea.setEnabled(False)

        # Connect signal to slot
        self.user_name_lineEdit_1.textChanged.connect(handle_username_change)

        


        # Containers
        self.widgets = []
        self.toggle_buttons = []
        # Populate the lists with widgets and toggle buttons (RAMP Lite)
        for i in range(1, 31):
            widget = getattr(self, f'widget_{i}')
            toggle_button = getattr(self, f'Togglebutton_{i}')
            self.widgets.append(widget)
            self.toggle_buttons.append(toggle_button)

            widget.setEnabled(False)
            widget.hide()

            
            
            

        # Function to handle changes in appliance names
        def handle_appliance_name_change(widget_index):
            def inner():
                if getattr(self, f'appliancename_lineEdit_{widget_index}').text():
                    self.widgets[widget_index-1].setEnabled(True)
                else:
                    self.widgets[widget_index-1].setEnabled(False)
            return inner

        # Connect signals to slots
        for i in range(1, 31):
            appliancename_lineEdit = getattr(self, f'appliancename_lineEdit_{i}')
            appliancename_lineEdit.textChanged.connect(handle_appliance_name_change(i))



            
        # Enable buttons when simulate button pressed ( RAMP Lite) 
        def enable_buttons():
            self.save_image_pushButton.setEnabled(True)
            self.save_csv_pushButton.setEnabled(True)
            self.generate_pushButton_1.setEnabled(True)

        # Connect simulate button press to enabling the buttons
        self.simulate_pushButton_1.clicked.connect(enable_buttons)
        
        # Create a layout for Ramp_lite_graphicsview_1
        self.rampLiteLayout = QtWidgets.QVBoxLayout(self.Ramp_lite_graphicsview_1)
        
        # Create a figure for plotting with dimensions matching the layout
        self.figure1, ax = plt.subplots(figsize=(5, 1), nrows=1, ncols=1)

        
        # Create a canvas to display the figure
        self.canvas1 = FigureCanvas(self.figure1)
        
        # Set up layout for plots
        self.plotLayout_1 = QtWidgets.QHBoxLayout()
        
        # Add the canvas to the layout
        self.plotLayout_1.addWidget(self.canvas1)
        
        # Add the plotLayout_1 to the rampLiteLayout
        self.rampLiteLayout.addLayout(self.plotLayout_1)
        
        
 
        
        self.create_user_tableWidget_1.setColumnCount(2)
        self.create_user_tableWidget_1.setHorizontalHeaderLabels(['User', 'Appliance'])
        self.create_user_tableWidget_1.setRowCount(1)  # Start with 3 rows

        # Set the "Appliance" column to adjust its size automatically
        header = self.create_user_tableWidget_1.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setStyleSheet("QHeaderView::section { border: 1px solid black; background-color: lightgray }")
    

 

 

        
        
        
        # RAMP Advance GUI Objects/elements Condition functionality
        #
        #
        #
        self.select_user_comboBox_1.setEnabled(False)
        self.selected_user_lineEdit_1.setEnabled(False)
        self.add_to_list_pushButton_1.setEnabled(False)
        self.simulate_pushButton_2.clicked.connect(self.ramp_advance_simulation)
        self.generate_pushButton_2.clicked.connect(self.generate_plots_ramp_advance)
        self.save_image_pushButton_1.clicked.connect(self.save_image_1)
        self.save_image_pushButton_2.clicked.connect(self.save_image_2)
        self.save_csv_pushButton_1.clicked.connect(self.save_as_csv_advance_individual_user)
        self.save_csv_pushButton_2.clicked.connect(self.save_as_csv_advance_sum_of_users)
        self.add_to_list_pushButton_1.clicked.connect(self.addUserFromComboBox)
        self.add_user_pushButton_1.clicked.connect(self.create_user)
        self.remove_user_pushButton_1.clicked.connect(self.remove_user)   
        self.save_set_pushButton_1.clicked.connect(self.save_set_parameters)
        self.parameter_save_pushButton_1.clicked.connect(self.save_created_file)
        
        # Connect the itemChanged signal to a function
        self.parameters_TableWidget_1.itemChanged.connect(self.enableSaveButton)

        # Connect the clicked signal of parameter_save_pushButton_1
        self.parameter_save_pushButton_1.clicked.connect(self.enableUseExportButtons)       
        self.create_user_tableWidget_1.itemChanged.connect(self.enableSaveSetButton)
        
        
        # For importing with file dialog
        self.import_pushButton_1.clicked.connect(self.importFile)
        
        # For importing with the default file
        self.Use_pushButton_1.clicked.connect(lambda: self.importFile(use_default=True))
      
        

        self.tabWidget_2.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)    
        
        #RamP Advance radio button for plot generation
        # Create a Timestamp Radiobutton's Group 
        radio_button_group_2 = QtWidgets.QButtonGroup()
        radio_button_group_2.addButton(self.Minute_radioButton_2)
        radio_button_group_2.addButton(self.FifteenMinute_radioButton_2)
        radio_button_group_2.addButton(self.Hourly_radioButton_2)
        radio_button_group_2.addButton(self.Daily_radioButton_2)
        radio_button_group_2.addButton(self.Monthly_radioButton_2)
        radio_button_group_2.addButton(self.barchart_radioButton_2)
        
        
        
        # Radio toggle (Allows only one radio button to be selected at a time)
        def handle_radio_button_toggled():
            if self.create_data_radioButton_1.isChecked():
                self.i_already_have_data_radioButton.setChecked(False)
            elif self.i_already_have_data_radioButton.isChecked():
                self.create_data_radioButton_1.setChecked(False)

        self.create_data_radioButton_1.toggled.connect(handle_radio_button_toggled)
        self.i_already_have_data_radioButton.toggled.connect(handle_radio_button_toggled)
        
        
        radio_button_group_2 = QtWidgets.QButtonGroup(self.ramp_advance_groupbox_1)
        radio_button_group_2.addButton(self.for_all_users_radioButton_1)
        radio_button_group_2.addButton(self.selected_users_radioButton_1)
        
        
        # When ' I already have .xlsx file selected it will enable 'import file' button
        def handle_i_already_have_data_radio_button_clicked():
            if self.i_already_have_data_radioButton.isChecked():
                self.import_pushButton_1.setEnabled(True)
            else:
                self.import_pushButton_1.setEnabled(False)

        self.i_already_have_data_radioButton.clicked.connect(handle_i_already_have_data_radio_button_clicked)
        
        
        # When import button clicked it will enable two more radio button for selection
        def handle_import_button_clicked():
            self.for_all_users_radioButton_1.setEnabled(True)
            self.selected_users_radioButton_1.setEnabled(True)

        self.import_pushButton_1.clicked.connect(handle_import_button_clicked)
        
        
        # When ' For all users' radio button selected it will enable following objects otherwise disabled
        def handle_all_users_radio_button_checked():
            if self.for_all_users_radioButton_1.isChecked():
                self.start_dateEdit_2.setEnabled(True)
                self.ndays_spinBox_2.setEnabled(True)
                self.set_title_lineEdit_2.setEnabled(True)
                self.set_title_lineEdit_3.setEnabled(True)
                self.simulate_pushButton_2.setEnabled(True)
                self.Ramp_advance_graphicsview_1.setEnabled(True)
                self.select_user_comboBox_1.setEnabled(False)
                self.add_to_list_pushButton_1.setEnabled(False)
                self.selected_user_lineEdit_1.setEnabled(False)
                
            else:
                self.start_dateEdit_2.setEnabled(False)
                self.ndays_spinBox_2.setEnabled(False)
                self.set_title_lineEdit_2.setEnabled(False)
                self.set_title_lineEdit_3.setEnabled(False)
                self.simulate_pushButton_2.setEnabled(False)
                self.Ramp_advance_graphicsview_1.setEnabled(False)

        self.for_all_users_radioButton_1.clicked.connect(handle_all_users_radio_button_checked)
        self.selected_users_radioButton_1.clicked.connect(handle_all_users_radio_button_checked)
        
        
        
        def handle_i_already_have_data_radio_button_toggled(checked):
            if not checked:
                self.for_all_users_radioButton_1.setChecked(False)
                self.selected_users_radioButton_1.setChecked(False)    
                
            self.i_already_have_data_radioButton.toggled.connect(handle_i_already_have_data_radio_button_toggled)
        
        
        # When selected user radio button selected it will enable follwing widgets otherwise disabled
        def handle_selected_users_radio_button_clicked():
            if self.selected_users_radioButton_1.isChecked():
                self.select_user_comboBox_1.setEnabled(True)
                self.add_to_list_pushButton_1.setEnabled(True)
                self.selected_user_lineEdit_1.setEnabled(True)
                
            else:
                self.select_user_comboBox_1.setEnabled(False)
                self.add_to_list_pushButton_1.setEnabled(False)
                self.selected_user_lineEdit_1.setEnabled(False)

        self.selected_users_radioButton_1.clicked.connect(handle_selected_users_radio_button_clicked)
        

        # When user for selected user selected they wil Appear in lineedit and further widgets will be enabled
        def handle_selected_user_lineEdit_text_changed():
            if self.selected_user_lineEdit_1.text():
                self.start_dateEdit_2.setEnabled(True)
                self.ndays_spinBox_2.setEnabled(True)
                self.set_title_lineEdit_2.setEnabled(True)
                self.set_title_lineEdit_3.setEnabled(True)
                self.simulate_pushButton_2.setEnabled(True)
                self.Ramp_advance_graphicsview_1.setEnabled(True)
            else:
                self.start_dateEdit_2.setEnabled(False)
                self.ndays_spinBox_2.setEnabled(False)
                self.set_title_lineEdit_2.setEnabled(False)
                self.set_title_lineEdit_3.setEnabled(False)
                self.simulate_pushButton_2.setEnabled(False)
                self.Ramp_advance_graphicsview_1.setEnabled(False)

        self.selected_user_lineEdit_1.textChanged.connect(handle_selected_user_lineEdit_text_changed)
        
        
        # When Simulation button clicked enables Timestamps radio buttons
        def enable_timestamp_Group_2_radio_buttons(enable=True):
            for button in radio_button_group_2.buttons():
                button.setEnabled(enable)

        # Disable the radio buttons initially
        enable_timestamp_Group_2_radio_buttons(False)

        # Connect simulate button press to enabling the radio buttons
        self.simulate_pushButton_2.clicked.connect(lambda: enable_timestamp_Group_2_radio_buttons(True))
        
        
        
        
        # Enable buttons when Simulate button pressed (RAMP Advance)
        def enable_buttons_2():
            self.save_image_pushButton_1.setEnabled(True)
            self.save_image_pushButton_2.setEnabled(True)
            self.save_csv_pushButton_1.setEnabled(True)
            self.save_csv_pushButton_2.setEnabled(True)
            self.generate_pushButton_2.setEnabled(True)

        # Connect simulate button press to enabling the buttons
        self.simulate_pushButton_2.clicked.connect(enable_buttons_2)
        
        
        def handle_create_data_radio_button_clicked():
            if self.create_data_radioButton_1.isChecked():
                self.tabWidget_2.setEnabled(True)
                self.create_user_tableWidget_1.setEnabled(True)
                self.add_user_pushButton_1.setEnabled(True)
            else:
                self.tabWidget_2.setEnabled(False)
                self.create_user_tableWidget_1.setEnabled(False)
                self.add_user_pushButton_1.setEnabled(False)

        def handle_add_user_button_clicked():
            self.remove_user_pushButton_1.setEnabled(True)
            

        def handle_save_set_button_clicked():
            self.parameters_TableWidget_1.setEnabled(True)


        def handle_parameter_save_button_clicked():
            self.Use_pushButton_1.setEnabled(True)


        self.create_data_radioButton_1.clicked.connect(handle_create_data_radio_button_clicked)
        self.add_user_pushButton_1.clicked.connect(handle_add_user_button_clicked)
        self.save_set_pushButton_1.clicked.connect(handle_save_set_button_clicked)


        #2
        # RAMP Advance plot setup
        # Create a QVBoxLayout for Ramp_advance_graphicsview_1
        self.rampLayout = QtWidgets.QHBoxLayout(self.Ramp_advance_graphicsview_1)

        # figure for plotting (Figure 2)
        self.figure2, self.ax1 = plt.subplots(figsize=(1, 1), nrows=1, ncols=1)
        self.figure2.subplots_adjust(left=0.08, right=0.97, bottom=0.1, top=0.9)
        self.canvas2 = FigureCanvas(self.figure2)

        # figure for plotting (Figure 3)
        self.figure3, self.ax2 = plt.subplots(figsize=(1, 1), nrows=1, ncols=1)
        self.figure3.subplots_adjust(left=0.08, right=0.97, bottom=0.1, top=0.9)
        self.canvas3 = FigureCanvas(self.figure3)

        # canvases to the layout
        self.rampLayout.addWidget(self.canvas2)
        self.rampLayout.addWidget(self.canvas3)

        # Set the layout for Ramp_advance_graphicsview_1
        self.Ramp_advance_graphicsview_1.setLayout(self.rampLayout)
            
        self.profiles_advance = None
        self.title = ""
 




        # RAMP Lite Main Functionality
        
        self.Togglebutton_1.clicked.connect(self.toggleWidget_1)
        self.Togglebutton_2.clicked.connect(self.toggleWidget_2)
        self.Togglebutton_3.clicked.connect(self.toggleWidget_3)
        self.Togglebutton_4.clicked.connect(self.toggleWidget_4)
        self.Togglebutton_5.clicked.connect(self.toggleWidget_5)
        self.Togglebutton_6.clicked.connect(self.toggleWidget_6)
        self.Togglebutton_7.clicked.connect(self.toggleWidget_7)
        self.Togglebutton_8.clicked.connect(self.toggleWidget_8)
        self.Togglebutton_9.clicked.connect(self.toggleWidget_9)
        self.Togglebutton_10.clicked.connect(self.toggleWidget_10)
        self.Togglebutton_11.clicked.connect(self.toggleWidget_11)
        self.Togglebutton_12.clicked.connect(self.toggleWidget_12)
        self.Togglebutton_13.clicked.connect(self.toggleWidget_13)
        self.Togglebutton_14.clicked.connect(self.toggleWidget_14)
        self.Togglebutton_15.clicked.connect(self.toggleWidget_15)
        self.Togglebutton_16.clicked.connect(self.toggleWidget_16)
        self.Togglebutton_17.clicked.connect(self.toggleWidget_17)
        self.Togglebutton_18.clicked.connect(self.toggleWidget_18)
        self.Togglebutton_19.clicked.connect(self.toggleWidget_19)
        self.Togglebutton_20.clicked.connect(self.toggleWidget_20)
        self.Togglebutton_21.clicked.connect(self.toggleWidget_21)
        self.Togglebutton_22.clicked.connect(self.toggleWidget_22)
        self.Togglebutton_23.clicked.connect(self.toggleWidget_23)
        self.Togglebutton_24.clicked.connect(self.toggleWidget_24)
        self.Togglebutton_25.clicked.connect(self.toggleWidget_25)
        self.Togglebutton_26.clicked.connect(self.toggleWidget_26)
        self.Togglebutton_27.clicked.connect(self.toggleWidget_27)
        self.Togglebutton_28.clicked.connect(self.toggleWidget_28)
        self.Togglebutton_29.clicked.connect(self.toggleWidget_29)
        self.Togglebutton_30.clicked.connect(self.toggleWidget_30)
        
        
        


    def toggleWidget_1(self):
        if self.widget_1.isHidden(): 
            self.widget_1.show(); 
            self.Togglebutton_1.setText("▼")  # Black down pointing unicode triangle
        else: 
            self.widget_1.hide(); 
            self.Togglebutton_1.setText("◀")   # Black left pointing unicode triangle
    
    def toggleWidget_2(self):
        if self.widget_2.isHidden(): 
            self.widget_2.show(); 
            self.Togglebutton_2.setText("▼")  # Black down pointing unicode triangle
        else: 
            self.widget_2.hide(); 
            self.Togglebutton_2.setText("◀")   # Black left pointing unicode triangle
    
    def toggleWidget_3(self):
        if self.widget_3.isHidden(): 
            self.widget_3.show(); 
            self.Togglebutton_3.setText("▼")  # Black down pointing unicode triangle
        else: 
            self.widget_3.hide(); 
            self.Togglebutton_3.setText("◀")   # Black left pointing unicode triangle
    
    def toggleWidget_4(self):
        if self.widget_4.isHidden(): 
            self.widget_4.show(); 
            self.Togglebutton_4.setText("▼")  # Black down pointing unicode triangle
        else: 
            self.widget_4.hide(); 
            self.Togglebutton_4.setText("◀")
    
    def toggleWidget_5(self):
        if self.widget_5.isHidden(): 
            self.widget_5.show(); 
            self.Togglebutton_5.setText("▼")  # Black down pointing unicode triangle
        else: 
            self.widget_5.hide(); 
            self.Togglebutton_5.setText("◀")   # Black left pointing unicode triangle
    
    def toggleWidget_6(self):
        if self.widget_6.isHidden(): 
            self.widget_6.show(); 
            self.Togglebutton_6.setText("▼")  # Black down pointing unicode triangle
        else: 
            self.widget_6.hide(); 
            self.Togglebutton_6.setText("◀")   # Black left pointing unicode triangle
    
    def toggleWidget_7(self):
        if self.widget_7.isHidden(): 
            self.widget_7.show(); 
            self.Togglebutton_7.setText("▼")  # Black down pointing unicode triangle
        else: 
            self.widget_7.hide(); 
            self.Togglebutton_7.setText("◀")
    
    def toggleWidget_8(self):
        if self.widget_8.isHidden(): 
            self.widget_8.show(); 
            self.Togglebutton_8.setText("▼")  # Black down pointing unicode triangle
        else: 
            self.widget_8.hide(); 
            self.Togglebutton_8.setText("◀")   # Black left pointing unicode triangle
    
    def toggleWidget_9(self):
        if self.widget_9.isHidden(): 
            self.widget_9.show(); 
            self.Togglebutton_9.setText("▼")  # Black down pointing unicode triangle
        else: 
            self.widget_9.hide(); 
            self.Togglebutton_9.setText("◀")   # Black left pointing unicode triangle
    
    def toggleWidget_10(self):
        if self.widget_10.isHidden(): 
            self.widget_10.show(); 
            self.Togglebutton_10.setText("▼")  # Black down pointing unicode triangle
        else: 
            self.widget_10.hide(); 
            self.Togglebutton_10.setText("◀")   # Black left pointing unicode triangle
    
    def toggleWidget_11(self):
        if self.widget_11.isHidden(): 
            self.widget_11.show(); 
            self.Togglebutton_11.setText("▼")  # Black down pointing unicode triangle
        else: 
            self.widget_11.hide(); 
            self.Togglebutton_11.setText("◀")   # Black left pointing unicode triangle
    
    def toggleWidget_12(self):
        if self.widget_12.isHidden(): 
            self.widget_12.show(); 
            self.Togglebutton_12.setText("▼")  # Black down pointing unicode triangle
        else: 
            self.widget_12.hide(); 
            self.Togglebutton_12.setText("◀")   # Black left pointing unicode triangle
    
    def toggleWidget_13(self):
        if self.widget_13.isHidden(): 
            self.widget_13.show(); 
            self.Togglebutton_13.setText("▼")  # Black down pointing unicode triangle
        else: 
            self.widget_13.hide(); 
            self.Togglebutton_13.setText("◀")   # Black left pointing unicode triangle
    
    def toggleWidget_14(self):
        if self.widget_14.isHidden(): 
            self.widget_14.show(); 
            self.Togglebutton_14.setText("▼")  # Black down pointing unicode triangle
        else: 
            self.widget_14.hide(); 
            self.Togglebutton_14.setText("◀")   # Black left pointing unicode triangle
    
    def toggleWidget_15(self):
        if self.widget_15.isHidden(): 
            self.widget_15.show(); 
            self.Togglebutton_15.setText("▼")  # Black down pointing unicode triangle
        else: 
            self.widget_15.hide(); 
            self.Togglebutton_15.setText("◀")   # Black left pointing unicode triangle
    
    def toggleWidget_16(self):
        if self.widget_16.isHidden(): 
            self.widget_16.show(); 
            self.Togglebutton_16.setText("▼")  # Black down pointing unicode triangle
        else: 
            self.widget_16.hide(); 
            self.Togglebutton_16.setText("◀")   # Black left pointing unicode triangle
    
    def toggleWidget_17(self):
        if self.widget_17.isHidden(): 
            self.widget_17.show(); 
            self.Togglebutton_17.setText("▼")  # Black down pointing unicode triangle
        else: 
            self.widget_17.hide(); 
            self.Togglebutton_17.setText("◀")   # Black left pointing unicode triangle
    
    def toggleWidget_18(self):
        if self.widget_18.isHidden(): 
            self.widget_18.show(); 
            self.Togglebutton_18.setText("▼")  # Black down pointing unicode triangle
        else: 
            self.widget_18.hide(); 
            self.Togglebutton_18.setText("◀")   # Black left pointing unicode triangle
    
    def toggleWidget_19(self):
        if self.widget_19.isHidden(): 
            self.widget_19.show(); 
            self.Togglebutton_19.setText("▼")  # Black down pointing unicode triangle
        else: 
            self.widget_19.hide(); 
            self.Togglebutton_19.setText("◀")   # Black left pointing unicode triangle
    
    def toggleWidget_20(self):
        if self.widget_20.isHidden(): 
            self.widget_20.show(); 
            self.Togglebutton_20.setText("▼")  # Black down pointing unicode triangle
        else: 
            self.widget_20.hide(); 
            self.Togglebutton_20.setText("◀")   # Black left pointing unicode triangle
    
    def toggleWidget_21(self):
        if self.widget_21.isHidden(): 
            self.widget_21.show(); 
            self.Togglebutton_21.setText("▼")  # Black down pointing unicode triangle
        else: 
            self.widget_21.hide(); 
            self.Togglebutton_21.setText("◀")   # Black left pointing unicode triangle
    
    def toggleWidget_22(self):
        if self.widget_22.isHidden(): 
            self.widget_22.show(); 
            self.Togglebutton_22.setText("▼")  # Black down pointing unicode triangle
        else: 
            self.widget_22.hide(); 
            self.Togglebutton_22.setText("◀")   # Black left pointing unicode triangle
    
    def toggleWidget_23(self):
        if self.widget_23.isHidden(): 
            self.widget_23.show(); 
            self.Togglebutton_23.setText("▼")  # Black down pointing unicode triangle
        else: 
            self.widget_23.hide(); 
            self.Togglebutton_23.setText("◀")   # Black left pointing unicode triangle
    
    def toggleWidget_24(self):
        if self.widget_24.isHidden(): 
            self.widget_24.show(); 
            self.Togglebutton_24.setText("▼")  # Black down pointing unicode triangle
        else: 
            self.widget_24.hide(); 
            self.Togglebutton_24.setText("◀")   # Black left pointing unicode triangle
    
    def toggleWidget_25(self):
        if self.widget_25.isHidden(): 
            self.widget_25.show(); 
            self.Togglebutton_25.setText("▼")  # Black down pointing unicode triangle
        else: 
            self.widget_25.hide(); 
            self.Togglebutton_25.setText("◀")   # Black left pointing unicode triangle
    
    def toggleWidget_26(self):
        if self.widget_26.isHidden(): 
            self.widget_26.show(); 
            self.Togglebutton_26.setText("▼")  # Black down pointing unicode triangle
        else: 
            self.widget_26.hide(); 
            self.Togglebutton_26.setText("◀")   # Black left pointing unicode triangle
    
    def toggleWidget_27(self):
        if self.widget_27.isHidden(): 
            self.widget_27.show(); 
            self.Togglebutton_27.setText("▼")  # Black down pointing unicode triangle
        else: 
            self.widget_27.hide(); 
            self.Togglebutton_27.setText("◀")   # Black left pointing unicode triangle
    
    def toggleWidget_28(self):
        if self.widget_28.isHidden(): 
            self.widget_28.show(); 
            self.Togglebutton_28.setText("▼")  # Black down pointing unicode triangle
        else: 
            self.widget_28.hide(); 
            self.Togglebutton_28.setText("◀")   # Black left pointing unicode triangle
    
    def toggleWidget_29(self):
        if self.widget_29.isHidden(): 
            self.widget_29.show(); 
            self.Togglebutton_29.setText("▼")  # Black down pointing unicode triangle
        else: 
            self.widget_29.hide(); 
            self.Togglebutton_29.setText("◀")   # Black left pointing unicode triangle
    
    def toggleWidget_30(self):
        if self.widget_30.isHidden(): 
            self.widget_30.show(); 
            self.Togglebutton_30.setText("▼")  # Black down pointing unicode triangle
        else: 
            self.widget_30.hide(); 
            self.Togglebutton_30.setText("◀")   # Black left pointing unicode triangle


    def handle_appliancename_change(self):
        for lineEdit in self.appliancename_lineEdits:
            if lineEdit.text():
                self.start_dateEdit_1.setEnabled(True)
                self.ndays_spinBox_1.setEnabled(True)
                self.set_title_lineEdit_1.setEnabled(True)
                self.simulate_pushButton_1.setEnabled(True)
                break
        else:
            self.start_dateEdit_1.setEnabled(False)
            self.ndays_spinBox_1.setEnabled(False)
            self.set_title_lineEdit_1.setEnabled(False)
            self.simulate_pushButton_1.setEnabled(False)






    # RAMP Lite Simulation Functionality
    #
    #
    #
    
    def ramplite_simulation(self):
        try:
            
            user_name =self.user_name_lineEdit_1.text()
            # Define User instance
            user1 = User(user_name , 1)
            
            print(f"User Name: {user1.user_name}")
            print(f"Number of Users: {user1.num_users}")
            
            for i in range(1, 31):
    
                appliance_name = getattr(self, f'appliancename_lineEdit_{i}').text()
    
                if not appliance_name:  # Check if the name is empty
                    continue
                
                
                w1_start_i = getattr(self, f'w1start_timeEdit_{i}').time()
                w1_end_i = getattr(self, f'w1end_timeEdit_{i}').time()     
    
                w2_start_i = getattr(self, f'w2start_timeEdit_{i}').time()
                w2_end_i = getattr(self, f'w2end_timeEdit_{i}').time()     
                
                w3_start_i = getattr(self, f'w3start_timeEdit_{i}').time()
                w3_end_i = getattr(self, f'w3end_timeEdit_{i}').time()     
                
    
                
                
                user1.add_appliance(
                    name= appliance_name,
                    number=getattr(self, f'number_spinBox_{i}').value(),
                    power=getattr(self, f'power_spinBox_{i}').value(),
                    func_time=getattr(self, f'function_time_spinBox_{i}').value(),
                    num_windows=getattr(self, f'num_windows_spinBox_{i}').value(),
                    occasional_use=getattr(self, f'occationaluse_spinBox_{i}').value() / 100,
                    wd_we_type=getattr(self, f'wd_we_comboBox_{i}').currentIndex(),
                    window_1=[w1_start_i.hour() * 60 + w1_start_i.minute(), w1_end_i.hour() * 60 + w1_end_i.minute()],
                    window_2=[w2_start_i.hour() * 60 + w2_start_i.minute(), w2_end_i.hour() * 60 + w2_end_i.minute()],
                    window_3=[w3_start_i.hour() * 60 + w3_start_i.minute(), w3_end_i.hour() * 60 + w3_end_i.minute()],
                    random_var_w=getattr(self, f'r_var_spinBox_{i}').value() / 100,
                    time_fraction_random_variability=getattr(self, f'tfrv_spinBox_{i}').value() / 100,
                    thermal_p_var=getattr(self, f'thermal_v_spinBox_{i}').value() / 100,
                    func_cycle=getattr(self, f'func_cycle_spinBox_{i}').value(),
                    fixed=getattr(self, f'fixe_comboBox_{i}').currentText(),
                    flat=getattr(self, f'flat_comboBox_{i}').currentText()
                    )
        
        
        
            start_date_widget = self.start_dateEdit_1 
            date_from_widget = start_date_widget.date().toString("yyyy-MM-dd")
            user_collect = UseCase(users=[user1], date_start = date_from_widget)
    
            
            
            self.figure1.clear()
    
            n_days = self.ndays_spinBox_1.value()
            user_collect.initialize(num_days=n_days, force=True)
            
            self.profiles_lite = pd.DataFrame(index = pd.date_range(start = date_from_widget, periods = 1440*n_days,freq="T"))
            
            
            
            for user in user_collect.users:
                
                # storing daily profiles for a user
                user_profiles = []
                for day_idx, day in enumerate(user_collect.days):
                    single_profile = user.generate_single_load_profile(
                        prof_i = day_idx, # the day to generate the profile
                        day_type = get_day_type(day)    
                        )
                    
                    user_profiles.extend(single_profile)
                    
                self.profiles_lite[user.user_name] = user_profiles
            
    
            self.title = self.set_title_lineEdit_1.text()
            self.ax = self.figure1.add_subplot(111)
            self.ax.set_xlabel('Time (Minutes)')
            self.ax.set_ylabel('Power(w)')
            self.profiles_lite.plot(ax=self.ax, title=self.title)
            self.figure1.tight_layout()
            
            # Redraw the canvas
            self.canvas1.draw()
            self.figure1.tight_layout()
            
            print("Plot with Default 1 minute timestamp is generated")
            
        except Exception as e:
            print(f"An error occurred: {e}")

        
    # Generate Plots based on Timestamp selected when 'Generate Button Pressed'  
    def generate_plots_lite(self):

      
        self.ax.clear()
        

        
        if self.Minute_radioButton_1.isChecked():
            # Plot for Minute profile 
            minute_profile_lite = self.profiles_lite            
            minute_profile_lite.plot(ax=self.ax, kind="line", title=self.title, xlabel="Time (Minutes)", ylabel="Power(W)")
            self.ax.set_xlabel("Time (Minutes)", fontsize=12)  # Set font size for x-label
            self.ax.set_ylabel("Power(W)", fontsize=12) # Set font size for x-label and y-label
            self.figure1.tight_layout()
            print("Plot with 1 minute timestamp is generated")

    
        elif self.FifteenMinute_radioButton_1.isChecked():
            # Plot for 15Minute profile 
            fifteen_minute_profile_lite = self.profiles_lite.resample("15T").sum()            
            fifteen_minute_profile_lite.plot(ax=self.ax, kind="line", title=self.title, xlabel="Time (15 Minutes)", ylabel="Power(W)")
            self.ax.set_xlabel("Time (1 Minutes)", fontsize=12)  # Set font size for x-label
            self.ax.set_ylabel("Power(W)", fontsize=12)  # Set font size for x-label and y-label
            self.figure1.tight_layout()
            print("Plot with 15 minute timestamp is generated")
            
        elif self.Hourly_radioButton_1.isChecked():
            # Plot for hourly profile 
            hourly_profile_lite = self.profiles_lite.resample("1H").sum()            
            hourly_profile_lite.plot(ax=self.ax, kind="line", title=self.title, xlabel="Time (Hours)", ylabel="Power(W)")
            self.ax.set_xlabel("Time (Hours)", fontsize=12)  # Set font size for x-label
            self.ax.set_ylabel("Power(W)", fontsize=12)  # Set font size for x-label and y-label
            self.figure1.tight_layout()
            print("Plot with Hourly timestamp is generated")
            
        elif self.Daily_radioButton_1.isChecked():
            # Plot for Daily profile 
            daily_profile_lite = self.profiles_lite.resample("1D").sum()            
            daily_profile_lite.plot(ax=self.ax, kind="line", title=self.title, xlabel="Time (Days)", ylabel="Power(W)")
            self.ax.set_xlabel("Time (days)", fontsize=12)  # Set font size for x-label
            self.ax.set_ylabel("Power(W)", fontsize=12)  # Set font size for x-label and y-label
            self.figure1.tight_layout()
            print("Plot with Daily timestamp is generated")
            
        elif self.Monthly_radioButton_1.isChecked():
            # Plot for hourly profile 
            monthly_profile_lite = self.profiles_lite.resample("1M").sum()            
            monthly_profile_lite.plot(ax=self.ax, kind="line", title=self.title, xlabel="Time (Months)", ylabel="Power(W)")
            self.ax.set_xlabel("Time (Months)", fontsize=12)  # Set font size for x-label
            self.ax.set_ylabel("Power(W)", fontsize=12) # Set font size for x-label and y-label
            self.figure1.tight_layout()
            print("Plot with Monthly timestamp is generated")
            
        elif self.barchart_radioButton_1.isChecked():
            # Plot for Monthly bar chart
            monthly_bar_profile_lite = self.profiles_lite.resample("1M").sum()            
            monthly_bar_profile_lite.index = monthly_bar_profile_lite.index.strftime('%B')  # Format the index to month names
            monthly_bar_profile_lite.plot(ax=self.ax, kind="bar", title=self.title, xlabel="Month", ylabel="Power(W)")
            self.ax.set_xlabel("Time (Months)", fontsize=12)  # Set font size for x-label
            self.ax.set_ylabel("Power(W)", fontsize=12) # Set font size for x-label and y-label
            self.figure1.tight_layout()
            print("bar Chart with Monthly timestamp is generated, Saving .CSV is not possible for this")
      

        
        # Redraw the canvases
        self.canvas1.draw()


    # Saves Plot as a image (RAMP Lite)    
    def save_figure_lite(self):
        
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self.tabWidget, "Save Figure", "", "PNG Files (*.png);;All Files (*)", options=options)

        
        if file_name:
            # Save the figure as an image with the chosen file name
            self.figure1.savefig(file_name)       
            
            print(f"Plot saved as image file: {file_name}")
        else:
            print("Plot saving canceled")
    
    
    # Saves Data frame as a .CSV file based on Timestamp Selected     
    def save_as_csv_lite(self):
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Save as .csv", "", "CSV Files (*.csv);;All Files (*)")
    
        if filename:
            # Resample data based on the selected radio button
            if self.Minute_radioButton_1.isChecked():
                df = self.profiles_lite.resample("1T").sum()
                timestamp_message = "Minute"
            elif self.FifteenMinute_radioButton_1.isChecked():
                df = self.profiles_lite.resample("15T").sum()
                timestamp_message = "Fifteen Minute"
            elif self.Hourly_radioButton_1.isChecked():
                df = self.profiles_lite.resample("1H").sum()
                timestamp_message = "Hourly"
            elif self.Daily_radioButton_1.isChecked():
                df = self.profiles_lite.resample("1D").sum()
                timestamp_message = "Daily"
            elif self.Monthly_radioButton_1.isChecked():
                df = self.profiles_lite.resample("1M").sum()
                timestamp_message = "Monthly"
    
            # Reset index to include timestamp as a separate column
            df.reset_index(inplace=True)
    
            # Save DataFrame to CSV file
            df.to_csv(filename, index=False)
    
            # Print the message with the file path and timestamp information
            print(f"Dataframe with {timestamp_message} timestamp is saved as CSV file: {filename}")
        else:
            print("CSV saving canceled")
            
            
    # RAMP Advance 
    #
    #
    
    # Creating User and Appliance data
    
    # To create New User
    def create_user(self):
        rowPosition = self.create_user_tableWidget_1.rowCount()
        self.create_user_tableWidget_1.insertRow(rowPosition)
     
    # To remove selected User   
    def remove_user(self):
        current_row = self.create_user_tableWidget_1.currentRow()
        if current_row >= 0:
            self.create_user_tableWidget_1.removeRow(current_row)
            
    # Save User and Apliance data in UseCase and allows Data edit in 'Set Parameter' Tab       
    def save_set_parameters(self):
        try:
            
            user_app = {}
        
            for row in range(self.create_user_tableWidget_1.rowCount()):
                user = self.create_user_tableWidget_1.item(row, 0).text()
                appliances = self.create_user_tableWidget_1.item(row, 1).text().split(',')  # Split the values
        
                for app in appliances:
                    # Remove leading and trailing spaces, and quotation marks
                    app = app.strip().strip("'").strip('"')
                    
                    if user not in user_app:
                        user_app[user] = [app]
                    else:
                        user_app[user].append(app)
            print(user_app)
            # Creating a UseCase class to create the database
            use_case = UseCase()
            print(user_app)
            
            # Assigning the appliances to users
            for user, apps in user_app.items():
            
                user_instance = User(user_name=user)
            
                for app in apps:
                    app_instance = user_instance.add_appliance(name=app)
                    app_instance.windows()
            
                use_case.add_user(user_instance)
            
            
    
            # Export data to a DataFrame
            df = use_case.export_to_dataframe()
            print(df)
            
            
            for i in range(df.shape[1]):
                self.parameters_TableWidget_1.resizeColumnToContents(i)
            
            # Clear existing data in the QTableWidget
            self.parameters_TableWidget_1.clear()
            
            # Set the number of rows and columns based on the DataFrame
            self.parameters_TableWidget_1.setRowCount(df.shape[0])
            self.parameters_TableWidget_1.setColumnCount(df.shape[1])
            
            # Set the headers
            self.parameters_TableWidget_1.setHorizontalHeaderLabels(df.columns)
            
            header2 = self.parameters_TableWidget_1.horizontalHeader()
            for i in range(df.shape[1]):
                header2.setSectionResizeMode(i, QHeaderView.ResizeToContents)
            
            # Populate the table with data from the DataFrame
            for i in range(df.shape[0]):
                for j in range(df.shape[1]):
                    item = QTableWidgetItem(str(df.iloc[i, j]))
                    self.parameters_TableWidget_1.setItem(i, j, item)
            print("User and Appliance are defined. Please set parameters in the 'Set Parameters' tab.")
            
            
        except Exception as e:
            print(f"An error occurred: {e}")
    # Enables Buttons           
    def enableSaveSetButton(self):
        self.save_set_pushButton_1.setEnabled(True)
 
    def enableSaveButton(self):
        self.parameter_save_pushButton_1.setEnabled(True)

    def enableUseExportButtons(self):
        self.Use_pushButton_1.setEnabled(True)

    
    # When Pressed 'Use For Simulation' it will create .xlsx file in Current Directory
    def save_created_file(self):
        try:
            
            # Get the current working directory
            current_directory = os.getcwd()
            
            # Combine with the desired file name
            file_path = os.path.join(current_directory, "User_Appliance_Data.xlsx")
        
            # Get the number of rows and columns in the table
            num_rows = self.parameters_TableWidget_1.rowCount()
            num_cols = self.parameters_TableWidget_1.columnCount()
        
            if num_rows > 0 and num_cols > 0:
                # Get the data from 'Exported Data Table'
                data = []
                for row in range(num_rows):
                    row_data = []
                    for col in range(num_cols):
                        item = self.parameters_TableWidget_1.item(row, col)
                        if item is not None:
                            text = item.text()
                            # Determine the type of data in the column
                            try:
                                value = float(text)  # Try to convert to float
                                row_data.append(value)
                            except ValueError:
                                row_data.append(text)
                        else:
                            row_data.append("")
                    data.append(row_data)
        
                # Create a DataFrame from the data
                df = pd.DataFrame(data)
        
                # Get the header data
                header = []
                for col in range(num_cols):
                    item = self.parameters_TableWidget_1.horizontalHeaderItem(col)
                    if item is not None:
                        header.append(item.text())
                    else:
                        header.append(f"Column {col+1}")
        
                # Add header to the DataFrame
                df.columns = header
        
                # Save the DataFrame to an Excel file with appropriate data types
                writer = pd.ExcelWriter(file_path, engine='xlsxwriter')
                df.to_excel(writer, index=False, sheet_name='Sheet1')
        
                # Access the xlsxwriter workbook and worksheet objects
                workbook  = writer.book
                worksheet = writer.sheets['Sheet1']
        
                # Set column widths based on the maximum length of the data in each column
                for i, col in enumerate(df.columns):
                    max_len = max(df[col].astype(str).apply(len).max(), len(col))
                    worksheet.set_column(i, i, max_len)
        
                # Close the Pandas Excel writer and output the Excel file
                writer._save()
                print(f"File named 'User and Appliance Database' is saved to {file_path}, File will be replaced when next time you save it, You may copy and save it somewhere else for future purpose or else")
            else:
                print("No data to save.")
                
        except Exception as e:
            print(f"An error occurred: {e}")
            

            
    # IMport file function
    # If data is created in GUI then it will import File created by save-created-file method
    # Or else it allowes you to upload your own .xlsx file
    def importFile(self, use_default=False):
        try:
            
            self.select_user_comboBox_1.clear()
            self.selected_user_lineEdit_1.clear()  
            if not use_default:
                file_path, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Import Edited Excel File")
                self.select_user_comboBox_1.clear()
                self.selected_user_lineEdit_1.clear() 
            else:
                # Use default file path if use_default is True
                current_directory = os.getcwd()
                file_path = os.path.join(current_directory, "User_Appliance_Data.xlsx")
                self.select_user_comboBox_1.clear()
                self.selected_user_lineEdit_1.clear() 
                
                
            if file_path:
                self.use_case = UseCase()  # Assign it to the instance variable
                self.use_case.load(file_path)
                print("File loaded successfully") # Prints if file is succesfully loaded
                
                user_names = pd.read_excel(file_path, header=None, skiprows=1).iloc[:, 0].tolist()
        
                # Remove duplicates by converting to a set and back to a list
                unique_user_names = list(set(user_names))
    
                
                # Populate the combo box with user names
                self.select_user_comboBox_1.addItems(unique_user_names)
                self.enableWidgetsAfterFileLoaded()
                self.treeview(file_path)
                
        except Exception as e:
            print(f"An error occurred: {e}")

        
    def enableWidgetsAfterFileLoaded(self):

        self.for_all_users_radioButton_1.setEnabled(True)
        self.selected_users_radioButton_1.setEnabled(True)

    # If simulation for selected users desired
    # All users will showup in Combo box and from combo box User can be added to list of selected users
    def addUserFromComboBox(self):
        try:
            
            selected_user = self.select_user_comboBox_1.currentText()
            current_text = self.selected_user_lineEdit_1.text()
            
            if current_text:
                updated_text = f"{current_text}, {selected_user}"
            else:
                updated_text = selected_user
    
            self.selected_user_lineEdit_1.setText(updated_text)
            self.selected_users.append(selected_user)
            
            print(f"{selected_user} is added to the list for simulation.")
            
        except Exception as e:
            print(f"An error occurred: {e}")

    # RAMP Advance Simulation
    def ramp_advance_simulation(self):
        
        try:
            
            plt.close('all')
            matplotlib.use('Qt5Agg')
        
            # Checks if Selected radio button is checked, if yes then selected Users will be collected for Simulation
            if self.selected_users_radioButton_1.isChecked() and hasattr(self, 'selected_users') and self.selected_users:
                selected_users = self.selected_users
            else: # else Selected user wil be considers as All Users
                selected_users = [user.user_name for user in self.use_case.users]
        
    
        
            n_days = self.ndays_spinBox_2.value() # Collects Number of days
            
            start_date_widget_2 = self.start_dateEdit_2
            date_from_widget_2 = start_date_widget_2.date()
            date_start  = date_from_widget_2.toString("yyyy-MM-dd")
            self.use_case.date_start = date_start
            self.use_case.initialize(num_days =n_days, force = True)
            self.use_case.generate_daily_load_profiles()
            
            
            selected_date = self.start_dateEdit_2.date() # Collects selected date
            
            # Define dataframe
            self.profiles_advance = pd.DataFrame(index=pd.date_range(start=selected_date.toString("yyyy-MM-dd"), periods=1440 * n_days, freq="T"))
        
            for user in self.use_case.users:
                if user.user_name in selected_users:
                    user_profiles = []
                    for day_idx, day in enumerate(self.use_case.days):
                        profile = user.generate_aggregated_load_profile(
                            prof_i=day_idx,
    
                            day_type= get_day_type(day)
                        )
        
                        user_profiles.extend(profile)
        
                    self.profiles_advance[user.user_name] = user_profiles
                    
    
            self.ax1.clear() # Clears previous plots
            self.ax2.clear()
            self.figure2.clear() # Clears previous figures
            self.figure3.clear()
    
        
            self.title1 = self.set_title_lineEdit_2.text() # Collects Title for the plot on left side
            self.ax1 = self.figure2.add_subplot(111) 
    
    
            self.profiles_advance.plot(ax=self.ax1, kind="line", title = self.title1, xlabel="Time(Minutes)", ylabel="Power(W)")
    
    
            
            self.title2 = self.set_title_lineEdit_3.text() # Collects Title for the plot on right
            self.ax2 = self.figure3.add_subplot(111)
            sum_of_all_users = self.profiles_advance.resample('1T').sum().sum(axis=1)
            sum_of_all_users.plot(ax=self.ax2, kind ='line', title = self.title2, xlabel="Time(Minutes)", ylabel="Power(W)")
    
            
            print("Plot with Default 1 minute timestamp is generated")
            
            # Redraw the canvas
            self.canvas2.draw()
            self.canvas3.draw()
    
    
            plt.show()
      
        except Exception as e:
            print(f"An error occurred: {e}")
        
        
    # Generates Plots Based on Timestamp Selected  
    def generate_plots_ramp_advance(self):
        matplotlib.use('Qt5Agg')
      
        self.ax1.clear()
        self.ax2.clear()
        
        if self.Minute_radioButton_2.isChecked():
            # Plot for Minute profile individual
            minute_profile_advance = self.profiles_advance         
            minute_profile_advance.plot(ax=self.ax1, kind="line", title=self.title1, xlabel="Time (Minutes)", ylabel="Power(W)")
            self.ax1.set_xlabel("Time (Minutes)", fontsize=12)  # Set font size for x-label
            self.ax1.set_ylabel("Power(W)", fontsize=12) # Set font size for x-label and y-label
            self.figure2.tight_layout()
            
            # Plot for Minute profile sum of all users
            minute_profile_advance_sum = self.profiles_advance.resample("1T").sum().sum(axis=1)         
            minute_profile_advance_sum.plot(ax=self.ax2, kind="line", title=self.title2, xlabel="Time (MInutes)", ylabel="Power(W)")
            self.ax2.set_xlabel("Time (Minutes)", fontsize=12)  # Set font size for x-label
            self.ax2.set_ylabel("Power(W)", fontsize=12) # Set font size for x-label and y-label
            self.figure3.tight_layout()
            print("Plot with 1 minute timestamp is generated")
        
        
        elif self.FifteenMinute_radioButton_2.isChecked():
            # Plot for 15Minute profile 
            fifteen_minute_profile_advance = self.profiles_advance.resample("15T").sum()            
            fifteen_minute_profile_advance.plot(ax=self.ax1, kind="line", title=self.title1, xlabel="Time (15 Minutes)", ylabel="Power(W)")
            self.ax1.set_xlabel("Time (15 Minutes)", fontsize=12)  # Set font size for x-label
            self.ax1.set_ylabel("Power(W)", fontsize=12) # Set font size for x-label and y-label
            self.figure2.tight_layout()

            # Plot for 15Minute profile 
            fifteen_minute_profile_advance_sum = self.profiles_advance.resample("15T").sum().sum(axis=1)           
            fifteen_minute_profile_advance_sum.plot(ax=self.ax2, kind="line", title=self.title2, xlabel="Time (15 Minutes)", ylabel="Power(W)")
            self.ax2.set_xlabel("Time (15 Minutes)", fontsize=12)  # Set font size for x-label
            self.ax2.set_ylabel("Power(W)", fontsize=12) # Set font size for x-label and y-label
            self.figure3.tight_layout()
            print("Plot with 15 minute timestamp is generated")
                        
        elif self.Hourly_radioButton_2.isChecked():
            # Plot for hourly profile 
            hourly_profile_advance = self.profiles_advance.resample("1H").sum()            
            hourly_profile_advance.plot(ax=self.ax1, kind="line", title=self.title1, xlabel="Time (Hours)", ylabel="Power(W)")
            self.ax1.set_xlabel("Time (Hours)", fontsize=12)  # Set font size for x-label
            self.ax1.set_ylabel("Power(W)", fontsize=12) # Set font size for x-label and y-label
            self.figure2.tight_layout()
            
            # Plot for hourly profile 
            hourly_profile_advance_sum = self.profiles_advance.resample("1H").sum().sum(axis=1)           
            hourly_profile_advance_sum.plot(ax=self.ax2, kind="line", title=self.title2, xlabel="Time (Hours)", ylabel="Power(W)")
            self.ax2.set_xlabel("Time (Hours)", fontsize=12)  # Set font size for x-label
            self.ax2.set_ylabel("Power(W)", fontsize=12) # Set font size for x-label and y-label
            self.figure3.tight_layout()
            print("Plot with Hourly timestamp is generated")
            
        elif self.Daily_radioButton_2.isChecked():
            # Plot for Daily profile 
            daily_profile_advance = self.profiles_advance.resample("1D").sum()            
            daily_profile_advance.plot(ax=self.ax1, kind="line", title=self.title1, xlabel="Time (Days)", ylabel="Power(W)")
            self.ax1.set_xlabel("Time (Days)", fontsize=12)  # Set font size for x-label
            self.ax1.set_ylabel("Power(W)", fontsize=12) # Set font size for x-label and y-label
            self.figure2.tight_layout()
            
            # Plot for Daily profile 
            daily_profile_advance_sum = self.profiles_advance.resample("1D").sum().sum(axis=1)           
            daily_profile_advance_sum.plot(ax=self.ax2, kind="line", title=self.title2, xlabel="Time (Days)", ylabel="Power(W)")
            self.ax2.set_xlabel("Time (Days)", fontsize=12)  # Set font size for x-label
            self.ax2.set_ylabel("Power(W)", fontsize=12) # Set font size for x-label and y-label
            self.figure3.tight_layout()
            print("Plot with Daily timestamp is generated")
            
        elif self.Monthly_radioButton_2.isChecked():
            # Plot for hourly profile 
            monthly_profile_advance = self.profiles_advance.resample("1M").sum()            
            monthly_profile_advance.plot(ax=self.ax1, kind="line", title=self.title1, xlabel="Time (Months)", ylabel="Power(W)")
            self.ax1.set_xlabel("Time (Months)", fontsize=12)  # Set font size for x-label
            self.ax1.set_ylabel("Power(W)", fontsize=12) # Set font size for x-label and y-label
            self.figure2.tight_layout()
            
            # Plot for hourly profile 
            monthly_profile_advance_sum = self.profiles_advance.resample("1M").sum().sum(axis=1)         
            monthly_profile_advance_sum.plot(ax=self.ax2, kind="line", title=self.title2, xlabel="Time (Months)", ylabel="Power(W)")
            self.ax2.set_xlabel("Time (Months)", fontsize=12)  # Set font size for x-label
            self.ax2.set_ylabel("Power(W)", fontsize=12) # Set font size for x-label and y-label
            self.figure3.tight_layout()
            print("Plot with Monthly timestamp is generated")
            
        elif self.barchart_radioButton_2.isChecked():
            # Plot for Monthly bar chart
            monthly_bar_profile_advance = self.profiles_advance.resample("1M").sum()            
            monthly_bar_profile_advance.index = monthly_bar_profile_advance.index.strftime('%B')  # Format the index to month names
            monthly_bar_profile_advance.plot(ax=self.ax1, kind="bar", title=self.title1, xlabel="Month", ylabel="Power(W)")
            self.ax1.set_xlabel("Time (Months)", fontsize=12)  # Set font size for x-label
            self.ax1.set_ylabel("Power(W)", fontsize=12) # Set font size for x-label and y-label
            self.figure2.tight_layout()

            # Plot for Monthly bar chart
            monthly_bar_profile_advance_sum = self.profiles_advance.resample("1M").sum().sum(axis=1)          
            monthly_bar_profile_advance_sum.index = monthly_bar_profile_advance_sum.index.strftime('%B')  # Format the index to month names
            monthly_bar_profile_advance_sum.plot(ax=self.ax2, kind="bar", title=self.title2, xlabel="Month", ylabel="Power(W)")
            self.ax2.set_xlabel("Time (Months)", fontsize=12)  # Set font size for x-label
            self.ax2.set_ylabel("Power(W)", fontsize=12) # Set font size for x-label and y-label
            self.figure3.tight_layout()
            print("Bar Chart with Monthly timestamp is generated")


        # Adjust layout
        
        
        # Redraw the canvases
        self.canvas2.draw()
        self.canvas3.draw()

    # Saves Current plots
    def save_image_1(self):   
        if self.figure2.axes:
            filename, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Save Ax1 Image", "", "Images (*.png *.xpm *.jpg *.bmp);;All Files (*)")
            if filename:
                self.figure2.savefig(filename)
                print(f"Plot With individual users is saved as image file to {filename}")
    
    def save_image_2(self):
        if self.figure3.axes:
            filename, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Save Ax2 Image", "", "Images (*.png *.xpm *.jpg *.bmp);;All Files (*)")
            if filename:
                self.figure3.savefig(filename)
                print(f"Plot With sum of all users is saved as image file to {filename}")
                
                
    
    # Saves dataframe as .CSV file based on Timestamp Selected
    def save_as_csv_advance_individual_user(self):
        if self.Minute_radioButton_2.isChecked():

                filename, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Save as .csv", "", "CSV Files (*.csv);;All Files (*)")
                if filename:
                    df = self.profiles_advance.resample("1T").sum()
                    df.reset_index(inplace=True)
                    df.to_csv(filename, index=False)
                    print(f"Dataframe with one minute timestamp(individual) is saved as CSV file to {filename}")

    
        elif self.FifteenMinute_radioButton_2.isChecked():

                filename, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Save as .csv", "", "CSV Files (*.csv);;All Files (*)")
                if filename:
                    df = self.profiles_advance.resample("15T").sum()
                    df.reset_index(inplace=True)
                    df.to_csv(filename, index=False)
                    print(f"Dataframe with 15 minute timestamp(individual) is saved as CSV file to {filename}")

    
        elif self.Hourly_radioButton_2.isChecked():

                filename, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Save as .csv", "", "CSV Files (*.csv);;All Files (*)")
                if filename:
                    df = self.profiles_advance.resample("1H").sum()
                    df.reset_index(inplace=True)
                    df.to_csv(filename, index=False)
                    print(f"Dataframe with Hourly timestamp(individual) is saved as CSV file to {filename}")


        elif self.Daily_radioButton_2.isChecked():

                filename, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Save as .csv", "", "CSV Files (*.csv);;All Files (*)")
                if filename:
                    df = self.profiles_advance.resample("1D").sum()
                    df.reset_index(inplace=True)
                    df.to_csv(filename, index=False)
                    print(f"Dataframe with Daily timestamp(individual) is saved as CSV file to {filename}")


        elif self.Monthly_radioButton_2.isChecked():

                filename, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Save as .csv", "", "CSV Files (*.csv);;All Files (*)")
                if filename:
                    df = self.profiles_advance.resample("1M").sum()
                    df.reset_index(inplace=True)
                    df.to_csv(filename, index=False)
                    print(f"Dataframe with Monthly timestamp(individual) is saved as CSV file to {filename}")
        

                    
    def save_as_csv_advance_sum_of_users(self):
        if self.Minute_radioButton_2.isChecked():
            filename, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Save as .csv", "", "CSV Files (*.csv);;All Files (*)")
            if filename:
                df = self.profiles_advance.resample("1T").sum().sum(axis=1)
                df.to_csv(filename, index=True, index_label='Timestamp')
                print(f"Dataframe with one minute timestamp(Aggregated) is saved as CSV file to {filename}")

        elif self.FifteenMinute_radioButton_2.isChecked():
            filename, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Save as .csv", "", "CSV Files (*..csv);;All Files (*)")
            if filename:
                df = self.profiles_advance.resample("15T").sum().sum(axis=1)
                df.to_csv(filename, index=True, index_label='Timestamp')
                print(f"Dataframe with 15 minute timestamp(Aggregated) is saved as CSV file to {filename}")
                

        elif self.Hourly_radioButton_2.isChecked():
            filename, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Save as .csv", "", "CSV Files (*.csv);;All Files (*)")
            if filename:
                df = self.profiles_advance.resample("1H").sum().sum(axis=1)
                df.to_csv(filename, index=True, index_label='Timestamp')
                print(f"Dataframe with Hourly timestamp(Aggregated) is saved as CSV file to {filename}")

        elif self.Daily_radioButton_2.isChecked():
            filename, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Save as .csv", "", "CSV Files (*.csv);;All Files (*)")
            if filename:
                df = self.profiles_advance.resample("1D").sum().sum(axis=1)
                df.to_csv(filename, index=True, index_label='Timestamp')
                print(f"Dataframe with Daily timestamp(Aggregated) is saved as CSV file to {filename}")

        elif self.Monthly_radioButton_2.isChecked():
            filename, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Save as .csv", "", "CSV Files (*.csv);;All Files (*)")
            if filename:
                df = self.profiles_advance.resample("1M").sum().sum(axis=1)
                df.to_csv(filename, index=True, index_label='Timestamp')
                print(f"Dataframe with Monthly timestamp(Aggregated) is saved as CSV file to {filename}")


            
    # Tree Visulization Tab
    #
    #
    #
    
    def treeview(self, file_path):
        try:
            
        
            # Read the Excel file currently used for Simulation
            df = pd.read_excel(file_path)
    
            # Create a QStandardItemModel with additional columns
            self.model = QStandardItemModel()
            self.model.setHorizontalHeaderLabels(['User Name> Appliance> Name / Number', 'power', 'num_windows', 'func_time', 'wd_we_type'])
    
            # Initialize variables to keep track of the current parent item
            current_user_name = None
            parent_item = None
            
            
            # Mapping for wd_we_type indices to their corresponding texts
            wd_we_type_mapping = {0: 'Weekdays', 1: 'Weekends', 2: 'Whole Week'}
    
            for index, row in df.iterrows():
                user_name = str(row['user_name'])
                name = str(row['name'])
                number = str(row['number'])
                power = f'power(W)={row["power"]}'
                num_windows = f'Number of Windows={row["num_windows"]}'
                func_time = f'Function time(Minutes) = {row["func_time"]}'
                wd_we_type = f'On Which days = {row["wd_we_type"]}'
                
                
                # Retrieve text for wd_we_type index
                wd_we_type_index = row["wd_we_type"]
                wd_we_type_text = wd_we_type_mapping.get(wd_we_type_index, f'Unknown: {wd_we_type_index}')
            
                wd_we_type = f'On Which days = {wd_we_type_text}'
    
                if user_name == current_user_name:
                    # If user_name is the same, append to the existing parent item
                    child_item2 = QStandardItem(number)
                    child_item3 = QStandardItem(power)
                    child_item4 = QStandardItem(num_windows)
                    child_item5 = QStandardItem(func_time)
                    child_item6 = QStandardItem(wd_we_type)
                    child_item1 = QStandardItem(name)
                    child_item1.appendRow([child_item2, child_item3, child_item4, child_item5, child_item6])
                    parent_item.appendRow([child_item1])
                else:
                    # If user_name is different, create a new parent item
                    parent_item = QStandardItem(user_name)
                    child_item1 = QStandardItem(name)
                    child_item2 = QStandardItem(number)
                    child_item3 = QStandardItem(power)
                    child_item4 = QStandardItem(num_windows)
                    child_item5 = QStandardItem(func_time)
                    child_item6 = QStandardItem(wd_we_type)
                    child_item1.appendRow([child_item2, child_item3, child_item4, child_item5, child_item6])
    
                    parent_item.appendRow([child_item1])
                    self.model.appendRow(parent_item)
    
                    current_user_name = user_name
    
            # Create a QTreeView
            self.treeView_1.setModel(self.model)
            
            # Collapse all nodes by default
            self.treeView_1.collapseAll()
    
            font = QtGui.QFont()
            font.setPointSize(13)
            self.treeView_1.setFont(font)
            
            # Set default widt for each column manually
            column_widths = [200,200, 200, 260, 260, 260]  # Replace these values with your desired widths
        
            for column, width in enumerate(column_widths):
                self.treeView_1.setColumnWidth(column, width)
                
        except Exception as e:
            print(f"An error occurred: {e}")
    



    def __del__(self):
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()  
    sys.exit(app.exec_())



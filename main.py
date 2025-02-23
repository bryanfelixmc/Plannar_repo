from PyQt5.QtWidgets import QMainWindow, QDialog, QApplication, QWidget,QFrame, QGridLayout, QLabel, QPushButton, QGraphicsScene, QGraphicsView, QGraphicsPixmapItem, QFormLayout, QLineEdit, QWidget, QVBoxLayout, QPushButton, QWidgetItem, QTableWidget, QTableWidgetItem
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap, QColor, QCursor
from PyQt5.QtCore import Qt, QTimer
from PyQt5 import QtCore
import sys
import os
from pyautocad import Autocad, APoint
import datetime

# dentro de "inputs" se guardan los metadatos de cada imagen (bloque) de construccion!
bil=1050
all_data_instances = []  # LISTA GLOBAL PARA GUARDAR TODAS LAS INSTANCIAS


class MainUI(QMainWindow):
    def __init__(self):
        super(MainUI, self).__init__()
        loadUi("main2.ui", self)  # Load the .ui file
        self.d_horizontal = 0

        # Create a QGraphicsScene
        self.scene = QGraphicsScene()
        # Assuming graphicsView is already set in the UI file
        # Set the scene for the existing graphicsView in the UI
        self.graphicsView.setScene(self.scene)
        # Create an instance of MyGraphicsView
        # If you want to replace the existing graphicsView with MyGraphicsView, you should do it like this:
        self.graphicsView = MyGraphicsView(self, self.scene)
        # If you want to keep the original graphicsView and just enhance it, you can skip creating a new instance
        # self.graphicsView = MyGraphicsView(self, self.scene)  # This line is not needed if you are using the existing graphicsView
        # Optionally, you can add items to the scene here
        # self.scene.addItem(...)

        # Connect buttons to their respective methods
        self.button01.clicked.connect(self.add_images)
        self.button02.clicked.connect(self.print_all_data_instances)
        self.button03.clicked.connect(self.some_functionality_3)
        self.button04.clicked.connect(self.cad_plot)
        #self.button04.clicked.connect(self.start_progress)

        # Initialize tables
        #self.table03.setRowCount(0)
        #self.table03.setColumnCount(2)
        #self.table03.setHorizontalHeaderLabels(["Key", "Value"])

        #self.table04.setRowCount(1)
        #self.table04.setColumnCount(2)
        #self.table04.setHorizontalHeaderLabels(["X", "Y"])
        

        #self.graphics_view = MyGraphicsView(self, self.scene)
        #self.graphics_view.setScene(self.scene)

        #Progress value
        self.progress_value = 0
        # Timer for updating the progress bar
        self.timer = QTimer()
        

        #menubar(QMenuBar)>menuInicio(QMenu)>actionParametros_generales(QAction)
        # Example dictionary to populate the form
        self.some_dictionary = {
            "Parameter 1": "Value 1",
            "Parameter 2": "Value 2",
            "Parameter 3": "Value 3"
        }
        # Connect the action to the method
        self.actionParametros_generales.triggered.connect(self.show_parametros_generales)

    def add_images(self):
        image_path = str(os.getcwd()) + "\\SB_LINEA_PROY"
        #("image_name", x_position, y_position, inputs, block_type)
        self.images = [
            ("LL__LINEA_PROY.jpg", self.d_horizontal, 40, {"Carga (MW)": 0, "Nombre": 0, "Codigo de Linea": 0}, "_"),
            ("PR__LINEA_PROY.jpg", self.d_horizontal, 80, {"Tension nominal (kV)": 0, "BIL (kVp)": bil, "I nominal (A)": 0, "Clase": 0}, "Pararrayos c-cd"),
            ("TTC_LINEA_PROY.jpg", self.d_horizontal, 120, {"Tension nominal (kV)": 0, "BIL (kVp)": bil, "Clase de Proteccion": 0, "Tipo": 0}, "TTB-1"),
            ("SL__LINEA_PROY.jpg", self.d_horizontal, 160, {"Tension nominal (kV)": 0, "BIL (kVp)": bil, "I nominal (A)": 0, "Tipo": 0}, "SL_AT_AV_DOWN"),
            ("TC__LINEA_PROY.jpg", self.d_horizontal, 200, {"Tension nominal (kV)": 0, "BIL (kVp)": bil, "I nominal (A)": 0, "Tipo": 0, "Relacion devanado primario": 0, "Relacion devanado secundario": 0, "Burden": 0}, "_"),
            ("IP__LINEA_PROY.jpg", self.d_horizontal, 240, {"Tension nominal (kV)": 0, "BIL (kVp)": bil, "I nominal (A)": 0}, "_"),
            ("SB__LINEA_PROY.jpg", self.d_horizontal, 280, {"Tension nominal (kV)": 0, "BIL (kVp)": bil, "I nominal (A)": 0, "Tipo": 0}, "_"),
        ]

        for image in self.images:
            pixmap = QPixmap(os.path.join(image_path, image[0]))
            pixmap = pixmap.scaled(85, 40)
            inputs = image[3]
            image_widget = ImageWidget(os.path.join(image_path, image[0]), inputs,self) # Pass the current instance of MainUI 
            image_widget.setPixmap(pixmap)
            self.scene.addItem(image_widget)
            image_widget.setPos(image[1], image[2])# Set the image position
            #image_widget.data = {key: "0" for key in image_widget.inputs.keys()} #agregado por BMC
            all_data_instances.append(image)  # Store the data instance globally  BMC  La palabra que se cambio fue data, por inputs... al final inputs contiene el diccionario  de cada imagen
        self.d_horizontal += 85   
    
    def some_functionality_2(self):
        # Placeholder for additional functionality
        pass

    def some_functionality_3(self):
        # Placeholder for additional functionality
        pass

    def cad_plot(self):
        self.button04.setEnabled(False)  # Disable the plot button
        try:
            ## INIICIA TIMER ##
            self.start_progress()
            self.progress_value = 0
            total_instances = len(all_data_instances)
            self.timer.start(100)  # Start the timer


            #Instanciar applicacion de pyautocad
            acad = Autocad(create_if_not_exists=True, visible=True)
            #Para obtener el listado de  bloques de forma automatica:
            lib_objetos=acad.doc.blocks
            listado = [elem.name for elem in lib_objetos]  # Ahora listado son los nombres de los bloques , es decir:         #lista_bloques=["BASE", "TTB-1", "TTB-2", "TTB-3", "MMOT", "TTS-1", "TTS-2", "TTS-3", "TCF-1", "TCF-2", "TCF-3", "DS", "TCT", "TCF-4", "BASE_TERMINACIÓN", "BASE_ACOPLE_BAJADA", "BASE_ACOPLE_SUBIDA", "BASE_MEDICION", "TTCM-1", "TTCM-2", "TTCM-3", "TC_GE_245_1050", "BASE_C_A_FT", "DS_A", "DS_CA", "TTS_CA_3", "TTS_CA_2", "TTS_CA_1", "TCF_CA_1", "TCF_CA_2", "TCF_CA_3", "TCF_CA_4", "BASE_C_A_TERMINACION", "BASE_C_A_ACOPLE_BAJADA", "BASE_C_A_ACOPLE_SUBIDA", "TTB_C_A_3", "TTB_C_A_1", "TTB_C_A_2", "BASE_C_A_MEDICION", "BASE_C_A_SALIDA_DIRECTA", "BASE_C_A_SSAA", "DS_AT_CD", "TTC_AT_2S", "TTC_AT_3S", "SL_AT", "IP_AT", "TO_AT", "SL_AT_DA", "SL_AT_AC", "SL_AT_AV", "SB_AT_DA", "SB_AT_AC", "SB_AT_AV", "SB_AT_P", "CT_AT_3S", "CT_AT_4S", "CT_AT_5S", "CT_AT_6S", "BASE_2B_UP", "TTI_2B_2S", "TTI_AT_2S", "TTI_AT_3S", "TTC_AT_1S", "TTI_AT_1S", "BASE_AT_ACOPLE_2B", "BASE_2B_DOWN", "DS_AT_CD_DOWN", "TTC_AT_1S_DOWN", "TTC_AT_2S_DOWN", "TTC_AT_3S_DOWN", "TTI_AT_1S_DOWN", "TTI_AT_2S_DOWN", "TTI_AT_3S_DOWN", "TO_AT_DONW", "SL_AT_DA_DOWN", "SL_AT_AC_DOWN", "SL_AT_AV_DOWN", "CT_AT_3S_DOWN", "CT_AT_4S_DOWN", "CT_AT_5S_DOWN", "CT_AT_6S_DOWN", "IP_AT_DOWN", "SB_AT_DA_DONW", "SB_AT_DA_DOWN", "SB_AT_AC_DOWN", "SB_AT_AV_DOWN", "SB_AT_P_DOWN", "BASE_AT_ACOPLE_2B_DOWN", "TO_AT_DOWN", "raiz de 3", "TERMINAL", "INTERRUPTOR", "Trafo tension", "Pararrayos c-cd", "SB 220", "BASE_2B_TRANSFORMACION_DOWN"]
            #Insertar cada bloque que corresponda en el lugar que corresponda segun la distribucion de cada bahia
            #ip = APoint(0, 0, 0)

            #block_name = "CT_AT_3S"
            for instance in all_data_instances:
                # Unpack the tuple directly
                image_name, x_position, y_position, inputs, block_type = instance
                
                for block_name in listado:
                    if block_name == block_type:  # Compare with block_type directly
                        # Insert the block into AutoCAD
                        block_ref1 = acad.model.InsertBlock(APoint(x_position, y_position, 0), block_name, 1, 1, 1, 0)
                        # Add text to the block
                        texto_ref1 = acad.model.AddMText(APoint(x_position, y_position, 0), 10, image_name) 
                self.progress_value += (1/total_instances)*100  # Increment progress value
                self.update_progress()  # Update the progress bar
            #Guardar Documento
            #path1="C:\\Users\\BMALPARTIDA\\Downloads\\Nueva carpeta\\Drawings\\"
            #file1="drawing1.dwg"
            #acad.doc.SaveAs(path1+now.strftime("%Y.%m.%d_%H.%M.%S")+"_copy_of_"+file1)

        finally:
            self.timer.stop()
            self.button04.setEnabled(True)  # Enable the plot button again

    ##########   BAR PROGRESS ###############
    def start_progress(self):
        self.progress_value = 0
        self.progressBar.setValue(self.progress_value)
    def update_progress(self):
        self.progressBar.setValue(self.progress_value)
    ##########   END OF BAR PROGRESS ###############   

    def print_all_data_instances(self):
        if not all_data_instances:
            print("No data instances available.")
        else:
            print("All Data Instances:")
            for index, data_instance in enumerate(all_data_instances):
                print(f"Instance {index + 1}: {data_instance}")

    def show_parametros_generales(self):
        """Show the ParametrosGenerales form."""
        self.parametros_widget = ParametrosGenerales(self.some_dictionary, self)
        self.parametros_widget.setWindowTitle("General Parameters")  # Set the window title
        self.parametros_widget.resize(400, 300)  # Set the size of the form
        self.parametros_widget.exec_()  # Show the dialog as a modal dialog



class ImageWidget(QGraphicsPixmapItem):
    def __init__(self, image_path, inputs, main_ui,*args, **kwargs):
        super(ImageWidget,self).__init__(*args, **kwargs)
        self.main_ui = main_ui  # Store reference to MainUI
        self.inputs = inputs
        self.pixmap = QPixmap(image_path)
        self.setPixmap(self.pixmap)
        # Initialize form widget and layout
        self.form_widget = QWidget()
        self.form_layout = QFormLayout()
        self.form_widget.setLayout(self.form_layout)
        
        #self.save_button = QPushButton("Save")
        #self.save_button.clicked.connect(self.save_data)
        #self.form_layout.addRow(self.save_button)
        #self.form_widget.hide()

        # Initialize data storage
        self.data = {}

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.set_form_inputs()
            self.form_widget.show()
        elif event.button() == Qt.LeftButton:
            self.show_data()

    def set_form_inputs(self):
        # Clear existing widgets in the form layout
        self.clear_form_layout()

        # Retrieve data from table03 and populate self.inputs
        for key, value in self.inputs.items():
            label = QLabel(key)
            line_edit = QLineEdit()
            line_edit.setText(str(value))
            self.form_layout.addRow(label, line_edit)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_data)
        self.form_layout.addRow(self.save_button)

    def clear_form_layout(self):
        """Clear all widgets from the form layout."""
        while self.form_layout.count():
            child = self.form_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def save_data(self):
        #self.data = {}
        for i in range(self.form_layout.count()):
            row = self.form_layout.itemAt(i)
            if isinstance(row, QWidgetItem):
                widget = row.widget()
                if isinstance(widget, QLineEdit):
                    label = self.form_layout.labelForField(widget)
                    self.data[label.text()] = widget.text()
        self.form_widget.hide()
        self.show_data()
        #all_data_instances.append(self.data)

    def show_data(self):
        main_window = self.scene().views()[0].parent().window()
        table_widget = main_window.table03
        table_widget.setRowCount(len(self.inputs))
        table_widget.setColumnCount(2)
        table_widget.setHorizontalHeaderLabels(["Key", "Value"])

        row = 0
        for key, value in self.inputs.items():
            if key in self.data:
                value = self.data[key]
            table_widget.setItem(row, 0, QTableWidgetItem(key))
            table_widget.setItem(row, 1, QTableWidgetItem(str(value)))
            row += 1

class MyGraphicsView(QGraphicsView):
    def __init__(self, parent, scene, *args, **kwargs):
        super(MyGraphicsView, self).__init__(scene, *args, **kwargs)
        self.parent_window = parent
        self.setMouseTracking(True)

    def mouseMoveEvent(self, event):
        x = event.pos().x()
        y = event.pos().y()
        self.parent_window.table04.setItem(0, 0, QTableWidgetItem(str(x)))
        self.parent_window.table04.setItem(0, 1, QTableWidgetItem(str(y)))
        super(MyGraphicsView, self).mouseMoveEvent(event)

class ParametrosGenerales(QDialog):
    def __init__(self, some_dictionary, parent=None):
        super(ParametrosGenerales, self).__init__(parent)
        self.some_dictionary = some_dictionary  # Dictionary to populate the form
        self.form_layout = QFormLayout()
        self.setLayout(self.form_layout)

        # Populate the form with data from some_dictionary
        self.populate_form()

        # Add a save button
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_data_as_dictionary)
        self.form_layout.addRow(self.save_button)

    def populate_form(self):
        """Populate the form with data from some_dictionary."""
        for key, value in self.some_dictionary.items():
            label = QLabel(key)
            line_edit = QLineEdit()
            line_edit.setText(str(value))
            self.form_layout.addRow(label, line_edit)

    def save_data_as_dictionary(self):
        """Save data from the form inputs to a dictionary."""
        saved_data = {}
        for i in range(self.form_layout.count()):
            row = self.form_layout.itemAt(i)
            if isinstance(row, QWidgetItem):
                widget = row.widget()
                if isinstance(widget, QLineEdit):
                    label = self.form_layout.labelForField(widget)
                    saved_data[label.text()] = widget.text()
        
        # Handle the saved_data as needed
        print("Saved Data:", saved_data)  # For demonstration purposes
        self.accept()  # Close the dialog after saving

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = MainUI()
    ui.show()
    sys.exit(app.exec_())
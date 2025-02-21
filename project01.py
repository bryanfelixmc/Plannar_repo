import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFrame, QGridLayout, QLabel, QPushButton, QGraphicsScene, QGraphicsView, QGraphicsPixmapItem, QFormLayout, QLineEdit, QWidget, QVBoxLayout, QPushButton, QWidgetItem, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QColor, QPixmap, QCursor
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
import os
from pyautocad import Autocad, APoint, aDouble
import datetime

# dentro de "inputs" se guardan los metadatos de cada imagen (bloque) de construccion!

bil=1050
all_data_instances = []  # LISTA GLOBAL PARA GUARDAR TODAS LAS INSTANCIAS
class ImageWidget(QGraphicsPixmapItem):
    def __init__(self, image_path, inputs, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.inputs = inputs #Aqui se esta guardando los diccionarios de cada 
        self.pixmap = QPixmap(image_path)  #para escalar imagenes
        self.setPixmap(self.pixmap)  #para escalar imagenes
        self.form_widget = QWidget()
        self.form_layout = QFormLayout()
        self.form_widget.setLayout(self.form_layout)
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_data)
        self.form_layout.addRow(self.save_button)
        self.form_widget.hide()
        self.data = {} # La variable "data" solo funciona para almacenar datos temporales

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.set_form_inputs()
            self.form_widget.show()
        elif event.button() == Qt.LeftButton:
            self.show_data()

    def set_form_inputs(self):
        while self.form_layout.count():
            child = self.form_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        for key, value in self.inputs.items():
            label = QLabel(key)
            line_edit = QLineEdit()
            if key in self.data:
                line_edit.setText(self.data[key])
            else:
                line_edit.setText(str(value))
            self.form_layout.addRow(label, line_edit)
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_data)
        self.form_layout.addRow(self.save_button)

    def save_data(self):
        self.data = {}
        for i in range(self.form_layout.count()):
            row = self.form_layout.itemAt(i)
            if isinstance(row, QWidgetItem):
                widget = row.widget()
                if isinstance(widget, QLineEdit):
                    label = self.form_layout.labelForField(widget)
                    self.data[label.text()] = widget.text()
        self.form_widget.hide()
        self.show_data()
        # Append the current data to the global list
        all_data_instances.append(self.data)  # Store the data instance globally

    def show_data(self):
        # Get the main window
        main_window = self.scene().views()[0].parent().window()

        # Create a table widget
        table_widget = main_window.table03
        table_widget.setRowCount(len(self.inputs))
        table_widget.setColumnCount(2)
        table_widget.setHorizontalHeaderLabels(["Key", "Value"])

        # Populate the table
        row = 0
        for key, value in self.inputs.items():
            if key in self.data:
                value = self.data[key]
            table_widget.setItem(row, 0, QTableWidgetItem(key))
            table_widget.setItem(row, 1, QTableWidgetItem(str(value)))
            row += 1

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, 900, 700) # x, y, width, height
        self.setWindowTitle('Subestaciones')
        self.setStyleSheet("background-color: rgba(221, 243, 243, 1);")



        # Create a main layout
        mainLayout = QGridLayout()
        self.setLayout(mainLayout)

        # Create frames
        self.frame01 = QFrame()
        self.frame01.setStyleSheet("background-color: rgba(255, 255, 255, 1); border: 1px solid lightgreen;")
        frame01Layout = QGridLayout()
        self.frame01.setLayout(frame01Layout)

        # Add buttons to frame01
        buttons = [
            "Bahía de Linea", "button02",
            "button03", "button04",
            "button05", "button06",
            "button07", "button08",
            "button09", "Plot"
        ]
        self.d_horizontal = 0
        row_val = 0
        col_val = 0
        self.x=[]
      
        for button in buttons:
            btn = QPushButton(button)
            btn.setStyleSheet("background-color: rgba(24, 242, 213, 1);")
            btn.setFlat(False)  # This will make the button raised
            btn.setMinimumHeight(50)
            
            if button == "Bahía de Linea":
                btn.clicked.connect(self.add_images)
            if button == "Plot":
                btn.clicked.connect(self.cad_plot)
                self.plot_button=btn # Aqui se guarda el boton plot para luego restringir su uso mientras autocad esta trabajando, ver: def cad_plot(self)


            if button == "button09":

                btn.clicked.connect(self.print_all_data_instances)  #BMC

            frame01Layout.addWidget(btn, row_val, col_val)
            col_val += 1
            if col_val > 1:
                col_val = 0
                row_val += 1

        self.frame02 = QFrame()
        self.frame02.setStyleSheet("background-color: rgba(255, 255, 255, 1); border: 1px dotted green;")
        self.scene = QGraphicsScene()
        self.graphics_view = MyGraphicsView(self, self.scene)
        self.graphics_view.setScene(self.scene)
        frame02Layout = QGridLayout()
        self.frame02.setLayout(frame02Layout)
        frame02Layout.addWidget(self.graphics_view)

        self.table03 = QTableWidget()
        self.table03.setStyleSheet("background-color: rgba(255, 255, 255, 1); border: 1px solid red;")
        self.table03.setRowCount(0)
        self.table03.setColumnCount(2)
        self.table03.setHorizontalHeaderLabels(["Key", "Value"])

        self.frame03 = QFrame()
        self.frame03.setStyleSheet("background-color: rgba(255, 255, 255, 1); border: 1px solid red;")
        frame03Layout = QGridLayout()
        self.frame03.setLayout(frame03Layout)
        frame03Layout.addWidget(self.table03)

        self.frame04 = QFrame()
        self.frame04.setStyleSheet("background-color: rgba(255, 255, 255, 1); border: 1px solid yellow;")
        frame04Layout = QGridLayout()
        self.frame04.setLayout(frame04Layout)

        # Creating a X Y Tracker to visualize the mouse pointer
        self.table04 = QTableWidget()
        self.table04.setRowCount(1)
        self.table04.setColumnCount(2)
        self.table04.setHorizontalHeaderLabels(["X", "Y"])
        frame04Layout.addWidget(self.table04)

        mainLayout.addWidget(self.frame01, 0, 0, 2, 1)
        mainLayout.addWidget(self.frame02, 0, 1, 2, 1)
        mainLayout.addWidget(self.frame03, 0, 2, 1 ,1)
        mainLayout.addWidget(self.frame04, 1, 2, 1, 1)

        # Set relative width for column 2
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 3)
        mainLayout.setColumnStretch(2, 1)
        mainLayout.setRowStretch(0, 1)
        mainLayout.setRowStretch(1, 1)

    def add_images(self):
        
        image_path = str(os.getcwd()) + "\\SB_LINEA_PROY"
        self.images = [
            ("LL__LINEA_PROY.jpg", self.d_horizontal, 40, {"Carga (MW)": 0, "Nombre": 0, "Codigo de Linea": 0},""),
            ("PR__LINEA_PROY.jpg", self.d_horizontal, 80, {"Tension nominal (kV)": 0, "BIL (kVp)": bil, "I nominal (A)": 0, "Clase": 0},"Pararrayos c-cd"),
            ("TTC_LINEA_PROY.jpg", self.d_horizontal, 120, {"Tension nominal (kV)": 0, "BIL (kVp)": bil, "Clase de Proteccion": 0, "Tipo": 0},"TTB-1"),
            ("SL__LINEA_PROY.jpg", self.d_horizontal, 160, {"Tension nominal (kV)": 0, "BIL (kVp)": bil, "I nominal (A)": 0, "Tipo": 0},"SL_AT_AV_DOWN"),
            ("TC__LINEA_PROY.jpg", self.d_horizontal, 200, {"Tension nominal (kV)": 0, "BIL (kVp)": bil, "I nominal (A)": 0, "Tipo": 0, "Relacion devanado primario": 0, "Relacion devanado secundario": 0, "Burden": 0},""),
            ("IP__LINEA_PROY.jpg", self.d_horizontal, 240, {"Tension nominal (kV)": 0, "BIL (kVp)": bil, "I nominal (A)": 0},""),
            ("SB__LINEA_PROY.jpg", self.d_horizontal, 280, {"Tension nominal (kV)": 0, "BIL (kVp)": bil, "I nominal (A)": 0, "Tipo": 0},""), 
        ]
        
        for image in self.images:
            pixmap = QPixmap(os.path.join(image_path, image[0]))  #para escalar imagenes
            pixmap = pixmap.scaled(85, 40)  # Set the image size  #para escalar imagenes
            inputs = image[3]
            image_widget = ImageWidget(os.path.join(image_path, image[0]), inputs)
            image_widget.setPixmap(pixmap)  #para escalar imagenes
            self.scene.addItem(image_widget)
            image_widget.setPos(image[1], image[2])  # Set the image position
            #image_widget.data = {key: "0" for key in image_widget.inputs.keys()} #agregado por BMC
            all_data_instances.append(image)  # Store the data instance globally  BMC  La palabra que se cambio fue data, por inputs... al final inputs contiene el diccionario  de cada imagen
            
        self.d_horizontal += 85   


    def print_all_data_instances(self):   #BMC
        if not all_data_instances:
            print("No data instances available.")
        else:
            print("All Data Instances:")
            for index, data_instance in enumerate(all_data_instances):
                print(f"Instance {index + 1}: {data_instance}")
            

    
    def cad_plot(self):
        self.plot_button.setEnabled(False)  # Disable the plot button
        try:
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
                    
            #Guardar Documento
            #path1="C:\\Users\\BMALPARTIDA\\Downloads\\Nueva carpeta\\Drawings\\"
            #file1="drawing1.dwg"
            #acad.doc.SaveAs(path1+now.strftime("%Y.%m.%d_%H.%M.%S")+"_copy_of_"+file1)

        finally:
            self.plot_button.setEnabled(True)  # Enable the plot button again


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
        super().mouseMoveEvent(event)

class DataPrinter:
    def __init__(self, data):
        self.data = data

    def print_data(self):
        if not self.data:
            print("No data available.")
            return
        
        print("Data Contents:")
        for key, value in self.data.items():
            print(f"{key}: {value}")

"""# Example usage
# Assuming you have an instance of ImageWidget
image_widget_instance = ImageWidget("path/to/image.jpg", {"Carga (MW)": 0, "Nombre": 0, "Codigo de Linea": 0})

# Simulating user input for demonstration
image_widget_instance.data = {
    "Carga (MW)": "100",
    "Nombre": "Transformador A",
    "Codigo de Linea": "TL-001"
}

# Create an instance of DataPrinter and print the data
data_printer = DataPrinter(image_widget_instance.data)
data_printer.print_data()"""

def main():
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
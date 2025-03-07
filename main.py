from PyQt5.QtWidgets import QMainWindow, QGraphicsItem, QDialog, QApplication, QWidget, QLabel, QPushButton, QGraphicsScene, QGraphicsPixmapItem, QFormLayout, QLineEdit, QWidget, QWidgetItem, QTableWidgetItem, QGraphicsView, QTableWidget,QVBoxLayout
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap, QTransform #SVC
from PyQt5.QtCore import Qt, QTimer
import sys
import os
from pyautocad import Autocad, APoint
import pandas as pd

class CADInstance:
    all_instances = []  # Class variable to store all CAD instances

    def __init__(self, image_name, x_position, y_position, inputs, block_type):
        self.image_name = image_name
        self.x_position = x_position
        self.y_position = y_position
        self.inputs = inputs
        self.block_type = block_type
        
        # Check for duplicates before appending
        if not self.is_duplicate():
            CADInstance.all_instances.append(self)  # Store instance in class variable
        else:
            print(f"Duplicate instance not added: {self}")

    def is_duplicate(self):
        """Check if an instance with the same attributes already exists."""
        for instance in CADInstance.all_instances:
            if (instance.image_name == self.image_name and
                instance.x_position == self.x_position and
                instance.y_position == self.y_position and
                instance.block_type == self.block_type and
                self.inputs == instance.inputs):  # Compare as dictionaries
                print(f"Duplicate found: {instance} with attributes: "
                    f"Image Name: {instance.image_name}, "
                    f"X Position: {instance.x_position}, "
                    f"Y Position: {instance.y_position}, "
                    f"Inputs: {instance.inputs}, "
                    f"Block Type: {instance.block_type}")
                return True
        return False

class MainUI(QMainWindow):
    def __init__(self):
        super(MainUI, self).__init__()

        loadUi("main.ui", self)  # Load the .ui file
        self.d_horizontal = 0
        self.progress_value = 0
        self.timer = QTimer()


        # Buscar la tabla de posiciones en main.ui      #MDELACRUZ
        self.position_table = self.findChild(QTableWidget, "table04")           #MDELACRUZ
        if not self.position_table:          #MDELACRUZ
            print("Error: No se encontró 'tabla04' en main.ui. Verifica el nombre en Qt Designer.") 
        else:  #MDELACRUZ
            print("Tabla de posiciones encontrada correctamente.")


        # Initialize images variations
        self.images_variations = self.initialize_images_variations()

        # Create a QGraphicsScene
        self.scene = QGraphicsScene()
        self.graphicsView.setScene(self.scene)  # Use the existing graphicsView

        # Invertir el eje Y del QGraphicsView            #SVC
        transform = QTransform()                             #SVC
        transform.scale(1, -1)  # Invertir el eje Y             #SVC
        self.graphicsView.setTransform(transform)             #SVC

        # Enable mouse tracking
        self.graphicsView.setMouseTracking(True)
        
        # Connect buttons to their respective methods
        self.button01.clicked.connect(lambda: self.add_images(self.images_variations[0]))
        self.button05.clicked.connect(lambda: self.add_images(self.images_variations[1]))
        self.button06.clicked.connect(lambda: self.add_images(self.images_variations[2]))
        self.button02.clicked.connect(self.print_all_data_instances)
        self.button04.clicked.connect(self.cad_plot)
        # Boton para limpiar el dibujo                          #MDELACRUZ
        self.borrar.clicked.connect(self.limpiar_dibujo)         #MDELACRUZ
        

        # Connect menu action
        self.actionParametros_generales.triggered.connect(self.show_parametros_generales)

        # Inicializar el nivel de zoom             #SVC
        self.zoom_level = 1.0             #SVC

        # Conectar el evento de la rueda del mouse             #SVC
        self.graphicsView.wheelEvent = self.wheelEvent             #SVC

        
    def wheelEvent(self, event):             #SVC
        """Manejar el evento de la rueda del mouse para hacer zoom."""
        # Determinar la dirección del scroll
        if event.angleDelta().y() > 0:  # Scroll hacia arriba
            self.zoom(1.2)  # Aumentar el zoom
        else:  # Scroll hacia abajo
            self.zoom(0.8)  # Disminuir el zoom

    def zoom(self, factor):             #SVC
        """Aplicar el factor de zoom al QGraphicsView."""
        self.zoom_level *= factor
        self.zoom_level = min(max(self.zoom_level, 1.0), 4.0)  # Limitar el zoom entre 1.0 y 4.0

        # Aplicar la transformación de zoom
        transform = QTransform()
        transform.scale(self.zoom_level, self.zoom_level)
        transform.scale(1, -1)  # Invertir el eje Y
        self.graphicsView.setTransform(transform)


        

    def initialize_images_variations(self):             #SVC
        bil = 1050
        return [
            # Variation 1
            [
                ["LL__LINEA_PROY_DWN.jpg", 0, 280+280, {"Carga (MW)": 0, "Nombre": 0, "Codigo de Linea": 0}, "SALIDA_LINEA"],
                ["PR__LINEA_PROY.jpg", 0, 280+240, {"Tension nominal (kV)": 0, "BIL (kVp)": bil, "I nominal (A)": 0, "Clase": 0}, "Pararrayos c-cd1"],
                ["TTC_LINEA_PROY.jpg", 0, 280+200, {"Tension nominal (kV)": 0, "BIL (kVp)": bil, "Clase de Proteccion": 0, "Tipo": 0}, "TTC_AT_2S"],
                ["SL__LINEA_PROY.jpg", 0, 280+160, {"Tension nominal (kV)": 0, "BIL (kVp)": bil, "I nominal (A)": 0, "Tipo": 0}, "SL_AT_AV_DOWN1"],
                ["TC__LINEA_PROY.jpg", 0, 280+120, {"Tension nominal (kV)": 0, "BIL (kVp)": bil, "I nominal (A)": 0, "Tipo": 0, "Relacion devanado primario": 0, "Relacion devanado secundario": 0, "Burden": 0}, "CT_AT_4S"],
                ["IP__LINEA_PROY.jpg", 0, 280+80, {"Tension nominal (kV)": 0, "BIL (kVp)": bil, "I nominal (A)": 0}, "IP_AT"],
                ["SB__LINEA_PROY_DWN.jpg", 0, 280+40, {"Tension nominal (kV)": 0, "BIL (kVp)": bil, "I nominal (A)": 0, "Tipo": 0}, "SB_AT_AC"],
            ],

            # Variation 2

            [
                ["LL__LINEA_PROY.jpg", 0, 40, {"Carga (MW)": 0, "Nombre": 0, "Codigo de Linea": 0}, "SALIDA_LINEA_DWN"],
                ["PR__LINEA_PROY.jpg", 0, 80, {"Tension nominal (kV)": 0, "BIL (kVp)": bil, "I nominal (A)": 0, "Clase": 0,}, "Pararrayos c-cd1"],
                ["TTC_LINEA_PROY.jpg", 0, 120, {"Tension nominal (kV)": 0, "BIL (kVp)": bil, "Clase de Proteccion": 0, "Tipo": 0}, "TTC_AT_2S"],
                ["SL__LINEA_PROY.jpg", 0, 160, {"Tension nominal (kV)": 0, "BIL (kVp)": bil, "I nominal (A)": 0, "Tipo": 0}, "SL_AT_AV_DOWN2"],
                ["TC__LINEA_PROY.jpg", 0, 200, {"Tension nominal (kV)": 0, "BIL (kVp)": bil, "I nominal (A)": 0, "Tipo": 0, "Relacion devanado primario": 0, "Relacion devanado secundario": 0, "Burden": 0}, "CT_AT_4S_DOWN"],
                ["IP__LINEA_PROY.jpg", 0, 240, {"Tension nominal (kV)": 0, "BIL (kVp)": bil, "I nominal (A)": 0}, "IP_AT_DOWN"],
                ["SB__LINEA_PROY.jpg", 0, 280, {"Tension nominal (kV)": 0, "BIL (kVp)": bil, "I nominal (A)": 0, "Tipo": 0}, "SB_AT_AC_DOWN"],
            ],

            # Variation 3
            [
                ["LL__LINEA_PROY.jpg", 0, 40, {"Carga (MW)": 0, "Nombre": 0, "Codigo de Linea": 0}, "-"],
                ["PR__LINEA_PROY.jpg", 0, 100, {"Tension nominal (kV)": 0, "BIL (kVp)": bil, "I nominal (A)": 0, "Clase": 0}, "Pararrayos c-cd1"],
                ["TTC_LINEA_PROY.jpg", 0, 160, {"Tension nominal (kV)": 0, "BIL (kVp)": bil, "Clase de Proteccion": 0, "Tipo": 0}, "TTB-1"],
                ["SL__LINEA_PROY.jpg", 0, 220, {"Tension nominal (kV)": 0, "BIL (kVp)": bil, "I nominal (A)": 0, "Tipo": 0}, "SL_AT_AV_DOWN"],
                ["TC__LINEA_PROY.jpg", 0, 280, {"Tension nominal (kV)": 0, "BIL (kVp)": bil, "I nominal (A)": 0, "Tipo": 0, "Relacion devanado primario": 0, "Relacion devanado secundario": 0, "Burden": 0}, "_"],
                ["IP__LINEA_PROY.jpg", 0, 340, {"Tension nominal (kV)": 0, "BIL (kVp)": bil, "I nominal (A)": 0}, "_"],
                ["SB__LINEA_PROY.jpg", 0, 400, {"Tension nominal (kV)": 0, "BIL (kVp)": bil, "I nominal (A)": 0, "Tipo": 0}, "_"],
            ]
        ]


    def add_images(self, images):
        image_path = os.path.join(os.getcwd(), "SB_LINEA_PROY")

        for image in images:
            image_name, _, y_position, inputs, block_type = image
            
           
            try:
                pixmap = QPixmap(os.path.join(image_path, image_name)).scaled(85, 40)
                image_widget = ImageWidget(
                    image_path=os.path.join(image_path, image_name),
                    inputs=inputs,
                    main_ui=self,
                    x=self.d_horizontal,
                    y=y_position,
                    block_type=block_type
                )
                image_widget.setPixmap(pixmap)
                image_widget.setPos(self.d_horizontal, y_position)
                self.scene.addItem(image_widget)
            

                # Create a CADInstance and it will be stored in the class variable
                CADInstance(image_name, self.d_horizontal, y_position, inputs, block_type)

            except Exception as e:
                print(f"Error loading image {image_name}: {e}")
        self.d_horizontal += 85  # Update d_horizontal for the next image

    def cad_plot(self):
        self.clear_autocad()  # Limpiar AutoCAD antes de dibujar  #MDELACRUZ
        self.button04.setEnabled(False)  # Disable the plot button
        try:
            self.start_progress()
            total_instances = len(CADInstance.all_instances)  # Use class variable
            self.timer.start(100)  # Start the timer

            acad = Autocad(create_if_not_exists=True, visible=True)
            lib_objetos = acad.doc.blocks
            listado = [elem.name for elem in lib_objetos]

            for instance in CADInstance.all_instances:  # Use class variable
                block_name = instance.block_type
                if block_name in listado:
                    acad.model.InsertBlock(APoint(instance.x_position, instance.y_position, 0), block_name, 1, 1, 1, 0)
                    acad.model.AddMText(APoint(instance.x_position+30, instance.y_position+5, 0), 10, instance.image_name)             #SVC

                bil_value = instance.inputs.get('BIL (kVp)', 'NULL')  # Use 'N/A' or any default value if the key doesn't exist
                vol_value = instance.inputs.get('Tension nominal (kV)', 'NULL')
                corr_value = instance.inputs.get('I nominal (A)', 'NULL')

                values_to_print = []
                if bil_value != 'NULL':
                    values_to_print.append(f"{bil_value}"+ "kVp")
                if vol_value != 'NULL' and corr_value != 'NULL':
                    values_to_print.append(f"{vol_value}kV,{corr_value}A")
                elif vol_value != 'NULL':
                    values_to_print.append(f"{vol_value} kV")
                elif corr_value != 'NULL':
                    values_to_print.append(f"{corr_value} A")

                # Join the values with a comma and space
                if values_to_print:
                    acad.model.AddMText(APoint(instance.x_position + 30, instance.y_position - 5, 0), 10, " ".join(values_to_print))

                    """
                   # Check if 'BIL (kVp)' exists in inputs before accessing it             #SVC
                    bil_value = instance.inputs.get('BIL (kVp)', 'NULL')  # Use 'N/A' or any default value if the key doesn't exist            #SVC
                    acad.model.AddMText(APoint(instance.x_position + 30, instance.y_position -5 , 0), 10, bil_value)         #SVC
                    """

                self.progress_value += (1 / total_instances) * 100
                self.update_progress()

        finally:
            self.timer.stop()
            self.button04.setEnabled(True)  # Enable the plot button again

    def start_progress(self):
        self.progress_value = 1
        self.progressBar.setValue(int(self.progress_value))

    def update_progress(self):
        self.progressBar.setValue(int(self.progress_value))

    def print_all_data_instances(self):
        if not CADInstance.all_instances:  # Use class variable
            print("No data instances available.")
        else:
            # Create a list of dictionaries to hold the data
            data = []
            for index, instance in enumerate(CADInstance.all_instances):  # Use class variable
                data.append({
                    "id": index + 1,
                    "Image Name": instance.image_name,
                    "X": instance.x_position,
                    "Y": instance.y_position,
                    "Inputs": instance.inputs,
                    "Block Type": instance.block_type
                })
            
            # Configure display options
            pd.set_option("display.max_columns", None)  # Show all columns
            pd.set_option("display.max_rows", None)     # Show all rows
            pd.set_option('display.width', None)        # Auto-detect terminal width
            #pd.set_option('display.max_colwidth', None) # Show full column content

            # Create a DataFrame from the data
            df = pd.DataFrame(data)
            # Print the DataFrame as a table
            print(df)#.to_string(index=False))  # Use to_string to format the output nicely

    def update_position_table(self, x, y):  #MDELACRUZ
        """Actualiza table04 con las coordenadas X e Y del bloque seleccionado"""
        if not self.position_table:  #MDELACRUZ
            print("No se puede actualizar porque la tabla no fue encontrada.")
            return

        self.position_table.setRowCount(2)  # Solo dos filas: X e Y  #MDELACRUZ
        self.position_table.setColumnCount(2)  #MDELACRUZ
       

        # Agregar valores X e Y a la tabla  #MDELACRUZ
        self.position_table.setItem(1, 0, QTableWidgetItem(str(x)))   #MDELACRUZ
        self.position_table.setItem(1, 1, QTableWidgetItem(str(y)))   #MDELACRUZ


    def show_parametros_generales(self):
        some_dictionary = {
            "Parameter 1": "Value 1",
            "Parameter 2": "Value 2",
            "Parameter 3": "Value 3"
        }
        self.parametros_widget = ParametrosGenerales(some_dictionary, self)
        self.parametros_widget.setWindowTitle("General Parameters")
        self.parametros_widget.resize(400, 300)
        self.parametros_widget.exec_()
    
    def clear_autocad(self):   #MDELACRUZ
        """Elimina todos los elementos de AutoCAD antes de dibujar un nuevo diagrama."""
        try:
            acad = Autocad(create_if_not_exists=True, visible=True)   #MDELACRUZ
            doc = acad.ActiveDocument

            # Iterar sobre los objetos de ModelSpace y eliminarlos  #MDELACRUZ
            for obj in list(doc.ModelSpace):
                obj.Delete()
        
            acad.ZoomAll()  # Ajustar la vista
            print("AutoCAD ha sido limpiado correctamente.")  #MDELACRUZ
        except Exception as e:
            print(f"Error al limpiar AutoCAD: {e}")

    def limpiar_dibujo(self):
        """Limpia la escena y reinicia las variables para empezar de nuevo."""
        self.scene.clear()  # Borra todos los elementos de la escena  #MDELACRUZ
        self.dibujos_guardados = []  # Vacía el historial de dibujos
        self.indice_dibujo_actual = -1  # Reinicia el índice del historial
        self.d_horizontal = 0  # Reinicia la posición de los elementos  #MDELACRUZ
        CADInstance.all_instances = []  # Borra las instancias de AutoCAD
        print("Se ha limpiado el dibujo y el historial.")  #MDELACRUZ

class ImageWidget(QGraphicsPixmapItem):
    def __init__(self, image_path, inputs, main_ui, x, y, block_type, parent=None):
        super().__init__(parent)
        self.cad_instance = CADInstance(
            image_name=os.path.basename(image_path),
            x_position=x,
            y_position=y,
            inputs=inputs,
            block_type=block_type
        )
  
        self.main_ui = main_ui
        self.inputs = inputs
        self.setPixmap(QPixmap(image_path))
        self.setPos(x, y)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)  # Ensure the item is movable
        self.form_widget = QWidget()
        self.form_layout = QFormLayout()
        self.form_widget.setLayout(self.form_layout)
        self.data = {}

        # Connect position synchronization
        self.position_changed()

    def position_changed(self):
        """Sync QGraphicsItem position with CADInstance data"""
        self.cad_instance.x_position = self.x()
        self.cad_instance.y_position = self.y()

    def itemChange(self, change, value):
        """Handle position updates"""
        if change == QGraphicsItem.ItemPositionHasChanged:
            prev_x, prev_y = self.x(), self.y()   #MDELACRUZ
            self.main_ui.save_action("move_block", (self.cad_instance.block_type, prev_x, prev_y))  #MDELACRUZ
            self.position_changed()
        return super().itemChange(change, value)

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.set_form_inputs()
            self.form_widget.show()
        elif event.button() == Qt.LeftButton:
            self.show_data()
            self.main_ui.update_position_table(self.x(), self.y())  #MDELACRUZ
        super().mousePressEvent(event)  # Call the base class implementation
    
    def set_form_inputs(self):
        self.clear_form_layout()
        for key, value in self.inputs.items():
            label = QLabel(key)
            line_edit = QLineEdit()
            line_edit.setText(str(value))
            self.form_layout.addRow(label, line_edit)

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_data)
        self.form_layout.addRow(save_button)

    def clear_form_layout(self):
        while self.form_layout.count():
            child = self.form_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def save_data(self):
        # Save data to the associated CADInstance
        for i in range(self.form_layout.count()):
            row = self.form_layout.itemAt(i)
            if isinstance(row, QWidgetItem):
                widget = row.widget()
                if isinstance(widget, QLineEdit):
                    label = self.form_layout.labelForField(widget)
                    self.data[label.text()] = widget.text()

        # Update the inputs of the associated CADInstance
        self.cad_instance.inputs = self.data
        self.form_widget.hide()
        self.show_data()

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

class PositionEditor(QDialog):  #MDELACRUZ
    def __init__(self, parent=None, pos_x=0, pos_y=0):  #MDELACRUZ
        super(PositionEditor, self).__init__(parent)
        self.setWindowTitle("Editar Posición")  #MDELACRUZ
        self.setGeometry(100, 100, 250, 150)
        
        layout = QVBoxLayout()  #MDELACRUZ

        # Campos de entrada para X y Y
        self.x_label = QLabel("Posición X:")  #MDELACRUZ
        self.x_input = QLineEdit(str(pos_x))
        layout.addWidget(self.x_label)
        layout.addWidget(self.x_input)  #MDELACRUZ

        self.y_label = QLabel("Posición Y:")
        self.y_input = QLineEdit(str(pos_y))  #MDELACRUZ
        layout.addWidget(self.y_label)
        layout.addWidget(self.y_input)  #MDELACRUZ

        # Botón para guardar
        self.save_button = QPushButton("Guardar")  #MDELACRUZ
        self.save_button.clicked.connect(self.accept)
        layout.addWidget(self.save_button)  #MDELACRUZ

        self.setLayout(layout)  #MDELACRUZ

    def get_positions(self):  #MDELACRUZ
        return float(self.x_input.text()), float(self.y_input.text())  #MDELACRUZ

class ParametrosGenerales(QDialog):
    def __init__(self, some_dictionary, parent=None):
        super(ParametrosGenerales, self).__init__(parent)
        self.some_dictionary = some_dictionary
        self.form_layout = QFormLayout()
        self.setLayout(self.form_layout)
        self.populate_form()

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_data_as_dictionary)
        self.form_layout.addRow(save_button)

    def populate_form(self):
        for key, value in self.some_dictionary.items():
            label = QLabel(key)
            line_edit = QLineEdit()
            line_edit.setText(str(value))
            self.form_layout.addRow(label, line_edit)

    def save_data_as_dictionary(self):
        saved_data = {}
        for i in range(self.form_layout.count()):
            row = self.form_layout.itemAt(i)
            if isinstance(row, QWidgetItem):
                widget = row.widget()
                if isinstance(widget, QLineEdit):
                    label = self.form_layout.labelForField(widget)
                    saved_data[label.text()] = widget.text()
        print("Saved Data:", saved_data)  # Consider replacing with logging
        self.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = MainUI()
    ui.show()
    sys.exit(app.exec_())

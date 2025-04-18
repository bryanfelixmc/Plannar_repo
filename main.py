from PyQt5.QtWidgets import QMainWindow, QGraphicsItem, QDialog, QApplication, QWidget, QLabel, QPushButton, QGraphicsScene, QGraphicsPixmapItem, QFormLayout, QLineEdit, QWidget, QWidgetItem, QTableWidgetItem, QGraphicsView, QTableWidget,QVBoxLayout,QGraphicsLineItem, QGraphicsTextItem
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap, QTransform,QCursor 
from PyQt5.QtCore import Qt, QTimer, QEvent,QObject,QPoint
import sys
import os
from pyautocad import Autocad, APoint
import pandas as pd

import win32com.client

class MainUI(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.inicializar() 
        self.d_horizontal = 0
        self.progress_value = 0
        self.timer = QTimer()
        # Initializa las imagenes
        self.images_variations = self.initialize_images_variations()
        #Inicializa la clase GraphicsView, como el objeto graphicsView que actualmente existe en el MainUI.
        self.graphics_view = GraphicsView(self.graphicsView)
        # Create an instance of MouseEventHandler
        self.mouse_event_handler = MouseEventHandler(self)
        # Connect buttons to their respective methods
        self.activar_botones()
        # Conectar cada opcion del menu de acciones (parte superior)
        self.dict_informacion_del_proyecto={}
        self.actionParametros_generales.triggered.connect(lambda: self.informacion_del_proyecto(self.dict_informacion_del_proyecto))
        self.dict_condiciones_ambientales={}
        self.actionCondiciones_ambientales.triggered.connect(lambda: self.show_Condiciones_ambientales(self.dict_condiciones_ambientales))
        self.dict_informacion_del_sistema={}
        self.actionInformacion_del_sistema.triggered.connect(lambda: self.show_Informacion_del_sistema(self.dict_informacion_del_sistema))
        self.dict_responsables={}
        self.actionResponsables.triggered.connect(lambda: self.show_Responsables(self.dict_responsables))

    def activar_botones(self):
        self.button01.clicked.connect(lambda: self.add_images(self.images_variations[0],"SB_LINEA_PROY"))### aqui deberia ir el nuevo objeto sb_bay_line()
        self.button05.clicked.connect(lambda: self.add_images(self.images_variations[1],"SB_LINEA_PROY"))
        self.button06.clicked.connect(lambda: self.add_images(self.images_variations[2],"SB_LINEA_PROY"))
        
        #DB BAY DOWN
        self.pushButton_29.clicked.connect(lambda: self.add_images(self.images_variations[3],"DB_LINEA_PROY"))

        #DB BAY UP
        self.pushButton_28.clicked.connect(lambda: self.add_images(self.images_variations[4],"DB_LINEA_PROY"))### aqui deberia ir el nuevo objeto sb_bay_line()

        self.button02.clicked.connect(self.print_all_data_instances)
        self.button04.clicked.connect(self.cad_plot)
        self.button03.clicked.connect(lambda: self.abrir_calc_aisl('CSL-242600-1-06-MC-001.xlsx'))
        self.borrar.clicked.connect(self.limpiar_dibujo)
        self.pushButton.clicked.connect(self.cambiar_tipologia_subestacion)


        #self.pushButton_3.clicked.connect(lambda: self.imprimir_2(self.dict_responsables))
 
    #def imprimir_2(self,valor):
    #    print(valor)
    
    def cambiar_tipologia_subestacion(self):
        #AIS
        if self.boton_AIS.isChecked() and self.boton_SB.isChecked():
            self.stackedWidget.setCurrentWidget(self.AIS_Simple_Barra)
        elif self.boton_AIS.isChecked() and self.boton_DB.isChecked():
            self.stackedWidget.setCurrentWidget(self.AIS_Doble_Barra)
        elif self.boton_AIS.isChecked() and self.boton_DBySECTRANSF.isChecked():
            self.stackedWidget.setCurrentWidget(self.AIS_DB_Y_SEC_TRANSF)
        elif self.boton_AIS.isChecked() and self.boton_INTyMEDIO.isChecked():
            self.stackedWidget.setCurrentWidget(self.AIS_Interruptor_medio)
        
        #GIS
        elif self.boton_GIS.isChecked() and self.boton_SB.isChecked():
            self.stackedWidget.setCurrentWidget(self.GIS_Simple_Barra)
        elif self.boton_GIS.isChecked() and self.boton_DB.isChecked():
            self.stackedWidget.setCurrentWidget(self.GIS_Doble_Barra)
        elif self.boton_GIS.isChecked() and self.boton_DBySECTRANSF.isChecked():
            self.stackedWidget.setCurrentWidget(self.GIS_DB_Y_SEC_TRANSF)
        elif self.boton_GIS.isChecked() and self.boton_INTyMEDIO.isChecked():
            self.stackedWidget.setCurrentWidget(self.GIS_Interruptor_medio)
        
        else:
            pass
            
   
    def abrir_calc_aisl(self,file):
        objeto_hoja_calculo_de_aislamiento(file)
    
    def inicializar(self):
        loadUi("main.ui", self)   
        
    def initialize_images_variations(self):             #SVC
        bil = 1050
        return [
            # SB  bay_down
            [
                ["LL__LINEA_PROY_DWN.jpg", 0, 280+270, {"Carga (MW)": 0, "Nombre": 0, "Codigo de Linea": 0}, "SALIDA_LINEA_DWN"],
                ["PR__LINEA_PROY.jpg", 0, 280+240, {"Tension nominal (kV)": 0, "BIL (kVp)": bil, "I nominal (A)": 0, "Clase": 0}, "Pararrayos c-cd1"],
                ["TTC_LINEA_PROY.jpg", 0, 280+200, {"Tension nominal (kV)": 0, "BIL (kVp)": bil, "Clase de Proteccion": 0, "Tipo": 0}, "TTC_AT_2S"],
                ["SL__LINEA_PROY.jpg", 0, 280+160, {"Tension nominal (kV)": 0, "BIL (kVp)": bil, "I nominal (A)": 0, "Tipo": 0}, "SL_AT_AV_DOWN1"],
                ["TC__LINEA_PROY.jpg", 0, 280+120, {"Tension nominal (kV)": 0, "BIL (kVp)": bil, "I nominal (A)": 0, "Tipo": 0, "Relacion devanado primario": 0, "Relacion devanado secundario": 0, "Burden": 0}, "CT_AT_4S"],
                ["IP__LINEA_PROY.jpg", 0, 280+80, {"Tension nominal (kV)": 0, "BIL (kVp)": bil, "I nominal (A)": 0}, "IP_AT"],
                ["SB__LINEA_PROY_DWN.jpg", 0, 280+40, {"Tension nominal (kV)": 0, "BIL (kVp)": bil, "I nominal (A)": 0, "Tipo": 0}, "SB_AT_AC_DOWN"],
            ],

            # SB   bay_up

            [
                ["LL__LINEA_PROY.jpg", 0, 50, {"Carga (MW)": 0, "Nombre": 0, "Codigo de Linea": 0}, "SALIDA_LINEA"],
                ["PR__LINEA_PROY.jpg", 0, 80, {"Tension nominal (kV)": 0, "BIL (kVp)": bil, "I nominal (A)": 0, "Clase": 0,}, "Pararrayos c-cd1"],
                ["TTC_LINEA_PROY.jpg", 0, 120, {"Tension nominal (kV)": 0, "BIL (kVp)": bil, "Clase de Proteccion": 0, "Tipo": 0}, "TTC_AT_2S"],
                ["SL__LINEA_PROY.jpg", 0, 160, {"Tension nominal (kV)": 0, "BIL (kVp)": bil, "I nominal (A)": 0, "Tipo": 0}, "SL_AT_AV_DOWN2"],
                ["TC__LINEA_PROY.jpg", 0, 200, {"Tension nominal (kV)": 0, "BIL (kVp)": bil, "I nominal (A)": 0, "Tipo": 0, "Relacion devanado primario": 0, "Relacion devanado secundario": 0, "Burden": 0}, "CT_AT_4S_DOWN"],
                ["IP__LINEA_PROY.jpg", 0, 240, {"Tension nominal (kV)": 0, "BIL (kVp)": bil, "I nominal (A)": 0}, "IP_AT_DOWN"],
                ["SB__LINEA_PROY.jpg", 0, 280, {"Tension nominal (kV)": 0, "BIL (kVp)": bil, "I nominal (A)": 0, "Tipo": 0}, "SB_AT_AC"],
            ],

            # SB _
            [
                ["LL__LINEA_PROY.jpg", 0, 40, {"Carga (MW)": 0, "Nombre": 0, "Codigo de Linea": 0}, "-"],
                ["PR__LINEA_PROY.jpg", 0, 100, {"Tension nominal (kV)": 0, "BIL (kVp)": bil, "I nominal (A)": 0, "Clase": 0}, "Pararrayos c-cd1"],
                ["TTC_LINEA_PROY.jpg", 0, 160, {"Tension nominal (kV)": 0, "BIL (kVp)": bil, "Clase de Proteccion": 0, "Tipo": 0}, "TTB-1"],
                ["SL__LINEA_PROY.jpg", 0, 220, {"Tension nominal (kV)": 0, "BIL (kVp)": bil, "I nominal (A)": 0, "Tipo": 0}, "SL_AT_AV_DOWN"],
                ["TC__LINEA_PROY.jpg", 0, 280, {"Tension nominal (kV)": 0, "BIL (kVp)": bil, "I nominal (A)": 0, "Tipo": 0, "Relacion devanado primario": 0, "Relacion devanado secundario": 0, "Burden": 0}, "_"],
                ["IP__LINEA_PROY.jpg", 0, 340, {"Tension nominal (kV)": 0, "BIL (kVp)": bil, "I nominal (A)": 0}, "_"],
                ["SB__LINEA_PROY.jpg", 0, 400, {"Tension nominal (kV)": 0, "BIL (kVp)": bil, "I nominal (A)": 0, "Tipo": 0}, "_"],
            ],
            #DB BAY DOWN
            [
                ["LL__LINEA_PROY_DWN.png", 0, 280+280-14, {"Carga (MW)": 0, "Nombre": 0, "Codigo de Linea": 0}, "SALIDA_LINEA_DWN"],
                ["PR__LINEA_PROY.png", 18.5, 280+240-14, {"Tension nominal (kV)": 0, "BIL (kVp)": bil, "I nominal (A)": 0, "Clase": 0}, "Pararrayos c-cd1"],
                ["TTC_LINEA_PROY.png", 10.5, 280+200-14, {"Tension nominal (kV)": 0, "BIL (kVp)": bil, "Clase de Proteccion": 0, "Tipo": 0}, "TTC_AT_2S"],
                ["SL__LINEA_PROY.png", -5, 280+160-14, {"Tension nominal (kV)": 0, "BIL (kVp)": bil, "I nominal (A)": 0, "Tipo": 0}, "SL_AT_AV_DOWN1"],
                ["TC__LINEA_PROY.png", 0.5, 280+120-14, {"Tension nominal (kV)": 0, "BIL (kVp)": bil, "I nominal (A)": 0, "Tipo": 0, "Relacion devanado primario": 0, "Relacion devanado secundario": 0, "Burden": 0}, "CT_AT_4S"],
                ["IP__LINEA_PROY.png", 9.5, 280+80-14, {"Tension nominal (kV)": 0, "BIL (kVp)": bil, "I nominal (A)": 0}, "IP_AT"],
                ["SB__LINEA_PROY_DWN.png", 0, 280+40-14, {"Tension nominal (kV)": 0, "BIL (kVp)": bil, "I nominal (A)": 0, "Tipo": 0}, "SB_AT_AC_DOWN"],
            ],

            #DB BAY UP

            [
                ["LL__LINEA_PROY.png", 0, 40, {"Carga (MW)": 0, "Nombre": 0, "Codigo de Linea": 0}, "SALIDA_LINEA"],
                ["PR__LINEA_PROY.png", 18.5, 80, {"Tension nominal (kV)": 0, "BIL (kVp)": bil, "I nominal (A)": 0, "Clase": 0,}, "Pararrayos c-cd1"],
                ["TTC_LINEA_PROY.png", 10.5, 120, {"Tension nominal (kV)": 0, "BIL (kVp)": bil, "Clase de Proteccion": 0, "Tipo": 0}, "TTC_AT_2S"],
                ["SL__LINEA_PROY.png", -5, 160, {"Tension nominal (kV)": 0, "BIL (kVp)": bil, "I nominal (A)": 0, "Tipo": 0}, "SL_AT_AV_DOWN2"],
                ["TC__LINEA_PROY.png", 0.5, 200, {"Tension nominal (kV)": 0, "BIL (kVp)": bil, "I nominal (A)": 0, "Tipo": 0, "Relacion devanado primario": 0, "Relacion devanado secundario": 0, "Burden": 0}, "CT_AT_4S_DOWN"],
                ["IP__LINEA_PROY.png", 9.5, 240, {"Tension nominal (kV)": 0, "BIL (kVp)": bil, "I nominal (A)": 0}, "IP_AT_DOWN"],
                ["SB__LINEA_PROY.png", 0, 280, {"Tension nominal (kV)": 0, "BIL (kVp)": bil, "I nominal (A)": 0, "Tipo": 0}, "SB_AT_AC"],
            ]
        ]


    def add_images(self, images, folder):
        folder1 = os.path.join(os.getcwd(), folder)
        aux1=[]
        for image in images:
            image_name, x_position, y_position, inputs, block_type = image

            try:
                pixmap = QPixmap(os.path.join(folder1, image_name)).scaled(85, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation) #(85,40)
                
                # Calculate the position to center the image
                x_centered = x_position+self.d_horizontal + (40 - pixmap.width()) / 2
                y_centered = y_position + (40 - pixmap.height()) / 2
                
                image_widget = CADInstance(
                    image_folder=os.path.join(os.getcwd(),folder),
                    image_name=image_name,
                    inputs=inputs,
                    main_ui=self,
                    x_position=x_centered,
                    y_position=y_centered,
                    block_type=block_type
                )
                
                image_widget.setPixmap(pixmap)
                image_widget.setPos(x_centered, y_centered)
                self.graphics_view.scene.addItem(image_widget)


                # Scroll the view to the position of the newly added image
                #self.graphics_view.view.horizontalScrollBar().setValue(self.d_horizontal)
                #self.graphics_view.view.verticalScrollBar().setValue(y_position)
                
                self.graphics_view.view.horizontalScrollBar().setValue(-25)
                self.graphics_view.view.verticalScrollBar().setValue(-25)
                aux1.append(image_widget)
            except Exception as e:
                
                print(f"Error loading image {image_name}: {e}")
        
        
        if folder=="SB_LINEA_PROY":
            self.d_horizontal += 78  # Update d_horizontal for the next image
        elif folder=="DB_LINEA_PROY":
            self.d_horizontal += 35  # Update d_horizontal for the next image
        return aux1
    
    def cad_plot(self):
        self.clear_autocad()  # Limpiar AutoCAD antes de dibujar  #MDELACRUZ
        self.button04.setEnabled(False)  # Disable the plot button
        try:
            self.start_progress()
            total_instances = len(CADInstance.all_instances)  # Use class variable
            self.timer.start(100)  # Start the timer

            acad = Autocad(create_if_not_exists=True, visible=True)
            doc = acad.ActiveDocument
            lib_objetos = doc.blocks
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

    def informacion_del_proyecto(self,current_dict={}):
        some_dictionary = {
            "Nombre de la Subestación Eléctrica     ": "Value 1",
            "Ubicacion - Pais              ": "Value 2",
            "Ubicacion - Departamento                  ": "Value 3",
            "Ubicacion - Distrito                  ": "Value 4",
        }

        # If current_dict is provided and not empty, update some_dictionary with its keys and values
        if current_dict:
            some_dictionary = {key: current_dict[key] for key in current_dict.keys()}

        self.parametros_widget = ParametrosGenerales(some_dictionary, self)
        self.dict_informacion_del_proyecto=self.parametros_widget.saved_data
        self.parametros_widget.setWindowTitle("informacion del proyecto")
        self.parametros_widget.exec_()
        
    def show_Condiciones_ambientales(self,current_dict={}):
        some_dictionary = {
            "Altura sobre el nivel del mar   (m.s.n.m.)": "Value 1",
            "Temperatura promedio            (°C)      ": "Value 2",
            "Nivel de descarga tipo rayo               ": "Value 3",
            "Resistividad del terreno            (Ω)   ": "Value 4",
            "Grado de contaminación ambiental          ": "Value 4",
            "Humedad Relativa                      (%) ": "Value 5"
        }
        # If current_dict is provided and not empty, update some_dictionary with its keys and values
        if current_dict:
            some_dictionary = {key: current_dict[key] for key in current_dict.keys()}
        
        self.parametros_widget = ParametrosGenerales(some_dictionary, self)
        self.dict_condiciones_ambientales=self.parametros_widget.saved_data
        self.parametros_widget.setWindowTitle("Condiciones ambientales")
        self.parametros_widget.exec_()

    def show_Informacion_del_sistema(self,current_dict={}):
        some_dictionary = {
            "Tensión                                       (kV) ": "Value 1",
            "Frecuencia                                 (Hz) ": "60",
            "Corriente de cortocircuito     (kA) ": "Value 3"
        }
        # If current_dict is provided and not empty, update some_dictionary with its keys and values
        if current_dict:
            some_dictionary = {key: current_dict[key] for key in current_dict.keys()}

        self.parametros_widget = ParametrosGenerales(some_dictionary, self)
        self.dict_informacion_del_sistema=self.parametros_widget.saved_data
        self.parametros_widget.setWindowTitle("Informacion del sistema")
        self.parametros_widget.exec_()

    def show_Responsables(self,current_dict={}):
        some_dictionary = {
            "Jefe del Proyecto          ": "Value 1",
            "Elaborado por              ": "Value 2",
            "Revisado por               ": "Value 3"
        }
        # If current_dict is provided and not empty, update some_dictionary with its keys and values
        if current_dict:
            some_dictionary = {key: current_dict[key] for key in current_dict.keys()}

        self.parametros_widget = ParametrosGenerales(some_dictionary, self)
        self.dict_responsables=self.parametros_widget.saved_data
        self.parametros_widget.setWindowTitle("Responsables")
        self.parametros_widget.exec_()
    
    def clear_autocad(self):   #MDELACRUZ
        """Elimina todos los elementos de AutoCAD antes de dibujar un nuevo diagrama."""
        try:
            acad = Autocad(create_if_not_exists=True, visible=True)   #MDELACRUZ
            doc = acad.ActiveDocument

            # Iterar sobre los objetos de ModelSpace y eliminarlos  #MDELACRUZ
            for obj in list(doc.ModelSpace):
                obj.Delete()
        
            # Use SendCommand to execute the Zoom All command
            #acad.doc.SendCommand("_.zoom _a ")  # The command to zoom all
        
            print("Cleaning & Ploting again...")  #MDELACRUZ
        except Exception as e:
            print(f"Error al limpiar AutoCAD: {e}")

    def limpiar_dibujo(self):
        self.graphics_view.scene.clear()
        self.graphics_view.draw_axes()
        self.d_horizontal = 0
        CADInstance.all_instances = []
        print("Se ha limpiado el dibujo y el historial.")

class GraphicsView:
    def __init__(self, existing_view):
        self.view=existing_view
        self.scene = QGraphicsScene()  # Create the scene here
        self.view.setScene(self.scene)
        self.view.setMouseTracking(True)  # Ensure mouse tracking is enabled
        #Dibuja los ejes de coordenadas
        self.draw_axes()

    def limpiar_dibujo(self):
        """Just clear the scene, let MainUI handle other cleanup"""
        self.scene.clear()


    def draw_axes(self):
        """Draw infinite X and Y axes centered at (0, 0)."""
        # Clear existing axes
        self.limpiar_dibujo()

        # Define a large value for the axes to appear infinite
        large_value = 10000  # Adjust this value as needed

        # Draw X axis (infinite line)
        x_axis = QGraphicsLineItem(-large_value, 0, large_value, 0)
        self.scene.addItem(x_axis)

        # Draw Y axis (infinite line)
        y_axis = QGraphicsLineItem(0, -large_value, 0, large_value)
        self.scene.addItem(y_axis)

        # Set the pen color and width for the X axis (red)
        x_pen = x_axis.pen()
        x_pen.setColor(Qt.red)  # Set the color to red
        x_pen.setWidth(1)  # Set the width of the line
        x_axis.setPen(x_pen)

        # Set the pen color and width for the Y axis (green)
        y_pen = y_axis.pen()
        y_pen.setColor(Qt.green)  # Set the color to green
        y_pen.setWidth(1)  # Set the width of the line
        y_axis.setPen(y_pen)


        # Draw marks every 100 units on the X axis
        for i in range(-large_value, large_value + 1, 100):
            if i != 0:  # Skip the origin
                mark = QGraphicsLineItem(i, -5, i, 5)  # Vertical mark
                self.scene.addItem(mark)

        # Draw marks every 100 units on the Y axis
        for i in range(-large_value, large_value + 1, 100):
            if i != 0:  # Skip the origin
                mark = QGraphicsLineItem(-5, i, 5, i)  # Horizontal mark
                self.scene.addItem(mark)



class MouseEventHandler(QObject):
    def __init__(self, main_ui):
        super().__init__(main_ui)  # Call the base class constructor
        self.main_ui = main_ui
        self.view = main_ui.graphics_view.view
        self.view.setMouseTracking(True)
        self.view.viewport().installEventFilter(self)
        self.zoom_level = 1.0
        self.is_panning = False
        self.pan_start_pos = QPoint()
        #self.apply_zoom_transform()


    def eventFilter(self, source, event):
        if source == self.view.viewport():
            if event.type() == QEvent.MouseButtonPress and event.button() == Qt.MiddleButton:
                self.start_panning(event.pos())
                return True
                
            if event.type() == QEvent.MouseMove:
                self.update_coordinates(event)
                if self.is_panning:
                    self.handle_panning(event.pos())
                    return True
                    
            if event.type() == QEvent.MouseButtonRelease and event.button() == Qt.MiddleButton:
                self.stop_panning()
                return True

            if event.type() == QEvent.Wheel:
                self.handle_wheel(event)
                return True
                
        return super().eventFilter(source, event)
    
    def start_panning(self, pos):
        self.is_panning = True
        self.pan_start_pos = pos
        self.view.setCursor(Qt.ClosedHandCursor)

    def stop_panning(self):
        self.is_panning = False
        self.view.setCursor(Qt.ArrowCursor)

    def handle_panning(self, current_pos):
        delta = current_pos - self.pan_start_pos
        self.pan_start_pos = current_pos
        self.view.horizontalScrollBar().setValue(self.view.horizontalScrollBar().value() - delta.x())
        self.view.verticalScrollBar().setValue(self.view.verticalScrollBar().value() - delta.y())

    def handle_wheel(self, event):
        factor = 1.1 if event.angleDelta().y() > 0 else 0.9
        self.zoom_level = min(max(self.zoom_level * factor, 0.1), 10.0)
        self.apply_zoom_transform()
        self.update_zoom_label()

       
    def apply_zoom_transform(self):
        transform = QTransform().scale(self.zoom_level, self.zoom_level)
        self.view.setTransform(transform)
    

    def update_coordinates(self, event):
        scene_pos = self.view.mapToScene(event.pos())
        self.main_ui.label_2.setText(f"X: {scene_pos.x():.2f}")
        self.main_ui.label_6.setText(f"Y: {scene_pos.y():.2f}")


    def update_zoom_label(self):
        zoom_percentage = self.zoom_level * 100  # Convert to percentage
        self.main_ui.label_zoom.setText(f"Zoom: {zoom_percentage:.0f}%")

class CADInstance(QGraphicsPixmapItem):
    all_instances = []  # Class variable to store all CAD instances
    def __init__(self, image_folder, image_name, inputs, main_ui, x_position, y_position, block_type):
        super().__init__()
        self.image_folder = image_folder
        self.image_name=image_name
        self.inputs = inputs
        self.main_ui = main_ui
        self.x_position = x_position
        self.y_position = -y_position
        self.block_type = block_type
        self.setPixmap(QPixmap(image_folder))
        self.setPos(self.x_position, self.y_position)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)  # Ensure the item is movable
        self.form_widget = QWidget()
        self.form_layout = QFormLayout()
        self.form_widget.setLayout(self.form_layout)
        self.data = {}
        # Check for duplicates before appending
        self.add_instance()
  
        # Connect position synchronization
        self.position_changed()


    def add_instance(self):
        if not self.is_duplicate():
            CADInstance.all_instances.append(self)  # Store instance in class variable
        else:
            print(f"Duplicate instance not added: {self}")

    def is_duplicate(self):
        """Check if an instance with the same attributes already exists."""
        for instance in CADInstance.all_instances:
            if (instance.image_folder == self.image_folder and
                instance.image_name == self.image_name and
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

    def position_changed(self):
        """Sync QGraphicsItem position with CADInstance data"""
        self.x_position = self.x()
        self.y_position = self.y()

        """
    def itemChange(self, change, value):
         #Handle position updates
        if change == QGraphicsItem.ItemPositionHasChanged:
            prev_x, prev_y = self.x(), self.y()   #MDELACRUZ
            self.main_ui.save_action("move_block", (self.cad_instance.block_type, prev_x, prev_y))  #MDELACRUZ
            self.position_changed()
        return super().itemChange(change, value)
        """

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.set_form_inputs()
            self.form_widget.show()
        elif event.button() == Qt.LeftButton:
            self.show_data()
            self.main_ui.table04.setItem(0, 0, QTableWidgetItem(str(self.x()))) 
            self.main_ui.table04.setItem(0, 1, QTableWidgetItem(str(self.y()))) 
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
        self.inputs = self.data
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

"""class PositionEditor(QDialog):  #MDELACRUZ
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
        return float(self.x_input.text()), float(self.y_input.text())  #MDELACRUZ"""

class ParametrosGenerales(QDialog):
    def __init__(self, some_dictionary, parent=None):
        super(ParametrosGenerales, self).__init__(parent)
        self.some_dictionary = some_dictionary
        self.form_layout = QFormLayout()
        self.setLayout(self.form_layout)
        self.populate_form()
        self.saved_data = {}
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

        for i in range(self.form_layout.count()):
            row = self.form_layout.itemAt(i)
            if isinstance(row, QWidgetItem):
                widget = row.widget()
                if isinstance(widget, QLineEdit):
                    label = self.form_layout.labelForField(widget)
                    self.saved_data[label.text()] = widget.text()
        print("Saved Data:", self.saved_data)  # Consider replacing with logging
        self.accept()


class objeto_hoja_calculo_de_aislamiento():

    def __init__(self,file):
        self.file=file


        self.excel = win32com.client.Dispatch("Excel.Application")
        self.hacer_libro_visible()

        self.workbook = self.excel.Workbooks.Open(os.path.join(os.getcwd(),'CSL-242600-1-06-MC-001.xlsx'))
        self.sheet = self.workbook.Sheets['CA-138kV']
        self.imprimir_valor()
        #ãself.escribir_valor()
        #self.guardar_libro()
        #self.cerrar_libro()
        #self.salir_de_aplicacion()

    def hacer_libro_visible(self):
        self.excel.Visible = True
    def imprimir_valor(self):
        #print(self.sheet.Cells(1, 1).Value)
        print(self.sheet.Range('P15').Value)
    def escribir_valor(self):
        self.sheet.Cells(2, 1).Value = "Hello, Excel!"
    def guardar_libro(self):
        self.workbook.Save()
    def cerrar_libro(self):
        self.workbook.Close()

    def salir_de_aplicacion(self):
        self.excel.Quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = MainUI()
    ui.show()
    sys.exit(app.exec_())

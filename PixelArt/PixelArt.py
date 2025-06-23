#Plugin Desarrollado por Gabo99x y MartinMigue
from krita import *
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PyQt5.QtGui import QImage
from PyQt5.QtCore import QByteArray

class PixelArt(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.boton = QPushButton("Convertir a Pixel Art")
        self.boton.clicked.connect(self.aplicarPixelArt)
        layout.addWidget(self.boton)
        self.setLayout(layout)

    def aplicarPixelArt(self):
        doc = Krita.instance().activeDocument()
        if doc:
            capa = doc.activeNode()
            if capa and capa.type() == "paintlayer":
                bounds = capa.bounds()
                width = bounds.width()
                height = bounds.height()
                imagen = capa.pixelData(0, 0, width, height)

                qimage = QImage(imagen, width, height, QImage.Format_ARGB32)

                nuevaImagen = qimage.scaled(width // 8, height // 8)

                application = Krita.instance()
                posterize_filter = application.filter("posterize") #Filtro nativo de Krita simulacion de pixeles
                posterize_filter.apply(capa, 0, 0, width, height)

                imagenFinal = nuevaImagen.scaled(width, height)

                byte_array = QByteArray(imagenFinal.bits().asstring(imagenFinal.byteCount()))

                capa.setPixelData(byte_array, 0, 0, width, height)

                doc.refreshProjection()

class Plugin(Extension):
    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        pass 

    def createActions(self, window):
        action = window.createAction("PixelArtFilter", "Convertir a Pixel Art", "tools/scripts")
        action.triggered.connect(self.mostrarPixelArt)

    def mostrarPixelArt(self):
        self.pixelart = PixelArt()
        self.pixelart.show()

Krita.instance().addExtension(Plugin(Krita.instance()))



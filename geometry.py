import sys
import numpy as np
import sympy
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QComboBox, QFrame, QCheckBox, QScrollArea)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# --- STYLING ---
STYLE_SHEET = """
QMainWindow { background-color: #0d0d0d; }
QLabel { color: #d0d0d0; font-family: 'Segoe UI'; font-size: 12px; }
QLineEdit { 
    background-color: #1a1a1a; color: #4ec9b0; border: 1px solid #333; 
    border-radius: 4px; padding: 8px; font-size: 14px; font-weight: bold;
}
QCheckBox { color: #ffffff; font-size: 11px; font-weight: bold; }
QComboBox { 
    background-color: #1a1a1a; color: white; border-radius: 4px; 
    padding: 8px; border: 1px solid #333; font-size: 13px;
}
#ResultBox { 
    background-color: #141414; border-radius: 10px; border-left: 5px solid #007acc;
    padding: 15px; margin-top: 10px;
}
#Title { font-size: 20px; font-weight: bold; color: #007acc; margin-bottom: 10px; }
.ResultHeader { font-size: 10px; color: #888; font-weight: bold; text-transform: uppercase; }
.ResultValue { font-size: 18px; font-weight: bold; color: #4ec9b0; margin-bottom: 5px; }
.DecimalValue { font-size: 12px; color: #9cdcfe; margin-bottom: 15px; }
"""

class GeometryCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.fig = Figure(figsize=(5, 5), facecolor='#0d0d0d')
        self.axes = self.fig.add_subplot(111, projection='3d')
        self.axes.set_facecolor('#0d0d0d')
        super().__init__(self.fig)

    def plot_solid(self, shape, base_type, r, h):
        self.axes.clear()
        self.axes.set_axis_off()
        limit = max(r, h, 10)
        self.axes.set_xlim(-limit, limit); self.axes.set_ylim(-limit, limit); self.axes.set_zlim(0, limit * 1.5)

        sides = 60
        if shape in ["Pyramid", "Prism"]:
            sides = {"Square": 4, "Triangle": 3, "Hexagon": 6}.get(base_type, 60)

        try:
            u = np.linspace(0, 2*np.pi, sides + 1)
            if shape == "Sphere":
                v = np.linspace(0, np.pi, 30)
                x = r * np.outer(np.cos(u), np.sin(v))
                y = r * np.outer(np.sin(u), np.sin(v))
                z = r * np.outer(np.ones(np.size(u)), np.cos(v)) + r
                self.axes.plot_surface(x, y, z, color='#007acc', alpha=0.6, edgecolors='w', lw=0.1)
            elif shape in ["Cone", "Pyramid"]:
                v = np.linspace(0, h, 15); us, vs = np.meshgrid(u, v)
                x, y, z = (r*(h-vs)/h)*np.cos(us), (r*(h-vs)/h)*np.sin(us), vs
                self.axes.plot_surface(x, y, z, color='#4ec9b0', alpha=0.6, edgecolors='w', lw=0.3)
            elif shape in ["Cylinder", "Prism"]:
                v = np.linspace(0, h, 2); us, vs = np.meshgrid(u, v)
                x, y, z = r*np.cos(us), r*np.sin(us), vs
                self.axes.plot_surface(x, y, z, color='#ce9178', alpha=0.6, edgecolors='w', lw=0.3)
        except: pass
        self.draw()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Spatial Geometry Calculator")
        self.setStyleSheet(STYLE_SHEET)
        self.setMinimumSize(1200, 850)

        container = QWidget(); self.setCentralWidget(container)
        layout = QHBoxLayout(container)

        # --- Sidebar ---
        scroll = QScrollArea(); scroll.setWidgetResizable(True); scroll.setFixedWidth(360); scroll.setFrameShape(QFrame.Shape.NoFrame)
        side_widget = QWidget(); sidebar = QVBoxLayout(side_widget); scroll.setWidget(side_widget)

        title = QLabel("CALCULATOR"); title.setObjectName("Title"); sidebar.addWidget(title)

        sidebar.addWidget(QLabel("SELECT SOLID:"))
        self.solid_combo = QComboBox()
        self.solid_combo.addItems(["Sphere", "Cone", "Cylinder", "Pyramid", "Prism"])
        self.solid_combo.currentTextChanged.connect(self.update_ui_state)
        sidebar.addWidget(self.solid_combo)

        self.base_wrap = QWidget(); bw_l = QVBoxLayout(self.base_wrap); bw_l.setContentsMargins(0,0,0,0)
        bw_l.addWidget(QLabel("BASE SHAPE:"))
        self.base_combo = QComboBox(); self.base_combo.addItems(["Square", "Triangle", "Hexagon"])
        self.base_combo.currentTextChanged.connect(self.update_all)
        bw_l.addWidget(self.base_combo); sidebar.addWidget(self.base_wrap)

        # Constant Toggles
        sidebar.addWidget(QLabel("CONSTANT SETTINGS:"))
        self.chk_pi = QCheckBox("Define π as Number"); self.chk_pi.toggled.connect(self.update_ui_state)
        self.pi_input = QLineEdit("3.14"); self.pi_input.textChanged.connect(self.update_all)
        sidebar.addWidget(self.chk_pi); sidebar.addWidget(self.pi_input)

        self.chk_sqrt = QCheckBox("Define √3 as Number"); self.chk_sqrt.toggled.connect(self.update_ui_state)
        self.sqrt_input = QLineEdit("1.732"); self.sqrt_input.textChanged.connect(self.update_all)
        sidebar.addWidget(self.chk_sqrt); sidebar.addWidget(self.sqrt_input)

        sidebar.addWidget(QLabel("DIMENSIONS:"))
        self.r_lbl = QLabel("Radius / Apothem (r):")
        self.r_input = QLineEdit("5")
        self.r_input.textChanged.connect(self.update_all)
        sidebar.addWidget(self.r_lbl); sidebar.addWidget(self.r_input)

        self.h_lbl = QLabel("Height (h):")
        self.h_input = QLineEdit("10")
        self.h_input.textChanged.connect(self.update_all)
        sidebar.addWidget(self.h_lbl); sidebar.addWidget(self.h_input)

        self.res_box = QFrame(); self.res_box.setObjectName("ResultBox")
        self.res_layout = QVBoxLayout(self.res_box)
        self.res_map = {}
        for m in ["Base Area", "Lateral Area", "Total Area", "Volume"]:
            h = QLabel(m.upper()); h.setProperty("class", "ResultHeader")
            v = QLabel("..."); v.setProperty("class", "ResultValue"); v.setWordWrap(True)
            d = QLabel("..."); d.setProperty("class", "DecimalValue")
            self.res_layout.addWidget(h); self.res_layout.addWidget(v); self.res_layout.addWidget(d)
            self.res_map[m] = (v, d)
        sidebar.addWidget(self.res_box); sidebar.addStretch()

        layout.addWidget(scroll, 1)
        self.canvas = GeometryCanvas(self); layout.addWidget(self.canvas, 2)
        self.update_ui_state()

    def format_math(self, expr):
        s = str(expr)
        s = s.replace('pi', 'π').replace('sqrt(3)', '√3').replace('*', '·').replace('**', '^')
        return s

    def update_ui_state(self):
        shape = self.solid_combo.currentText()
        self.base_wrap.setVisible(shape in ["Pyramid", "Prism"])
        self.h_lbl.setVisible(shape != "Sphere"); self.h_input.setVisible(shape != "Sphere")
        
        self.pi_input.setVisible(self.chk_pi.isChecked())
        self.sqrt_input.setVisible(self.chk_sqrt.isChecked())
        self.update_all()

    def update_all(self):
        shape = self.solid_combo.currentText()
        base = self.base_combo.currentText()
        try:
            r = float(self.r_input.text()) if self.r_input.text() else 0
            h = float(self.h_input.text()) if self.h_input.text() else 0
            
            # Symbolic Logic
            pi_symbolic = not self.chk_pi.isChecked()
            sqrt_symbolic = not self.chk_sqrt.isChecked()
            
            pi = float(self.pi_input.text()) if not pi_symbolic else sympy.pi
            sqrt3 = float(self.sqrt_input.text()) if not sqrt_symbolic else sympy.sqrt(3)

            # Calculation
            if shape in ["Sphere", "Cone", "Cylinder"]:
                ab, perim, apothem = pi * r**2, 2 * pi * r, r
            else:
                if base == "Square": side = 2*r; ab, perim, apothem = side**2, 4*side, r
                elif base == "Triangle":
                    side = r * 2 * sqrt3
                    ab, perim, apothem = (side**2 * sqrt3) / 4, 3 * side, r
                elif base == "Hexagon":
                    side = (2 * r) / sqrt3
                    ab, perim, apothem = (3 * side**2 * sqrt3) / 2, 6 * side, r

            if shape == "Sphere":
                al = 4*pi*r**2; at = al; vol = (sympy.Rational(4,3))*pi*r**3
            elif shape in ["Cone", "Pyramid"]:
                s = sympy.sqrt(h**2 + apothem**2) 
                al = (perim*s)/2; at = ab+al; vol = (sympy.Rational(1,3))*ab*h
            else: # Cylinder / Prism
                al = perim*h; at = 2*ab+al; vol = ab*h

            res_list = [ab, al, at, vol]
            for i, m in enumerate(["Base Area", "Lateral Area", "Total Area", "Volume"]):
                val = res_list[i]
                self.res_map[m][0].setText(self.format_math(val))
                
                # Show decimal ONLY if symbolic constants are replaced by numbers
                if not pi_symbolic or not sqrt_symbolic:
                    try:
                        self.res_map[m][1].setText(f"≈ {float(val.evalf()):,.4f}")
                        self.res_map[m][1].setVisible(True)
                    except:
                        self.res_map[m][1].setVisible(False)
                else:
                    self.res_map[m][1].setVisible(False)
            
            self.canvas.plot_solid(shape, base, r, h)
        except: pass

if __name__ == "__main__":
    app = QApplication(sys.argv); mw = MainWindow(); mw.show(); sys.exit(app.exec())
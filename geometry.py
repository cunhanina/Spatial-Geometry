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

    def plot_solid(self, shape, base_type, r1, h, r2=0, w=0):
        self.axes.clear()
        self.axes.set_axis_off()
        limit = max(r1, h, r2, w, 10)
        self.axes.set_xlim(-limit, limit); self.axes.set_ylim(-limit, limit); self.axes.set_zlim(0, limit * 1.5)

        sides = 60
        if shape in ["Pyramid", "Prism", "Frustum"]:
            sides = {"Square": 4, "Triangle": 3, "Hexagon": 6, "Rectangle": 4}.get(base_type, 60)

        try:
            u = np.linspace(0, 2*np.pi, sides + 1)
            if shape == "Sphere":
                v = np.linspace(0, np.pi, 30)
                x = r1 * np.outer(np.cos(u), np.sin(v))
                y = r1 * np.outer(np.sin(u), np.sin(v))
                z = r1 * np.outer(np.ones(np.size(u)), np.cos(v)) + r1
                self.axes.plot_surface(x, y, z, color='#007acc', alpha=0.6, edgecolors='w', lw=0.1)
            elif shape in ["Cone", "Pyramid", "Frustum"]:
                v = np.linspace(0, h, 15); us, vs = np.meshgrid(u, v)
                curr_r = r1 - (r1 - r2) * (vs / h)
                x, y, z = curr_r * np.cos(us), curr_r * np.sin(us), vs
                self.axes.plot_surface(x, y, z, color='#4ec9b0', alpha=0.6, edgecolors='w', lw=0.3)
            elif shape in ["Cylinder", "Prism"]:
                v = np.linspace(0, h, 2); us, vs = np.meshgrid(u, v)
                x, y, z = r1 * np.cos(us), r1 * np.sin(us), vs
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

        scroll = QScrollArea(); scroll.setWidgetResizable(True); scroll.setFixedWidth(360); scroll.setFrameShape(QFrame.Shape.NoFrame)
        side_widget = QWidget(); sidebar = QVBoxLayout(side_widget); scroll.setWidget(side_widget)

        title = QLabel("CALCULATOR"); title.setObjectName("Title"); sidebar.addWidget(title)

        sidebar.addWidget(QLabel("SELECT SOLID:"))
        self.solid_combo = QComboBox()
        self.solid_combo.addItems(["Sphere", "Cone", "Cylinder", "Pyramid", "Prism", "Frustum"])
        self.solid_combo.currentTextChanged.connect(self.update_ui_state)
        sidebar.addWidget(self.solid_combo)

        self.base_wrap = QWidget(); bw_l = QVBoxLayout(self.base_wrap); bw_l.setContentsMargins(0,0,0,0)
        bw_l.addWidget(QLabel("BASE SHAPE:"))
        self.base_combo = QComboBox(); self.base_combo.addItems(["Square", "Rectangle", "Triangle", "Hexagon"])
        self.base_combo.currentTextChanged.connect(self.update_ui_state)
        bw_l.addWidget(self.base_combo); sidebar.addWidget(self.base_wrap)

        sidebar.addWidget(QLabel("CONSTANT SETTINGS:"))
        self.chk_pi = QCheckBox("Define π as Number"); self.chk_pi.toggled.connect(self.update_ui_state)
        self.pi_input = QLineEdit("3.14159"); self.pi_input.textChanged.connect(self.update_all)
        sidebar.addWidget(self.chk_pi); sidebar.addWidget(self.pi_input)

        self.chk_sqrt = QCheckBox("Define √3 as Number"); self.chk_sqrt.toggled.connect(self.update_ui_state)
        self.sqrt_input = QLineEdit("1.732"); self.sqrt_input.textChanged.connect(self.update_all)
        sidebar.addWidget(self.chk_sqrt); sidebar.addWidget(self.sqrt_input)

        sidebar.addWidget(QLabel("DIMENSIONS:"))
        self.r1_lbl = QLabel("Radius / Apothem (r1):")
        self.r1_input = QLineEdit("5"); self.r1_input.textChanged.connect(self.update_all)
        sidebar.addWidget(self.r1_lbl); sidebar.addWidget(self.r1_input)

        self.w_lbl = QLabel("Width (w):")
        self.w_input = QLineEdit("5"); self.w_input.textChanged.connect(self.update_all)
        sidebar.addWidget(self.w_lbl); sidebar.addWidget(self.w_input)

        self.r2_lbl = QLabel("Top Radius / Apothem (r2):")
        self.r2_input = QLineEdit("2"); self.r2_input.textChanged.connect(self.update_all)
        sidebar.addWidget(self.r2_lbl); sidebar.addWidget(self.r2_input)

        self.h_lbl = QLabel("Height (h):")
        self.h_input = QLineEdit("10"); self.h_input.textChanged.connect(self.update_all)
        sidebar.addWidget(self.h_lbl); sidebar.addWidget(self.h_input)

        self.res_box = QFrame(); self.res_box.setObjectName("ResultBox")
        res_layout = QVBoxLayout(self.res_box)
        self.res_map = {}
        for m in ["Base Area", "Lateral Area", "Total Area", "Volume"]:
            h_lbl = QLabel(m.upper()); h_lbl.setProperty("class", "ResultHeader")
            v = QLabel("..."); v.setProperty("class", "ResultValue"); v.setWordWrap(True)
            d = QLabel("..."); d.setProperty("class", "DecimalValue")
            res_layout.addWidget(h_lbl); res_layout.addWidget(v); res_layout.addWidget(d)
            self.res_map[m] = (v, d)
        sidebar.addWidget(self.res_box); sidebar.addStretch()

        layout.addWidget(scroll, 1)
        self.canvas = GeometryCanvas(self); layout.addWidget(self.canvas, 2)
        self.update_ui_state()

    def format_math(self, expr):
        """Converts SymPy symbols to a clean math string."""
        s = str(expr)
        s = s.replace('pi', 'π').replace('sqrt(3)', '√3').replace('*', '·').replace('**', '^')
        return s

    def update_ui_state(self):
        shape = self.solid_combo.currentText()
        base = self.base_combo.currentText()
        
        # Visibility controls based on geometry rules
        self.base_wrap.setVisible(shape in ["Pyramid", "Prism", "Frustum"])
        self.w_lbl.setVisible(shape in ["Pyramid", "Prism", "Frustum"] and base == "Rectangle")
        self.w_input.setVisible(shape in ["Pyramid", "Prism", "Frustum"] and base == "Rectangle")
        self.r2_lbl.setVisible(shape == "Frustum")
        self.r2_input.setVisible(shape == "Frustum")
        self.h_lbl.setVisible(shape != "Sphere")
        self.h_input.setVisible(shape != "Sphere")
        
        # Input label morphing
        if shape == "Sphere": self.r1_lbl.setText("Radius (r):")
        elif base == "Rectangle": self.r1_lbl.setText("Length (l):")
        else: self.r1_lbl.setText("Radius / Apothem (r1):")

        self.pi_input.setVisible(self.chk_pi.isChecked())
        self.sqrt_input.setVisible(self.chk_sqrt.isChecked())
        self.update_all()

    def get_base_data(self, b_type, r, w, pi_val, sqrt3_val):
        """Calculates area, perimeter, and apothem for any base."""
        if b_type == "Rectangle": return r * w, 2*r + 2*w, 0
        if b_type == "Square": side = 2*r; return side**2, 4*side, r
        if b_type == "Triangle": side = r * 2 * sqrt3_val; return (side**2 * sqrt3_val)/4, 3*side, r
        if b_type == "Hexagon": side = (2*r)/sqrt3_val; return (3 * side**2 * sqrt3_val)/2, 6*side, r
        return pi_val * r**2, 2 * pi_val * r, r 

    def update_all(self):
        shape = self.solid_combo.currentText()
        base = self.base_combo.currentText()
        
        pi_is_num = self.chk_pi.isChecked()
        sqrt_is_num = self.chk_sqrt.isChecked()
        
        try:
            r1 = float(self.r1_input.text()) if self.r1_input.text() else 0
            # FIX: Force r2 to 0 if the shape is NOT a Frustum, otherwise it reads the hidden input.
            r2 = float(self.r2_input.text()) if (self.r2_input.text() and shape == "Frustum") else 0
            w = float(self.w_input.text()) if (self.w_input.text() and self.w_input.isVisible()) else 0
            h = float(self.h_input.text()) if self.h_input.text() else 0
            
            pi = sympy.Float(self.pi_input.text()) if self.chk_pi.isChecked() else sympy.pi
            sqrt3 = sympy.Float(self.sqrt_input.text()) if self.chk_sqrt.isChecked() else sympy.sqrt(3)

            b_type = base if shape in ["Pyramid", "Prism", "Frustum"] else "Circle"
            ab1, p1, a1 = self.get_base_data(b_type, r1, w, pi, sqrt3)
            
            if shape == "Sphere":
                al = 4*pi*r1**2; at = al; vol = (sympy.Rational(4,3))*pi*r1**3
            elif shape == "Frustum":
                ab2, p2, a2 = self.get_base_data(b_type, r2, w, pi, sqrt3)
                vol = (sympy.Rational(1,3)) * h * (ab1 + ab2 + sympy.sqrt(ab1 * ab2))
                s = sympy.sqrt(h**2 + (a1 - a2)**2)
                al = ((p1 + p2) / 2) * s
                at = ab1 + ab2 + al
            elif shape in ["Cone", "Pyramid"]:
                if b_type == "Rectangle" and shape == "Pyramid":
                    s_len = sympy.sqrt(h**2 + (w/2)**2)
                    s_wid = sympy.sqrt(h**2 + (r1/2)**2)
                    al = (r1 * s_len) + (w * s_wid)
                else:
                    s = sympy.sqrt(h**2 + a1**2)
                    al = (p1 * s) / 2
                at = ab1 + al; vol = (sympy.Rational(1,3))*ab1*h
            else: # Prism / Cylinder
                al = p1*h; at = 2*ab1 + al; vol = ab1*h

            res = [ab1, al, at, vol]
            for i, m in enumerate(["Base Area", "Lateral Area", "Total Area", "Volume"]):
                val = sympy.sympify(res[i])
                has_symbols = val.has(sympy.pi) or val.has(sympy.sqrt(3))
                
                if has_symbols:
                    self.res_map[m][0].setText(self.format_math(val))
                    self.res_map[m][1].setVisible(False)
                else:
                    self.res_map[m][0].setText(f"{float(val.evalf()):,.4f}")
                    self.res_map[m][1].setVisible(False)
            
            self.canvas.plot_solid(shape, b_type, r1, h, r2, w)
        except Exception as e:
            pass

if __name__ == "__main__":
    app = QApplication(sys.argv); mw = MainWindow(); mw.show(); sys.exit(app.exec())
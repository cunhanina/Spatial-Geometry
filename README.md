# 🧊 Spatial Geometry Calculator

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg?logo=python&logoColor=white)
![PyQt6](https://img.shields.io/badge/UI-PyQt6-green?logo=qt&logoColor=white)
![SymPy](https://img.shields.io/badge/Math-SymPy-yellow?logo=python&logoColor=black)
![Matplotlib](https://img.shields.io/badge/Viz-Matplotlib-orange)

A robust desktop application designed to calculate the areas and volumes of geometric solids with absolute mathematical precision. Unlike standard calculators, this tool preserves symbolic constants such as $\pi$ and $\sqrt{3}$, delivering results identical to those found in academic textbooks.



## 🌟 The Competitive Edge
**The Problem:** Most geometry scripts and calculators convert irrational numbers into floating-point decimals, leading to a loss of precision and making the results difficult to use in formal proofs or academic exams.

**The Solution:** Leveraging the **SymPy** library, we processes formulas symbolically. Users can toggle between defining decimal values for constants or maintaining them as pure mathematical symbols. Additionally, the application features a reactive 3D visualization that scales instantly as dimensions are modified.

---

## 🚀 Key Features

* **Exact Symbolic Computation:** Results maintain $\pi$ and square roots without unwanted decimal approximations.
* **Real-Time 3D Visualization:** An integrated interface that renders the solid and scales the view instantly as inputs change.
* **Multi-Base Support:** Calculate pyramids and prisms with triangular, square, or hexagonal bases, automatically adjusting the apothem mathematics.

* **Precision Geometry:** Correct implementation of complex formulas, including the generatrix (slant height) for lateral area calculations in cones and pyramids.
* **Reactive Interface:** No "Calculate" buttons required. Results and the 3D plot update as you type.

---

## 🛠 Tech Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Language** | Python 3.10+ | Core logic and integration |
| **Interface (GUI)** | PyQt6 | Framework for a native desktop experience |
| **Mathematics** | SymPy | Symbolic computation for exact precision |
| **3D Graphics** | Matplotlib | Mesh and geometric surface rendering |

---

## 📦 Installation & Usage

### Prerequisites
Ensure you have Python installed along with the required libraries:

```bash
pip install PyQt6 matplotlib sympy numpy
```

### Running the App
1. Clone the repository:
```bash
git clone https://github.com/cunhanina/Spatial-Geometry.git
cd Spatial-Geometry
```
2. Run the application:
```bash
python geometry.py
```

---

## 🧠 Applied Mathematical Logic
The system is designed to be mathematically rigorous:

1.  **Apothem Calculation:** For regular polygons, the application derives the side length from the provided apothem ($r$) to ensure the base area and perimeter are consistent with the 3D visualization.
2.  **Slant Height ($s$):** In pyramids and cones, the lateral area is calculated via the Pythagorean theorem: $s = \sqrt{h^2 + r^2}$, where $r$ is the base apothem.

3.  **Symbolic Branching:** If the user unchecks "Define constants," SymPy isolates the symbols throughout the entire calculation chain until the final output.

---

<div align="center">

### Built with ❤️ by [Nina Cunha](https://github.com/maxykoin)

**Data Science · Industrial Automation · Software Engineering**

[![LinkedIn](https://img.shields.io/badge/Connect-LinkedIn-blue?style=for-the-badge&logo=linkedin)]([https://www.linkedin.com/in/nscunha/](https://www.linkedin.com/in/nscunha/))
[![GitHub](https://img.shields.io/badge/Follow-GitHub-181717?style=for-the-badge&logo=github)](https://github.com/maxykoin)

</div>

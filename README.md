# 🧊 Spatial Geometry Calculator

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg?logo=python&logoColor=white)
![SymPy](https://img.shields.io/badge/Library-SymPy-yellow?logo=python&logoColor=black)
![Math](https://img.shields.io/badge/Focus-Mathematics-green)
![Geometry](https://img.shields.io/badge/Domain-Spatial_Geometry-purple)

A Python program designed to precisely calculate the area and volume of various 3D objects, supporting exact symbolic representations rather than floating-point approximations.

**The Problem:** Standard calculators and basic scripts usually convert irrational numbers (like π or √3) into long, messy floating-point decimals. This is practically useless for students or mathematicians who need exact, simplified symbolic answers for exams or formal proofs.

**The Solution:** A specialized geometric calculator that leverages the `sympy` library to process and output exact mathematical symbols. It natively supports undisclosed square root values and symbolic π, calculating precise areas and volumes for pyramids, cones, cylinders, and spheres.

---

## 📸 Capabilities
* **Symbolic Computation:** Operates with exact mathematical values (e.g., leaving answers in terms of π or √3) instead of approximating decimals.
* **Multi-Solid Support:** Capable of handling the complex formulas for Pyramids, Cones, Cylinders, and Spheres.
* **Optimized Control Flow:** Uses modern `match...case` statements for clean, efficient menu navigation and function dispatching.
* **Educational Tool:** Built specifically as a dual-purpose project: to optimize Python logic (nested logic, loops, custom functions) and to serve as an interactive study aid for memorizing spatial geometry formulas.

## 🛠 Tech Stack
| Component | Technology | Description |
| :--- | :--- | :--- |
| **Core** | Python 3.10+ | Main application and logic |
| **Mathematics** | SymPy | Symbolic mathematics library for exact computations |
| **Architecture** | Functional | Clean, optimized functions with structural pattern matching |
| **Domain** | Geometry | 3D solid area and volume formulas |

## 🚀 Quick Start

```bash
# 1. Clone the repo
git clone [https://github.com/cunhanina/Spatial-Geometry.git](https://github.com/cunhanina/Spatial-Geometry.git)
cd Spatial-Geometry

# 2. Install dependencies (SymPy)
pip install sympy

# 3. Run the calculator
python geometry.py
```

## 🧠 System Architecture
The application is structured around a procedural, interactive command-line interface:
1.  **State Loop:** A robust `while` loop maintains the application state, allowing users to perform multiple calculations without restarting the program.
2.  **Pattern Matching (`match...case`):** Replaces deeply nested `if-else` chains with modern structural pattern matching to route the user's geometric choice to the correct mathematical function.
3.  **Symbolic Processing:** * User inputs are parsed and fed into `sympy` variables.
    * Mathematical formulas are applied (e.g., $V = \frac{4}{3}\pi r^3$ for a sphere).
    * The output is formatted to preserve irrational numbers and constants, providing a clean, textbook-style answer.

---

<div align="center">

### Built with ❤️ by [Nina Cunha](https://github.com/maxykoin)

**Data Science · Industrial Automation · Software Engineering**

[![LinkedIn](https://img.shields.io/badge/Connect-LinkedIn-blue?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/nscunha/)
[![GitHub](https://img.shields.io/badge/Follow-GitHub-181717?style=for-the-badge&logo=github)](https://github.com/maxykoin)

</div>

---

# 📘 Mittelwert und Standardabweichung

## 🔹 Mittelwert (arithmetisches Mittel)
- **Definition:** Durchschnitt aller Messwerte  
- **Formel:**
  \[
  \bar{x} = \frac{1}{N} \sum_{i=1}^{N} x_i
  \]
- **Python:**
  ```python
  daten = [125, 129, 140, 121, 127]
  mean = sum(daten) / len(daten)
  print("Mittelwert:", mean)

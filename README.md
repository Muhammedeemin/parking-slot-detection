# 🅿️ Real-Time Parking Slot Detection using OpenCV

A computer vision system that detects whether parking spaces are **occupied** or **vacant** in real time using classical image processing techniques — no deep learning required.

> **Course:** Image and Video Processing (2025-2026)  
> **Group:** İrem ACINAN & Muhammed Emin AKBULUT  
> **Supervisor:** Tuğçem PARTAL

---

## 📌 About

This project analyzes video footage from a fixed overhead camera and determines the occupancy status of each parking space in real time. The system uses adaptive thresholding, morphological operations, and pixel counting to classify spaces as vacant (green) or occupied (red).

**Key Features:**
- Real-time detection with low computational cost
- No deep learning or GPU required
- Interactive parking space selection tool
- Adjustable threshold during runtime
- Debug mode to visualize preprocessing steps

---

## 🛠️ Technologies Used

| Tool | Purpose |
|------|---------|
| Python 3.x | Programming language |
| OpenCV | Image processing |
| NumPy | Numerical operations |
| Pickle | Data serialization |

---

## 📂 Project Structure

```
parking_project/
├── main.py                    # Main detection program
├── parking_space_picker.py    # Parking space selection tool
├── requirements.txt           # Required libraries
├── CarParkPositions           # Saved parking positions (generated)
└── carPark.mp4                # Parking lot video (not included)
```

---

## 🚀 How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Add a parking lot video
Place a fixed-camera parking lot video in the project folder as `carPark.mp4`.

### 3. Mark parking spaces
```bash
python parking_space_picker.py
```
- **Left click:** Add a parking space
- **Right click:** Remove a parking space
- **Q:** Save and quit

### 4. Run the detection system
```bash
python main.py
```
- **Q:** Quit
- **+/-:** Adjust threshold value
- **D:** Toggle debug mode (shows preprocessing output)

---

## ⚙️ How It Works

The system processes each video frame through the following pipeline:

1. **Grayscale Conversion** — Reduces to single channel
2. **Gaussian Blur (5×5)** — Removes noise
3. **Adaptive Thresholding** — Handles varying illumination
4. **Median Filter (5×5)** — Removes salt-and-pepper noise
5. **Morphological Dilation (3×3)** — Fills gaps in binary image

For each parking space, the system counts white pixels in the ROI:
- **Pixel count < Threshold** → ✅ Vacant (green)
- **Pixel count ≥ Threshold** → 🔴 Occupied (red)

---

## 📊 Results

| Metric | Value |
|--------|-------|
| Total parking spaces | 69 |
| Threshold value | 250 |
| ROI dimensions | 90 × 45 px |
| Detection accuracy | ~100% |

---

## 📸 Screenshots

### Parking Space Selection
![Picker](https://github.com/user-attachments/assets/0b16d3ad-acd0-42d4-b0e1-172bd5097c81)

### Detection Result
![Detection](https://github.com/user-attachments/assets/e48c7d54-b61d-4cb3-8e01-78f0d8444176)

### Debug Mode (Preprocessing)
![Debug](https://github.com/user-attachments/assets/5a95058d-da9c-49ab-87e5-3ebf5957b8ec)

---

## 📚 References

1. de Almeida, P.R.L. et al. (2015). *PKLot – A robust dataset for parking lot classification.* Expert Systems with Applications, 42(11), 4937-4949.
2. Amato, G. et al. (2017). *Deep learning for decentralized parking lot occupancy detection.* Expert Systems with Applications, 72, 327-334.
3. True, N. (2007). *Vacant parking space detection in static images.* University of California San Diego.

---

## 📄 License

This project was developed for educational purposes as part of the Image and Video Processing course (2025-2026 Academic Year).

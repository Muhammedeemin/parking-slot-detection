"""
Gercek Zamanli Park Yeri Tespit Sistemi
(Real-Time Parking Slot Detection using OpenCV)
================================================

Yazarlar: Irem ACINAN, Muhammed Emin AKBULUT
Ders: Image and Video Processing - 2025-2026
"""

import cv2
import pickle
import numpy as np
import os
import sys

# ============================================================
# AYARLAR
# ============================================================
VIDEO_PATH = "carPark.mp4"
POSITIONS_FILE = "CarParkPositions"

WIDTH = 90
HEIGHT = 33

THRESHOLD = 250

GAUSSIAN_BLUR_KERNEL = (5, 5)
MEDIAN_BLUR_KERNEL = 5
ADAPTIVE_BLOCK_SIZE = 25
ADAPTIVE_C = 16
DILATE_KERNEL = np.ones((3, 3), np.uint8)
DILATE_ITERATIONS = 1

COLOR_FREE = (0, 255, 0)
COLOR_OCCUPIED = (0, 0, 255)
RECT_THICKNESS = 2
FONT = cv2.FONT_HERSHEY_SIMPLEX

# ============================================================


def load_positions():
    if not os.path.isfile(POSITIONS_FILE):
        print(f"[HATA] Pozisyon dosyasi bulunamadi: {POSITIONS_FILE}")
        print("Once parking_space_picker.py calistirarak park yerlerini belirleyin.")
        sys.exit(1)
    with open(POSITIONS_FILE, "rb") as f:
        pos_list = pickle.load(f)
    print(f"[BILGI] {len(pos_list)} park yeri pozisyonu yuklendi.")
    return pos_list


def preprocess_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, GAUSSIAN_BLUR_KERNEL, 1)
    thresh = cv2.adaptiveThreshold(
        blurred, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        ADAPTIVE_BLOCK_SIZE, ADAPTIVE_C
    )
    median = cv2.medianBlur(thresh, MEDIAN_BLUR_KERNEL)
    dilated = cv2.dilate(median, DILATE_KERNEL, iterations=DILATE_ITERATIONS)
    return dilated


def check_parking_space(processed_frame, pos_list, threshold):
    results = []
    free_count = 0
    for pos in pos_list:
        x, y = pos
        roi = processed_frame[y:y + HEIGHT, x:x + WIDTH]
        pixel_count = cv2.countNonZero(roi)
        is_free = pixel_count < threshold
        if is_free:
            free_count += 1
        results.append((pos, pixel_count, is_free))
    return results, free_count


def draw_results(frame, results, free_count, total_count):
    for pos, pixel_count, is_free in results:
        x, y = pos
        color = COLOR_FREE if is_free else COLOR_OCCUPIED
        cv2.rectangle(frame, (x, y), (x + WIDTH, y + HEIGHT), color, RECT_THICKNESS)
        cv2.putText(frame, str(pixel_count), (x + 5, y + HEIGHT - 5),
                    FONT, 0.4, color, 1)

    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (400, 60), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
    info_text = f"Bos: {free_count} / {total_count}"
    cv2.putText(frame, info_text, (15, 40), FONT, 0.8, (255, 255, 255), 2)
    return frame


def main():
    print("=" * 60)
    print("  GERCEK ZAMANLI PARK YERI TESPIT SISTEMI")
    print("=" * 60)

    pos_list = load_positions()
    total_count = len(pos_list)

    if not os.path.isfile(VIDEO_PATH):
        print(f"[HATA] Video dosyasi bulunamadi: {VIDEO_PATH}")
        sys.exit(1)

    cap = cv2.VideoCapture(VIDEO_PATH)
    if not cap.isOpened():
        print("[HATA] Video acilamadi.")
        sys.exit(1)

    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"[BILGI] Video: {VIDEO_PATH}")
    print(f"[BILGI] FPS: {fps:.1f}, Toplam Kare: {total_frames}")
    print(f"[BILGI] 'q' ile cikis | '+'/'-' ile esik ayari | 'd' ile debug modu")
    print("=" * 60)

    threshold = THRESHOLD
    show_debug = False
    frame_count = 0

    window_name = "Park Yeri Tespit Sistemi"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    while True:
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        frame_count += 1
        processed = preprocess_frame(frame)
        results, free_count = check_parking_space(processed, pos_list, threshold)
        output = draw_results(frame, results, free_count, total_count)

        cv2.putText(output, f"Kare: {frame_count}  Esik: {threshold}",
                    (10, output.shape[0] - 15), FONT, 0.5, (200, 200, 200), 1)

        cv2.imshow(window_name, output)

        if show_debug:
            h, w = processed.shape[:2]
            small = cv2.resize(processed, (w // 2, h // 2))
            cv2.imshow("On Isleme Sonucu (Debug)", small)

        key = cv2.waitKey(25) & 0xFF
        if key == ord("q"):
            break
        elif key == ord("+") or key == ord("="):
            threshold += 50
            print(f"[AYAR] Esik: {threshold}")
        elif key == ord("-") or key == ord("_"):
            threshold = max(50, threshold - 50)
            print(f"[AYAR] Esik: {threshold}")
        elif key == ord("d"):
            show_debug = not show_debug
            if not show_debug:
                cv2.destroyWindow("On Isleme Sonucu (Debug)")

    cap.release()
    cv2.destroyAllWindows()
    print("[BILGI] Program sonlandirildi.")


if __name__ == "__main__":
    main()
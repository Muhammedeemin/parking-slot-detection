"""
Park Yeri Secici (Parking Space Picker)
=======================================
Bu script, otopark videosunun ilk karesini alir ve kullanicinin
fare ile park yerlerini isaretlemesini saglar.

Kullanim:
  - Sol tikla: Yeni park yeri ekle (sol ust kose)
  - Sag tikla: Son eklenen park yerini sil
  - 'q' tusu: Kaydet ve cik
  - 's' tusu: Kaydet (cikmadan)

Her park yeri sabit genislik x yukseklik dikdortgen olarak eklenir.
Boyutlari asagidaki WIDTH ve HEIGHT degiskenlerinden ayarlayabilirsiniz.

Yazarlar: Irem ACINAN, Muhammed Emin AKBULUT
Ders: Image and Video Processing - 2025-2026
"""

import cv2
import pickle
import os

# ============================================================
# AYARLAR - Park yeri dikdortgen boyutlari
# Videonuza gore bu degerleri ayarlayin
# ============================================================
WIDTH = 90  # Park yeri genisligi (piksel)
HEIGHT = 33    # Park yeri yuksekligi (piksel)

# Dosya yollari
VIDEO_PATH = "carPark.mp4"           # Otopark videosu
POSITIONS_FILE = "CarParkPositions"     # Kayit dosyasi (pickle)

# ============================================================

def load_positions():
    """Daha once kaydedilmis park yeri pozisyonlarini yukle."""
    if os.path.isfile(POSITIONS_FILE):
        with open(POSITIONS_FILE, "rb") as f:
            return pickle.load(f)
    return []


def save_positions(pos_list):
    """Park yeri pozisyonlarini dosyaya kaydet."""
    with open(POSITIONS_FILE, "wb") as f:
        pickle.dump(pos_list, f)
    print(f"[BILGI] {len(pos_list)} park yeri kaydedildi.")


def mouse_callback(event, x, y, flags, param):
    """
    Fare olaylari:
      Sol tikla  -> park yeri ekle
      Sag tikla  -> o noktadaki park yerini sil
    """
    pos_list = param

    if event == cv2.EVENT_LBUTTONDOWN:
        pos_list.append((x, y))
        print(f"[+] Park yeri eklendi: ({x}, {y})  |  Toplam: {len(pos_list)}")

    elif event == cv2.EVENT_RBUTTONDOWN:
        # Tiklanan noktanin icinde olan dikdortgeni bul ve sil
        for i, pos in enumerate(pos_list):
            px, py = pos
            if px < x < px + WIDTH and py < y < py + HEIGHT:
                pos_list.pop(i)
                print(f"[-] Park yeri silindi: ({px}, {py})  |  Toplam: {len(pos_list)}")
                break


def main():
    # Pozisyonlari yukle
    pos_list = load_positions()

    # Videodan ilk kareyi al
    if not os.path.isfile(VIDEO_PATH):
        print(f"[HATA] Video dosyasi bulunamadi: {VIDEO_PATH}")
        print("Lutfen VIDEO_PATH degiskenini dogru video yoluna ayarlayin.")
        return

    cap = cv2.VideoCapture(VIDEO_PATH)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("[HATA] Video okunamadi.")
        return

    # Pencere ve fare callback
    window_name = "Park Yeri Secici - Sol:Ekle | Sag:Sil | Q:Kaydet&Cik"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.setMouseCallback(window_name, mouse_callback, pos_list)

    print("=" * 60)
    print("  PARK YERI SECICI")
    print("=" * 60)
    print("  Sol tikla  : Park yeri ekle")
    print("  Sag tikla  : Park yeri sil")
    print("  's' tusu   : Kaydet")
    print("  'q' tusu   : Kaydet ve cik")
    print(f"  Mevcut park yeri sayisi: {len(pos_list)}")
    print("=" * 60)

    while True:
        # Her karede dikdortgenleri ciz
        img = frame.copy()
        for i, pos in enumerate(pos_list):
            x, y = pos
            cv2.rectangle(img, (x, y), (x + WIDTH, y + HEIGHT), (255, 0, 255), 2)
            # Park yeri numarasini yaz
            cv2.putText(img, str(i + 1), (x + 5, y + 15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 0), 1)

        # Bilgi metni
        info_text = f"Park Yerleri: {len(pos_list)}  |  Sol:Ekle  Sag:Sil  Q:Cik"
        cv2.putText(img, info_text, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.imshow(window_name, img)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            save_positions(pos_list)
            break
        elif key == ord("s"):
            save_positions(pos_list)

    cv2.destroyAllWindows()
    print("[BILGI] Program sonlandirildi.")


if __name__ == "__main__":
    main()

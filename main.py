import json
import os
import tkinter as tk
from nlp_processor import metni_temizle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# gui.py dosyasındaki arayüz sınıfımızı buraya dahil ediyoruz
try:
    from gui import IntihalUygulamasi
except ImportError:
    IntihalUygulamasi = None

def terminal_intihal_kontrol_sistemi():
    print("\n--- PlagiarismDetectorNLP: Terminal İntihal Tespit Sistemi ---")
    
    json_yolu = 'makaleler.json'
    if not os.path.exists(json_yolu):
        print("Hata: 'makaleler.json' dosyası bulunamadı! Lütfen önce scraper.py dosyasını çalıştırın.")
        return

    with open(json_yolu, 'r', encoding='utf-8') as f:
        makale_havuzu = json.load(f)
    
    print(f"Sistem aktif: Veri havuzunda {len(makale_havuzu)} adet resmi makale ve özet yüklenmiş durumda.")

    test_metni = input("\nKontrol etmek istediğiniz metni/cümleyi girin: ")
    if not test_metni.strip():
        print("Boş metin girilemez.")
        return

    temiz_test_metni = metni_temizle(test_metni)
    
    temiz_makaleler = []
    for makale in makale_havuzu:
        temiz_makaleler.append(metni_temizle(makale['tam_metin']))

    tum_metinler = [temiz_test_metni] + temiz_makaleler
    
    vectorizer = TfidfVectorizer()
    tfidf_matrisi = vectorizer.fit_transform(tum_metinler)
    
    benzerlik_skorlari = cosine_similarity(tfidf_matrisi[0:1], tfidf_matrisi[1:]).flatten()

    en_yuksek_benzerlik_orani = 0
    en_benzer_makale = None

    for index, skor in enumerate(benzerlik_skorlari):
        if skor > en_yuksek_benzerlik_orani:
            en_yuksek_benzerlik_orani = skor
            en_benzer_makale = makale_havuzu[index]

    print("\n" + "="*50)
    print("AKADEMİK ANALİZ SONUÇLARI")
    print("="*50)
    
    yuzde_skor = en_yuksek_benzerlik_orani * 100

    if yuzde_skor > 0:
        print(f"Girdiğiniz Metin: '{test_metni}'")
        print(f"\nEn Benzer Akademik Yayın: '{en_benzer_makale['baslik']}'")
        print(f"Yayın Kaynağı: {en_benzer_makale['kaynak']}")
        print(f"Eşleşen Makale Özeti (Abstract): {en_benzer_makale['ozet'][:150]}...")
        print(f"\nMatematiksel Benzerlik Oranı: %{yuzde_skor:.2f}")
    else:
        print("Veri havuzundaki makale ve özetlerle hiçbir benzerlik bulunamadı (Benzerlik Oranı: %0.00).")
    print("="*50)

if __name__ == "__main__":
    print("--- PlagiarismDetectorNLP Yönetim Merkezi ---")
    print("1 - Programı Grafiksel Arayüz (GUI) ile Başlat")
    print("2 - Programı Konsol / Terminal Modunda Başlat")
    
    secim = input("\nLütfen çalıştırma modunu seçin (1 veya 2): ").strip()
    
    if secim == "1":
        if IntihalUygulamasi is not None:
            print("\nGörsel arayüz başlatılıyor...")
            root = tk.Tk()
            app = IntihalUygulamasi(root)
            root.mainloop()
        else:
            print("\nHata: 'gui.py' dosyası bulunamadı! Terminal moduna yönlendiriliyorsunuz...")
            terminal_intihal_kontrol_sistemi()
    elif secim == "2":
        terminal_intihal_kontrol_sistemi()
    else:
        print("\nGeçersiz seçim yapıldı. Varsayılan olarak Görsel Arayüz başlatılıyor...")
        if IntihalUygulamasi is not None:
            root = tk.Tk()
            app = IntihalUygulamasi(root)
            root.mainloop()
        else:
            terminal_intihal_kontrol_sistemi()
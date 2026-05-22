import json
import os
import tkinter as tk
from tkinter import messagebox, scrolledtext
from nlp_processor import metni_temizle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class IntihalUygulamasi:
    def __init__(self, root):
        self.root = root
        self.root.title("PlagiarismDetectorNLP - Grafiksel İntihal Ekranı")
        self.root.geometry("700x550")
        self.root.configure(bg="#f4f6f9")

        # Yerel diskteki makale havuzunu yükle
        self.makale_havuzu = self.verileri_yukle()

        # Arayüz Elemanlarını Oluşturma
        self.arayuz_tasarla()

    def verileri_yukle(self):
        json_yolu = 'makaleler.json'
        if not os.path.exists(json_yolu):
            messagebox.showerror("Hata", "'makaleler.json' bulunamadı!\nLütfen önce scraper.py dosyasını çalıştırın.")
            return []
        with open(json_yolu, 'r', encoding='utf-8') as f:
            return json.load(f)

    def arayuz_tasarla(self):
        # Üst Başlık
        baslik_label = tk.Label(self.root, text="PlagiarismDetectorNLP - Görsel Arayüz", font=("Helvetica", 14, "bold"), bg="#f4f6f9", fg="#2c3e50")
        baslik_label.pack(pady=10)

        # Havuz Bilgisi
        havuz_text = f"Sistem Aktif: Veri havuzunda {len(self.makale_havuzu)} adet resmi makale ve özet yüklü."
        havuz_label = tk.Label(self.root, text=havuz_text, font=("Helvetica", 10, "italic"), bg="#f4f6f9", fg="#7f8c8d")
        havuz_label.pack(pady=5)

        # Giriş Alanı Etiketi
        giris_label = tk.Label(self.root, text="Kontrol Etmek İstediğiniz Metni / Cümleyi Giriniz:", font=("Helvetica", 11, "bold"), bg="#f4f6f9", fg="#34495e")
        giris_label.pack(pady=5, anchor="w", padx=40)

        # Metin Giriş Kutusu
        self.input_text = scrolledtext.ScrolledText(self.root, width=80, height=6, font=("Helvetica", 10))
        self.input_text.pack(pady=5, padx=40)

        # Analiz Et Butonu
        analiz_butonu = tk.Button(self.root, text="Arayüz Üzerinden İntihal Analizi Yap", font=("Helvetica", 11, "bold"), bg="#3498db", fg="white", bd=0, padx=20, pady=8, command=self.analiz_et)
        analiz_butonu.pack(pady=15)

        # Sonuç Alanı Etiketi
        sonuc_label = tk.Label(self.root, text="Arayüz Analiz Sonuçları:", font=("Helvetica", 11, "bold"), bg="#f4f6f9", fg="#34495e")
        sonuc_label.pack(pady=5, anchor="w", padx=40)

        # Sonuç Gösterim Kutusu
        self.output_text = scrolledtext.ScrolledText(self.root, width=80, height=12, font=("Helvetica", 10), bg="#ffffff", fg="#2c3e50")
        self.output_text.pack(pady=5, padx=40)
        self.output_text.config(state=tk.DISABLED)

    def analiz_et(self):
        test_metni = self.input_text.get("1.0", tk.END).strip()
        
        if not test_metni:
            messagebox.showwarning("Uyarı", "Lütfen analiz edilecek bir metin girin.")
            return

        if not self.makale_havuzu:
            messagebox.showerror("Hata", "Veri havuzu boş. Analiz yapılamaz.")
            return

        temiz_test_metni = metni_temizle(test_metni)
        
        temiz_makaleler = []
        for makale in self.makale_havuzu:
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
                en_benzer_makale = self.makale_havuzu[index]

        yuzde_skor = en_yuksek_benzerlik_orani * 100

        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)

        sonuc_raporu = f"Girdiğiniz Metin:\n'{test_metni}'\n\n"
        sonuc_raporu += "="*65 + "\n"
        
        if yuzde_skor > 0:
            sonuc_raporu += f"En Benzer Akademik Yayın: {en_benzer_makale['baslik']}\n\n"
            sonuc_raporu += f"Yayın Kaynağı: {en_benzer_makale['kaynak']}\n\n"
            sonuc_raporu += f"Eşleşen Makale Özeti (Abstract):\n{en_benzer_makale['ozet'][:200]}...\n\n"
            sonuc_raporu += f"Matematiksel Benzerlik Oranı: %{yuzde_skor:.2f}\n"
        else:
            sonuc_raporu += "Veri havuzundaki makale ve özetlerle hiçbir benzerlik saptanmadı.\n"
            sonuc_raporu += "Matematiksel Benzerlik Oranı: %0.00\n"
            
        sonuc_raporu += "="*65

        self.output_text.insert(tk.END, sonuc_raporu)
        self.output_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = IntihalUygulamasi(root)
    root.mainloop()
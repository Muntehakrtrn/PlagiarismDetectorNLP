import requests
from bs4 import BeautifulSoup
import json
import os
import time

print("PlagiarismDetectorNLP - 'konular.txt' + IEEE Entegreli Havuz Büyütücü Aktif.")

def doaj_api_ile_cek(arama_terimi):
    biçimlendirilmiş_terim = arama_terimi.strip().replace(" ", "%20")
    url = f"https://doaj.org/api/v3/search/articles/(bibjson.title:%22{biçimlendirilmiş_terim}%22)?pageSize=50"
    
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            veri = response.json()
            makale_listesi = veri.get("results", [])
            
            makaleler = []
            for item in makale_listesi:
                bibjson = item.get("bibjson", {})
                baslik = bibjson.get("title", "").strip()
                ozet = bibjson.get("abstract", "").strip()
                
                if baslik:
                    makaleler.append({
                        "id": 0,
                        "kaynak": f"DOAJ API ({arama_terimi.title()})",
                        "baslik": baslik,
                        "ozet": ozet,
                        "tam_metin": f"{baslik} {ozet}"
                    })
            return makaleler
        else:
            return []
    except Exception:
        return []

def ieee_kaynagindan_cek():
    url = "https://spectrum.ieee.org/feeds/topic/computing.rss"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    print("\n[IEEE] Resmi veri kaynağından güncel teknoloji ve mühendislik akışı çekiliyor...")
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'xml')
            maddeler = soup.find_all('item')
            
            makaleler = []
            for madde in maddeler:
                baslik = madde.find('title').text.strip() if madde.find('title') else ""
                ozet = madde.find('description').text.strip() if madde.find('description') else ""
                
                if ozet:
                    # İçindeki olası HTML etiketlerini arındırıyoruz
                    ozet = BeautifulSoup(ozet, "html.parser").text.strip()
                
                if baslik:
                    makaleler.append({
                        "id": 0,
                        "kaynak": "IEEE (Teknoloji/Mühendislik)",
                        "baslik": baslik,
                        "ozet": ozet,
                        "tam_metin": f"{baslik} {ozet}"
                    })
            print(f"[IEEE] Bağlantı başarılı! {len(makaleler)} adet güncel yayın süzüldü.")
            return makaleler
        else:
            print(f"[IEEE] Bağlantı hatası. Hata kodu: {response.status_code}")
            return []
    except Exception as e:
        print(f"[IEEE] Teknik hata oluştu: {e}")
        return []

def konulari_txt_dosyasindan_oku():
    txt_yolu = 'konular.txt'
    if not os.path.exists(txt_yolu):
        varsayilanlar = ["computer science", "cyber security", "fpga"]
        with open(txt_yolu, 'w', encoding='utf-8') as f:
            for v in varsayilanlar:
                f.write(v + "\n")
        return varsayilanlar
    
    with open(txt_yolu, 'r', encoding='utf-8') as f:
        konular = [satir.strip() for satir in f.readlines() if satir.strip()]
    return konular

if __name__ == "__main__":
    # 1. Aşama: Konuları harici dosyadan oku
    DURMAKSIZIN_GELISEN_KONULAR = konulari_txt_dosyasindan_oku()
    
    json_yolu = 'makaleler.json'
    mevcut_veriler = []
    
    # Eskileri koruma altına alıyoruz
    if os.path.exists(json_yolu):
        with open(json_yolu, 'r', encoding='utf-8') as f:
            try:
                mevcut_veriler = json.load(f)
            except:
                mevcut_veriler = []
                
    print(f"Mevcut Havuz Durumu: Veri tabanınızda {len(mevcut_veriler)} adet makale kayıtlı.")
    
    # 2. Aşama: DOAJ API üzerinden txt konularını çek
    print(f"\n--- DOAJ API TARAMASI ({len(DURMAKSIZIN_GELISEN_KONULAR)} Konu) ---")
    internet_havuzu = []
    
    for sira, alan in enumerate(DURMAKSIZIN_GELISEN_KONULAR, 1):
        print(f"[{sira}/{len(DURMAKSIZIN_GELISEN_KONULAR)}] '{alan}' aranıyor...", end="", flush=True)
        yakalananlar = doaj_api_ile_cek(alan)
        internet_havuzu.extend(yakalananlar)
        print(f" -> {len(yakalananlar)} sonuç toplandı.")
        time.sleep(1)
        
    # 3. Aşama: IEEE Canlı Akışını Çek
    print("\n--- IEEE CANLI AKIŞ TARAMASI ---")
    ieee_yayinlari = ieee_kaynagindan_cek()
    internet_havuzu.extend(ieee_yayinlari)
    
    # 4. Aşama: Birleştirme ve Mükerrer Kontrolü
    eklenen_sayisi = 0
    baslangic_id = len(mevcut_veriler) + 1
    
    for makale in internet_havuzu:
        # Başlık bazında mükerrer kontrolü
        durum_var_mi = any(d['baslik'].lower().strip() == makale['baslik'].lower().strip() for d in mevcut_veriler)
        
        if not durum_var_mi:
            makale["id"] = baslangic_id
            mevcut_veriler.append(makale)
            baslangic_id += 1
            eklenen_sayisi += 1
            
    # Dev listeyi JSON'a yazma
    with open(json_yolu, 'w', encoding='utf-8') as f:
        json.dump(mevcut_veriler, f, ensure_ascii=False, indent=4)
        
    print("\n" + "="*50)
    print("MİMARİ ENTEGRASYON TAMAMLANDI!")
    print("="*50)
    print(f"-> Havuza eklenen yeni benzersiz yayın: {eklenen_sayisi}")
    print(f"-> TOPLAM GÜNCEL HAVUZ BOYUTU: {len(mevcut_veriler)} MAKALE.")
    print("="*50)
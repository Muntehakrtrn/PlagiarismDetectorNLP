# Mini İntihal Tespit Yazılımı (PlagiarismDetectorNLP)

Bu proje, Doğal Dil İşleme (NLP) tekniklerini kullanarak akademik literatür taraması yapan, internet üzerinden veri toplayan ve metin benzerlik analizi gerçekleştiren modüler bir intihal tespit yazılımıdır.

## Proje Gereksinimleri ve Karşılanma Durumu

1. **Web'den Makale Çekme:** `scraper.py` modülü aracılığıyla resmi DOAJ API entegrasyonu ve IEEE Spectrum akademik veri akışları (RSS) dinamik olarak taranır. `konular.txt` yapılandırma dosyası üzerinden yeni arama terimleri koda müdahale edilmeden eklenebilir.
2. **Makaleleri Uygun Şekilde Saklama:** Çekilen tüm akademik yayınlar, veri bütünlüğü korunarak ve mükerrer kayıt kontrolü (duplicate check) yapılarak yerel depolama ortamında (`makaleler.json`) NoSQL formatında hafif ve taşınabilir olarak saklanır. Güncellemelerde eski veriler silinmez.
3. **Bilgi Çıkarımı (Metin Ön İşleme):** `nlp_processor.py` katmanı ile ham metinler üzerinde büyük/küçük harf dönüşümü, noktalama işaretlerinin temizlenmesi ve stop-words (anlamsız kelimeler) ayıklama işlemleri uygulanarak yapılandırılmış öznitelikler çıkarılır. Tarama işlemi makalelerin özet (abstract) metinlerini kapsar.
4. **Benzer Olan Makaleleri Bulma ve Benzerlik Oranı Çıkarma:** `main.py` motoru bünyesinde geliştirilen TF-IDF (Term Frequency-Inverse Document Frequency) vektör modeli ve Kosinüs Benzerliği (Cosine Similarity) algoritması sayesinde, girilen metinler ile veri havuzundaki makaleler karşılaştırılarak matematiksel ve nesnel yüzdelik oranlar çıkarılır.

## Sistem Mimarisi ve Dosya Yapısı

* **`nlp_processor.py`**: Metin temizleme, tokenizasyon ve bilgi çıkarımı süreçlerini yürüten NLP katmanı.
* **`scraper.py`**: DOAJ API ve IEEE kaynaklarından dinamik, asenkron ve kümülatif veri toplayan modül.
* **`main.py`**: TF-IDF tabanlı matematiksel intihal analiz motoru.
* **`gui.py`**: Kullanıcının ve değerlendiricinin sistemi test etmesini sağlayan grafiksel masaüstü arayüzü (Tkinter).
* **`konular.txt`**: Sistemin çalışma kapsamını genişleten dinamik arama terimleri listesi.
* **`makaleler.json`**: Yapılandırılmış akademik makale veri havuzu veri tabanı.

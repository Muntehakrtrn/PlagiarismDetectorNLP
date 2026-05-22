import string
import nltk
from nltk.corpus import stopwords

# İlk çalıştırmada stop words paketini bilgisayarımıza indirmek için bu satırları ekliyoruz
nltk.download('stopwords', quiet=True)

def metni_temizle(metin):
    # 1. Hepsini küçük harfe çeviriyoruz
    metin = metin.lower()
    
    # 2. Noktalama işaretlerini kaldırıyoruz
    metin = metin.translate(str.maketrans('', '', string.punctuation))
    
    # 3. İngilizce stop words (etkisiz kelimeler) listesini alıyoruz
    durma_kelimeleri = set(stopwords.words('english'))
    
    # 4. Metni kelimelerine ayırıp, stop words olmayanları seçiyoruz
    kelimeler = metin.split()
    temiz_kelimeler = [kelime for kelime in kelimeler if kelime not in durma_kelimeleri]
    
    # Temizlenmiş kelimeleri tekrar birleştirip tek bir metin haline getiriyoruz
    return " ".join(temiz_kelimeler)

# Test etmek için alt kısım
if __name__ == "__main__":
    ornek_metin = "The Artificial Intelligence in Computer Science and Engineering!"
    print("Ham Metin:", ornek_metin)
    print("Temizlenmiş Metin:", metni_temizle(ornek_metin))
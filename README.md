# MindLaw - Türk Hukuku Üzerine Eğitilmiş Chatbot

MindLaw, T5 modeli kullanılarak Türk hukuku üzerine eğitilmiş bir chatbot projesidir. Bu proje, kullanıcıların Türk hukuku ile ilgili sorularına doğru ve hızlı yanıtlar vermeyi amaçlamaktadır.

![image](https://user-images.githubusercontent.com/your-image.png)

[![Kaggle](http://img.shields.io/static/v1?logo=kaggle&style=plastic&color=blue&label=kaggle&labelColor=grey&message=notebooks)](https://www.kaggle.com/code/your-kaggle)

# Projenin Motivasyonu

Türk hukuk sistemine ilişkin doğru bilgiye hızlı erişim sağlamak amacıyla bu projeyi geliştirdik. Projemiz, Türkiye'nin çeşitli hukuk kaynaklarından elde edilen verilerle oluşturulmuştur. Veri seti, Türk Anayasası ve diğer yasal belgelerden derlenmiştir. Bu kapsamlı veri seti, Türk hukuku üzerine daha önce açık kaynak olarak mevcut olmayan bir veri setini sunmaktadır.

# Örnek

![Sample](https://user-images.githubusercontent.com/your-sample.png)

# Modelin Detayları

Proje iki ana bileşenden oluşur: image encoder ve text decoder. Image encoder, verilen resmi 512 uzunluğunda bir vektöre dönüştürür. Bu vektör, resimdeki önemli detayları içerir. Oluşturulan bu vektör, text decoder'a verilmek üzere başka bir model tarafından genişletilir. Text decoder modeli, bu vektöre bakarak yeni bir metin oluşturur. Bu metin, modelin resimde gördüklerini ifade eder.

| ![Model Schema](https://user-images.githubusercontent.com/your-model-schema.png) |
|:--:|
| Model Şeması |

Projede, Türkçe verilerle eğitilmiş GPT-2 modeli kullanılmıştır. Image encoder olarak OpenAI'ın CLIP modeli kullanılmıştır.

## Kullanım

Projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyin:

1. Bu projeyi klonlayın:
   ```sh
   git clone https://github.com/kullanici-adi/mindlaw.git
   ```

2. Gerekli bağımlılıkları yükleyin:
   ```sh
   cd mindlaw
   pip install -r requirements.txt
   ```

3. Chatbot'u başlatın:
   ```sh
   python run_chatbot.py
   ```

# Gelecek Hedefler

1. Veriyi genişletmek.
2. Modelin videoları daha iyi anlaması için video encoder modeli kullanmak.
3. Projenin mobil uygulama olarak kullanılabilir hale getirilmesi.
4. Giyilebilir teknoloji ile projeyi hayata geçirmek.

## Lisans

Bu proje MIT Lisansı ile lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakabilirsiniz.

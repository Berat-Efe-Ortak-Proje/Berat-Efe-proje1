# Öğrenci Kulüp Yönetim Sistemi

Flask ile yazılmış, öğrenci kulüplerinin yönetimini kolaylaştıran bir web uygulamasıdır.

## Özellikler

- Kullanıcı kayıt ve giriş
- Kulüp oluşturma ve yönetimi
- Etkinlik planlama ve yönetimi
- Üye takibi
- Etkinlik katılımcı listesi

## Kurulum

1. Python 3.8+ yükleyin
2. Repository'yi klonlayın
3. Sanal ortam oluşturun:
   ```bash
   python -m venv venv
   ```

4. Sanal ortamı etkinleştirin (Windows):
   ```bash
   venv\Scripts\activate
   ```

5. Gerekli paketleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

## Kullanım

Uygulamayı başlatmak için:

```bash
python run.py
```

Tarayıcıda `http://localhost:5000` adresine gidin.

## Veritabanı

Proje SQLite veritabanı kullanmaktadır. İlk çalıştırmada otomatik olarak oluşturulur.

## Geliştirme

Kod geliştirme sırasında debug modu etkindir.

## Lisans

MIT License

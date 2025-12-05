# Kulüp Yönetim Sistemi

Flask ile geliştirilmiş bir öğrenci kulüp yönetim uygulaması.

## 🎯 Özellikler

- 👤 Kullanıcı kayıt ve giriş sistemi
- 📚 Kulüp oluşturma ve yönetimi
- 🎯 Etkinlik planlama ve takibi
- 👥 Üyelik yönetimi
- 📅 Etkinlik katılımcı listesi
- 🎨 Modern Bootstrap 5 arayüzü

## 🛠️ Teknolojiler

- **Backend**: Flask 2.3.0
- **Veritabanı**: SQLAlchemy (SQLite lokal, PostgreSQL Render'da)
- **Kimlik Doğrulama**: Flask-Login
- **Frontend**: Bootstrap 5, Jinja2
- **Sunucu**: Gunicorn (Render production)

## 📦 Lokal Kurulum

### Gereksinimler
- Python 3.8+
- pip

### Adımlar

1. **Depoyu klonla:**
```bash
git clone https://github.com/Berat-Efe-Ortak-Proje/Berat-Efe-proje1.git
cd Berat-Efe-proje1/1
```

2. **Virtual environment oluştur:**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. **Bağımlılıkları yükle:**
```bash
pip install -r requirements.txt
```

4. **Uygulamayı çalıştır:**
```bash
python run.py
```

5. **Tarayıcıda aç:**
```
http://localhost:5000
```

## 🚀 Render'da Dağıtım

### Ön Koşullar
- GitHub hesabı
- Render hesabı (render.com)

### Adım Adım Kurulum

#### 1. Repository Hazırlığı
Aşağıdaki dosyalar zaten eklenmiştir:
- ✅ `Procfile` - Web işlemi tanımı
- ✅ `requirements.txt` - Python bağımlılıkları  
- ✅ `.env.example` - Çevresel değişken şablonu

#### 2. Render Hesabı Oluştur
1. [render.com](https://render.com) adresine git
2. GitHub hesabınızla oturum aç / kayıt ol

#### 3. Yeni Web Servisi Oluştur
1. Dashboard'da **New +** → **Web Service** tıkla
2. GitHub repositorynizi seç (`Berat-Efe-proje1`)
3. Bağla ve aşağıdaki ayarları yap:

   | Ayar | Değer |
   |------|-------|
   | **Name** | `klub-yonetim-sistemi` |
   | **Environment** | `Python 3` |
   | **Build Command** | `pip install -r requirements.txt` |
   | **Start Command** | `gunicorn run:app` |
   | **Root Directory** | `1` |

#### 4. Çevresel Değişkenleri Ayarla
Dashboard'da **Environment** bölümüne ekle:

```env
SECRET_KEY=your-very-secret-key-here-make-it-random
FLASK_ENV=production
```

Secret key için (terminal'de):
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

#### 5. Deploy Et
1. **Create Web Service** tıkla
2. Render otomatik olarak deploy edecek (~2-3 dakika)
3. Tamamlandığında URL verilecek (örn: `https://klub-yonetim-sistemi.onrender.com`)

## 💡 Kullanım

### Kayıt ve Giriş
1. Ana sayfada **Kayıt Ol** tıkla
2. Kullanıcı adı, email ve şifre gir
3. **Giriş Yap** sayfasından oturum aç

### Kulüp Oluşturma
1. Giriş yaptıktan sonra **Kulüp Oluştur** tıkla
2. Kulüp adı ve açıklaması gir
3. **Kulüp Oluştur** butonuna tıkla

### Etkinlik Oluşturma
1. Kulüp detay sayfasına git
2. **Yeni Etkinlik Oluştur** tıkla
3. Etkinlik bilgilerini doldur (adı, açıklama, tarih, yer)
4. **Oluştur** tıkla

## 📁 Proje Yapısı

```
1/
├── app/
│   ├── __init__.py              # Flask app fabrikası
│   ├── models.py                # Veritabanı modelleri
│   ├── routes.py                # API route'ları
│   ├── static/
│   │   └── css/
│   │       └── style.css        # CSS stil dosyaları
│   └── templates/
│       ├── base.html            # Taban template
│       ├── index.html           # Ana sayfa
│       ├── clubs.html           # Kulüpler sayfası
│       ├── club_detail.html     # Kulüp detayı
│       ├── create_club.html     # Kulüp oluşturma
│       ├── create_event.html    # Etkinlik oluşturma
│       ├── event_detail.html    # Etkinlik detayı
│       ├── login.html           # Giriş sayfası
│       └── register.html        # Kayıt sayfası
├── run.py                       # Uygulamayı başlat
├── Procfile                     # Render production config
├── requirements.txt             # Python bağımlılıkları
├── .env.example                 # Çevresel değişken şablonu
└── .gitignore                   # Git ignore kuralları
```

## 🐛 Sorun Giderme

### Render'da Veritabanı Hatası
SQLite Render'da sınırlı olabilir. PostgreSQL eklemek için:
1. Render dashboard'da **+ New** → **PostgreSQL**
2. Database oluştur
3. `DATABASE_URL` ortam değişkenine connection string ekle
4. Web Service'i restart et

### İlk Kullanıcı Oluştulamıyor
- Tarayıcı cache'i temizle
- Sayfayı yenile (F5)
- Şifre en az 1 karakter olmalı

### Assets Yüklenmiyor (CSS/JS)
- `static/` klasörünün doğru yolda olduğunu kontrol et
- Browser cache'i temizle
- Production'da `FLASK_ENV=production` olduğunu kontrol et

## 📝 Lisans

Bu proje eğitim amaçlı açık kaynak kodlu projedir.

## 👥 Katkıda Bulunma

Pull request'ler açıktan bekliyor!

MIT License

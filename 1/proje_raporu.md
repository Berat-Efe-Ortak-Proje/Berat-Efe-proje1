# Proje Geliştirme Süreci ve Teknik Kazanımlar Raporu

**Proje Adı:** Üniversite Kulüp Yönetim Sistemi
**Geliştirici:** Berat Efe
**Tarih:** 7 Aralık 2025

## 1. Proje Özeti
Bu proje, üniversite öğrencilerinin kampüs kulüplerini inceleyebileceği, etkinlikleri takip edebileceği ve kulüplere üye olabileceği dinamik bir web platformudur. Proje, modern web geliştirme standartlarına uygun olarak **Full Stack (Uçtan Uca)** bir yaklaşımla geliştirilmiş ve canlı sunucu ortamına (Render) başarıyla taşınmıştır.

## 2. Kullanılan Teknolojiler ve Araçlar
*   **Programlama Dili:** Python 3.x
*   **Web Framework:** Flask
*   **Veri Tabanı:** SQLite (Geliştirme), PostgreSQL (Canlı Ortam), SQLAlchemy (ORM)
*   **Frontend:** HTML5, CSS3, Jinja2 Template Engine
*   **Versiyon Kontrol:** Git & GitHub
*   **Sunucu & Deployment:** Render, Gunicorn

## 3. Temel Teknik Kazanımlar

### A. Backend Geliştirme (Sunucu Taraflı Programlama)
*   **Flask Mimarisi:** Modüler bir yapı kurmak için `Blueprint` yapısı kullanıldı. Uygulama başlatma süreci `Application Factory` deseni ile profesyonel hale getirildi.
*   **Routing ve HTTP Metotları:** Kullanıcı isteklerini (GET/POST) karşılayan ve dinamik yanıtlar üreten yönlendirme yapıları (`routes.py`) oluşturuldu.
*   **Oturum Yönetimi:** `Flask-Login` kütüphanesi entegre edilerek güvenli kullanıcı girişi, çıkışı ve yetkilendirme (Admin/Üye ayrımı) mekanizmaları kodlandı.

### B. Veri Tabanı Tasarımı ve Yönetimi
*   **ORM Kullanımı:** SQL sorguları yerine Python sınıfları (`User`, `Club`, `Event`) kullanılarak veri tabanı işlemleri soyutlandı.
*   **İlişkisel Veri Modeli:** Tablolar arasında **One-to-Many** (Bir kulübün çok etkinliği olması) ve **Many-to-Many** (Bir kullanıcının çok kulübe üye olması) ilişkileri kuruldu.
*   **Data Seeding (Veri Tohumlama):** Uygulama her başlatıldığında veri tabanının tutarlılığını sağlayan, eksik verileri tamamlayan ve hatalı kayıtları temizleyen otomatik algoritmalar geliştirildi.

### C. Güvenlik Uygulamaları
*   **Parola Güvenliği:** Kullanıcı şifreleri veri tabanında asla açık metin olarak saklanmadı; `Werkzeug` kütüphanesi ile hash'lenerek (şifrelenerek) kaydedildi.
*   **CSRF Koruması:** Form güvenliği için Flask-WTF ve CSRF token yapıları hakkında bilgi edinildi.

### D. Frontend Entegrasyonu (Arayüz Geliştirme)
*   **Dinamik İçerik Yönetimi:** Jinja2 şablon motoru kullanılarak, Python tarafındaki verilerin (kulüp listesi, resimler, kullanıcı adı) HTML sayfalarına dinamik olarak aktarılması sağlandı.
*   **Statik Dosya Yönetimi:** CSS stilleri ve kulüp görselleri gibi statik varlıkların proje yapısına entegrasyonu ve `url_for` fonksiyonu ile dinamik çağrılması öğrenildi.

### E. DevOps ve Yayına Alma (Deployment)
*   **Versiyon Kontrolü (Git):** Kod değişikliklerinin takibi, hata durumunda geri alma ve GitHub ile uzak sunucu senkronizasyonu süreçleri aktif olarak yönetildi.
*   **Canlı Ortam Yönetimi:** Lokal bilgisayarda çalışan proje, bulut tabanlı bir platforma (Render) taşındı. `requirements.txt` ile bağımlılık yönetimi ve `Gunicorn` ile uygulama sunucusu yapılandırması gerçekleştirildi.

## 4. Sonuç
Bu proje sayesinde, sadece kod yazma becerisi değil; bir yazılım ürününü **fikir aşamasından alıp, veri tabanı tasarımına, arayüz giydirmesine ve son kullanıcıya sunulmasına kadar geçen tüm yaşam döngüsü (SDLC)** deneyimlenmiştir. Karşılaşılan hatalar (Debugging) ve yapılan iyileştirmeler (Refactoring) ile problem çözme yetkinliği geliştirilmiştir.

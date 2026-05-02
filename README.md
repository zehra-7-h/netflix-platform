# 🎬 Netflix Platform — Masaüstü İçerik Yönetim Uygulaması

> PyQt6 + Microsoft SQL Server ile geliştirilmiş, Netflix ilhamı almış masaüstü içerik platformu.  
> Kullanıcı & yönetici rolleri, içerik keşfi, izleme geçmişi, favori listesi ve öneri sistemi içerir.

---

## Özellikler

### Kullanıcı Paneli
- **Giriş / Kayıt** — bcrypt ile şifrelenmiş kimlik doğrulama
- **Keşfet** — Tür, tip ve puana göre filtrelenebilir içerik arama
- **İçerik Detayı** — Program bilgisi, bölüm listesi, kullanıcı puanı
- **İzleme Geçmişi** — Tüm izlenen içeriklerin kaydı
- **Favorilerim** — Favori içerikleri ekleme / çıkarma
- **Profilim** — Profil bilgisi düzenleme, şifre değiştirme, istatistikler
- **Size Özel Öneriler** — Favori türlere dayalı öneri motoru

### Yönetici Paneli
- **İçerik Yönetimi** — Film / Dizi / TV Show ekleme, düzenleme, silme
- **Tür Yönetimi** — Kategori CRUD işlemleri
- **Kullanıcı Yönetimi** — Kullanıcı listeleme, aktif/pasif yapma, istatistik görüntüleme
- **Raporlar** — En çok izlenen, en yüksek puanlı, popüler türler, aktif kullanıcılar, son 7 gün

---

## Ekran Görüntüleri

> _(Buraya uygulama ekran görüntüleri eklenebilir)_

---

## Teknoloji Yığını

| Katman | Teknoloji |
|--------|-----------|
| Arayüz | PyQt6 |
| Veritabanı | Microsoft SQL Server (MSSQL) |
| DB Sürücüsü | pyodbc |
| Şifreleme | bcrypt |
| Dil | Python 3.11+ |

---

## Proje Yapısı

```
netflix_platform/
├── main.py                    # Uygulama giriş noktası
├── requirements.txt
│
├── config/
│   └── settings.py            # Veritabanı bağlantı ayarları
│
├── database/
│   ├── connection.py          # MSSQL bağlantı yönetimi
│   ├── setup.py               # Tablo kurulum scripti
│   └── migrations/
│       └── 001_create_tables.sql
│
├── models/                    # Veri modelleri
│   ├── user.py
│   └── program.py
│
├── repositories/              # Veri erişim katmanı
│   ├── user_repository.py
│   ├── program_repository.py
│   ├── genre_repository.py
│   └── report_repository.py
│
├── services/                  # İş mantığı katmanı
│   ├── auth_service.py
│   ├── content_service.py
│   ├── recommendation_service.py
│   └── admin_service.py
│
├── ui/                        # PyQt6 arayüzü
│   ├── main_window.py
│   ├── styles/
│   │   └── dark_theme.py
│   ├── components/
│   │   └── sidebar.py
│   └── pages/
│       ├── login_page.py
│       ├── register_page.py
│       ├── user_home_page.py
│       ├── content_detail_page.py
│       ├── watch_history_page.py
│       ├── favorites_page.py
│       ├── profile_page.py
│       └── admin/
│           └── admin_dashboard.py
│
├── utils/
│   ├── session.py
│   ├── password_hasher.py
│   └── validators.py
│
└── seed/
    ├── seed_data.py           # Demo veri yükleme
    └── seed_demo_ratings.py
```

---

## Kurulum

### Gereksinimler
- Python 3.11+
- Microsoft SQL Server (Express veya üstü)
- ODBC Driver 17 for SQL Server

### 1. Depoyu klonlayın

```bash
git clone https://github.com/KULLANICI_ADI/netflix-platform.git
cd netflix-platform
```

### 2. Bağımlılıkları yükleyin

```bash
pip install -r requirements.txt
```

### 3. Veritabanını yapılandırın

`config/settings.py` dosyasını açıp MSSQL bağlantı bilgilerinizi girin:

```python
DB_SERVER   = "localhost"          # SQL Server adresi
DB_NAME     = "netflix_db"
DB_DRIVER   = "ODBC Driver 17 for SQL Server"
# Windows Authentication kullanılıyorsa aşağıdakini bırakın:
DB_TRUSTED  = True
```

### 4. Tabloları oluşturun

```bash
python -c "from database.setup import create_tables; create_tables()"
```

veya `database/migrations/001_create_tables.sql` dosyasını SSMS üzerinden çalıştırın.

### 5. Demo veriyi yükleyin _(isteğe bağlı)_

```bash
python seed/seed_data.py
python seed/seed_demo_ratings.py
```

### 6. Uygulamayı başlatın

```bash
python main.py
```

---

## Varsayılan Hesaplar

Demo veri yüklendiyse:

| Rol | E-posta | Şifre |
|-----|---------|-------|
| Yönetici | admin@netflix.com | admin123 |
| Kullanıcı | kullanici@test.com | test123 |

> Şifreler bcrypt ile hashlenerek saklanmaktadır.

---

## Veritabanı Şeması

```
Kullanici ──┬── KullaniciTur  ──── Tur ──── ProgramTur ──┐
            ├── KullaniciProgram                          │
            ├── Favori                                    Program
            ├── IzlemeLog                                 │
            └── OturumLog          Bolum ────────────────┘
```

**Tetikleyiciler:**
- `trg_puan_guncelle` — Puan değiştiğinde `Program.ortalama_puan` otomatik güncellenir
- `trg_izlenme_guncelle` — İzleme kaydedildiğinde `Program.toplam_izlenme` artar

---

## Mimari

Uygulama katmanlı mimari (Layered Architecture) kullanır:

```
UI (PyQt6 Pages)
      │
   Services          ← İş mantığı
      │
  Repositories       ← Veri erişimi (SQL sorguları)
      │
   Database          ← MSSQL bağlantısı
```

---

## Geliştirici

| | |
|---|---|
| **Ad** | _(Adınızı buraya ekleyin)_ |
| **Okul** | Kocaeli Sağlık ve Teknoloji Üniversitesi |
| **Ders** | Veritabanı Yönetim Sistemleri |

---

## Lisans

Bu proje akademik amaçlı geliştirilmiştir.

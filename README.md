# Netflix Platform

Netflix Platform, Python ve PyQt6 kullanılarak geliştirilmiş masaüstü tabanlı bir dijital içerik platformu uygulamasıdır. Proje; kullanıcı kayıt sistemi, giriş işlemleri, içerik listeleme, favorilere ekleme, izleme geçmişi, puanlama, öneri sistemi ve yönetici paneli gibi temel yayın platformu özelliklerini içermektedir.

Bu proje, bilgisayar mühendisliği kapsamında masaüstü uygulama geliştirme, veritabanı yönetimi, kullanıcı oturum sistemi, katmanlı mimari ve SQL Server entegrasyonu konularını uygulamalı olarak göstermek amacıyla hazırlanmıştır.

## İçindekiler

- [Proje Hakkında](#proje-hakkında)
- [Temel Özellikler](#temel-özellikler)
- [Kullanılan Teknolojiler](#kullanılan-teknolojiler)
- [Proje Mimarisi](#proje-mimarisi)
- [Klasör Yapısı](#klasör-yapısı)
- [Veritabanı Yapısı](#veritabanı-yapısı)
- [Kurulum](#kurulum)
- [Veritabanı Kurulumu](#veritabanı-kurulumu)
- [Uygulamayı Çalıştırma](#uygulamayı-çalıştırma)
- [Varsayılan Yönetici Hesabı](#varsayılan-yönetici-hesabı)
- [Kullanım Senaryoları](#kullanım-senaryoları)
- [Olası Hatalar ve Çözümleri](#olası-hatalar-ve-çözümleri)
- [Geliştirici Notları](#geliştirici-notları)
- [Test](#test)
- [Geliştirici](#geliştirici)
- [Lisans](#lisans)

## Proje Hakkında

Netflix Platform, kullanıcıların kayıt olup giriş yapabildiği, içerikleri görüntüleyebildiği, favorilerine ekleyebildiği, izleme geçmişini takip edebildiği ve içeriklere puan verebildiği bir masaüstü uygulamasıdır. Uygulama, gerçek bir dijital yayın platformunun temel işleyişini örnek alır. Kullanıcılar film, dizi ve programları görüntüleyebilir; ilgi alanlarına göre öneriler alabilir ve izleme durumlarını sistem üzerinde takip edebilir. Projede ayrıca yönetici paneli bulunmaktadır. Yönetici rolüne sahip kullanıcılar içerik, tür ve kullanıcı yönetimi gibi işlemleri gerçekleştirebilir.

## Temel Özellikler

### Kullanıcı Özellikleri

- Kullanıcı kaydı oluşturma
- E-posta ve şifre ile giriş yapma
- Şifre değiştirme
- Kayıt sırasında ilgi alanı / tür seçimi
- Seçilen türlere göre içerik önerisi alma
- Film, dizi ve programları listeleme
- İçerik arama ve filtreleme
- İçerik detaylarını görüntüleme
- İçeriği favorilere ekleme
- Favorilerden içerik çıkarma
- İzleme geçmişini görüntüleme
- İzleme ilerlemesini kaydetme
- İzlenen içeriklere puan verme

### Yönetici Özellikleri

- İçerik ekleme
- İçerik güncelleme
- İçerik silme
- Tür ekleme
- Tür güncelleme
- Tür silme
- Kullanıcıları görüntüleme
- Kullanıcı aktif/pasif durumunu yönetme
- Platform istatistiklerini görüntüleme
- En çok izlenen içerikleri listeleme
- En yüksek puanlı içerikleri görüntüleme
- En aktif kullanıcıları görüntüleme

### Öneri Sistemi

Uygulamada kullanıcıya özel öneriler oluşturulmaktadır. Öneri sistemi genel olarak şu bilgilere göre çalışır: Kullanıcının kayıt sırasında seçtiği türler, kullanıcının izleme geçmişi, kullanıcının yüksek puan verdiği içerikler, içeriklerin ortalama puanları ve popüler içerikler.

## Kullanılan Teknolojiler

| Teknoloji | Açıklama |
|-----------|----------|
| Python | Projenin ana programlama dili |
| PyQt6 | Masaüstü arayüz geliştirme |
| MSSQL / SQL Server | Veritabanı yönetim sistemi |
| T-SQL | Veritabanı sorguları ve tablo yapıları |
| pyodbc | Python ile SQL Server bağlantısı |
| bcrypt | Şifre hashleme ve doğrulama |
| OOP | Nesne yönelimli programlama yaklaşımı |
| Repository Pattern | Veritabanı işlemlerini ayrı katmanda yönetme |
| Service Layer | İş kurallarını ayrı katmanda yönetme |

## Proje Mimarisi

Proje katmanlı mimari yaklaşımıyla geliştirilmiştir. Bu sayede arayüz, iş mantığı ve veritabanı işlemleri birbirinden ayrılmıştır.

Genel mimari yapı:

```
UI Katmanı
    ↓
Service Katmanı
    ↓
Repository Katmanı
    ↓
Database Katmanı
    ↓
SQL Server
```

**UI Katmanı:** Kullanıcının gördüğü arayüz ekranlarını içerir. PyQt6 kullanılarak oluşturulmuştur. Bu katmanda giriş ekranı, kayıt ekranı, ana sayfa, içerik detayları, favoriler, profil ve yönetici paneli gibi ekranlar bulunur.

**Service Katmanı:** Uygulamanın iş kurallarını içerir. Örneğin: kullanıcı giriş kontrolü, kayıt işlemleri, şifre değiştirme, içerik listeleme, favori işlemleri, puanlama işlemleri, öneri sistemi ve yönetici işlemleri.

**Repository Katmanı:** Veritabanı sorgularının bulunduğu katmandır. Uygulamada SQL işlemleri doğrudan arayüz dosyalarında yapılmaz. Bunun yerine repository sınıfları kullanılır.

**Database Katmanı:** Veritabanı bağlantısı, tablo oluşturma işlemleri ve başlangıç verilerinin yüklenmesi bu katmanda yer alır.

## Klasör Yapısı

```
netflix_platform/
│
├── config/
│   └── settings.py
│
├── database/
│   ├── connection.py
│   ├── setup.py
│   └── migrations/
│       └── 001_create_tables.sql
│
├── models/
│   ├── program.py
│   └── user.py
│
├── repositories/
│   ├── genre_repository.py
│   ├── program_repository.py
│   ├── report_repository.py
│   └── user_repository.py
│
├── seed/
│   └── seed_data.py
│
├── services/
│   ├── admin_service.py
│   ├── auth_service.py
│   ├── content_service.py
│   └── recommendation_service.py
│
├── tests/
│   └── test.py
│
├── ui/
│   ├── assets/
│   ├── components/
│   ├── pages/
│   ├── styles/
│   └── main_window.py
│
├── utils/
│
├── main.py
├── requirements.txt
└── README.md
```

## Veritabanı Yapısı

Projede SQL Server üzerinde `netflix_db` adlı veritabanı kullanılmaktadır. Veritabanında kullanılan temel tablolar şunlardır: Rol, Kullanici, Tur, KullaniciTur, Program, ProgramTur, Bolum, KullaniciProgram, Favori, OturumLog, IzlemeLog. Bu tablolar; kullanıcı yönetimi, içerik yönetimi, tür ilişkileri, favoriler, izleme geçmişi, oturum kayıtları ve raporlama işlemleri için kullanılmaktadır.

## Kurulum

### 1. Projeyi Bilgisayara İndirme

Projeyi GitHub üzerinden klonlamak için:

```bash
git clone https://github.com/reyhancetinn/netflix_platform.git
cd netflix_platform
```

Git kullanmıyorsanız GitHub üzerinden Code > Download ZIP seçeneğiyle projeyi indirebilirsiniz.

### 2. Sanal Ortam Oluşturma

```bash
python -m venv venv
venv\Scripts\activate
```

Eğer python komutu çalışmazsa:

```bash
py -m venv venv
venv\Scripts\activate
```

### 3. Gerekli Paketleri Kurma

```bash
python -m pip install -r requirements.txt
```

Alternatif olarak:

```bash
py -m pip install -r requirements.txt
```

Kurulacak temel paketler: PyQt6, pyodbc, bcrypt

## Veritabanı Kurulumu

Bu proje MSSQL / SQL Server kullanmaktadır. Uygulamanın çalışması için bilgisayarınızda SQL Server ve uygun ODBC Driver kurulu olmalıdır.

Varsayılan veritabanı ayarları `config/settings.py` dosyasında bulunmaktadır:

```python
DB_CONFIG = {
    "server": r".\SQLEXPRESS",
    "database": "netflix_db",
    "driver": "ODBC Driver 17 for SQL Server",
    "trusted_connection": "yes",
}
```

Eğer SQL Server sunucu adınız farklıysa, server değerini kendi SSMS sunucu adınıza göre değiştirmeniz gerekir. Örnek: `"server": r"DESKTOP-ABC123\SQLEXPRESS"`

### Veritabanını Oluşturma

```bash
python database/setup.py
```

Alternatif olarak:

```bash
py database/setup.py
```

Bu işlem şunları yapar: netflix_db veritabanını oluşturur, gerekli tabloları kurar, roller tablosunu hazırlar, varsayılan yönetici hesabını oluşturur ve veritabanı bağlantısını kontrol eder.

### Seed Data Yükleme

Film, dizi ve program verilerini veritabanına eklemek için:

```bash
python -X utf8 seed/seed_data.py
```

Alternatif olarak:

```bash
py -X utf8 seed/seed_data.py
```

## Uygulamayı Çalıştırma

Kurulum ve veritabanı hazırlığı tamamlandıktan sonra:

```bash
python main.py
```

Alternatif olarak:

```bash
py main.py
```

Uygulama açıldığında önce SQL Server bağlantısı kontrol edilir. Bağlantı başarısız olursa uygulama hata mesajı gösterir.

## Varsayılan Yönetici Hesabı

Veritabanı kurulum scripti çalıştırıldıktan sonra varsayılan yönetici hesabı oluşturulur.

| Alan | Değer |
|------|-------|
| E-posta | admin@netflix.com |
| Şifre | admin123 |

Bu hesap ile yönetici paneline giriş yapılabilir.

## Kullanım Senaryoları

### Normal Kullanıcı Akışı

1. Kullanıcı uygulamayı açar
2. Kayıt ekranından kişisel bilgilerini girer
3. Kayıt sırasında ilgi alanlarını / türleri seçer
4. E-posta ve şifre ile giriş yapar
5. Ana sayfada önerilen içerikleri görüntüler
6. Film, dizi veya programları listeler
7. İçerik detaylarını görüntüler
8. İçeriği favorilerine ekleyebilir
9. İzleme geçmişini takip edebilir
10. İzlediği içeriklere puan verebilir

### Yönetici Akışı

1. Yönetici hesabı ile giriş yapılır
2. Yönetici paneline erişilir
3. İçerik ekleme, güncelleme ve silme işlemleri yapılabilir
4. Tür yönetimi gerçekleştirilebilir
5. Kullanıcılar görüntülenebilir
6. Kullanıcıların aktif/pasif durumları yönetilebilir
7. Platform istatistikleri incelenebilir

### Puanlama ve İzleme Mantığı

Kullanıcılar izledikleri içeriklere puan verebilir. Bu sayede içeriklerin ortalama puanı hesaplanabilir ve öneri sistemi daha anlamlı hale gelir. İzleme işlemleri sırasında kullanıcının hangi içeriği izlediği, izleme ilerlemesi ve kullanıcı hareketleri veritabanında saklanır. Böylece izleme geçmişi ve devam edilen içerikler takip edilebilir.

### Öneri Sistemi Mantığı

Öneri sistemi, kullanıcıya daha uygun içerikler göstermek amacıyla geliştirilmiştir. Sistem şu kriterlerden yararlanır: Kullanıcının seçtiği türler, kullanıcının izlediği içerikler, kullanıcının puan verdiği içerikler, popüler içerikler ve ortalama puanı yüksek içerikler. Eğer kullanıcı hakkında yeterli veri yoksa sistem genel popüler içerikleri öneri olarak gösterebilir.

## Test

Projede test dosyası `tests/test.py` altında bulunmaktadır. Testleri çalıştırmak için:

```bash
python tests/test.py
```

Alternatif olarak:

```bash
py tests/test.py
```

## Olası Hatalar ve Çözümleri

**Veritabanına Bağlanılamadı Hatası:** SQL Server servisinin çalıştığından emin olun, SSMS üzerinden sunucu adınızı kontrol edin, `config/settings.py` içindeki server değerini kendi sunucu adınıza göre güncelleyin.

**ODBC Driver Hatası:** ODBC Driver 17 for SQL Server veya ODBC Driver 18 for SQL Server kurulmalıdır. Kurulumdan sonra terminal kapatılıp tekrar açılmalıdır.

**pyodbc Kurulu Değil Hatası:** `python -m pip install pyodbc` veya `py -m pip install pyodbc` komutunu çalıştırın.

**PyQt6 Bulunamadı Hatası:** `python -m pip install PyQt6` veya `python -m pip install -r requirements.txt` komutunu çalıştırın.

**Veritabanı Bulunamadı Hatası:** Önce `python database/setup.py` sonra `python -X utf8 seed/seed_data.py` komutlarını çalıştırın.

## Geliştirici Notları

Projede katmanlı mimari kullanılmıştır. Arayüz PyQt6 ile hazırlanmıştır. Veritabanı olarak MSSQL / SQL Server tercih edilmiştir. SQL işlemleri doğrudan UI dosyalarında yapılmamıştır. Veritabanı işlemleri repository sınıfları üzerinden yönetilmiştir. İş kuralları service sınıflarında toplanmıştır. Kullanıcı şifreleri düz metin olarak saklanmaz, hashlenerek veritabanına kaydedilir. Kullanıcı, içerik, tür, favori ve izleme geçmişi işlemleri ayrı sorumluluklara bölünmüştür. Yönetici paneli ile platform yönetimi sağlanmıştır.

Projenin amacı, gerçek hayattaki bir dijital yayın platformunun temel özelliklerini masaüstü uygulama olarak modellemektir. Proje kapsamında şu yazılım geliştirme konuları uygulanmıştır: masaüstü arayüz tasarımı, kullanıcı kayıt ve giriş sistemi, veritabanı bağlantısı, SQL sorguları, katmanlı mimari, nesne yönelimli programlama, öneri sistemi, admin paneli, favori ve izleme geçmişi yönetimi ve temel raporlama işlemleri.

## Geliştirici

Fatma Zehra Karavar - Bilgisayar Mühendisliği Öğrencisi

## Lisans

Bu proje eğitim ve akademik çalışma amacıyla geliştirilmiştir.

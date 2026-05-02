-- ============================================================
-- NETFLIX PLATFORMU - MSSQL TABLO OLUŞTURMA
-- Programlama Lab 2 - Proje 2
-- ============================================================

USE netflix_db;
GO

-- 1. ROL
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Rol')
CREATE TABLE Rol (
    rol_id   INT IDENTITY(1,1) PRIMARY KEY,
    rol_adi  VARCHAR(20) NOT NULL UNIQUE
);
GO

-- 2. KULLANICI
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Kullanici')
CREATE TABLE Kullanici (
    kullanici_id  INT IDENTITY(1,1) PRIMARY KEY,
    ad            VARCHAR(50)  NOT NULL,
    soyad         VARCHAR(50)  NOT NULL,
    email         VARCHAR(100) NOT NULL UNIQUE,
    sifre_hash    VARCHAR(255) NOT NULL,
    dogum_tarihi  DATE         NOT NULL,
    cinsiyet      VARCHAR(10),
    ulke          VARCHAR(50),
    rol_id        INT          NOT NULL REFERENCES Rol(rol_id),
    aktif         BIT          NOT NULL DEFAULT 1,
    kayit_tarihi  DATETIME     NOT NULL DEFAULT GETDATE()
);
GO

-- 3. TUR
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Tur')
CREATE TABLE Tur (
    tur_id   INT IDENTITY(1,1) PRIMARY KEY,
    tur_adi  VARCHAR(60) NOT NULL UNIQUE
);
GO

-- 4. KULLANICI_TUR (kullanıcının favori türleri — kayıtta 3 seçilir)
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'KullaniciTur')
CREATE TABLE KullaniciTur (
    kullanici_id  INT NOT NULL REFERENCES Kullanici(kullanici_id) ON DELETE CASCADE,
    tur_id        INT NOT NULL REFERENCES Tur(tur_id),
    PRIMARY KEY (kullanici_id, tur_id)
);
GO

-- 5. PROGRAM (Film / Dizi / Tv Show)
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Program')
CREATE TABLE Program (
    program_id      INT IDENTITY(1,1) PRIMARY KEY,
    ad              VARCHAR(150) NOT NULL,
    aciklama        VARCHAR(MAX),
    program_tipi    VARCHAR(20)  NOT NULL CHECK (program_tipi IN ('Film', 'Dizi', 'Tv Show')),
    yayin_yili      SMALLINT     CHECK (yayin_yili BETWEEN 1900 AND 2100),
    bolum_sayisi    SMALLINT     NOT NULL DEFAULT 1,
    bolum_suresi    SMALLINT,
    ortalama_puan   DECIMAL(4,2) NOT NULL DEFAULT 0.00,
    toplam_izlenme  INT          NOT NULL DEFAULT 0,
    eklenme_tarihi  DATETIME     NOT NULL DEFAULT GETDATE()
);
GO

-- 6. PROGRAM_TUR (Program-Tür çoktan çoğa köprü tablosu)
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'ProgramTur')
CREATE TABLE ProgramTur (
    program_id  INT NOT NULL REFERENCES Program(program_id) ON DELETE CASCADE,
    tur_id      INT NOT NULL REFERENCES Tur(tur_id),
    PRIMARY KEY (program_id, tur_id)
);
GO

-- 7. BOLUM (Dizi bölümleri)
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Bolum')
CREATE TABLE Bolum (
    bolum_id    INT IDENTITY(1,1) PRIMARY KEY,
    program_id  INT         NOT NULL REFERENCES Program(program_id) ON DELETE CASCADE,
    bolum_no    SMALLINT    NOT NULL,
    bolum_adi   VARCHAR(150),
    sure        SMALLINT,
    UNIQUE (program_id, bolum_no)
);
GO

-- 8. KULLANICI_PROGRAM (izleme durumu + puan — kullanıcı başına program başına 1 kayıt)
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'KullaniciProgram')
CREATE TABLE KullaniciProgram (
    kullanici_id  INT      NOT NULL REFERENCES Kullanici(kullanici_id) ON DELETE CASCADE,
    program_id    INT      NOT NULL REFERENCES Program(program_id),
    son_izleme    DATETIME NOT NULL DEFAULT GETDATE(),
    son_bolum     SMALLINT NOT NULL DEFAULT 1,
    son_dakika    SMALLINT NOT NULL DEFAULT 0,
    tamamlandi    BIT      NOT NULL DEFAULT 0,
    puan          SMALLINT CHECK (puan BETWEEN 1 AND 10),
    PRIMARY KEY (kullanici_id, program_id)
);
GO

-- 9. FAVORİ
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Favori')
CREATE TABLE Favori (
    favori_id      INT IDENTITY(1,1) PRIMARY KEY,
    kullanici_id   INT      NOT NULL REFERENCES Kullanici(kullanici_id) ON DELETE CASCADE,
    program_id     INT      NOT NULL REFERENCES Program(program_id),
    eklenme_tarihi DATETIME NOT NULL DEFAULT GETDATE(),
    UNIQUE (kullanici_id, program_id)
);
GO

-- 10. OTURUM_LOG
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'OturumLog')
CREATE TABLE OturumLog (
    oturum_id     INT IDENTITY(1,1) PRIMARY KEY,
    kullanici_id  INT      NOT NULL REFERENCES Kullanici(kullanici_id) ON DELETE CASCADE,
    giris_tarihi  DATETIME NOT NULL DEFAULT GETDATE(),
    cikis_tarihi  DATETIME,
    ip_adresi     VARCHAR(45)
);
GO

-- 11. İZLEME_LOG (her izleme seansı)
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'IzlemeLog')
CREATE TABLE IzlemeLog (
    log_id        INT IDENTITY(1,1) PRIMARY KEY,
    kullanici_id  INT      NOT NULL REFERENCES Kullanici(kullanici_id) ON DELETE CASCADE,
    program_id    INT      NOT NULL REFERENCES Program(program_id),
    izleme_tarihi DATETIME NOT NULL DEFAULT GETDATE(),
    izlenen_bolum SMALLINT NOT NULL DEFAULT 1,
    izleme_suresi SMALLINT NOT NULL DEFAULT 0,
    tamamlandi    BIT      NOT NULL DEFAULT 0
);
GO

-- ============================================================
-- TRIGGER: Ortalama puan otomatik güncelleme
-- ============================================================
IF OBJECT_ID('trg_puan_guncelle', 'TR') IS NOT NULL
    DROP TRIGGER trg_puan_guncelle;
GO

CREATE TRIGGER trg_puan_guncelle
ON KullaniciProgram
AFTER INSERT, UPDATE, DELETE
AS
BEGIN
    SET NOCOUNT ON;
    DECLARE @program_id INT;
    SELECT @program_id = COALESCE(
        (SELECT TOP 1 program_id FROM inserted),
        (SELECT TOP 1 program_id FROM deleted)
    );
    UPDATE Program
    SET ortalama_puan = (
        SELECT COALESCE(AVG(CAST(puan AS DECIMAL(4,2))), 0)
        FROM KullaniciProgram
        WHERE program_id = @program_id AND puan IS NOT NULL
    )
    WHERE program_id = @program_id;
END;
GO

-- ============================================================
-- TRIGGER: Toplam izlenme sayısı otomatik güncelleme
-- ============================================================
IF OBJECT_ID('trg_izlenme_guncelle', 'TR') IS NOT NULL
    DROP TRIGGER trg_izlenme_guncelle;
GO

CREATE TRIGGER trg_izlenme_guncelle
ON IzlemeLog
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE Program
    SET toplam_izlenme = (
        SELECT COUNT(*) FROM IzlemeLog WHERE program_id = i.program_id
    )
    FROM inserted i
    WHERE Program.program_id = i.program_id;
END;
GO

-- ============================================================
-- INDEXLER (performans için)
-- ============================================================
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_kullanici_email')
    CREATE INDEX idx_kullanici_email ON Kullanici(email);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_program_tipi')
    CREATE INDEX idx_program_tipi ON Program(program_tipi);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_program_puan')
    CREATE INDEX idx_program_puan ON Program(ortalama_puan DESC);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_izlemelog_tarih')
    CREATE INDEX idx_izlemelog_tarih ON IzlemeLog(izleme_tarihi DESC);
GO

PRINT 'Kurulum tamamlandi.';
GO

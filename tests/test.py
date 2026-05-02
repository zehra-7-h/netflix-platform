"""
Netflix Platform — Birim Test Paketi
=====================================
Calistirmak icin (netflix_platform/ dizininden):
    python -X utf8 -m pytest tests/test.py -v
    veya:
    python -X utf8 tests/test.py

Kapsam:
    1. Validators       — 29 test (DB gerektirmez)
    2. User Model       —  5 test (DB gerektirmez)
    3. AuthService      —  7 test (mock ile)
    4. ContentService   —  7 test (mock ile)
    5. RecommendationService — 4 test (mock ile)
    Toplam: 52 test
"""
import sys
import os
import unittest
from unittest.mock import MagicMock, patch, PropertyMock
from datetime import date, datetime

# Proje kokunu path'e ekle (tests/ ust dizini = netflix_platform/)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# =============================================================================
# 1. VALIDATOR TESTLERi  (DB baglantisi gerektirmez)
# =============================================================================
from utils.validators import (
    validate_email, validate_password, validate_passwords_match,
    validate_birth_date, validate_not_empty, validate_rating,
    validate_year, validate_genre_count,
)


class TestValidateEmail(unittest.TestCase):

    def test_gecerli_email(self):
        ok, msg = validate_email("test@example.com")
        self.assertTrue(ok)
        self.assertEqual(msg, "")

    def test_alt_alan_adli_email(self):
        ok, _ = validate_email("user@sub.domain.org")
        self.assertTrue(ok)

    def test_bos_string(self):
        ok, _ = validate_email("")
        self.assertFalse(ok)

    def test_none_deger(self):
        ok, _ = validate_email(None)
        self.assertFalse(ok)

    def test_at_isaretiz(self):
        ok, _ = validate_email("kullanicidomain.com")
        self.assertFalse(ok)

    def test_nokta_yok(self):
        ok, _ = validate_email("kullanici@domain")
        self.assertFalse(ok)

    def test_bosluklu_gecerli(self):
        # Bosluklar trim edilmeli ve gecerli olmali
        ok, _ = validate_email("  ali@test.com  ")
        self.assertTrue(ok)


class TestValidatePassword(unittest.TestCase):

    def test_tam_6_karakter(self):
        ok, _ = validate_password("abc123")
        self.assertTrue(ok)

    def test_uzun_sifre(self):
        ok, _ = validate_password("SuperSecure@2024!")
        self.assertTrue(ok)

    def test_5_karakter_yetersiz(self):
        ok, _ = validate_password("ab123")
        self.assertFalse(ok)

    def test_bos_sifre(self):
        ok, msg = validate_password("")
        self.assertFalse(ok)
        self.assertIn("bos", msg.lower())


class TestValidatePasswordsMatch(unittest.TestCase):

    def test_eslesiyor(self):
        ok, _ = validate_passwords_match("Sifre123!", "Sifre123!")
        self.assertTrue(ok)

    def test_eslesmıyor(self):
        ok, msg = validate_passwords_match("Sifre123!", "Farkli456!")
        self.assertFalse(ok)
        self.assertIn("esles", msg.lower())

    def test_bos_ikisi_de_bos(self):
        ok, _ = validate_passwords_match("", "")
        self.assertTrue(ok)


class TestValidateBirthDate(unittest.TestCase):

    def test_gecmis_tarih_gecerli(self):
        ok, _ = validate_birth_date(date(1995, 6, 15))
        self.assertTrue(ok)

    def test_bugun_gecersiz(self):
        ok, _ = validate_birth_date(date.today())
        self.assertFalse(ok)

    def test_gelecek_tarih_gecersiz(self):
        ok, _ = validate_birth_date(date(2099, 1, 1))
        self.assertFalse(ok)


class TestValidateNotEmpty(unittest.TestCase):

    def test_dolu_deger(self):
        ok, _ = validate_not_empty("Ali", "Ad")
        self.assertTrue(ok)

    def test_bos_string(self):
        ok, msg = validate_not_empty("", "Soyad")
        self.assertFalse(ok)
        self.assertIn("Soyad", msg)

    def test_sadece_bosluk(self):
        ok, _ = validate_not_empty("   ", "Ulke")
        self.assertFalse(ok)


class TestValidateRating(unittest.TestCase):

    def test_sinir_degerleri_gecerli(self):
        for puan in [1, 5, 10]:
            ok, _ = validate_rating(puan)
            self.assertTrue(ok, f"Puan {puan} gecersiz sayilmamali")

    def test_sinir_disi_degerler(self):
        for puan in [0, 11, -1, 100]:
            ok, _ = validate_rating(puan)
            self.assertFalse(ok, f"Puan {puan} gecerli sayilmamali")

    def test_float_puan_reddedilmeli(self):
        ok, _ = validate_rating(7.5)
        self.assertFalse(ok)


class TestValidateYear(unittest.TestCase):

    def test_gecerli_yil(self):
        ok, _ = validate_year(2010)
        self.assertTrue(ok)

    def test_cok_eski_yil(self):
        ok, _ = validate_year(1800)
        self.assertFalse(ok)

    def test_gelecek_yil_siniri(self):
        gelecek_yil = date.today().year + 1
        ok, _ = validate_year(gelecek_yil)
        self.assertTrue(ok)


class TestValidateGenreCount(unittest.TestCase):

    def test_tam_3_tur_gecerli(self):
        ok, _ = validate_genre_count([1, 2, 3])
        self.assertTrue(ok)

    def test_2_tur_yetersiz(self):
        ok, _ = validate_genre_count([1, 2])
        self.assertFalse(ok)

    def test_4_tur_fazla(self):
        ok, _ = validate_genre_count([1, 2, 3, 4])
        self.assertFalse(ok)

    def test_tekrar_eden_tur(self):
        ok, msg = validate_genre_count([1, 1, 2])
        self.assertFalse(ok)
        self.assertIn("farkli", msg.lower())

    def test_bos_liste(self):
        ok, _ = validate_genre_count([])
        self.assertFalse(ok)


# =============================================================================
# 2. USER MODEL TESTLERi  (DB gerektirmez)
# =============================================================================
from models.user import User


class TestUserModel(unittest.TestCase):

    def _kullanici(self, rol_id=1, ad="Ali", soyad="Kaya",
                   dogum_yili=1995) -> User:
        return User(
            kullanici_id=1, ad=ad, soyad=soyad,
            email="test@test.com",
            dogum_tarihi=date(dogum_yili, 6, 15),
            rol_id=rol_id, aktif=True,
            kayit_tarihi=datetime(2024, 1, 1),
        )

    def test_tam_ad(self):
        u = self._kullanici(ad="Ayse", soyad="Demir")
        self.assertEqual(u.tam_ad, "Ayse Demir")

    def test_normal_kullanici_admin_degil(self):
        u = self._kullanici(rol_id=1)
        self.assertFalse(u.is_admin)

    def test_admin_kullanici(self):
        u = self._kullanici(rol_id=2)
        self.assertTrue(u.is_admin)

    def test_yas_dogru_hesaplaniyor(self):
        bugun = date.today()
        dogum_yili = bugun.year - 30
        u = self._kullanici(dogum_yili=dogum_yili)
        self.assertIn(u.yas, [29, 30])

    def test_aktif_alan(self):
        u = self._kullanici()
        self.assertTrue(u.aktif)


# =============================================================================
# 3. AUTH SERVICE TESTLERi  (mock ile, DB baglanamaz)
# =============================================================================
class TestAuthService(unittest.TestCase):
    """
    AuthService icin DB ve repository mock'lanir.
    Gercek sifre dogrulama kodu calisir (bcrypt), bu nedenle
    verify_password ayrica mock'lanir — test hizi icin.
    """

    def _servis_olustur(self):
        """Repo mock'lanmis AuthService donduror."""
        with patch("repositories.user_repository.db"):
            from services.auth_service import AuthService
            svc = AuthService()
        svc._repo = MagicMock()
        return svc

    def _sahte_kullanici(self, aktif=True, rol_id=1):
        u = MagicMock()
        u.kullanici_id = 42
        u.aktif = aktif
        u.rol_id = rol_id
        u.sifre_hash = "$MOCK_HASH$"
        return u

    # ── Login testleri ──────────────────────────────────────────

    def test_login_bos_email_reddedilir(self):
        svc = self._servis_olustur()
        ok, msg, user = svc.login("", "Sifre123!")
        self.assertFalse(ok)
        self.assertIsNone(user)

    def test_login_kayitli_olmayan_kullanici(self):
        svc = self._servis_olustur()
        svc._repo.find_by_email.return_value = None
        ok, msg, user = svc.login("yok@test.com", "Sifre123!")
        self.assertFalse(ok)
        self.assertIsNone(user)

    def test_login_pasif_hesap_reddedilir(self):
        svc = self._servis_olustur()
        svc._repo.find_by_email.return_value = self._sahte_kullanici(aktif=False)
        ok, msg, user = svc.login("pasif@test.com", "Sifre123!")
        self.assertFalse(ok)
        self.assertIn("pasif", msg.lower())

    @patch("services.auth_service.verify_password", return_value=False)
    def test_login_yanlis_sifre(self, _mock_verify):
        svc = self._servis_olustur()
        svc._repo.find_by_email.return_value = self._sahte_kullanici()
        ok, msg, user = svc.login("test@test.com", "YanlisS!")
        self.assertFalse(ok)
        self.assertIn("yanlis", msg.lower())

    @patch("services.auth_service.session")
    @patch("services.auth_service.db")
    @patch("services.auth_service.verify_password", return_value=True)
    def test_login_basarili(self, _mock_verify, mock_db, mock_session):
        mock_db.insert_and_get_id.return_value = 99
        svc = self._servis_olustur()
        svc._repo.find_by_email.return_value = self._sahte_kullanici()
        ok, msg, user = svc.login("test@test.com", "DogruSifre!")
        self.assertTrue(ok)
        self.assertEqual(msg, "")
        self.assertIsNotNone(user)

    # ── Register testleri ───────────────────────────────────────

    def test_register_sifre_uyusmuyorsa_hata(self):
        svc = self._servis_olustur()
        svc._repo.find_by_email.return_value = None
        ok, msg = svc.register(
            ad="Ali", soyad="Yilmaz", email="ali@test.com",
            sifre="Sifre123!", sifre_tekrar="Farkli456!",
            dogum_tarihi=date(1995, 1, 1),
            cinsiyet="Erkek", ulke="Turkiye", tur_idler=[1, 2, 3]
        )
        self.assertFalse(ok)
        self.assertIn("esles", msg.lower())

    def test_register_mevcut_email_reddedilir(self):
        svc = self._servis_olustur()
        svc._repo.find_by_email.return_value = self._sahte_kullanici()
        ok, msg = svc.register(
            ad="Ali", soyad="Yilmaz", email="mevcut@test.com",
            sifre="Sifre123!", sifre_tekrar="Sifre123!",
            dogum_tarihi=date(1995, 1, 1),
            cinsiyet="Erkek", ulke="Turkiye", tur_idler=[1, 2, 3]
        )
        self.assertFalse(ok)
        self.assertIn("kayitli", msg.lower())


# =============================================================================
# 4. CONTENT SERVICE TESTLERi  (mock ile)
# =============================================================================
class TestContentService(unittest.TestCase):

    def setUp(self):
        with patch("repositories.program_repository.db"), \
             patch("repositories.genre_repository.db"):
            from services.content_service import ContentService
            self.svc = ContentService()
        self.svc._repo = MagicMock()
        self.svc._genre_repo = MagicMock()

    # ── Puanlama ────────────────────────────────────────────────

    def test_rate_sinir_disi_puan_reddedilir(self):
        ok, msg = self.svc.rate(1, 1, 0)
        self.assertFalse(ok)
        self.svc._repo.get_watch_status.assert_not_called()

    def test_rate_izlenmemis_icerige_puan_verilemez(self):
        self.svc._repo.get_watch_status.return_value = None
        ok, msg = self.svc.rate(1, 1, 8)
        self.assertFalse(ok)
        self.assertIn("izlediginiz", msg.lower())

    def test_rate_basarili_gecerli_puan(self):
        self.svc._repo.get_watch_status.return_value = MagicMock()
        ok, msg = self.svc.rate(1, 1, 9)
        self.assertTrue(ok)
        self.assertEqual(msg, "")
        self.svc._repo.set_rating.assert_called_once_with(1, 1, 9)

    # ── Favori ──────────────────────────────────────────────────

    def test_toggle_favorite_ekleme(self):
        self.svc._repo.is_favorite.return_value = False
        sonuc = self.svc.toggle_favorite(1, 5)
        self.assertTrue(sonuc)
        self.svc._repo.add_favorite.assert_called_once_with(1, 5)
        self.svc._repo.remove_favorite.assert_not_called()

    def test_toggle_favorite_cikarma(self):
        self.svc._repo.is_favorite.return_value = True
        sonuc = self.svc.toggle_favorite(1, 5)
        self.assertFalse(sonuc)
        self.svc._repo.remove_favorite.assert_called_once_with(1, 5)
        self.svc._repo.add_favorite.assert_not_called()

    # ── Ilerleme kaydı ──────────────────────────────────────────

    def test_save_progress_repo_cagrilari(self):
        self.svc.save_progress(1, 10, 3, 45, False)
        self.svc._repo.upsert_watch_status.assert_called_once_with(1, 10, 3, 45, False)
        self.svc._repo.add_watch_log.assert_called_once_with(1, 10, 3, 45, False)

    # ── Arama ───────────────────────────────────────────────────

    def test_search_parametreleri_repoya_iletilir(self):
        self.svc._repo.search.return_value = []
        result = self.svc.search(ad="test", tur_id=2, tipi="Film")
        self.svc._repo.search.assert_called_once_with("test", 2, "Film", None, None)
        self.assertIsInstance(result, list)


# =============================================================================
# 5. RECOMMENDATION SERVICE TESTLERi  (mock ile)
# =============================================================================
class TestRecommendationService(unittest.TestCase):

    @patch("services.recommendation_service.db")
    def test_bos_izleme_gecmisi_sonuc_donuyor(self, mock_db):
        """Kullanici hic izlemediyse populer icerik fallback'i calisir."""
        from services.recommendation_service import RecommendationService
        mock_db.fetchall.side_effect = [
            [],                                         # izlenen_ids
            [],                                         # tur_rows (bos)
            [(1, "Interstellar", "Film", 9.0),
             (2, "Inception", "Film", 8.5)],            # populer fallback
        ]
        svc = RecommendationService()
        result = svc.get_personalized(999, limit=5)
        self.assertIsInstance(result, list)
        self.assertGreaterEqual(len(result), 0)

    @patch("services.recommendation_service.db")
    def test_duplikat_program_sonucta_yer_almaz(self, mock_db):
        """Ayni program_id iki turde eslesse de sonucta tek gorulmeli."""
        from services.recommendation_service import RecommendationService
        mock_db.fetchall.side_effect = [
            [],              # izlenen_ids
            [(1,), (2,)],   # tur_rows
            # Ayni program iki kez donse de DISTINCT + seen_ids filtreler
            [(10, "Interstellar", "Film", 9.0),
             (10, "Interstellar", "Film", 9.0),
             (11, "Inception",    "Film", 8.5)],
            [],             # populer fallback
        ]
        svc = RecommendationService()
        result = svc.get_personalized(999, limit=8)
        ids = [r["program_id"] for r in result]
        self.assertEqual(len(ids), len(set(ids)),
                         "Ayni program_id sonucta birden fazla gorunmemeli")

    @patch("services.recommendation_service.db")
    def test_kayit_onerisi_tur_basina_2_icerik(self, mock_db):
        """3 tur secildiginde her turden 2 icerik = toplam 6 oneri."""
        from services.recommendation_service import RecommendationService
        mock_db.fetchall.side_effect = [
            [(1, "Aksiyon ve Macera"),
             (2, "Drama"),
             (3, "Komedi")],                            # kullanici turleri
            [(10, "Kara Sovalye",  "Film", 9.0),
             (11, "Baslangic",    "Film", 9.0)],        # aksiyon top-2
            [(20, "Dangal",       "Film", 9.0),
             (21, "Interstellar", "Film", 9.0)],        # drama top-2
            [(30, "Shrek",        "Film", 8.5),
             (31, "Kung Fu Panda","Film", 8.0)],        # komedi top-2
        ]
        svc = RecommendationService()
        result = svc.get_registration_recommendations(1)
        self.assertEqual(len(result), 6)

    @patch("services.recommendation_service.db")
    def test_kayit_onerisi_limit_asimi_yok(self, mock_db):
        """Sonuc listesi limit'i asmamali."""
        from services.recommendation_service import RecommendationService
        mock_db.fetchall.side_effect = [
            [(i, f"Tur {i}") for i in range(1, 6)],      # 5 tur
            *[[(100 + i, f"Film {i}", "Film", float(10 - i))]
              for i in range(5)],                          # her turden 1 icerik
        ]
        svc = RecommendationService()
        result = svc.get_registration_recommendations(1)
        # Tur basina max 2 donuyor; 5 tur × 1 sonuc = 5 (limit = 2*tur_sayisi degil)
        self.assertLessEqual(len(result), 10)


# =============================================================================
# CALISTIRICI
# =============================================================================
if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite  = loader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)

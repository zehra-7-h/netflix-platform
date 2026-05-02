import pyodbc
from config.settings import DB_CONFIG


class DatabaseConnection:
    """
    Singleton veritabanı bağlantı yöneticisi.
    Uygulama boyunca tek bir bağlantı nesnesi kullanılır.

    Singleton neden? Her ekran ayrı bağlantı açmasın diye.
    Sunumda sorulursa: "Tasarım deseni kullandık, tekrar eden
    bağlantıların önüne geçtik" diyebilirsin.
    """

    _instance = None
    _connection = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_connection(self):
        if self._connection is None or self._is_closed():
            self._connection = self._create_connection()
        return self._connection

    def _create_connection(self):
        try:
            # Önce modern sürücüyü dene, yoksa eski sürücüye geç
            drivers_to_try = [
                "ODBC Driver 17 for SQL Server",
                "ODBC Driver 18 for SQL Server",
                "SQL Server",
            ]
            last_error = None
            for driver in drivers_to_try:
                try:
                    conn_str = (
                        f"DRIVER={{{driver}}};"
                        f"SERVER={DB_CONFIG['server']};"
                        f"DATABASE={DB_CONFIG['database']};"
                        f"Trusted_Connection=yes;"
                        f"TrustServerCertificate=yes;"
                    )
                    conn = pyodbc.connect(conn_str, autocommit=False)
                    print(f"[DB] Bağlantı başarılı ({driver})")
                    return conn
                except pyodbc.Error as e:
                    last_error = e
                    continue
            raise last_error
        except pyodbc.Error as e:
            print(f"[DB HATA] Bağlantı kurulamadı: {e}")
            raise

    def _is_closed(self):
        try:
            self._connection.cursor()
            return False
        except Exception:
            return True

    def execute(self, query: str, params: tuple = ()):
        """SELECT dışı sorgular için (INSERT, UPDATE, DELETE)."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor

    def insert_and_get_id(self, query: str, params: tuple = ()):
        """INSERT + OUTPUT INSERTED sorgularında ID'yi commit öncesi okur."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
        conn.commit()
        return row[0] if row else None

    def fetchall(self, query: str, params: tuple = ()):
        """SELECT sorguları için — tüm satırları döndürür."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

    def fetchone(self, query: str, params: tuple = ()):
        """SELECT sorguları için — tek satır döndürür."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchone()

    def close(self):
        if self._connection:
            self._connection.close()
            self._connection = None
            print("[DB] Bağlantı kapatıldı.")


# Modül içinden kolayca erişim için tek örnek
db = DatabaseConnection()

try:
    import pyodbc
except ModuleNotFoundError as exc:
    pyodbc = None
    _PYODBC_IMPORT_ERROR = exc
else:
    _PYODBC_IMPORT_ERROR = None

from config.settings import DB_CONFIG


def _iter_connection_strings(database_name: str):
    """Yield compatible connection strings for the installed SQL drivers."""
    preferred_drivers = [
        DB_CONFIG.get("driver"),
        "ODBC Driver 18 for SQL Server",
        "ODBC Driver 17 for SQL Server",
        "SQL Server",
    ]
    seen = set()

    for driver in preferred_drivers:
        if not driver or driver in seen:
            continue
        seen.add(driver)

        parts = [
            f"DRIVER={{{driver}}}",
            f"SERVER={DB_CONFIG['server']}",
            f"DATABASE={database_name}",
            f"Trusted_Connection={DB_CONFIG.get('trusted_connection', 'yes')}",
        ]

        # Newer ODBC drivers support explicit encryption settings.
        if "ODBC Driver" in driver:
            parts.extend(["Encrypt=no", "TrustServerCertificate=yes"])

        yield driver, ";".join(parts) + ";"


class DatabaseConnection:
    """
    Singleton veritabani baglanti yoneticisi.
    Uygulama boyunca tek bir baglanti nesnesi kullanilir.
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
        if pyodbc is None:
            raise RuntimeError(
                "pyodbc kurulu degil. Veritabani baglantisi icin `pip install pyodbc` calistirin."
            ) from _PYODBC_IMPORT_ERROR

        errors = []

        for driver, conn_str in _iter_connection_strings(DB_CONFIG["database"]):
            try:
                conn = pyodbc.connect(conn_str, autocommit=False)
                print(f"[DB] Baglanti basarili ({driver})")
                return conn
            except pyodbc.Error as exc:
                errors.append(f"{driver}: {exc}")

        joined_errors = "\n".join(errors)
        if "Cannot open database" in joined_errors:
            message = (
                f"Veritabani '{DB_CONFIG['database']}' bulunamadi. "
                "Once `py -3.12 database/setup.py` komutunu calistirin.\n\n"
                f"Ayrinti:\n{joined_errors}"
            )
        else:
            message = f"Baglanti kurulamadi.\n{joined_errors}"

        print(f"[DB HATA] {message}")
        raise RuntimeError(message)

    def _is_closed(self):
        try:
            self._connection.cursor()
            return False
        except Exception:
            return True

    def execute(self, query: str, params: tuple = ()):
        """SELECT disi sorgular icin (INSERT, UPDATE, DELETE)."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor

    def insert_and_get_id(self, query: str, params: tuple = ()):
        """INSERT + OUTPUT INSERTED sorgularinda ID'yi commit oncesi okur."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
        conn.commit()
        return row[0] if row else None

    def fetchall(self, query: str, params: tuple = ()):
        """SELECT sorgulari icin tum satirlari dondurur."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

    def fetchone(self, query: str, params: tuple = ()):
        """SELECT sorgulari icin tek satir dondurur."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchone()

    def close(self):
        if self._connection:
            self._connection.close()
            self._connection = None
            print("[DB] Baglanti kapatildi.")


db = DatabaseConnection()

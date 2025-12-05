from typing import Dict
import pandas as pd

class ETLLoader:
    """
    ETL işlemleri için veri yükleme fonksiyonlarını içerir.
    """
    
    @staticmethod
    def load_to_sqlite(data: Dict[str, pd.DataFrame], db_path: str = "cache.sqlite3") -> None:
        """
        DataFrame'leri cache.sqlite3 veritabanına uygun tablo adlarıyla kaydeder.
        Args:
            data (dict): Tablo adı -> DataFrame
            db_path (str): SQLite dosya yolu
        """
        import sqlite3
        try:
            conn = sqlite3.connect(db_path)
            for table_name, df in data.items():
                df.to_sql(table_name, conn, if_exists='replace', index=False)
                print(f"{table_name} tablosu başarıyla {db_path} veritabanına yüklendi.")
            conn.close()
        except Exception as e:
            print(f"Veritabanına yükleme sırasında hata oluştu: {e}")
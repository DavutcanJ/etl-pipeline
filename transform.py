
import pandas as pd
import logging
from typing import Dict, Any, Type
from models import UserModel, ProductModel, OrderModel, OrderDetailModel, InventoryModel

logging.basicConfig(level=logging.INFO)

class ETLTransformer:
    """
    ETL işlemleri için veri dönüştürme, doğrulama ve eksik veri yönetimi fonksiyonlarını içerir.
    """
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

 
    def transform_text_upper(self) -> pd.DataFrame:
        """Tüm metinleri büyük harfe çevirir."""
        logging.info("Veri dönüştürme işlemi başladı.")
        transformed = self.df.applymap(lambda x: x.upper() if isinstance(x, str) else x)
        logging.info("Veri dönüştürme işlemi tamamlandı.")
        self.df = transformed
        return self.df

    def check_missing(self) -> pd.Series:
        """Eksik değerleri kontrol eder."""
        logging.info("Eksik değer kontrolü başladı.")
        missing = self.df.isnull().sum()
        logging.info("Eksik değer kontrolü tamamlandı.")
        return missing

    def normalize(self) -> pd.DataFrame:
        """Sayısal verileri normalize eder."""
        logging.info("Veri normalizasyonu başladı.")
        normalized = (self.df - self.df.min()) / (self.df.max() - self.df.min())
        logging.info("Veri normalizasyonu tamamlandı.")
        return normalized

    def encode_categorical(self) -> pd.DataFrame:
        """Kategorik verileri one-hot encoding ile kodlar."""
        logging.info("Kategorik verilerin kodlanması başladı.")
        encoded = pd.get_dummies(self.df)
        logging.info("Kategorik verilerin kodlanması tamamlandı.")
        return encoded

    @staticmethod
    def split_and_validate_by_model(df: pd.DataFrame) -> Dict[str, list]:
        """
        Verileri modellere göre böler, eksik sütunları None ile doldurur ve ilgili Pydantic model nesnelerine dönüştürür.
        Dönüş: {model_adi: [ModelNesnesi, ...]}
        """
        user_cols = ['id', 'username', 'email', 'is_active', 'created_at']
        product_cols = ['product_id', 'name', 'description', 'price', 'in_stock', 'created_at']
        order_cols = ['order_id', 'user_id', 'product_id', 'quantity', 'total_price', 'order_date', 'status']
        inventory_cols = ['product_id', 'quantity_available', 'restock_date', 'supplier_name']
        order_detail_cols = [
            'order_id', 'user_id', 'product_id', 'quantity', 'total_price', 'order_date', 'status',
            'shipping_address', 'billing_address', 'payment_method', 'delivery_date'
        ]
        def ensure_columns(dataframe, columns):
            for col in columns:
                if col not in dataframe.columns:
                    dataframe[col] = None
            return dataframe[columns].copy()

        user_df = ensure_columns(df, user_cols)
        product_df = ensure_columns(df, product_cols)
        order_df = ensure_columns(df, order_cols)
        inventory_df = ensure_columns(df, inventory_cols)
        order_detail_df = ensure_columns(df, order_detail_cols)

        return {
            'user': ETLTransformer.validate_dataframe(user_df, UserModel),
            'product': ETLTransformer.validate_dataframe(product_df, ProductModel),
            'order': ETLTransformer.validate_dataframe(order_df, OrderModel),
            'inventory': ETLTransformer.validate_dataframe(inventory_df, InventoryModel),
            'order_detail': ETLTransformer.validate_dataframe(order_detail_df, OrderDetailModel)
        }

    def aggregate(self, group_by: str, agg_col: str, agg_func: str) -> pd.DataFrame:
        """Verileri gruplayıp toplar."""
        logging.info("Veri toplama işlemi başladı.")
        aggregated = self.df.groupby(group_by)[agg_col].agg(agg_func).reset_index()
        logging.info("Veri toplama işlemi tamamlandı.")
        return aggregated

    def filter(self, condition: str) -> pd.DataFrame:
        """Veriyi verilen koşula göre filtreler."""
        logging.info("Veri filtreleme işlemi başladı.")
        filtered = self.df.query(condition)
        logging.info("Veri filtreleme işlemi tamamlandı.")
        return filtered

    def enrich(self, enrichment_df: pd.DataFrame, on: str) -> pd.DataFrame:
        """Veriyi başka bir veriyle birleştirerek zenginleştirir."""
        logging.info("Veri zenginleştirme işlemi başladı.")
        enriched = pd.merge(self.df, enrichment_df, on=on, how='left')
        logging.info("Veri zenginleştirme işlemi tamamlandı.")
        return enriched

    def deduplicate(self) -> pd.DataFrame:
        """Çoğaltılmış satırları kaldırır."""
        logging.info("Veri çoğaltma kaldırma işlemi başladı.")
        deduped = self.df.drop_duplicates()
        logging.info("Veri çoğaltma kaldırma işlemi tamamlandı.")
        return deduped

    def standardize(self) -> pd.DataFrame:
        """Sayısal verileri standartlaştırır."""
        logging.info("Veri standardizasyonu başladı.")
        standardized = (self.df - self.df.mean()) / self.df.std()
        logging.info("Veri standardizasyonu tamamlandı.")
        return standardized

    def handle_outliers(self, z_threshold: float = 3.0) -> pd.DataFrame:
        """Aykırı değerleri z-score ile filtreler."""
        logging.info("Aykırı değer işleme başladı.")
        from scipy import stats
        num_df = self.df.select_dtypes(include=['number'])
        z_scores = stats.zscore(num_df)
        abs_z_scores = abs(z_scores)
        filtered_entries = (abs_z_scores < z_threshold).all(axis=1)
        cleaned = self.df[filtered_entries]
        logging.info("Aykırı değer işleme tamamlandı.")
        return cleaned

    def fill_missing_with_clustering(self, n_clusters: int = 5, random_state: int = 42) -> pd.DataFrame:
        """Eksik verileri KMeans ile kümeleyip doldurur."""
        logging.info("Eksik verileri kümeleme ile doldurma başladı.")
        from sklearn.cluster import KMeans
        import numpy as np
        df = self.df.copy()
        num_cols = df.select_dtypes(include=['number']).columns
        temp = df[num_cols].fillna(df[num_cols].mean())
        kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=10)
        clusters = kmeans.fit_predict(temp)
        df['cluster'] = clusters
        for col in num_cols:
            for cluster_id in range(n_clusters):
                mask = (df['cluster'] == cluster_id) & (df[col].isnull())
                mean_val = df.loc[df['cluster'] == cluster_id, col].mean()
                df.loc[mask, col] = mean_val
        cat_cols = df.select_dtypes(include=['object', 'category']).columns
        for col in cat_cols:
            for cluster_id in range(n_clusters):
                mask = (df['cluster'] == cluster_id) & (df[col].isnull())
                mode_val = df.loc[df['cluster'] == cluster_id, col].mode()
                if not mode_val.empty:
                    df.loc[mask, col] = mode_val[0]
        df = df.drop(columns=['cluster'])
        logging.info("Eksik verileri kümeleme ile doldurma tamamlandı.")
        return df

    def transform(self) -> pd.DataFrame:

        """Tüm dönüşüm adımlarını uygular."""
        self.df = self.deduplicate()
        self.df = self.fill_missing_with_clustering()
        self.df = ETLTransformer.split_and_validate_by_model(self.df)
        self.df = self.normalize()
        self.df = self.encode_categorical()
        self.df = self.standardize()
        self.df = self.handle_outliers()
        self.df = self.transform_text_upper()
        self.df = self.aggregate(group_by=self.df.columns[0], agg_col=self.df.columns[1], agg_func='sum')
        self.df = self.filter(condition=f"{self.df.columns[1]} > 0")
        self.df = self.enrich(enrichment_df=self.df, on=self.df.columns[0])
        self.df = self.check_missing()
        

    
        return self.df      






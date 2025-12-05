
def start_pipeline():
    print("Veri işleme pipeline'ı başlatıldı.")
    

    #1. Extract
    df = extract_data('mock_data.csv')

    if df is None or len(df) == 0:
        return
    
    print("Veri çıkarma tamamlandı.")
    print(df.head())

    print("Veri dönüştürme başladı.")
    # 2. Transform
    transformer = ETLTransformer(df)
    # Verileri modellere böl ve doğrula
    model_data = ETLTransformer.split_and_validate_by_model(df)
    # İsteğe bağlı: Diğer transform işlemleri
    # transformed_df = transformer.transform_text_upper()

    # 3. Load
    # DataFrame olarak yüklemek isterseniz:
    # split_df = ETLTransformer.split_by_model(df)
    # ETLLoader.load_to_sqlite(split_df)
    # Doğrudan model nesnelerini yüklemek isterseniz:
    # Önce DataFrame'e çevirip yükleyebilirsiniz
    split_df = ETLTransformer.split_by_model(df)
    ETLLoader.load_to_sqlite(split_df)

    

if __name__ == "__main__":

    import pandas as pd
    from extract import extract_data
    from transform import ETLTransformer
    from load import ETLLoader
    from generate_mock_data import generate_mock_data, write_to_csv

    # Generate mock data and write to CSV
        



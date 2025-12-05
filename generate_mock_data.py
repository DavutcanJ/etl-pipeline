import csv
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker('tr_TR')  # Türkçe locale

def generate_mock_data(num_records=10000):
    """10.000 satır mock data üretir"""
    
    # Rastgele veriler için listeler
    products = [
        "Laptop", "Wireless Mouse", "Mechanical Keyboard", "USB-C Hub", "Monitor Stand",
        "Webcam", "Headphones", "Smartphone", "Tablet", "SSD Drive", "Graphics Card",
        "Power Bank", "Bluetooth Speaker", "Gaming Chair", "Desk Lamp"
    ]
    
    statuses = ["pending", "processing", "shipped", "delivered", "cancelled"]
    carriers = ["Aras Kargo", "MNG Kargo", "Yurtiçi Kargo", "PTT Kargo", "UPS"]
    payment_methods = ["credit_card", "debit_card", "paypal", "bank_transfer"]
    
    data = []
    
    for i in range(1, num_records + 1):
        # Rastgele tarihler
        created_date = fake.date_between(start_date='-1y', end_date='today')
        order_date = created_date + timedelta(days=random.randint(1, 30))
        shipment_date = order_date + timedelta(days=random.randint(1, 5))
        delivery_date = shipment_date + timedelta(days=random.randint(1, 7))
        
        # Product bilgileri
        product_name = random.choice(products)
        price = round(random.uniform(19.99, 2999.99), 2)
        quantity = random.randint(1, 5)
        total_price = round(price * quantity, 2)
        
        row = {
            'id': i,
            'username': fake.user_name(),
            'email': fake.email(),
            'is_active': random.choice([True, False]),
            'created_at': created_date.strftime('%Y-%m-%d'),
            'name': product_name,
            'description': f"{product_name} - {fake.text(max_nb_chars=50)}",
            'price': price,
            'in_stock': random.choice([True, False]),
            'product_id': random.randint(100, 999),
            'user_id': i,
            'quantity': quantity,
            'total_price': total_price,
            'order_date': order_date.strftime('%Y-%m-%d'),
            'status': random.choice(statuses),
            'quantity_available': random.randint(0, 500),
            'restock_date': (datetime.now() + timedelta(days=random.randint(1, 60))).strftime('%Y-%m-%d'),
            'supplier_name': fake.company(),
            'supplier_contact': fake.email(),
            'rating': random.randint(1, 5),
            'comment': fake.text(max_nb_chars=100),
            'review_date': (order_date + timedelta(days=random.randint(7, 30))).strftime('%Y-%m-%d'),
            'contact_name': fake.name(),
            'contact_email': fake.email(),
            'phone_number': fake.phone_number(),
            'address': fake.address().replace('\n', ', '),
            'order_id': 1000 + i,
            'shipment_date': shipment_date.strftime('%Y-%m-%d'),
            'delivery_date': delivery_date.strftime('%Y-%m-%d'),
            'carrier': random.choice(carriers),
            'tracking_number': f"TRK{random.randint(100000, 999999)}",
            'payment_date': order_date.strftime('%Y-%m-%d'),
            'amount': total_price,
            'payment_method': random.choice(payment_methods),
            'product_ids': f"[{random.randint(100, 999)},{random.randint(100, 999)},{random.randint(100, 999)}]",
            'code': f"SAVE{random.randint(10, 50)}",
            'discount_percentage': random.randint(5, 50),
            'valid_from': created_date.strftime('%Y-%m-%d'),
            'valid_to': (created_date + timedelta(days=random.randint(30, 365))).strftime('%Y-%m-%d'),
            'active': random.choice([True, False]),
            'shipping_address': fake.address().replace('\n', ', '),
            'billing_address': fake.address().replace('\n', ', ')
        }
        
        data.append(row)
    
    return data

def write_to_csv(data, filename='mock_data.csv'):
    """CSV dosyasına veri yazar"""
    if not data:
        return
    
    fieldnames = data[0].keys()
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    
    print(f"{len(data)} satır veri {filename} dosyasına yazıldı.")

if __name__ == "__main__":
    print("10.000 satır mock data üretiliyor...")
    mock_data = generate_mock_data(10000)
    write_to_csv(mock_data)
    print("Tamamlandı!")
import pydantic

class UserModel(pydantic.BaseModel):
    id: int | None = None
    username: str | None = None
    email: str | None = None
    is_active: bool | None = None
    created_at: str | None = None

class ProductModel(pydantic.BaseModel):
    id: int | None = None
    name: str | None = None
    description: str | None = None
    price: float | None = None
    in_stock: bool | True = False
    created_at: str | None = None

class OrderModel(pydantic.BaseModel):
    id: int | None = None
    user_id: int | None = None
    product_id: int | None = None
    quantity: int | None = None
    total_price: float | None = None
    order_date: str | None = None
    status: str | None = None

class OrderDetailModel(pydantic.BaseModel):
    order: OrderModel | None = None
    user: UserModel | None = None
    product: ProductModel | None = None
    shipping_address: str | None = None
    billing_address: str | None = None
    payment_method: str | None = None
    delivery_date: str | None = None

class InventoryModel(pydantic.BaseModel):
    product_id: int | None = None
    quantity_available: int | None = None
    restock_date: str | None = None
    supplier_name: str | None = None
    supplier_contact: str | None = None

class ReviewModel(pydantic.BaseModel):
    id: int | None = None
    user_id: int | None = None
    product_id: int | None = None
    rating: int | None = None
    comment: str | None = None
    review_date: str | None = None

class CategoryModel(pydantic.BaseModel):
    id: int | None = None
    name: str | None = None
    description: str | None = None
    created_at: str | None = None

class SupplierModel(pydantic.BaseModel):
    id: int | None = None
    name: str | None = None
    contact_name: str | None = None
    contact_email: str | None = None
    phone_number: str | None = None
    address: str | None = None

class ShipmentModel(pydantic.BaseModel):
    id: int | None = None
    order_id: int | None = None
    shipment_date: str | None = None
    delivery_date: str | None = None
    carrier: str | None = None
    tracking_number: str | None = None
    status: str | None = None

class PaymentModel(pydantic.BaseModel):
    id: int | None = None
    order_id: int | None = None
    payment_date: str | None = None
    amount: float | None = None
    payment_method: str | None = None
    status: str | None = None

class WishlistModel(pydantic.BaseModel):
    id: int | None = None
    user_id: int | None = None
    product_ids: list[int] | None = None
    created_at: str | None = None

class CartModel(pydantic.BaseModel):
    id: int | None = None
    user_id: int | None = None
    product_ids: list[int] | None = None
    total_price: float | None = None
    created_at: str | None = None

class DiscountModel(pydantic.BaseModel):
    id: int | None = None
    code: str | None = None
    description: str | None = None
    discount_percentage: float | None = None
    valid_from: str | None = None
    valid_to: str | None = None
    active: bool | None = None


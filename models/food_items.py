from odmantic import Model


class FoodItem(Model):
    title: str
    description: str
    price: float
    isVeg: bool
    qty: int

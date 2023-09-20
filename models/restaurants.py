from typing import List
from bson import ObjectId
from models.food_items import FoodItem
from odmantic import Model


class Restaurant(Model):
    name: str
    password: str
    menu: List[ObjectId]
    address: str


class RestaurantResponse(Model):
    name: str
    menu: List[FoodItem]
    address: str

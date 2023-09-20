from odmantic import Model
from typing import List, Optional
from bson import ObjectId
from models.users import UserResponse
from models.riders import RiderResponse
from models.food_items import FoodItem
from models.restaurants import RestaurantResponse


class Order(Model):
    restaurant: ObjectId
    user: ObjectId
    rider: Optional[ObjectId]
    items: List[ObjectId]
    amount: Optional[float]
    status: Optional[str]


class OrderResponse(Model):
    user: Optional[UserResponse]
    restaurant: Optional[RestaurantResponse]
    rider: Optional[RiderResponse]
    items: List[FoodItem]
    amount: float
    status: str


class OrdersByUser(Model):
    restaurant: Optional[RestaurantResponse]
    rider: Optional[RiderResponse]
    items: List[FoodItem]
    amount: float
    status: str


class OrdersByRider(Model):
    restaurant: Optional[RestaurantResponse]
    user: Optional[UserResponse]
    items: List[FoodItem]
    amount: float
    status: str

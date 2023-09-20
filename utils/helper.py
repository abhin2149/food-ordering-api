from typing import List
from utils.api import get_distance_time_between_locations
from models.restaurants import Restaurant, RestaurantResponse
from models.users import User, UserResponse
from models.riders import Rider, RiderResponse
from models.food_items import FoodItem
from models.orders import Order, OrderResponse, OrdersByUser, OrdersByRider


def build_user_response(user: User) -> UserResponse:
    return UserResponse(username=user.username, address=user.address)


def build_rider_response(rider: Rider) -> RiderResponse:
    return RiderResponse(username=rider.username, cur_loc=rider.cur_loc, isActive=rider.isActive)


async def build_restaurant_response(outlet: Restaurant, engine) -> RestaurantResponse:
    menu: List[FoodItem] = []
    for _id in outlet.menu:
        item = await engine.find_one(FoodItem, FoodItem.id == _id)
        menu.append(item)
    return RestaurantResponse(name=outlet.name, address=outlet.address, menu=menu)


async def build_order_response(order: Order, engine) -> OrderResponse:
    items: List[FoodItem] = []
    user: User = await engine.find_one(User, User.id == order.user)
    restaurant: Restaurant = await engine.find_one(Restaurant, Restaurant.id == order.restaurant)
    rider: Rider = await engine.find_one(Rider, Rider.id == order.rider) if order.rider else None
    for _id in order.items:
        item = await engine.find_one(FoodItem, FoodItem.id == _id)
        items.append(item)
    return OrderResponse(restaurant=await build_restaurant_response(restaurant, engine),
                         user=build_user_response(user),
                         rider=build_rider_response(rider) if rider else None,
                         items=items, amount=order.amount, status=order.status)


async def get_order_amount(order: Order, engine) -> float:
    amount: float = 0.0
    for _id in order.items:
        item: FoodItem = await engine.find_one(FoodItem, FoodItem.id == _id)
        # update the inventory of given item
        item.qty = item.qty - 1
        await engine.save(item)
        amount += item.price
    return amount


async def get_orders_by_user(orders: List[Order], engine) -> List[OrdersByUser]:
    orders_response: List[OrdersByUser] = []
    for order in orders:
        new_order: OrderResponse = await build_order_response(order, engine)
        orders_response.append(OrdersByUser(restaurant=new_order.restaurant, rider=new_order.rider,
                                            items=new_order.items, amount=new_order.amount, status=new_order.status))
    return orders_response


async def get_orders_by_rider(orders: List[Order], engine) -> List[OrdersByRider]:
    orders_response: List[OrdersByRider] = []
    for order in orders:
        new_order: OrderResponse = await build_order_response(order, engine)
        orders_response.append(OrdersByRider(restaurant=new_order.restaurant, user=new_order.user,
                                             items=new_order.items, amount=new_order.amount, status=new_order.status))
    return orders_response


async def get_nearest_rider(order: Order, engine) -> Rider:
    restaurant: Restaurant = await engine.find_one(Restaurant, Restaurant.id == order.restaurant)
    riders: List[Rider] = await engine.find(Rider)
    rider_time = get_distance_time_between_locations(restaurant.address, [rider.cur_loc for rider in riders])
    rider_time_map = dict(zip(rider_time, riders))
    rider_time.sort()
    return rider_time_map.get(rider_time[0])


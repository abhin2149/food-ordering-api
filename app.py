from models.users import User, UserResponse
from models.food_items import FoodItem
from models.restaurants import Restaurant, RestaurantResponse
from models.riders import Rider, RiderResponse, Location
from models.orders import Order, OrderResponse, OrdersByUser, OrdersByRider
from utils.helper import (build_restaurant_response, build_order_response, get_order_amount, build_user_response,
                          build_rider_response, get_orders_by_user, get_orders_by_rider, get_nearest_rider)
from utils.hasher import hash_password
from db.mongo_connect import mongo_engine
from odmantic import ObjectId
from fastapi import FastAPI, HTTPException
from typing import List

app = FastAPI()
engine = mongo_engine()


@app.get("/")
def get_status():
    """Get status of server."""
    return {"status": "running"}


# User API

# Register a user
@app.put("/user", response_model=User)
async def register_user(user: User):
    user.password = hash_password(user.password)
    await engine.save(user)
    return build_user_response(user)


# Fetch a user
@app.get("/user/{id}", response_model=UserResponse)
async def get_user(id: ObjectId):
    user = await engine.find_one(User, User.id == id)
    if user is None:
        raise HTTPException(404)
    return build_user_response(user)


# FoodItem API

# Add a food item
@app.put("/food-item", response_model=FoodItem)
async def add_food_item(item: FoodItem):
    await engine.save(item)
    return item


# Fetch a food item
@app.get("/food-item/{id}", response_model=FoodItem)
async def get_food_item(id: ObjectId):
    item = await engine.find_one(FoodItem, FoodItem.id == id)
    if item is None:
        raise HTTPException(404)
    return item


# Rider API

# Register a rider
@app.put("/rider", response_model=Rider)
async def register_rider(rider: Rider):
    rider.password = hash_password(rider.password)
    await engine.save(rider)
    return build_rider_response(rider)


# Fetch a rider
@app.get("/rider/{id}", response_model=RiderResponse)
async def get_rider(id: ObjectId):
    rider = await engine.find_one(Rider, Rider.id == id)
    if rider is None:
        raise HTTPException(404)
    return build_rider_response(rider)


# Update Rider Location
@app.put("/rider/location/{id}", response_model=RiderResponse)
async def get_rider(id: ObjectId, loc: Location):
    rider = await engine.find_one(Rider, Rider.id == id)
    if rider is None:
        raise HTTPException(404)
    rider.cur_loc = loc
    await engine.save(rider)
    return build_rider_response(rider)

# Restaurant API


# Register a restaurant
@app.put("/restaurant", response_model=Restaurant)
async def register_restaurant(outlet: Restaurant):
    outlet.password = hash_password(outlet.password)
    await engine.save(outlet)
    return outlet


# Fetch details of a restaurant
@app.get("/restaurant/{id}", response_model=RestaurantResponse)
async def get_restaurant(id: ObjectId):
    outlet = await engine.find_one(Restaurant, Restaurant.id == id)
    if outlet is None:
        raise HTTPException(404)
    return await build_restaurant_response(outlet, engine)


# Get Restaurants by delivery time and user food preferences


# Order API


# Accept an Order
@app.put("/order", response_model=Order)
async def register_order(order: Order):
    order.amount = await get_order_amount(order, engine)
    order.status = "Accepted"
    await engine.save(order)
    return order


# Get an Order
@app.get("/order/{id}", response_model=OrderResponse)
async def get_order(id: ObjectId):
    order = await engine.find_one(Order, Order.id == id)
    if order is None:
        raise HTTPException(404)
    return await build_order_response(order, engine)


# Assign a Rider nearest to the restaurant to pickup order
@app.get("/order/assign/{order_id}", response_model=OrderResponse)
async def assign_rider(order_id: ObjectId):
    order = await engine.find_one(Order, Order.id == order_id)
    if order is None:
        raise HTTPException(404)
    rider = await get_nearest_rider(order, engine)
    if rider is None:
        raise HTTPException(404)
    order.rider = rider.id
    order.status = "Ready"
    await engine.save(order)
    return await build_order_response(order, engine)


# Get history of Orders placed by a User
@app.get("/order/user/{user_id}", response_model=List[OrdersByUser])
async def get_order_by_user(user_id: ObjectId):
    orders = await engine.find(Order, Order.user == user_id)
    if len(orders) == 0:
        raise HTTPException(404)
    return await get_orders_by_user(orders, engine)


# Get history of Orders delivered by a rider
@app.get("/order/rider/{rider_id}", response_model=List[OrdersByRider])
async def get_order_by_rider(rider_id: ObjectId):
    orders = await engine.find(Order, Order.rider == rider_id)
    if len(orders) == 0:
        raise HTTPException(404)
    return await get_orders_by_rider(orders, engine)



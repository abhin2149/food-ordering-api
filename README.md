# Food Ordering API
Python backend build top of FastAPI, MongoDB, Pydantic and Odmantic (for Object Relational Mapping), Uvicorn and uses distance-matrix API to find realtime travel distances
between given locations. 

Uses docker containerization for easy deployments and scaling

Uses SHA-256 hashing to hash and salt passwords before they are persisted in the database.

### Entity Classes

* User
* Rider
* Restaurant
* Order
* FoodItem

## Getting Started with the project

### Steps to run the project

* Create a MongoDB cluster either locally or on MongoDB Atlas cloud free [tier](https://cloud.mongodb.com/v2#/org/650933202a6ca578dc275398/).
* Sign up for a free Distance-Matrix API account [here](https://distancematrix.ai/).
* Create a new ``.env`` file from ``sample.env`` and add all the relevant env variables.
* From the root of the project run ``docker-compose up``.
* Visit `http://localhost:5000/` to check if the server is up and running.


### Available Scripts

NOTE: To make sure docker is up and running in your system, run the following command:

### `docker --version`

In the project directory, you can run:

### `docker-compose up`

Runs the app in the development mode.\
Open [http://localhost:5000](http://localhost:5000) to view it in the browser.

### API Documentation

You can view the API documentation at [http://localhost:5000/docs](http://localhost:5000/docs)

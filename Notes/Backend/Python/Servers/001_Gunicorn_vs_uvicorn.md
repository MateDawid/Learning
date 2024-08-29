# Gunicorn vs Uvicorn

Source: https://ismatsamadov.medium.com/gunicorn-vs-uvicorn-369635b92809

Imagine you’re hosting a party. You need a capable host (web server) to manage the guests (requests) and ensure a smooth experience.

Gunicorn and Uvicorn are two popular options, but they excel in different ways.

In the world of Python web development, you’ll encounter two terms that might seem interchangeable at first glance: GUVICORN and UVICORN. But these two players serve distinct purposes in running your web applications. Let’s break down their roles and when to use each one, with a touch of fun to make it easier to remember!

## Gunicorn

* **Built for WSGI applications**: Gunicorn shines when dealing with WSGI frameworks like Django or Flask. It can handle many guests (requests) efficiently, even with limited resources.
* **Synchronous processing**: Gunicorn follows a traditional approach, handling one guest (request) at a time. This works well for most web applications.
* **Mature and reliable**: Gunicorn is a proven solution with a long track record of stability.

**The WSGI Wrapper, a.k.a. The Adapter**

GUVICORN, is like a resourceful engineer. It can take your brave knight, Uvicorn, and equip it with heavier armor. GUVICORN itself is an ASGI to WSGI (Web Server Gateway Interface) adapter. WSGI is an older protocol commonly used by web frameworks like Flask and Django.

**Why Use GUVICORN?**

* Taming Uvicorn for WSGI Servers: GUVICORN allows you to leverage Uvicorn’s ASGI prowess even with WSGI servers like Gunicorn, a popular option for production environments. Gunicorn excels at managing worker processes, ensuring your application can handle heavy traffic.
* Best of Both Worlds: With GUVICORN, you get the asynchronous magic of Uvicorn for development and the battle-tested stability of Gunicorn for production.

## Uvicorn 

* **Built for ASGI applications**: Uvicorn is designed for modern ASGI frameworks like Starlette or FastAPI. It can leverage asynchronous processing to handle a large influx of guests (requests) simultaneously.
* **Asynchronous processing**: Uvicorn can juggle multiple guests (requests) at once, ideal for real-time features like chat applications or live updates.
* **Built for speed and scalability**: Uvicorn is optimized for performance, making it perfect for high-traffic web applications.

Key Points about Uvicorn:

* Built for ASGI: Uvicorn is the perfect companion for modern web frameworks like FastAPI, which leverage the power of ASGI.
* Development Server: Uvicorn shines during development. It’s lightweight and easy to use, allowing you to quickly test and debug your web application as you code.
* Limited Worker Support: While Uvicorn can spin up multiple worker processes, its capabilities in this area are more basic compared to GUVICORN.

## Analogy

* **Gunicorn**: Imagine a party host who takes coat checks one by one (synchronous processing). They handle each guest efficiently but can get overwhelmed with a large crowd.
* **Uvicorn**: This host has multiple assistants who tag coats simultaneously (asynchronous processing). This allows them to handle a large number of guests efficiently, especially for high-traffic situations.

## Examples
* Choosing Gunicorn: If you’re building a traditional Django blog or a data processing API with Flask, Gunicorn is a solid choice.
* Choosing Uvicorn: If you’re creating a real-time chat application with Starlette or a high-performance API with FastAPI, Uvicorn’s asynchronous processing will give you an edge.

## Building a FastAPI Application with GUVicorn or UVicorn

```python
from fastapi import FastAPI

# Create an instance of the FastAPI class
app = FastAPI()

# Define a route and corresponding handler function
@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}
```

### For GUVicorn
```commandline
gunicorn -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000
```

### For UVicorn
```commandline
uvicorn main:app --host 0.0.0.0 --port 8000
```
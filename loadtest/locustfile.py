from locust import HttpUser, task, between
import os

POST_PATH = os.getenv("POST_PATH", "/")

class BlogReader(HttpUser):
    wait_time = between(1, 3)

    @task
    def open_post(self):
        with self.client.get(POST_PATH, name=POST_PATH, timeout=30, catch_response=True) as r:
            if r.status_code != 200:
                r.failure(f"HTTP {r.status_code}")

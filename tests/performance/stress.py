from locust import HttpUser, task


class TestSomething(HttpUser):
    @task
    def send_something(self):
        pass

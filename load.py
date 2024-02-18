from locust import HttpUser, task, between
from antisocial_backend.resources.notes.notes_routes import events
import json
from datetime import datetime
class PerformanceTest(HttpUser):
    wait_time = between(1,3)

    @task(1)
    def test_tf(self):
        #event = events.Create(name="test", location="test", organizer="test", date="2021-10-10")
        response = self.client.post("/", 
                                    json={
                                        "name": "Yusuf",
                                        "description": "locate",
                                        "start_date": str(datetime.now())
                                    })
         
        #response = self.client.get("/")
        

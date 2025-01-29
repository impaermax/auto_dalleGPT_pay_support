import requests
import time

class RecraftImageGenerator:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.url_endpoint = "https://api.gen-api.ru/api/v1/networks/recraft"
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }

    def generate_image(self, prompt: str, style: str = "realistic_image", aspect_ratio: str = "4:3"):
        payload = {
            "translate_input": True,
            "is_sync": False,
            "model": "v3",
            "prompt": prompt,
            "style": style,
            "aspect_ratio": aspect_ratio
        }
        
        response = requests.post(self.url_endpoint, json=payload, headers=self.headers)
        if response.status_code != 200:
            return {"error": "Ошибка при отправке запроса"}
        
        data = response.json()
        request_id = data.get("request_id")
        if not request_id:
            return {"error": "Ошибка в получении request_id"}
        
        return self._wait_for_result(request_id)
    
    def _wait_for_result(self, request_id: int, retries: int = 10, delay: int = 5):
        result_url = f"{self.url_endpoint}/{request_id}"
        for _ in range(retries):
            response = requests.get(result_url, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    return data.get("output")
            time.sleep(delay)
        return {"error": "Превышено время ожидания ответа"}

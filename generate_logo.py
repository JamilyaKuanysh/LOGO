import requests
import random
import time
import base64
import config as cfg

def generate_logo(style, description):
    try:
        headers = {
            "Authorization": f"Bearer {cfg.iam_token}",
            "Content-Type": "application/json"
        }

        data = {
            "modelUri": f"art://{cfg.catalog_id}/yandex-art/latest",
            "generationOptions": {
                "seed": f"{random.randint(0, 1000000)}",
                "aspectRatio": {
                    "widthRatio": "1",
                    "heightRatio": "1"
                }
            },
            "messages": [
                {
                    "weight": "1",
                    "text": f"Нарисуй логотип под описание: {description}, в стиле: {style}, высокое качество"
                }
            ]
        }

        response = requests.post(cfg.url_1, headers=headers, json=data)
        if response.status_code == 200:
            request_id = response.json().get('id')
            time.sleep(20)
            headers.pop("Content-Type", None)
            response = requests.get(f"{cfg.url_2}/{request_id}", headers=headers)
            if response.status_code == 200:
                image_base64 = response.json().get('response', {}).get('image')
                if image_base64:
                    image_data = base64.b64decode(image_base64)
                    image_path = "static/generated_logo.jpeg"
                    with open(image_path, 'wb') as file:
                        file.write(image_data)
                    return image_path
                else:
                    return None
        return None
    except Exception as e:
        print(f"Ошибка: {e}")
        return None
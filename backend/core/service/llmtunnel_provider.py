import re
import time
import json
from openai import OpenAI
from typing import Union
from typing import List
from typing import Tuple
from PIL import Image
from core.utils.image_utils import get_base64_image


class LLMProvider():

    MAX_TOKENS = 50000

    def __init__(self, provider_secret_key, provider_url, provider_submodel):
        self.provider_secret_key = provider_secret_key
        self.provider_url = provider_url
        self.provider_submodel = provider_submodel

    def predict(self, prompt: str, image: Image.Image = None, submodel: str = None):
        client = OpenAI(
            api_key=self.provider_secret_key,
            base_url=self.provider_url,
        )

        llm_request = {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt
                },
            ]
        }

        if image:
            
            image_base64 = get_base64_image(image)

            llm_request['content'].append({
                "type": "image_url",
                "image_url": {
                    "url": image_base64,
                    "detail": "auto"
                }}
            )

        
        # print(llm_request)
        photo_result = client.chat.completions.create(
            messages=[llm_request],
            model=submodel if submodel else self.provider_submodel,
            max_tokens=LLMProvider.MAX_TOKENS,
            temperature=0,
        )
        # В прошлый раз с этой api были баги, если не поставить задержку
        # TODO: разобраться в чём была проблема
        time.sleep(0.1)
        results = []
        try:
            response_message = photo_result.choices[0].message.content
            print('response_message', response_message)
            results = LLMProvider.extract_json_from_llm_output(response_message)
            if not isinstance(results, dict):
                raise ValueError("Ожидался словарь результатов")
        except Exception as e:
            print(f"Ошибка при выполнении запроса к GPT: {e}")

        return results

    @staticmethod
    def extract_json_from_llm_output(text: str) -> Union[dict, list]:
        text = text.replace('```json', '').replace('```', '')
        try:
            return json.loads(text)
        except (AttributeError, json.JSONDecodeError):
            print('Не удалось просто получить json')
        try:
            # Попробуем найти JSON-блок в тексте
            json_str = re.search(r'({.*?}|\[.*?\])', text, re.DOTALL).group(1)
            return json.loads(json_str)
        except (AttributeError, json.JSONDecodeError):
            raise ValueError("Не удалось извлечь корректный JSON из ответа модели.")
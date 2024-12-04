import aiohttp

TRANSLATION_API_URL = "https://external-translation-api.com/translate"

async def translate_content(text: str, source_language: str, target_language: str):
    async with aiohttp.ClientSession() as session:
        payload = {"text": text, "source_lang": source_language, "target_lang": target_language}
        async with session.post(TRANSLATION_API_URL, json=payload) as response:
            if response.status != 200:
                raise Exception("Translation API error")
            result = await response.json()
            return result.get("translated_text")

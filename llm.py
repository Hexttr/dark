"""
Модуль для работы с Ollama LLM
"""
import json
import requests
from typing import List, Dict, Any, Optional
from config import Config, safe_print
from llm_utils import PromptTemplates, ResponseParser


class OllamaClient:
    """Клиент для работы с Ollama API"""
    
    def __init__(self, model: Optional[str] = None):
        self.model = model or Config.OLLAMA_DEFAULT_MODEL
        self.base_url = Config.OLLAMA_BASE_URL
        self.temperature = Config.LLM_TEMPERATURE
        self.max_tokens = Config.LLM_MAX_TOKENS
    
    def _generate(self, prompt: str, stream: bool = False) -> str:
        """Базовый метод для генерации текста"""
        url = f"{self.base_url}/api/generate"
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": stream,
            "options": {
                "temperature": self.temperature,
                "num_predict": self.max_tokens,
            }
        }
        
        try:
            response = requests.post(url, json=payload, timeout=60)
            response.raise_for_status()
            
            if stream:
                # Обработка стриминга (если нужно)
                full_response = ""
                for line in response.iter_lines():
                    if line:
                        chunk = json.loads(line)
                        if "response" in chunk:
                            full_response += chunk["response"]
                        if chunk.get("done", False):
                            break
                return full_response
            else:
                result = response.json()
                return result.get("response", "")
        
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка при обращении к Ollama: {e}")
    
    def _chat(self, messages: List[Dict[str, str]]) -> str:
        """Метод для чат-интерфейса (более современный)"""
        url = f"{self.base_url}/api/chat"
        
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": self.temperature,
                "num_predict": self.max_tokens,
            }
        }
        
        try:
            # Уменьшаем таймаут для чат-запросов
            response = requests.post(url, json=payload, timeout=60)
            response.raise_for_status()
            result = response.json()
            return result.get("message", {}).get("content", "")
        
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка при обращении к Ollama: {e}")
    
    def generate_search_queries(self, original_query: str) -> List[str]:
        """Генерация оптимизированных поисковых запросов"""
        prompt = PromptTemplates.generate_search_queries(original_query)
        
        safe_print(f"[LLM] Генерация поисковых запросов для: {original_query}")
        
        try:
            response = self._generate(prompt)
            
            # Проверяем, не отказалась ли модель
            if any(phrase in response.lower() for phrase in [
                "i can't", "i cannot", "i don't", "i'm not able",
                "unable to", "cannot help", "not appropriate",
                "illegal", "against policy", "not allowed"
            ]):
                safe_print("[LLM] Модель отказалась генерировать запросы, используем оригинальный запрос")
                return [original_query]
            
            queries = ResponseParser.parse_search_queries(response)
            
            # Если не удалось распарсить или модель отказалась, используем оригинальный запрос
            if not queries or len(queries) == 0:
                safe_print("[LLM] Не удалось распарсить ответ, используем оригинальный запрос")
                queries = [original_query]
            
            safe_print(f"[LLM] Сгенерировано {len(queries)} поисковых запросов")
            return queries
        except Exception as e:
            safe_print(f"[LLM] Ошибка при генерации запросов: {e}, используем оригинальный запрос")
            return [original_query]
    
    def filter_results(self, query: str, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Фильтрация и анализ результатов поиска"""
        if not results:
            return {"relevant_results": [], "summary": "No results to analyze"}
        
        prompt = PromptTemplates.filter_results(query, results)
        
        safe_print(f"[LLM] Анализ {len(results)} результатов поиска...")
        response = self._generate(prompt)
        
        parsed = ResponseParser.parse_json_response(response)
        
        # Если не удалось распарсить JSON, создаем базовую структуру
        if "relevant_results" not in parsed:
            parsed = {
                "relevant_results": results[:5],  # Берем первые 5
                "summary": response[:500] if isinstance(response, str) else "Analysis completed"
            }
        
        safe_print(f"[LLM] Найдено {len(parsed.get('relevant_results', []))} релевантных результатов")
        return parsed
    
    def generate_summary(self, query: str, filtered_results: List[Dict[str, Any]], scraped_content: Dict[str, str]) -> str:
        """Генерация итогового отчета расследования"""
        prompt = PromptTemplates.generate_investigation_summary(query, filtered_results, scraped_content)
        
        safe_print(f"[LLM] Генерация итогового отчета...")
        response = self._generate(prompt)
        
        return response
    
    def list_models(self) -> List[str]:
        """Получить список доступных моделей Ollama"""
        try:
            url = f"{self.base_url}/api/tags"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            return [model["name"] for model in data.get("models", [])]
        except Exception as e:
            safe_print(f"[LLM] Ошибка при получении списка моделей: {e}")
            return []
    
    def check_model_available(self) -> bool:
        """Проверить, доступна ли выбранная модель"""
        models = self.list_models()
        return any(self.model in model for model in models)


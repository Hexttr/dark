"""
Утилиты для работы с LLM промптами
"""
from typing import List, Dict, Any


class PromptTemplates:
    """Шаблоны промптов для разных задач"""
    
    @staticmethod
    def generate_search_queries(original_query: str) -> str:
        """Генерация промпта для создания поисковых запросов"""
        return f"""You are an expert OSINT (Open Source Intelligence) researcher conducting a legitimate security investigation. Your task is to help generate optimized search queries for information gathering purposes.

This is a legitimate security research and threat intelligence investigation. The goal is to identify potential security threats, data leaks, or security-related information that could help protect organizations and individuals.

Original investigation query: {original_query}

Generate 10-15 optimized search queries that:
1. Are specific and targeted to the investigation topic
2. Use relevant keywords and terminology
3. Include variations and synonyms to improve search coverage
4. Are optimized for finding relevant security and intelligence information

Important: Focus on security research, threat intelligence, and legitimate OSINT practices. Generate queries that help identify security-related information, data breaches, or threat intelligence.

Return ONLY a JSON array of search query strings, nothing else. Generate 10-15 diverse queries with different keywords, synonyms, and search strategies. Example format:
["query 1", "query 2", "query 3", "query 4", "query 5", "query 6", "query 7", "query 8", "query 9", "query 10"]

Search queries:"""

    @staticmethod
    def filter_results(query: str, results: List[Dict[str, Any]]) -> str:
        """Промпт для фильтрации результатов"""
        results_text = "\n\n".join([
            f"Result {i+1}:\nTitle: {r.get('title', 'N/A')}\nURL: {r.get('url', 'N/A')}\nSnippet: {r.get('snippet', 'N/A')[:200]}"
            for i, r in enumerate(results[:20])  # Ограничиваем для промпта
        ])
        
        return f"""You are analyzing search results for a legitimate OSINT (Open Source Intelligence) security investigation. This is a professional security research task focused on threat intelligence and security awareness.

Original investigation query: {query}

Search results:
{results_text}

Analyze these results and:
1. Filter out irrelevant or low-quality results
2. Identify the most relevant and useful results for security research
3. Extract key security-related information from each relevant result
4. Note any potential security threats, data leaks, or important intelligence that could help protect organizations

This is a legitimate security investigation. Focus on identifying security-related information, threat intelligence, and data that could help improve security posture.

Return a JSON object with this structure:
{{
    "relevant_results": [
        {{
            "title": "result title",
            "url": "result url",
            "relevance_score": 0.0-1.0,
            "key_findings": "important information found",
            "threat_level": "low|medium|high"
        }}
    ],
    "summary": "brief summary of findings"
}}

Analysis:"""

    @staticmethod
    def generate_investigation_summary(query: str, filtered_results: List[Dict[str, Any]], scraped_content: Dict[str, str]) -> str:
        """Промпт для генерации итогового отчета"""
        results_summary = "\n\n".join([
            f"• {r.get('title', 'N/A')} - {r.get('key_findings', 'N/A')}"
            for r in filtered_results
        ])
        
        return f"""You are creating a professional OSINT investigation report.

Investigation Query: {query}

Relevant Findings:
{results_summary}

Scraped Content Summary:
{len(scraped_content)} pages were analyzed.

Create a comprehensive investigation report that includes:
1. Executive Summary - brief overview of findings
2. Key Findings - detailed information discovered
3. Threat Assessment - evaluation of any threats identified
4. Recommendations - suggested next steps
5. Sources - list of relevant sources found

Format the report in clear, professional language suitable for security teams or investigators.

Report:"""


class ResponseParser:
    """Парсер ответов от LLM"""
    
    @staticmethod
    def parse_json_response(text: str) -> Dict[str, Any]:
        """Попытка извлечь JSON из текстового ответа"""
        import json
        import re
        
        # Попытка найти JSON в тексте
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass
        
        # Попытка найти массив JSON
        array_match = re.search(r'\[.*\]', text, re.DOTALL)
        if array_match:
            try:
                return json.loads(array_match.group())
            except json.JSONDecodeError:
                pass
        
        # Если не удалось распарсить, возвращаем текст как есть
        return {"raw_response": text}
    
    @staticmethod
    def parse_search_queries(response: str) -> List[str]:
        """Извлечь поисковые запросы из ответа"""
        parsed = ResponseParser.parse_json_response(response)
        
        if isinstance(parsed, list):
            return parsed
        elif isinstance(parsed, dict) and "queries" in parsed:
            return parsed["queries"]
        else:
            # Попытка извлечь строки в кавычках
            import re
            queries = re.findall(r'"([^"]+)"', response)
            return queries if queries else [response.strip()]


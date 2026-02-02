"""
Утилиты для работы с LLM промптами
"""
from typing import List, Dict, Any


class PromptTemplates:
    """Шаблоны промптов для разных задач"""
    
    @staticmethod
    def generate_search_queries(original_query: str) -> str:
        """Генерация промпта для создания поисковых запросов для кибербезопасности"""
        # Определяем, является ли запрос доменом
        is_domain = '.' in original_query and ('http' not in original_query.lower() and 'www' not in original_query.lower())
        domain_name = original_query.strip().replace('http://', '').replace('https://', '').replace('www.', '').split('/')[0].split('?')[0]
        
        if is_domain:
            # Если это домен, создаем специальный промпт для кибербезопасности
            return f"""You are an expert cybersecurity OSINT researcher conducting a legitimate security threat intelligence investigation. Your task is to generate optimized search queries to find security-related information about a domain/company.

This is a legitimate cybersecurity investigation focused on threat intelligence, vulnerability assessment, and security awareness. The goal is to identify potential security threats, data breaches, vulnerabilities, attack discussions, or compromised data that could help protect the organization.

Target domain/company: {domain_name}

Generate 12-15 optimized search queries specifically focused on cybersecurity threats and security intelligence. The queries should help discover:

1. **Data Breaches & Leaks:**
   - Database dumps, credential leaks, data breaches
   - Stolen credentials, passwords, customer data
   - Compromised accounts, email leaks

2. **Vulnerabilities & Exploits:**
   - Security vulnerabilities, CVEs, exploits
   - Zero-day vulnerabilities, security flaws
   - Attack vectors, exploitation discussions

3. **Attack Discussions & Threats:**
   - Attack discussions, hacking forums mentions
   - Ransomware attacks, DDoS discussions
   - Social engineering campaigns, phishing

4. **Compromised Data:**
   - Sold/stolen data, database sales
   - Account credentials for sale
   - Personal information leaks

5. **Security Incidents:**
   - Security incidents, breaches reports
   - Compromised infrastructure discussions
   - Security research findings

IMPORTANT: Generate queries that are:
- Specific to cybersecurity threats and security intelligence
- Use relevant security terminology (breach, leak, exploit, vulnerability, credentials, dump, etc.)
- Include variations with and without domain name
- Focus on finding actionable threat intelligence
- Suitable for dark web search engines

Return ONLY a JSON array of search query strings, nothing else. Example format:
["{domain_name} data breach credentials leak", "{domain_name} database dump", "domain {domain_name} vulnerability exploit", ...]

Search queries:"""
        else:
            # Обычный запрос - улучшенный промпт для кибербезопасности
            return f"""You are an expert cybersecurity OSINT researcher conducting a legitimate security threat intelligence investigation. Your task is to generate optimized search queries for cybersecurity information gathering.

This is a legitimate cybersecurity investigation focused on threat intelligence, vulnerability assessment, and security awareness. The goal is to identify potential security threats, data breaches, vulnerabilities, attack discussions, or compromised data.

Original investigation query: {original_query}

Generate 12-15 optimized search queries specifically focused on cybersecurity threats and security intelligence. The queries should help discover:

1. **Data Breaches & Leaks:**
   - Database dumps, credential leaks, data breaches
   - Stolen credentials, passwords, customer data
   - Compromised accounts, email leaks

2. **Vulnerabilities & Exploits:**
   - Security vulnerabilities, CVEs, exploits
   - Zero-day vulnerabilities, security flaws
   - Attack vectors, exploitation discussions

3. **Attack Discussions & Threats:**
   - Attack discussions, hacking forums mentions
   - Ransomware attacks, DDoS discussions
   - Social engineering campaigns, phishing

4. **Compromised Data:**
   - Sold/stolen data, database sales
   - Account credentials for sale
   - Personal information leaks

5. **Security Incidents:**
   - Security incidents, breaches reports
   - Compromised infrastructure discussions
   - Security research findings

IMPORTANT: Generate queries that are:
- Specific to cybersecurity threats and security intelligence
- Use relevant security terminology (breach, leak, exploit, vulnerability, credentials, dump, etc.)
- Include variations and synonyms
- Focus on finding actionable threat intelligence
- Suitable for dark web search engines

Return ONLY a JSON array of search query strings, nothing else. Example format:
["query 1", "query 2", "query 3", "query 4", "query 5", "query 6", "query 7", "query 8", "query 9", "query 10"]

Search queries:"""

    @staticmethod
    def filter_results(query: str, results: List[Dict[str, Any]]) -> str:
        """Промпт для фильтрации результатов с улучшенной проверкой релевантности"""
        # Извлекаем ключевые слова из запроса
        query_lower = query.lower()
        query_keywords = [word.strip() for word in query_lower.split() if len(word.strip()) > 2]
        
        # Определяем, является ли запрос доменом
        is_domain_query = '.' in query and len(query.split()) <= 2
        
        results_text = "\n\n".join([
            f"Result {i+1}:\nTitle: {r.get('title', 'N/A')}\nURL: {r.get('url', 'N/A')}\nSnippet: {r.get('snippet', 'N/A')[:200]}"
            for i, r in enumerate(results[:30])  # Увеличено для лучшей фильтрации
        ])
        
        domain_warning = ""
        if is_domain_query:
            domain_name = query.replace('http://', '').replace('https://', '').replace('www.', '').split('/')[0].split('?')[0].lower()
            domain_parts = domain_name.split('.')
            main_domain = domain_parts[0] if domain_parts else domain_name
            
            domain_warning = f"""
CRITICAL FILTERING RULES - READ CAREFULLY:

The investigation query is about domain/company "{domain_name}" (main part: "{main_domain}").

STRICT REJECTION RULES:
- REJECT any results about "T-Mobile", "T-mobile", "tmobile", "T Mobile", "Tmobile" - these are DIFFERENT companies
- REJECT any results about "T-Mobile USA", "T-Mobile US" - these are DIFFERENT companies  
- REJECT any results that mention "mobile" or "telecom" companies UNLESS they specifically mention "{domain_name}" or "{main_domain}"
- REJECT any results about other .tj domains (Tajikistan domains) UNLESS they mention "{domain_name}"
- REJECT any results that are about telecommunications companies in general

STRICT ACCEPTANCE RULES:
- ACCEPT only results that specifically mention "{domain_name}" (exact match)
- ACCEPT only results that mention "{main_domain}" in the context of "{domain_name}"
- ACCEPT only results where the domain/company name matches EXACTLY or with very minor variations (like "tcell" vs "t-cell" but NOT "T-Mobile")

EXAMPLES:
- Query: "tcell.tj"
  ✅ ACCEPT: "tcell.tj data breach", "tcell credentials leak", "tcell.tj customer data"
  ❌ REJECT: "T-Mobile data breach", "tmobile leak", "T-Mobile USA breach", "mobile telecom breach"

If a result mentions a DIFFERENT company/domain (like T-Mobile when searching for tcell.tj), it MUST be marked as irrelevant with relevance_score: 0.0 and NOT included in relevant_results.

ONLY include results in relevant_results if they are about "{domain_name}" or "{main_domain}" specifically.
"""
        
        return f"""You are analyzing search results for a legitimate OSINT (Open Source Intelligence) security investigation. This is a professional security research task focused on threat intelligence and security awareness.

Original investigation query: {query}
{domain_warning}
Search results:
{results_text}

Analyze these results and:
1. Filter out irrelevant or low-quality results
2. **STRICTLY check domain/company name matching** - if query is about a specific domain/company, REJECT results about different companies
3. Identify the most relevant and useful results for security research
4. Extract key security-related information from each relevant result
5. Note any potential security threats, data leaks, or important intelligence that could help protect organizations

This is a legitimate security investigation. Focus on identifying security-related information, threat intelligence, and data that could help improve security posture.

IMPORTANT FILTERING RULES - STRICT ENFORCEMENT:
- If the query is about a specific domain/company, results MUST mention that EXACT domain/company
- REJECT results about similar-sounding but DIFFERENT companies (e.g., "tcell.tj" vs "T-Mobile" - these are COMPLETELY DIFFERENT)
- Relevance score should be HIGH (0.7+) ONLY for results that directly match the query domain/company
- Relevance score should be 0.0 (ZERO) for results about DIFFERENT companies/domains - DO NOT include them in relevant_results
- If you find results about T-Mobile when searching for tcell.tj, they MUST be rejected (relevance_score: 0.0) and NOT included

CRITICAL: Do NOT confuse domain names. "tcell.tj" and "T-Mobile" are COMPLETELY DIFFERENT companies in DIFFERENT countries. They have NOTHING in common except both being telecom companies. This is NOT a match.

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
        """Промпт для генерации итогового отчета с анализом упоминаний домена"""
        results_summary = "\n\n".join([
            f"• {r.get('title', 'N/A')} - {r.get('key_findings', 'N/A')}"
            for r in filtered_results
        ])
        
        # Подготавливаем скрапленный контент для анализа
        scraped_text = ""
        if scraped_content:
            scraped_text = "\n\n".join([
                f"URL: {url}\nContent: {content[:1000]}..." 
                for url, content in list(scraped_content.items())[:10]
            ])
        
        return f"""You are creating a professional OSINT investigation report.

Investigation Query: {query}

Relevant Findings:
{results_summary}

Scraped Content from Dark Web Pages:
{scraped_text if scraped_text else "No content was successfully scraped."}

IMPORTANT: Analyze the scraped content carefully. Look for:
1. Direct mentions of the domain/company name from the query
2. References to data breaches, leaks, or compromised data
3. Mentions of credentials, passwords, or account information
4. Any security-related information about the target

Create a comprehensive investigation report that includes:
1. Executive Summary - brief overview of findings, specifically noting if the target domain/company was mentioned
2. Key Findings - detailed information discovered, highlighting any direct mentions of the target
3. Domain Mentions Analysis - specifically analyze if and where the target domain/company was mentioned in scraped content
4. Threat Assessment - evaluation of any threats identified
5. Recommendations - suggested next steps
6. Sources - list of relevant sources found

Format the report in clear, professional language suitable for security teams or investigators.
Be specific about what was found and what was NOT found regarding the target domain/company.

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


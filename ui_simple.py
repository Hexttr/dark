"""
Упрощенная версия UI для диагностики
"""
import streamlit as st
from config import Config

st.set_page_config(
    page_title="Robin - Dark Web OSINT",
    page_icon="🕵️",
    layout="wide"
)

st.title("🕵️ Robin - AI-Powered Dark Web OSINT Tool")
st.markdown("---")

# Проверка соединений
st.header("Проверка соединений")

try:
    tor_ok = Config.validate_tor_connection()
    if tor_ok:
        st.success("✅ Tor подключен")
    else:
        st.error("❌ Tor не доступен")
except Exception as e:
    st.error(f"Ошибка проверки Tor: {e}")

try:
    ollama_ok = Config.validate_ollama_connection()
    if ollama_ok:
        st.success("✅ Ollama подключен")
    else:
        st.error("❌ Ollama не доступен")
except Exception as e:
    st.error(f"Ошибка проверки Ollama: {e}")

st.markdown("---")

# Простая форма
st.header("Тестовая форма")

query = st.text_input("Введите запрос", value="test")

if st.button("Тест"):
    st.write(f"Вы ввели: {query}")
    st.success("Форма работает!")

st.markdown("---")
st.info("Если вы видите эту страницу, значит Streamlit работает правильно.")



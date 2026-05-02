# **Автор:** Глеб Телицин (GaussArc)

# Currency-Converter
Конвертор валют - GUI-приложение «Currency Converter» с использованием внешнего API, сохранением истории и Git.

Простое приложение для конвертации валют с графическим интерфейсом (Tkinter). Использует бесплатное API [ExchangeRate-api](https://exchangerate-api.com). Сохраняет историю конвертаций в JSON-файл.

## Как получить API-ключ
1. Перейдите на [exchangerate-api.com](https://exchangerate-api.com).
2. Нажмите **Get Free Key**, введите ваш email и подтвердите.
3. После входа скопируйте ваш API-ключ.
4. Откройте файл `currency_converter.py`, найдите строку `self.api_key = "Введите сюда свой ключ"` и вставьте туда ваш ключ.

## Установка и запуск
1. Убедитесь, что установлен Python 3.7+.
2. Установите библиотеку `requests`:
   ```bash
   pip install requests

## Запустить программу можно с помощью команды
python currency_converter.py

import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import os
from datetime import datetime

# =================== Класс приложения ===================
class CurrencyConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")
        self.root.geometry("920x800")
        self.root.resizable(False, False)

        # API-ключ 
        self.api_key = "3ac228f2a4b552437ed19ad6"  
        self.base_url = "https://v6.exchangerate-api.com/v6/" + self.api_key + "/latest/"

        # Список популярных валют
        self.currencies = ["USD", "EUR", "GBP", "JPY", "CNY", "RUB", "CAD", "AUD", "CHF"]

        # Загрузка истории
        self.history_file = "history.json"
        self.history = self.load_history()

        # Переменные для виджетов
        self.from_currency = tk.StringVar(value="USD")
        self.to_currency = tk.StringVar(value="EUR")
        self.amount = tk.StringVar()
        self.result_var = tk.StringVar()

        # Построение интерфейса
        self.create_widgets()
        self.update_history_display()


    # =================== Работа с API ===================
    def get_exchange_rate(self, from_curr, to_curr):
        """Возвращает курс from_curr -> to_curr через API."""
        try:
            url = self.base_url + from_curr
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data["result"] == "success":
                    rates = data["conversion_rates"]
                    if to_curr in rates:
                        return rates[to_curr]
                    else:
                        messagebox.showerror("Ошибка", f"Валюта {to_curr} не найдена")
                        return None
                else:
                    messagebox.showerror("Ошибка", "Ошибка в ответе API")
                    return None
            else:
                messagebox.showerror("Ошибка", f"HTTP ошибка: {response.status_code}")
                return None
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось подключиться к API: {e}")
            return None

    # =================== Конвертация =================
    def convert(self):
        amount_str = self.amount.get().strip()
        if not amount_str:
            messagebox.showwarning("Предупреждение", "Введите сумму.")
            return
        try:
            amount = float(amount_str)
            if amount <= 0:
                messagebox.showwarning("Предупреждение", "Сумма должна быть положительным числом.")
                return
        except ValueError:
            messagebox.showwarning("Предупреждение", "Сумма должна быть числом.")
            return

        from_curr = self.from_currency.get()
        to_curr = self.to_currency.get()
        if from_curr == to_curr:
            result = amount
        else:
            rate = self.get_exchange_rate(from_curr, to_curr)
            if rate is None:
                return
            result = amount * rate

        result_text = f"{result:.2f} {to_curr}"
        self.result_var.set(result_text)

        # Добавление в историю
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history.append({
            "date": now,
            "amount": amount,
            "from": from_curr,
            "to": to_curr,
            "result": round(result, 2)
        })
        self.save_history()
        self.update_history_display()

    # =================== Работа с файлом JSON ===================
    def load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_history(self):
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=4)

    def update_history_display(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for rec in self.history:
            self.tree.insert("", "end", values=(
                rec["date"],
                rec["amount"],
                rec["from"],
                rec["to"],
                rec["result"]
            ))

    def clear_history(self):
        self.history = []
        self.save_history()
        self.update_history_display()
        messagebox.showinfo("Информация", "История очищена.")
        
        
    # =================== Интерфейс ===================
    def create_widgets(self):
        # Рамка ввода
        input_frame = ttk.LabelFrame(self.root, text="Конвертация", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(input_frame, text="Сумма:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(input_frame, textvariable=self.amount, width=15).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Из валюты:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        ttk.Combobox(input_frame, textvariable=self.from_currency, values=self.currencies, state="readonly", width=10).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="В валюту:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        ttk.Combobox(input_frame, textvariable=self.to_currency, values=self.currencies, state="readonly", width=10).grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(input_frame, text="Конвертировать", command=self.convert).grid(row=3, column=0, columnspan=2, pady=10)

        ttk.Label(input_frame, text="Результат:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(input_frame, textvariable=self.result_var, state="readonly", width=20).grid(row=4, column=1, padx=5, pady=5)

        # Рамка истории
        history_frame = ttk.LabelFrame(self.root, text="История конвертаций", padding=10)
        history_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("Дата", "Сумма", "Из", "В", "Результат")
        self.tree = ttk.Treeview(history_frame, columns=columns, show="headings", height=12)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Кнопка очистки истории
        ttk.Button(history_frame, text="Очистить историю", command=self.clear_history).pack(pady=5)
        
        

# =================== Запуск ===================
if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverter(root)
    root.mainloop()
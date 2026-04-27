import tkinter as tk
import os
import platform  # Додаємо цей модуль

def say_hello():
    name = entry.get().lower().strip()
    disallowed_words = ["блять", "иди нахуй", "сука"] 
    
    if any(word in name for word in disallowed_words):
        label_result.config(text="Ой-ой... Подивись у консоль!", fg="red")
        
        message = "He Delai tak bolbsie ;)"
        current_os = platform.system()

        if current_os == "Windows":
            os.system(f'start cmd /k "color 06 && echo {message}"')
        
        elif current_os == "Darwin":  # macOS
            # Скрипт AppleScript відкриває термінал і виконує команду
            os.system(f"osascript -e 'tell application \"Terminal\" to do script \"echo {message}\"'")
        
        elif current_os == "Linux":
            # Намагаємось відкрити найпопулярніші термінали
            # 'bash -c' дозволяє виконати команду і залишити вікно (через sleep або read)
            cmd_linux = f'bash -c "echo {message}; exec bash"'
            os.system(f'gnome-terminal -- {cmd_linux} || xterm -e {cmd_linux} || konsole -e {cmd_linux}')
            
    elif name:
        label_result.config(text=f"Привіт, {name.capitalize()}!", fg="black")
    else:
        label_result.config(text="Будь ласка, введіть ім'я", fg="gray")

# Создание интерфейса
root = tk.Tk()
root.title("Программа с характером")
root.geometry("350x250")

tk.Label(root, text="Як тебе звати?").pack(pady=10)
entry = tk.Entry(root)
entry.pack(pady=5)
tk.Button(root, text="Привітатись", command=say_hello).pack(pady=10)
label_result = tk.Label(root, text="", font=("Arial", 12, "bold"))
label_result.pack(pady=10)

root.mainloop()
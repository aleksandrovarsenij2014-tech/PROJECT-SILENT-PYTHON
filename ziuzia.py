import time
import random
import sys

# --- НАСТРОЙКИ И СОСТОЯНИЕ ---
state = {
    "hp": 100,
    "stamina": 100,
    "inventory": [],
    "location": "start",
    "lights_on": False,
    "elevator_fixed": False,
    "monster_pos": "unknown",
    "day": 1,
    "sanity": 100  # Рассудок (если 0 - галлюцинации)
}

# --- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ---
def p(text, delay=0.02):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def status():
    print(f"\n[ ❤️ HP: {state['hp']} | ⚡ Выносливость: {state['stamina']} | 🧠 Рассудок: {state['sanity']} ]")
    print(f"[ 🎒 Инвентарь: {', '.join(state['inventory']) if state['inventory'] else 'пусто'} ]")
    print("-" * 50)

def game_over(reason):
    p(f"\n--- {reason.upper()} ---", 0.1)
    p("Ваша история закончилась в этих стенах...", 0.05)
    sys.exit()

# --- МЕХАНИКИ ---
def check_death():
    if state['hp'] <= 0: game_over("Вы погибли от ран")
    if state['sanity'] <= 0: game_over("Вы сошли с ума от ужаса")

def spend_stamina(amount):
    state['stamina'] -= amount
    if state['stamina'] < 0:
        state['hp'] -= 10
        p("! Вы истощены и теряете здоровье !")

# --- ЛОКАЦИИ ---

def loc_start():
    p("\nВы в подсобке. Пахнет бензином и старой бумагой.")
    status()
    print("1. Выйти в главный зал")
    print("2. Обыскать ящики")
    print("3. Отдохнуть (восстановить силы)")
    
    cmd = input("> ")
    if cmd == "1":
        state['location'] = "hall"
    elif cmd == "2":
        if "Лом" not in state['inventory']:
            p("Вы нашли тяжелый стальной Лом.")
            state['inventory'].append("Лом")
        else:
            p("Тут больше ничего нет.")
    elif cmd == "3":
        p("Вы немного поспали, но монстр стал ближе...")
        state['stamina'] = min(100, state['stamina'] + 30)
        state['sanity'] -= 5

def loc_hall():
    p("\nОгромный холл больницы. Тьма здесь кажется живой.")
    if not state['lights_on']:
        p("Слишком темно. Вы слышите скрежет когтей где-то справа.")
    
    status()
    print("1. Идти к посту медсестры")
    print("2. Идти к лифтам")
    print("3. Спуститься в подвал (нужен свет)")
    print("4. Вернуться в подсобку")
    
    cmd = input("> ")
    if cmd == "1": state['location'] = "nurse_post"
    elif cmd == "2": state['location'] = "elevator_lobby"
    elif cmd == "3":
        if "Фонарик" in state['inventory'] or state['lights_on']:
            state['location'] = "basement"
        else:
            p("Вы боитесь идти в такую темень без света.")
    elif cmd == "4": state['location'] = "start"

def loc_nurse_post():
    p("\nРазбитый стол регистрации. На стене висит карта.")
    status()
    print("1. Искать ключи")
    print("2. Искать аптечку")
    print("3. Вернуться в холл")
    
    cmd = input("> ")
    if cmd == "1":
        if "Ключ-карта" not in state['inventory']:
            p("Вы нашли Ключ-карту от электрощитовой!")
            state['inventory'].append("Ключ-карта")
        else:
            p("Ключей больше нет.")
    elif cmd == "2":
        p("Вы нашли бинты. +20 HP.")
        state['hp'] = min(100, state['hp'] + 20)
    elif cmd == "3": state['location'] = "hall"

def loc_basement():
    p("\nПодвал. Здесь гудят трубы. Виден электрощиток.")
    status()
    if "Предохранитель" in state['inventory']:
        print("1. Починить щиток (вставить предохранитель)")
    print("2. Искать что-нибудь полезное")
    print("3. Уйти обратно")
    
    cmd = input("> ")
    if cmd == "1" and "Предохранитель" in state['inventory']:
        p("Свет моргнул и загорелся! Теперь лифты работают.")
        state['lights_on'] = True
        state['inventory'].remove("Предохранитель")
    elif cmd == "2":
        if "Фонарик" not in state['inventory']:
            p("Вы нашли Фонарик!")
            state['inventory'].append("Фонарик")
        else:
            p("Только ржавые трубы.")
    elif cmd == "3": state['location'] = "hall"

def loc_elevator_lobby():
    p("\nЛифтовая площадка. Двери лифта закрыты.")
    status()
    if state['lights_on']:
        print("1. Вызвать лифт и уехать (ПОБЕДА)")
    else:
        p("Лифт обесточен. Нужно питание из подвала.")
    print("2. Идти в столовую")
    print("3. Вернуться в холл")
    
    cmd = input("> ")
    if cmd == "1" and state['lights_on']:
        p("Двери открываются... Вы заходите внутрь и нажимаете кнопку 1 этажа.")
        p("Свет в лифте мигает, но вы чувствуете движение вверх.")
        game_over("Победа! Вы выбрались!")
    elif cmd == "2": state['location'] = "canteen"
    elif cmd == "3": state['location'] = "hall"

def loc_canteen():
    p("\nСтоловая. Повсюду перевернутые столы.")
    status()
    print("1. Обыскать кухню")
    print("2. Спрятаться под стол (безопасно)")
    print("3. Вернуться к лифтам")
    
    cmd = input("> ")
    if cmd == "1":
        if "Предохранитель" not in state['inventory'] and not state['lights_on']:
            p("В кухонном ящике вы нашли Предохранитель!")
            state['inventory'].append("Предохранитель")
        else:
            p("Тут только гнилая еда. Вы теряете рассудок.")
            state['sanity'] -= 10
    elif cmd == "2":
        p("Вы сидите в тишине. Снаружи кто-то бродит...")
        spend_stamina(-20) # Отдых
        time.sleep(2)
    elif cmd == "3": state['location'] = "elevator_lobby"

# --- ГЛАВНЫЙ ЦИКЛ ---
p("--- PROJECT: SILENT PYTHON ---", 0.05)
p("Вы очнулись в заброшенной лечебнице. Единственный выход - лифт в холле.")
p("Но здание обесточено, а в тенях КТО-ТО есть...")

while True:
    check_death()
    
    # Случайное событие "Монстр"
    if random.random() < 0.2:
        p("\n!!! ИЗ ТЕМНОТЫ ВЫПРЫГИВАЕТ ТВАРЬ !!!")
        p("1. Бить ломом (нужен лом)")
        p("2. Бежать (тратит выносливость)")
        p("3. Замереть")
        
        act = input("?? ")
        if act == "1" and "Лом" in state['inventory']:
            p("Вы отбились, но тварь ранила вас!")
            state['hp'] -= 15
        elif act == "2":
            p("Вы убежали, задыхаясь от страха.")
            spend_stamina(40)
        else:
            p("Тварь терзает вас!")
            state['hp'] -= 40
            state['sanity'] -= 20

    # Переход по локациям
    if state['location'] == "start": loc_start()
    elif state['location'] == "hall": loc_hall()
    elif state['location'] == "nurse_post": loc_nurse_post()
    elif state['location'] == "basement": loc_basement()
    elif state['location'] == "elevator_lobby": loc_elevator_lobby()
    elif state['location'] == "canteen": loc_canteen()
    
    # Естественный износ
    spend_stamina(5)
    state['sanity'] -= 2
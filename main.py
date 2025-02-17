import json
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.graphics import Line
import math

# Funkcja do załadowania danych z pliku JSON
def load_data():
    try:
        with open('data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"history": [], "progress": 0}  # Jeśli plik nie istnieje, zwróć pustą historię

# Funkcja do zapisania danych do pliku JSON
def save_data(data):
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)

# Funkcja do zapamiętywania postępu dziecka
def update_progress(data, correct):
    data['progress'] += 1 if correct else 0
    save_data(data)

# Rysowanie drzewa fraktalnego
class FractalTree(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.draw_tree(self.width / 2, 100, 90, 100, 10)
    
    def draw_tree(self, x, y, angle, length, level):
        if level == 0:
            return
        # Obliczanie końcowego punktu
        x_end = x + length * math.cos(math.radians(angle))
        y_end = y + length * math.sin(math.radians(angle))
        
        # Rysowanie linii
        with self.canvas:
            Line(points=[x, y, x_end, y_end], width=2)
        
        # Rekurencyjne rysowanie gałęzi
        self.draw_tree(x_end, y_end, angle - 30, length * 0.7, level - 1)
        self.draw_tree(x_end, y_end, angle + 30, length * 0.7, level - 1)

# Aplikacja główna
class EduTreeApp(App):
    def build(self):
        self.label = Label(text="Witaj w EduTree!")
        
        # Tworzenie przycisku do rozpoczęcia nauki
        button = Button(text="Rozpocznij naukę")
        button.bind(on_press=self.start_learning)
        
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.label)
        layout.add_widget(button)
        
        # Inicjalizowanie widgetu drzewa
        self.tree_widget = FractalTree()
        layout.add_widget(self.tree_widget)
        
        # Wczytanie danych o postępach
        self.data = load_data()
        
        return layout
    
    def start_learning(self, instance):
        # Zadawanie pytania matematycznego
        self.ask_question()

    def ask_question(self):
        question = "Ile to 2 + 3?"
        correct_answer = 5
        
        # Wyświetlenie pytania w etykiecie
        self.label.text = f"Pytanie: {question}"
        
        # Tworzenie przycisku do udzielenia odpowiedzi
        button = Button(text="5")
        button.bind(on_press=lambda x: self.check_answer(x, correct_answer))
        
        # Dodanie przycisku odpowiedzi do układu
        self.root.add_widget(button)

    def check_answer(self, instance, correct_answer):
        user_answer = int(instance.text)
        
        if user_answer == correct_answer:
            self.label.text = "Dobra odpowiedź!"
            update_progress(self.data, True)
            self.tree_widget.draw_tree(self.tree_widget.width / 2, 100, 90, 100, 10 + self.data['progress'])
        else:
            self.label.text = "Zła odpowiedź. Spróbuj ponownie!"
            update_progress(self.data, False)

# Uruchomienie aplikacji
if __name__ == '__main__':
    EduTreeApp().run()
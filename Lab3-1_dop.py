# Вивести час виконання через popup
import kivy.app
import kivy.uix.boxlayout
import kivy.uix.textinput
import kivy.uix.label
import kivy.uix.button
import kivy.uix.popup
import time
from kivy.clock import Clock


def ferma(n):
    if n == 1:
        return [1]
    if n%2 == 0:
        return [2]+ferma(n/2)
    x = int(n**0.5) + 1
    while not ((x**2 - n)**0.5).is_integer():
        x += 1
    y = (x**2 - n)**0.5
    p = x + y
    q = x - y
    if p == 1:
        return [q]
    if q == 1:
        return [p]
    return ferma(p)+ferma(q)


class SimpleApp(kivy.app.App):
    def build(self):
        self.textInput = kivy.uix.textinput.TextInput()
        self.label = kivy.uix.label.Label()
        self.button = kivy.uix.button.Button(text="ОК!")
        self.button.bind(on_press=self.displayMessage)
        self.boxLayout = kivy.uix.boxlayout.BoxLayout(orientation="vertical")
        self.boxLayout.add_widget(self.textInput)
        self.boxLayout.add_widget(self.label)
        self.boxLayout.add_widget(self.button)
        return self.boxLayout
    def displayMessage(self, btn):
        start_time = time.time()
        text = self.textInput.text
        if not text.isdigit():
             self.label.text = 'Введено недопустиме значення'
             return
        text = int(text)    

        self.label.text = str(list(map(int, ferma(text))))[1:-1]
        popup = kivy.uix.popup.Popup(title='Time', content=kivy.uix.label.Label(text=f'Час виконання: {time.time()-start_time}'),
              auto_dismiss=False)
        popup.open()
        Clock.schedule_once(lambda x: popup.dismiss(), 3)
if __name__ == "__main__":
    simpleApp = SimpleApp()
    simpleApp.run()

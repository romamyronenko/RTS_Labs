import time
import kivy.app
import kivy.uix.boxlayout
import kivy.uix.textinput
import kivy.uix.label
import kivy.uix.button


def to_dots(dots: str):
    d = dots.replace(" ", "")[:-1].split("),")
    for i in range(len(d)):
        d[i] = tuple(map(int, d[i][1:].split(",")))
    return d


def learn(dots, p, speed=0.01, count_of_iter=1000, deadline=float('inf')):
    start_time = time.time()
    w1, w2 = 0, 0
    flag = False
    for _ in range(count_of_iter):
        for (i, j) in dots:
            delta = p - (i*w1 + j*w2)
            w1 = w1 + delta*i*speed
            w2 = w1 + delta*j*speed
            if time.time() - start_time > deadline*1000:
                flag = True
                break
        if flag:
            break
    return w1, w2


class SimpleApp(kivy.app.App):
    def build(self):
        self.dotslabel = kivy.uix.label.Label()
        self.textInput1 = kivy.uix.textinput.TextInput(text="(0, 6),(1, 5),(3, 3),(2, 4)")
        self.plabel = kivy.uix.label.Label()
        self.textInput2 = kivy.uix.textinput.TextInput(text="4")
        self.label = kivy.uix.label.Label()
        self.button = kivy.uix.button.Button(text="ОК!")
        self.button.bind(on_press=self.displayMessage)
        self.boxLayout = kivy.uix.boxlayout.BoxLayout(orientation="vertical")
        self.boxLayout.add_widget(self.dotslabel)
        self.boxLayout.add_widget(self.textInput1)
        self.boxLayout.add_widget(self.plabel)
        self.boxLayout.add_widget(self.textInput2)
        self.dotslabel.text = "                Точки\n(наприклад, '(1, 2), (3, 4)')"
        self.plabel.text = "Значення p"
        self.boxLayout.add_widget(self.label)
        self.boxLayout.add_widget(self.button)
        return self.boxLayout

    def displayMessage(self, btn):
        try:
            dots = to_dots(self.textInput1.text)
            result = learn(dots, int(self.textInput2.text))
            check = [i[0]*result[0] + i[1]*result[1] for i in dots]
            self.label.text = f'w1 = {result[0]}\nw2 = {result[1]}\nПеревірка: {check}'
        except:
            self.label.text = "Введено некоректні значення"
if __name__ == "__main__":
    simpleApp = SimpleApp()
    simpleApp.run()


def test():
    """Значення, задані в лабораторній"""
    P = 4
    dots = ((0, 6),
            (1, 5),
            (3, 3),
            (2, 4))
    speeds = (0.001, 0.01, 0.05, 0.1, 0.2, 0.3)
    deadlines = (0.5, 1, 2, 5)
    counts_of_iter = (100, 200, 500, 1000)
    for speed in speeds:
        print(f'speed: {speed}')
        for dl, coi in zip(deadlines, counts_of_iter):
            w1, w2 = learn(dots, P, speed, coi, dl)
            print(f'\tcount of iter: {coi}, w1 = {w1}, w2 = {w2}', coi)
            for x, y in dots:
                print(f'\t\t{(x, y)}, res: {w1*x + w2*y}')
        print()

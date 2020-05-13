import random
import kivy.app
import kivy.uix.boxlayout
import kivy.uix.textinput
import kivy.uix.label
import kivy.uix.button


class GenesContainer:
    def __init__(self, count=10, coefs=(1,2,3,4), y=14, mutation_probability=0.05):
        self.y = y
        self.length = count
        self.coefs = coefs
        self.gene_length = len(coefs)
        self.mutate_prob = mutation_probability
        self.genes = [Gene(length=self.gene_length) for _ in range(self.length)]
        self.deltas = [i*self.coefs-self.y for i in self.genes]        
    
    def mutate(self):
        """Mutate random gene with probability mutate_prob."""
        if random.random() < self.mutate_prob:
            random.choice(self.genes).mutate()
    
    def next_generation(self):
        """Cross genes in pairs."""
        self.inverse_deltas = [1/i for i in self.deltas]
        self.ps = [i/sum(self.inverse_deltas) for i in self.inverse_deltas]
        self.mutate()

        a, b = random.randint(0, self.length-1), random.randint(0, self.length-1)
        self.genes[a], self.genes[b] = self.genes[a] | self.genes[b]
        self.deltas = [i*self.coefs-self.y for i in self.genes]
       
    @property     
    def done(self):
        return 0 in self.deltas
    
    @property
    def result(self):
        while not self.done:
            self.next_generation()
        return self.genes[self.deltas.index(0)]


    def __str__(self):
        return str(self.deltas)


class Gene:
    def __init__(self, value=None, length=4):
        if value is not None:
            self.value = value
        else:
            self.value = [random.randint(0, 10) for _ in range(length)]
    
    def mutate(self):
        """Mutate random gene parameter."""
        self.value[random.randint(0, len(self.value)-1)] += random.choice((1, -1))

    @property
    def length(self):
        """Return count of nums in gene."""
        return len(self.value)

    def __or__(self, other):
        """Crossing of genes."""
        if self.length != other.length:
            assert "Crossing is unreal"

        r = random.randint(0, self.length - 1)
        self.value[r], other.value[r] = other.value[r], self.value[r]
        return self, other

    def __mul__(self, other):
        """Return gene multiply by weights"""
        if len(other) != self.length:
            assert "Different lengths"
        return sum([self.value[i]*other[i] for i in range(self.length)])
    
    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return str(self.value)


class SimpleApp(kivy.app.App):
    def build(self):
        self.dotslabel = kivy.uix.label.Label()
        self.textInput1 = kivy.uix.textinput.TextInput(text="1, 5, 6, 1")
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
        self.dotslabel.text = "                Коефіцієнти\n(наприклад, '1, 5, 6, 1')"
        self.plabel.text = "Значення y"
        self.boxLayout.add_widget(self.label)
        self.boxLayout.add_widget(self.button)
        return self.boxLayout

    def displayMessage(self, btn):
        try:
            coefs = list(map(int, self.textInput1.text.replace(" ", "").split(",")))
            g = GenesContainer(count=11, coefs=coefs, y=int(self.textInput2.text), mutation_probability=0.001)
            result = g.result
            self.label.text = f'Результат: {result}'
        except:
            self.label.text = "Введено некоректні значення"
if __name__ == "__main__":
    simpleApp = SimpleApp()
    simpleApp.run()
g = GenesContainer(count=11, coefs=(1, 0, -2, 4), y=-4, mutation_probability=0.001)

print(g.result)


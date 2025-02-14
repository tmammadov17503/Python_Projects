class Animal:
    def __init__(self):
        self.num_eyes = 2
        self.num_ears = 2
        self.num_nose = 1

    def breathe(self):
        print("Inhale, exhale")


class Fish(Animal):
    def __init__(self):
        super().__init__()

    def breathe(self):
        super().breathe()
        print("doing this underwater")
    def swim(self):
        print("Fish is moving in water")

nemo_fish = Fish()
nemo_fish.swim()
nemo_fish.breathe()
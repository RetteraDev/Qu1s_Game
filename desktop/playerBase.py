

playerClasses = ['Медик', 'Картограф', 'Журналист', 'Полицейский']


class Player:
    def __init__(self):
        self.equipment = []
        self.sex = ''
        
        self.carDriving = False
        self.smoking = False
        self.drinking = False
        self.sick = False
        
        self.health = 100
        self.heat = 100
        self.food = 100
        self.water = 100      
        

class Doctor(Player):
    def __init__(self, name):
        super().__init__()
        
        self.name = name
        self.carDriving = True 


class Policeman(Player):
    def __init__(self, name):
        super().__init__()
        
        self.name = name
        self.carDriving = True 
        self.shooting = True

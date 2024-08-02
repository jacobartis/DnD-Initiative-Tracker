import random as rnd

class initiative_creature:
    _id:int = 0
    _name:str = ""
    _initiative:int = 0
    def __init__(self,id:int,initia:int) -> None:
        self._id = id
        self._initiative = initia
    
    def get_id(self) -> int:
        return self._id

    def get_name(self) -> str:
        return self._name
    
    def get_initiative(self) -> int:
        return self._initiative

class intiative_tracker:
    CREATURE_ID:int = 0
    CREATURE:int = 1

    next_id = 0
    initiative: int = 0
    creatures: dict = {
    }

    #Stores upcomming creatures
    initiative_stack:list[initiative_creature] = []
    #Stores prev creatures
    initiative_stack_prev:list[initiative_creature] = []

    def get_next_id(self):
        id = self.next_id
        self.next_id += 1
        return id 

    def next_turn(self):
        self.generate_stack()
        self.initiative = self.initiative_stack[0][self.CREATURE].get_initiative()

    
    def next_initiative(self):
        #Resets if empty or last creature finished their turn
        if len(self.initiative_stack)<= 1:
            self.next_turn()
        #Adds current latest creature to the front of the prev stack
        self.initiative_stack_prev.insert(0,self.initiative_stack.pop(0))

        #Sets current initiative to next turns initiative
        self.initiative = self.initiative_stack[0][self.CREATURE].get_initiative()
        print(self.initiative)

    def prev_initiative(self):
        #Returns if at start of initiative
        if not len(self.initiative_stack_prev):
            return
        
        #Readds top of prev stack to current stack
        self.initiative_stack.insert(0,self.initiative_stack_prev.pop(0))

        #Updates initiative to current turn
        self.initiative = self.initiative_stack[0][self.CREATURE].get_initiative()
        print(self.initiative)

    #Adds a new creature to the list
    def add_creature(self,initia:int):
        new_creature = initiative_creature(self.get_next_id(),initia)
        self.creatures[new_creature.get_id()] = new_creature

    #Generates the initiative stack using the current creature list
    def generate_stack(self, current=0):
        #Sorts creatures by initiative high to low and adds them to the stack
        creature_list = list(self.creatures.items())
        creature_list.sort(key=lambda x:x[self.CREATURE].get_initiative())
        creature_list.reverse()
        self.initiative_stack = creature_list
        self.initiative_stack_prev = []




tracker = intiative_tracker()
for x in range(5):
    tracker.add_creature(rnd.randint(0,20))
tracker.generate_stack()

tracker.next_initiative()
tracker.next_initiative()
tracker.next_initiative()
tracker.prev_initiative()
tracker.next_initiative()
tracker.next_initiative()
tracker.next_initiative()
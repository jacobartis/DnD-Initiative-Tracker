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

    _next_id = 0
    _initiative: int = 0
    _creatures: dict = {}

    #Stores upcomming creatures
    _initiative_stack:list[initiative_creature] = []
    #Stores prev creatures
    _initiative_stack_prev:list[initiative_creature] = []

    def get_creatures(self):
        return self._creatures

    def get_initiative(self):
        return self._initiative

    def _get_next_id(self):
        id = self._next_id
        self._next_id += 1
        return id 

    #Updates initiative to current turn
    def _update_initiative(self):
        self._initiative = self._initiative_stack[0][self.CREATURE].get_initiative()

    #Adds a new creature to the list
    def add_creature(self,initia:int):
        new_creature = initiative_creature(self._get_next_id(),initia)
        self._creatures[new_creature.get_id()] = new_creature
    
    #Generates the initiative stack using the current creature list
    def _generate_stack(self, current=0):
        #Sorts creatures by initiative high to low and adds them to the stack
        creature_list = list(self._creatures.items())
        creature_list.sort(key=lambda x:x[self.CREATURE].get_initiative())
        creature_list.reverse()
        self._initiative_stack = creature_list
        self._initiative_stack_prev = []

    def next_turn(self):
        self._generate_stack()
        self._update_initiative()
    
    def next_initiative(self):
        #Resets if empty or last creature finished their turn
        if len(self._initiative_stack)<= 1:
            self.next_turn()
        #Adds current latest creature to the front of the prev stack
        self._initiative_stack_prev.insert(0,self._initiative_stack.pop(0))

        self._update_initiative()
        print(self._initiative)

    def prev_initiative(self):
        #Returns if at start of initiative
        if not len(self._initiative_stack_prev):
            return
        
        #Readds top of prev stack to current stack
        self._initiative_stack.insert(0,self._initiative_stack_prev.pop(0))

        self._update_initiative()

        print(self._initiative)


def main():
    tracker = intiative_tracker()
    for x in range(5):
        tracker.add_creature(rnd.randint(0,20))
    tracker.next_turn()

    tracker.next_initiative()
    tracker.next_initiative()
    tracker.next_initiative()
    tracker.prev_initiative()
    tracker.next_initiative()
    tracker.next_initiative()
    tracker.next_initiative()

if __name__ == "__main__":
    main()
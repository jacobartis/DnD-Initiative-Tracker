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

class tracker:
    CREATURE_ID:int = 0
    CREATURE:int = 1

    _next_id = 0
    _creatures: dict = {}

    #Stores upcomming creatures
    _initiative_stack:list[initiative_creature] = []
    #Stores prev creatures
    _initiative_stack_prev:list[initiative_creature] = []

    #Returns creature dict
    def get_creatures(self):
        return self._creatures

    #Returns the current creature
    def get_active_creature(self):
        if not self._initiative_stack: return
        return self._initiative_stack[0][self.CREATURE]

    #Return initiative of current creature
    def get_initiative(self):
        if not self.get_active_creature(): return
        return self.get_active_creature().get_initiative()

    def _get_next_id(self):
        id = self._next_id
        self._next_id += 1
        return id 

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
    
    def next_initiative(self):
        #Resets if empty or last creature finished their turn
        if len(self._initiative_stack)<= 1:
            self.next_turn()
            return
        #Adds current latest creature to the front of the prev stack
        self._initiative_stack_prev.insert(0,self._initiative_stack.pop(0))

    def prev_initiative(self):
        #Returns if at start of initiative
        if not len(self._initiative_stack_prev):
            return
        
        #Readds top of prev stack to current stack
        self._initiative_stack.insert(0,self._initiative_stack_prev.pop(0))


def main():
    tracker = intiative_tracker()
    for x in range(5):
        tracker.add_creature(rnd.randint(0,20))

if __name__ == "__main__":
    main()
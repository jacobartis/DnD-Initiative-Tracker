import initiative_tracker as it
import unittest

class TestStringMethods(unittest.TestCase):

    def test_creature_creation(self):
        self.assertIsInstance(it.initiative_creature(),it.initiative_creature,"creatures are being created")

    def test_creature_name(self):
        creature = it.initiative_creature()
        creature.set_name("Johnson")
        self.assertEqual(creature.get_name(),'Johnson',"Creature get or set name incorrect.")

    def test_creature_name_int(self):
        creature = it.initiative_creature()
        creature.set_name(30)
        self.assertEqual(creature.get_name(),'30',"Creature name breaks when entering int.")

    def test_creature_initiative(self):
        creature = it.initiative_creature()
        creature.set_initiative(20)
        self.assertEqual(creature.get_initiative(),20,"Creature get or set initiative incorrect.")

    def test_creature_initiative_str(self):
        creature = it.initiative_creature()
        creature.set_initiative("warning")
        self.assertEqual(creature.get_initiative(),0,"Creature get or set initiative incorrect.")

    def test_tracker_creation(self):
        self.assertIsInstance(it.tracker(),it.tracker,"tracker installed an working")

if __name__ == '__main__':
    unittest.main()
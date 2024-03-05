"""
Roguelike game 1 - stats and weapon

DESCRIPTION:
To solve this kata, you need to create a character class that can be used for a roguelike game. 
Instances of this class must have the characteristics strength, dexterity and intelligence and can call some test-generated methods 
that will change these characteristics or give the character a new weapon.

The Character class must have 2 mandatory instance methods - one will display character information and the other will display the event log. 
Only these output methods will be checked by tests The names of the properties or how the user stores any values is entirely up to the user and individual properties will not be checked.

Character
The character has a name and 3 main characteristics: strength, dexterity, intelligence. Name and characteristics are set randomly when creating a character; 
if some characteristic is not specified, then the default value is taken equal to 10, name default value is 'Hero'. Initially, the character is armed only with his 'limbs'(lowercase), 
the damage from which is equal to the sum of his characteristics.

https://www.codewars.com/kata/651bfcbd409ea1001ef2c3cb - full description with example of usage the character class
"""

from types import MethodType
import re


class Unit:
    def __init__(self, name: str, dexterity: int, strength: int, intelligence: int):
        self.name = name
        self.strength = strength
        self.dexterity = dexterity
        self.intelligence = intelligence

    def __repr__(self):
        return self.name

class Weapon(Unit):
    def __init__(self, name, dexterity, strength, intelligence, extra_damage: int):
        super().__init__(name, dexterity, strength, intelligence)
        self.extra_damage = extra_damage
        self.name = name.capitalize().replace("_", " ")

class Character(Unit):
    WEAPON_NAME_PATTERN = r"\w+_of_\w+"

    def __init__(self, name = 'Hero', dexterity = 10, strength = 10, intelligence = 10):
        super().__init__(name, dexterity, strength, intelligence)
        self.name = name.capitalize()
        self.weapons = {}

    def add_weapon(self, name, dexterity, strength, intelligence, extra_damage):
        if name not in self.weapons:
            self.weapons.update({name: Weapon(name, dexterity, strength, intelligence, extra_damage)})
        else:
            weapon = self.weapons[name]
            weapon.name = f"{weapon.name}(enhanced)"
            updates = [
                ("dexterity", dexterity), 
                ("strength", strength), 
                ("intelligence", intelligence), 
                ("extra_damage", extra_damage)]
            for attr, value in updates:
                setattr(weapon, attr, max(getattr(weapon, attr), value))


    def __getattr__(self, attr):
        if re.match(self.WEAPON_NAME_PATTERN, attr):
            def _add_weapon(*args):
                return self.add_weapon(attr, *args)
            return _add_weapon
        raise AttributeError(f"{attr} is not a valid attribute")

    @property
    def get_strength(self):
        return self.strength

    @property
    def get_dexterity(self):
        return self.dexterity

    @property
    def get_intelligence(self):
        return self.intelligence

    def set_strength(self, value):
        self.strength += value

    def set_dexterity(self, value):
        self.dexterity += value

    def set_intelligence(self, value):
        self.intelligence += value
    

    def limbs(self):
        return sum([self.get_strength, self.get_dexterity, self.get_intelligence])
    
    def strange_fruit(self, strength, dexterity, intelligence):
        self.set_strength(strength)
        self.set_dexterity(dexterity)
        self.set_intelligence(intelligence)

    def character_info(self):
        """ Return a multiline string representing the current characteristics of the hero """
        return f"{self.name}\nstr {self.strength}\ndex {self.dexterity}\nint {self.intelligence}\nlimbs {self.limbs()} dmg"
        
    def event_log(self) -> str:
        """ Return a multiline string representing the events that occured in chronological order """

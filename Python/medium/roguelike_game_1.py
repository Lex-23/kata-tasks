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


import re


class Unit:
    def __init__(self, name: str, strength: int, dexterity: int, intelligence: int):
        self.name = name.capitalize()
        self.strength = strength
        self.dexterity = dexterity
        self.intelligence = intelligence

    def __repr__(self):
        return self.name
    
class Event(Unit):
    def __init__(self, name, strength, dexterity, intelligence):
        super().__init__(name, strength, dexterity, intelligence)
        self.name = name.capitalize().replace("_", " ")

class RandomEvent(Event):
    """Class for describing random event that may change Charcter's attributes"""

    def get_log(self):
        def _prepare_value(event: Event, attr: str) -> str:
            value = getattr(event, attr)
            if value == 0:
                return ""
            else:
                return f"{attr} +{value}," if value > 0 else f"{attr} {value},"
        return f"{self.name}: {_prepare_value(self, 'strength')} {_prepare_value(self, 'dexterity')} {_prepare_value(self, 'intelligence')}"[0: -1]

class Weapon(Event):
    def __init__(self, name, strength, dexterity, intelligence, extra_damage: int):
        super().__init__(name, strength, dexterity, intelligence)
        self.extra_damage = extra_damage

class Character(Unit):
    WEAPON_NAME_PATTERN = r"\w+_of_\w+"
    RANDOM_EVENT_PATTERN = r"\w+_\w+"

    def __init__(self, name = 'Hero', strength = 10, dexterity = 10, intelligence = 10):
        super().__init__(name, strength, dexterity, intelligence)
        self.name = name.capitalize()
        self.weapons = {}
        self.log = ""

    def log_weapon(self, weapon: Weapon) -> None:
        log = self.log
        self.log = log + f"{self.name} finds '{weapon.name}'\n"

    def log_random_event(self, event: RandomEvent) -> None:
        log = self.log
        self.log = log + f"{event.get_log()}\n"

    def add_weapon(self, name, strength, dexterity, intelligence, extra_damage) -> None:
        if name not in self.weapons:
            new_weapon = Weapon(name, strength, dexterity, intelligence, extra_damage)
            self.weapons.update({name: new_weapon})
            self.log_weapon(new_weapon)
        else:
            weapon = self.weapons[name]
            self.log_weapon(weapon)
            weapon.name = f"{weapon.name}(enhanced)"
            updates = [
                ("dexterity", dexterity), 
                ("strength", strength), 
                ("intelligence", intelligence), 
                ("extra_damage", extra_damage)]
            for attr, value in updates:
                setattr(weapon, attr, max(getattr(weapon, attr), value))

    def perform_random_event(self, name, strength, dexterity, intelligence) -> None:
            event = RandomEvent(name, strength, dexterity, intelligence)
            updates = [
                ("strength", event.strength),
                ("dexterity", event.dexterity), 
                ("intelligence", event.intelligence), 
            ]
            for attr, value in updates:
                setattr(self, attr, value)
            self.log_random_event(event)

    def count_damage(self, weapon=None) -> int:
        if not weapon:
            return sum([self.get_strength, self.get_dexterity, self.get_intelligence])
        return sum(
                    [self.get_strength * weapon.strength,
                    self.get_dexterity * weapon.dexterity, 
                    self.get_intelligence * weapon.intelligence, 
                    weapon.extra_damage]
                )

    def find_strongest_weapon(self) -> tuple:
        weapons = self.weapons
        damage_dict = {weapon: self.count_damage(weapon) for weapon in weapons.values()}
        if len(weapons) == 1: 
            weapon = list(weapons.values())[0]
        else:
            weapon = max(damage_dict, key=damage_dict.get)
        return (weapon, damage_dict[weapon])

    def get_damage_record(self) -> str:
        if not self.weapons:
            return f'limbs {self.count_damage()} dmg'
        weapon_data = self.find_strongest_weapon()
        return f'{weapon_data[0].name} {weapon_data[1]} dmg'

    def __getattr__(self, attr):
        if re.match(self.WEAPON_NAME_PATTERN, attr):
            def _add_weapon(*args):
                return self.add_weapon(attr, *args)
            return _add_weapon
        elif re.match(self.RANDOM_EVENT_PATTERN, attr):
            def _perform_random_event(*args):
                return self.perform_random_event(attr, *args)
            return _perform_random_event 
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

    def character_info(self):
        """ Return a multiline string representing the current characteristics of the hero """
        return f"{self.name}\nstr {self.strength}\ndex {self.dexterity}\nint {self.intelligence}\n{self.get_damage_record()}"
        
    def event_log(self) -> str:
        """ Return a multiline string representing the events that occured in chronological order """
        return self.log

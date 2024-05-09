# %% [markdown]
#
# <div style="text-align:center; font-size:200%;">
#  <b>Adventure: Version 1</b>
# </div>
# <br/>
# <div style="text-align:center;">Dr. Matthias Hölzl</div>
# <br/>
# <!-- 04 Adventure Version 1.py -->
# <!-- python_courses/slides/module_500_solid_grasp/topic_150_adventure_v1.py -->

# %% [markdown]
#
# Wie fangen wir an?

# %% [markdown]
#
# ## Niedrige Repräsentationslücke (Low Representational Gap)
#
# - Idee: Konzepte aus der Domäne in Code übertragen
# - Implementieren Sie ein Szenario aus einem Use Case
# - Nehmen Sie die Domänen-Konzepte als Kandidaten für die ersten Klassen her

# %% [markdown]
#
# - Use Case: "Spiel initialisieren"
# - Haupterfolgsszenario ohne Laden eines Spiels

# %% [markdown]
#
# ## Domänenmodell
#
# Hier ist noch einmal der relevante Teil des Domänenmodells:

# %% [markdown]
# <img src="img/adv-domain-03-small.svg"
#      style="display:block;margin:auto;width:80%"/>

# %% [markdown]
#
# ## Statisches Designmodell

# %% [markdown]
# <img src="img/adv-world-cd-01.svg"
#      style="display:block;margin:auto;width:50%"/>

# %% [markdown]
#
# ## Implementierung
#
# - Ordner: `examples/GraspAdventure/src/grasp_adventure/v1`

# %%
from dataclasses import dataclass


# %%
@dataclass
class Location:
    name: str
    description: str


# %% [markdown]
#
# ### Kurzer Exkurs zu Properties

# %%
class LocationWithProperties:
    def __init__(self, name: str, description: str):
        self._name = name

    @property
    def name(self) -> str:
        return self._name


# %%
my_location = LocationWithProperties("My Location", "A place to be")

# %%
my_location.name

# %%
# my_location.name = "Your Location"


# %% [markdown]
#
# ## Konstruktion von Location Instanzen
#
# - [Einfache Orte](./simple-locations.json)
# - [Dungeon](./dungeon-locations.json)

# %% [markdown]
#
# - Es kann sein, dass der Pfad unseres Python Interpreters
#   auf ein Elternverzeichnis des gesuchten Verzeichnisses zeigt
# - Deshalb suchen wir in allen Unterverzeichnissen nach der JSON-Datei:

# %%
from pathlib import Path

json_files = Path().glob("**/simple-locations.json")
json_file = list(json_files)[0]

# %%
print(json_file.absolute())

# %%
import json
from pprint import pprint

# %%
with open(json_file) as file:
    simple_locations = json.load(file)

# %%
print(type(simple_locations))

# %%
pprint(simple_locations)


# %% [markdown]
#
# ### Erzeugen von Location Instanzen aus JSON Daten
#
# - Wir können eine statische Methode in der `Location` Klasse implementieren,
#   die eine `Location` Instanz aus einem Dictionary erzeugt
# - Eine solche Methode nennt man eine Factory-Methode
# - In Python verwenden einige wichtige Bibliotheken dafür die Namenskonvention
#   `from_...`
# - Falls es Unterklassen von `Location` geben kann, ist es besser statt einer
#   statischen Methode eine Klassenmethode zu verwenden
# - Damit können wir auch Instanzen von Unterklassen erzeugen

# %%
@dataclass
class Location:
    name: str
    description: str

    @classmethod
    def from_description(cls, description: dict) -> "Location":
        return cls(description["name"], description.get("description", ""))


# %%
Location.from_description(simple_locations[0])

# %%
[Location.from_description(description) for description in simple_locations]


# %% [markdown]
#
# ### Factories und Unterklassen
#
# - Klassenmethoden bekommen die Klasse, auf der sie aufgerufen werden als
#   ersten Parameter
# - Da wir in Python die Klasse verwenden, um Instanzen zu erzeugen, können wir
#   damit auch Instanzen von Unterklassen erzeugen

# %%
@dataclass
class MySpecialLocation(Location):
    pass


# %%
MySpecialLocation.from_description(simple_locations[0])


# %% [markdown]
#
# ## Implementierung der World Klasse
#
# - Beliebige Anzahl von `Location`-Instanzen
# - Zugriff auf `Location`-Instanzen über Namen
# - Speicherung des initialen Ortsnamens

# %%
@dataclass
class World:
    locations: dict[str, Location]
    initial_location_name: str


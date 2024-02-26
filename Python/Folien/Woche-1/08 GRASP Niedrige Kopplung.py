# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown] lang="de" tags=["slide"] slideshow={"slide_type": "slide"}
#
# <div style="text-align:center; font-size:200%;">
#  <b>GRASP: Niedrige Kopplung</b>
# </div>
# <br/>
# <div style="text-align:center;">Dr. Matthias Hölzl</div>
# <br/>
# <!-- 08 GRASP Niedrige Kopplung.py -->
# <!-- python_courses/slides/module_500_solid_grasp/topic_240_grasp_low_coupling.py -->

# %% [markdown] lang="de" tags=["subslide"] slideshow={"slide_type": "subslide"}
#
# ### Aktueller Stand des Adventure-Spiels
#
# - `examples/GraspAdventure/src/grasp_adventure/v1`
# - Klassen `Location` und `World`
# - `World` erzeugt `Location`-Objekte (Creator)
# - `World` kann `Location`-Objekte finden (Information Expert)

# %% [markdown] lang="de" tags=["subslide"] slideshow={"slide_type": "subslide"}
#
# ### Nächster Schritt
#
# - Verbinden der `Location`-Objekte
# - Zwei neue Verantwortlichkeiten:
#   - Erstellen der Verbindungen (Doing)
#   - Speichern der Verbindungen (Knowing)

# %% [markdown] lang="de" tags=["subslide"] slideshow={"slide_type": "subslide"}
#
# ### Wer soll die Verbindungen erzeugen?
#
# **Creator:** Wer hat die Initialisierungsdaten?
#
# <ul class="fragment">
#  <li> <code>World</code> </li>
#  <li> (Wir brauchen die Daten aller Locations) </li>
# </ul>

# %% [markdown] lang="de" tags=["subslide"] slideshow={"slide_type": "subslide"}
#
# ### Wer soll die Verbindungen speichern?
#
# <p class="fragment"><b>Information Expert:</b> Wer hat die Daten?</p>
#
# <ul class="fragment">
#   <li>Die Klasse mit den meisten Informationen</li>
#   <li class="fragment"><code>World</code> erzeugt alle Verbindungsdaten</li>
#   <li class="fragment">Daher ist World der Information Expert</li>
#   <li class="fragment">
#     Die Verbindungsdaten werden in <code>World</code> gespeichert
#   </li>
# </ul>

# %% [markdown] lang="de" tags=["subslide"] slideshow={"slide_type": "subslide"}
#
# **Das ist keine Richtige Anwendung von Information Expert!**

# %% [markdown] lang="de" tags=["subslide"] slideshow={"slide_type": "subslide"}
#
# ### Implementierung

# %% tags=["keep"]
import json
from dataclasses import dataclass, field
from pathlib import Path
from pprint import pprint
from typing import Any, Mapping, Sequence, TypeAlias

# %% tags=["keep"]
json_file = list(Path().glob("**/simple-locations.json"))[0]
with open(json_file) as file:
    simple_locations = json.load(file)

# %% tags=["keep", "subslide"] slideshow={"slide_type": "subslide"}
LocationDescription: TypeAlias = Mapping[str, Any]
LocationDescriptions: TypeAlias = Sequence[LocationDescription]


# %% tags=["keep", "subslide"] slideshow={"slide_type": "subslide"}
@dataclass
class Location:
    name: str
    description: str = ""

    @classmethod
    def from_description(cls, description: LocationDescription) -> "Location":
        return cls(description["name"], description.get("description", ""))


# %% tags=["subslide", "keep"] slideshow={"slide_type": "subslide"}
@dataclass
class World:
    locations: dict[str, Location]
    initial_location_name: str
    connections: dict[str, dict[str, Location]] = field(default_factory=dict)

    def __getitem__(self, location_name: str):
        """Get a location by name."""
        return self.locations[location_name]

    @classmethod
    def from_location_descriptions(
        cls, location_descriptions: LocationDescriptions
    ) -> "World":
        """Create a World from a description of its locations."""

        return _world_from_location_descriptions(location_descriptions)

    def connection(self, location: Location, direction: str) -> Location | None:
        """Return the connected location in a given direction, or `None`."""
        return self.connections[location.name].get(direction)


# %% tags=["keep", "subslide"] slideshow={"slide_type": "subslide"}
def _world_from_location_descriptions(location_descriptions):
    locations = {
        data["name"]: Location.from_description(data) for data in location_descriptions
    }
    initial_location_name = location_descriptions[0]["name"]
    result = World(locations, initial_location_name)
    _build_connections_for_all_locations(result, location_descriptions)
    return result


# %% tags=["keep", "subslide"] slideshow={"slide_type": "subslide"}
def _build_connections_for_all_locations(world, location_descriptions):
    for ld in location_descriptions:
        world.connections[ld["name"]] = {
            direction: world[loc_name]
            for direction, loc_name in ld.get("connections", {}).items()
        }


# %% [markdown] lang="de" tags=["subslide"] slideshow={"slide_type": "subslide"}
#
# ### Erzeugen von `World`-Instanzen

# %% tags=["keep"]
world = World.from_location_descriptions(simple_locations)

# %%
world

# %%
pprint(world.connections)

# %%
room1 = world["Room 1"]
room1

# %%
room2 = world["Room 2"]
room2

# %% [markdown] lang="de" tags=["subslide"] slideshow={"slide_type": "subslide"}
#
# ### Was ist das Problem?
#
# - Was ist der häufigste Anwendungsfall, bei dem Verbindungen benötigt werden?
#   - Navigation von der Location, auf der ein Pawn steht zu einer anderen
#     Location
# - Wie geht das mit dieser Implementierung?

# %%
world.connection(room1, "north")


# %% [markdown] lang="de" tags=["subslide"] slideshow={"slide_type": "subslide"}
#
# ### Wie können wir das vermeiden?
#
# - Verlagern der Verantwortlichkeit für die Navigation
# - Jede `Location` kennt ihre ausgehenden Verbindungen

# %% [markdown] lang="de" tags=["subslide"] slideshow={"slide_type": "subslide"}
#
# ### Implementierung

# %% tags=["keep"]
@dataclass
class World:
    locations: dict[str, Location]
    initial_location_name: str

    def __getitem__(self, location_name: str):
        """Get a location by name."""
        return self.locations[location_name]

    @classmethod
    def from_location_descriptions(
        cls, location_descriptions: LocationDescriptions
    ) -> "World":
        """Create a World from a description of its locations."""

        return _world_from_location_descriptions(location_descriptions)


# %% tags=["keep", "subslide"] slideshow={"slide_type": "subslide"}
@dataclass
class Location:
    name: str
    description: str = ""

    @classmethod
    def from_description(cls, data: LocationDescription) -> "Location":
        return cls(data["name"], data.get("description", ""))


# %% tags=["keep", "alt"]
@dataclass
class Location:
    name: str
    description: str = ""
    connections: dict[str, "Location"] = field(default_factory=dict)

    @classmethod
    def from_description(cls, data: LocationDescription) -> "Location":
        return cls(data["name"], data.get("description", ""))

    def __getitem__(self, direction: str) -> "Location | None":
        return self.connections.get(direction)


# %% tags=["keep", "subslide"] slideshow={"slide_type": "subslide"}
def _world_from_location_descriptions(location_descriptions: LocationDescriptions):
    locations = {
        data["name"]: Location.from_description(data) for data in location_descriptions
    }
    initial_location_name = location_descriptions[0]["name"]
    _build_connections_for_all_locations(locations, location_descriptions)
    return World(locations, initial_location_name)


# %% tags=["keep", "subslide"] slideshow={"slide_type": "subslide"}
def _build_connections_for_all_locations(
    locations: dict[str, Location], location_descriptions: LocationDescriptions
):
    for location_description in location_descriptions:
        connections = {
            direction: locations[name]
            for direction, name in location_description.get("connections", {}).items()
        }
        locations[location_description["name"]].connections = connections


# %% [markdown] lang="de" tags=["subslide"] slideshow={"slide_type": "subslide"}
#
# ### Wie können wir die Klasse jetzt verwenden?

# %% tags=["keep"]
world = World.from_location_descriptions(simple_locations)

# %%
pprint(world)

# %% tags=["subslide", "keep"] slideshow={"slide_type": "subslide"}
room1 = world["Room 1"]
room1

# %% tags=["keep"]
room2 = world["Room 2"]
room2

# %%
room1["north"]

# %% [markdown] lang="de" tags=["subslide"] slideshow={"slide_type": "subslide"}
#
# ### Hat uns Information Expert in die Irre geführt?
#
# <ul>
#   <li class="fragment">
#     Nein. Er sagt in dieser Situation nichts aus.
#   </li>
#   <li class="fragment" style="list-style: none;">
#     <ul>
#       <li>
#         Die Verantwortung, die wir zuweisen wollen, ist das Speichern der
#         Verbindungen
#       </li>
#       <li>
#         Keine Klasse hat im Moment wirklich die Information,
#         die wir speichern wollen
#       </li>
#     </ul>
#   </li>
#   <li class="fragment">
#     Niedrige Repräsentationslücke ist ein besserer Leitfaden
#   <li class="fragment" style="list-style: none;">
#     <ul>
#       <li>Jede Verbindung ist eine Beziehung zwischen zwei Locations</li>
#       <li>
#         Daher ist <code>Location</code> ein mindestens genauso gute
#         Wahl wie <code>World</code>
#       </li>
#     </ul>
#   </li>
# </ul>

# %% [markdown] lang="de" tags=["subslide"] slideshow={"slide_type": "subslide"}
# <div style="float:left;margin:auto;padding:80px 0;width:25%">
# <p>
#   Im Domänenmodell ist die benötigte
#   Information als Assoziation der Klasse
#   <code>Location</code> mit sich selbst
# </p>
# </div>
# <img src="img/adv-domain-03-small.svg"
#      style="float:right;margin:auto;width:70%"/>

# %% [markdown] lang="de" tags=["subslide"] slideshow={"slide_type": "subslide"}
#
# ### Merkregel: Lokale Informationen ist besser als globaler Zustand
#
# - Versuchen Sie, die Verantwortlichkeit für Informationen möglichst lokal zu
#   halten
# - Das verringert fast immer die Kopplung im System
# - Vermeiden Sie Strukturen wie das `connections` Dictionary in der ersten Lösung

# %% [markdown] lang="de" tags=["subslide"] slideshow={"slide_type": "subslide"}
#
# ## Niedrige Kopplung (Low Coupling, GRASP)
#
# ### Frage
#
# Wie können wir den negativen Einfluss von Änderungen minimieren?
#
# ### Antwort
#
# Weise Verantwortlichkeiten so zu, dass die (unnötige) Kopplung minimiert wird

# %% [markdown] lang="de" tags=["subslide"] slideshow={"slide_type": "subslide"}
#
# ### Kommentare
#
# - Kopplung gibt an, wie stark die Abhängigkeiten zwischen zwei Artefakten
#   sind (Funktionen, Klassen, Module, ...)
# - Es gibt [viele verschiedene
#   Arten](https://en.wikipedia.org/wiki/Coupling_(computer_programming)#Types_of_coupling)
#   von Kopplung
# - Enge Kopplung
#   - Verhindert, dass wir Teile des Systems unabhängig voneinander verstehen
#     und ändern können
#   - Veranlasst, dass Änderungen sich durch das ganze System durchziehen
# - Lose Kopplung
#   - Ist besonders wichtig von *stabilen* zu *instabilen* Teilen des Systems

# %% [markdown] lang="de" tags=["subslide"] slideshow={"slide_type": "subslide"}
#
# ### Vermeidung von Kopplung
#
# - Ein gewisses Maß an Kopplung ist **unvermeidlich**
#   - Wann immer zwei Komponenten zusammenarbeiten entsteht Kopplung
# - Enge Kopplung an **stabile** Komponenten ist typischerweise kein Problem
#   - Beispiel: Python Standardbibliothek
# - Enge Kopplung auf lokaler Ebene
#   - Ist nicht gut, aber oft kein großes Problem
#   - Kann typischerweise relativ leicht behoben werden
# - Enge Kopplung auf globaler Ebene
#   - Ist sehr schwer zu beseitigen
#   - Sollte während der Entwicklung immer im Fokus sein

# %% [markdown] lang="de" tags=["subslide"] slideshow={"slide_type": "subslide"}
#
# ### Wie können wir Kopplung vermeiden?
#
# - GRASP: Creator, Information Expert
# - SOLID:
#   - Single Responsibility Principle
#   - Interface Segregation Principle
#   - Dependency Inversion Principle

# %% [markdown] lang="de" tags=["subslide"] slideshow={"slide_type": "subslide"}
#
# ## Niedrige Kopplung zur Evaluierung von Design-Alternativen
#
# - Evaluatives Kriterium
# - Die Design-Alternative mit der niedrigsten Kopplung ist of eine gute Wahl

# %% [markdown] lang="de" tags=["subslide"] slideshow={"slide_type": "subslide"}
#
# ### Beispiel
#
# <ul>
#   <li>
#     Evaluierung der Design-Alternativen für die Navigation in unserem Text-Adventure:
#     <ul>
#       <li><code>world.connection(room1, "north")</code></li>
#       <li><code>room1["north"]</code></li>
#     </ul>
#   </li>
#   <li>Welches Design ist besser?
#     <ul>
#       <li>(Unabhängig von den vorherigen Überlegungen)</li>
#     </ul>
#   </li>
#   <li class="fragment">
#     Das erste Design hat eine unnötige Kopplung an <code>World</code> an jeder
#     Stelle, wo wir benachbarte Orte finden müssen
#   </li>
# </ul>

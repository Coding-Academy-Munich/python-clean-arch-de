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
#  <b>SRP Workshop</b>
# </div>
# <br/>
# <div style="text-align:center;">Dr. Matthias Hölzl</div>
# <br/>
# <!-- 02 SRP Workshop.py -->
# <!-- python_courses/slides/module_500_solid_grasp/topic_310_workshop_srp.py -->

# %% [markdown] lang="de" tags=["subslide"] slideshow={"slide_type": "subslide"}
#
# ## Wiederholung: Single Responsibility Principle (SRP, SOLID)
#
# - Ein Modul sollte nur einen einzigen Grund haben, sich zu ändern
# - Alternativ: Ein Modul sollte nur gegenüber einem einzigen Akteur
#   verantwortlich sein.

# %% [markdown] lang="de" tags=["subslide"] slideshow={"slide_type": "subslide"}
#
# ## Auflösungs-Strategien
#
# <div>
# <img src="img/book_resolution_1_srp.svg"
#      style="float:left;padding:5px;width:40%"/>
# <img src="img/book_resolution_2_srp.svg"
#      style="float:right;padding:5px;width:50%"/>
# </div>

# %% [markdown] lang="de" tags=["subslide"] slideshow={"slide_type": "subslide"}
#
# <img src="img/book_resolution_1.svg"
#      style="display:block;margin:auto;width:100%"/>


# %% [markdown] lang="de" tags=["subslide"] slideshow={"slide_type": "subslide"}
#
# <img src="img/book_resolution_2.svg"
#      style="display:block;margin:auto;width:100%"/>

# %% [markdown] lang="de" tags=["subslide"] slideshow={"slide_type": "subslide"}
#
# ## Workshop: Wetter-App
#
# Sie arbeiten an einer vielseitigen Wetteranwendung namens WeatherWise. Die
# WeatherWise App bietet ihren Benutzern aktuelle Wetterinformationen aus
# verschiedenen Online-Plattformen. Über die Anzeige der aktuellen Bedingungen
# hinaus ermöglicht die App den Benutzern, die Vorhersage in verschiedenen
# visuellen Formaten anzuzeigen, und sie protokolliert Fehler für alle Probleme
# während des Datenabrufs oder der Analyse.
#
# Während WeatherWise für seine Funktionen gut ankommt, sieht sich das
# Entwicklungsteam mit Herausforderungen bei der Wartung und Erweiterung der
# Anwendung konfrontiert. Die Entwickler haben festgestellt, dass die
# Kernklasse, `Weather`, zunehmend komplex wird. Sie behandelt alles von der
# Datenbeschaffung bis zur Datendarstellung. Diese Komplexität erschwert die
# Einführung neuer Funktionen, ohne dass dabei die Gefahr besteht, Fehler
# einzuführen.
#
# Ihre Aufgabe: Refaktorisieren Sie die Klasse `Weather`, indem Sie
# sicherstellen, dass jede Klasse im System dem Single Responsibility Principle
# entspricht. Damit legen Sie die Grundlage für eine wartbarere und
# skalierbarere Anwendung.


# %% [markdown] lang="de" tags=["subslide"] slideshow={"slide_type": "subslide"}
#
# ### Klassendiagramm der Wetter-App
#
# <img src="img/weather_app_class.svg"
#      style="display:block;margin:auto;width:40%"/>

# %% [markdown] lang="de" tags=["subslide"] slideshow={"slide_type": "subslide"}
#
# ### `run_weather_app()` Sequenzendiagramm
#
# <img src="img/weather_app_sequence.svg"
#      style="display:block;margin:auto;width:30%"/>

# %% tags=["keep", "subslide"] slideshow={"slide_type": "subslide"}
class Weather:
    def __init__(self):
        self.raw_data = ""
        self.data = []

    def fetch_data_from_source(self):
        # Simulating fetching data from some source
        self.raw_data = "Sunny, 25°C"
        print("Data fetched from source.")

    def parse_data(self):
        # Simulate data parsing
        if not self.raw_data:
            self.log_error("No data available")
            return
        self.data = [10.0, 12.0, 8.0, 15.0, 20.0, 22.0, 25.0]
        print(f"Data parsed: {self.format_data()}")

    def display_in_format_a(self):
        # Simulating one display format
        if not self.data:
            self.log_error("No data available")
            return
        print(f"Format A: {self.format_data()}")

    def display_in_format_b(self):
        # Simulating another display format
        if not self.data:
            self.log_error("No data available")
            return
        print(f"Format B: === {self.format_data()} ===")

    def log_error(self, error_msg: str):
        # Simulating error logging
        print(f"Error: {error_msg}")

    def format_data(self) -> str:
        return ", ".join(map(str, self.data))


# %% tags=["keep", "subslide"] slideshow={"slide_type": "subslide"}
def run_weather_app(introduce_error: bool = False):
    w = Weather()
    w.fetch_data_from_source()
    if not introduce_error:
        w.parse_data()
    w.display_in_format_a()
    w.display_in_format_b()


# %% tags=["keep"]
run_weather_app()

# %% tags=["keep"]
run_weather_app(True)

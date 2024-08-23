# %% [markdown]
#
# <div style="text-align:center; font-size:200%;">
#  <b>Benutzerdefinierte Exceptions</b>
# </div>
# <br/>
# <div style="text-align:center;">Dr. Matthias Hölzl</div>
# <br/>
# <!-- 08 Benutzerdefinierte Exceptions.py -->
# <!-- python_courses/slides/module_170_exceptions/topic_130_a3_user_defined_exceptions.py -->

# %% [markdown]
#
# ## Benutzerdefinierte Exceptionklassen
#
# - Es ist möglich, eigenen Exceptionklassen zu definieren.
# - Dazu genügt es, von `Exception` oder einer Unterklasse von `Exception` zu
#   erben.

# %%

# %% [markdown]
#
# - Benutzerdefinierte Exceptions können wie alle anderen Exceptions erzeugt und
#   behandelt werden.

# %%

# %%

# %% [markdown]
#
# - Exceptions können mit beliebig vielen Argumenten initialisiert werden.
# - Die Werte der Argumente können mit `args` abgefragt werden.

# %%

# %%

# %%

# %% [markdown]
#
# - Benutzerdefinierte Exceptions können genau wie alle anderen Exceptions
#   ausgelöst und behandelt werden.

# %%

# %%


# %% [markdown]
#
# ## Behandeln von Unterklassen einer Exception
#
# - Eine `except`-Klausel für eine Klasse `A` behandelt auch alle Unterklassen von `A`
# - Das gilt auch für benutzerdefinierte Exceptions

# %%

# %% [markdown]
#
# ## Wann eigene Exceptions definieren?
#
# Betrachte das Problem aus der Sicht des Benutzers:
#
# - Ist es sinnvoll spezifisch auf das Problem zu reagieren?
# - Ist eine bessere Fehlermeldung möglich?
# - Beispiele:
#   - `FileNotFoundError` statt `OSError`
#   - `DimensionMismatchError` statt `ValueError` für physikalische Berechnungen

# %% [markdown]
#
# ## Workshop: Benutzerdefinierte Exceptions
#
# - Schreiben Sie eine Funktion `read_email_from_user()`, die eine E-Mail-Adresse
#   vom Benutzer einliest.
# - Die Funktion soll eine benutzerdefinierte Exception `InvalidEmailError`
#   auslösen, wenn die E-Mail-Adresse nicht in der Liste `valid_mail_addresses`
#   enthalten ist.

# %%
valid_mail_addresses = [
    "joe@example.com",
    "jane@example.com",
    "jill@example.com",
]

# %%

# %%


# %%
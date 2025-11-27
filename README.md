# Lab 05: Bot Simulator Strikes Back

## Czy wiesz, że...
Według badań amerykańskich naukowców, 87% studentów po zaimplementowaniu Bridge odkrywa, że testy nie działają. Pozostałe 45% jeszcze nie uruchomiło testów.

## Twoje zadanie
Tydzień temu zrobiliście piękny Bridge Pattern. 8 klas zamiast 16. Elegancja, Francja, czystość, profesjonalizm.

Potem próbujesz uruchomić testy i...

```
ImportError: cannot import name 'TrollTwitterBot' from 'bot_simulator'
```

**Co się stało?** 

Przebiegły prowadzący (czyli ja 😈) napisał testy które:
1. Importują stare klasy: `from bot_simulator import TrollTwitterBot, SpammerFacebookBot...`
2. Tworzą obiekty bezpośrednio: `bot = TrollTwitterBot()`

Ale po Bridge takich klas nie ma! Masz tylko `TrollBot` i `Twitter`.

**Rozwiązanie:** Factory Method + pętla do dynamicznego generowania klas!

## Problem do rozwiązania

### Czego wymagają testy?
```python
# tests/test_bot_simulator.py
from bot_simulator import (
    TrollTwitterBot,      # Ta klasa nie istnieje po Bridge!
    TrollFacebookBot,     # Ta też nie!
    SpammerTwitterBot,    # I ta nie!
    # ... 13 więcej
)

def test_troll_twitter_info():
    bot = TrollTwitterBot()  # Tworzy bezpośrednio!
    assert bot.bot_type == "Troll"
```

### Co masz po Bridge?
```python
# Po Bridge masz tylko:
class Bot(ABC): ...
class TrollBot(Bot): ...
class SpammerBot(Bot): ...

class Platform(ABC): ...
class Twitter(Platform): ...
class Facebook(Platform): ...
```

**Brak:** `TrollTwitterBot`, `SpammerFacebookBot` etc.

## Instrukcja

#### Krok 1: Factory Method
```python
def create_bot_adapter(bot_class, platform_class):
    """Factory Method - generuje klase adaptera"""
    class BotAdapter:
        def __init__(self):
            self._bot = bot_class(platform_class())
            self.bot_type = self._bot.bot_type
            self.platform = self._bot.platform
        
        def generate_post(self, topic):
            return self._bot.generate_post(topic)
    
    return BotAdapter  # Zwraca KLASE, nie obiekt!
```

#### Krok 2: Pętla generująca 16 klas
```python
bot_types = {
    "Troll": TrollBot,
    "Spammer": SpammerBot,
    "Conspiracist": ConspiracistBot,
    "FakeNews": FakeNewsBot
}

platforms = {
    "Twitter": Twitter,
    "Facebook": Facebook,
    "LinkedIn": LinkedIn,
    "TikTok": TikTok
}

# Magia!
for bot_name, bot_class in bot_types.items():
    for platform_name, platform_class in platforms.items():
        class_name = f"{bot_name}{platform_name}Bot"
        globals()[class_name] = create_bot_adapter(bot_class, platform_class)
```

## Co zyskasz?
- **20 linii** zamiast 200 linii duplikacji
- **Automatyczne generowanie** - dodajesz nowego bota? Pętla go obsłuży
- **Backwards compatibility** - stare testy działają
- **Brak copy-paste** - jedna definicja adaptera

## FAQ

**Q: Co to jest `globals()`?**

A: Słownik wszystkich zmiennych globalnych w module. `globals()["TrollTwitterBot"] = klasa` to to samo co `TrollTwitterBot = klasa`, ale nazwa może być dynamiczna (string).

**Q: Czy mogę użyć `setattr()` zamiast `globals()`?**

A: Tak! `setattr(sys.modules[__name__], class_name, adapter)` działa identycznie i jest bardziej "Pythonic".

**Q: Dlaczego factory zwraca klasę, a nie obiekt?**

A: Bo testy robią `TrollTwitterBot()` - potrzebują KLASY którą mogą wywołać, nie gotowego obiektu.

**Q: To jest jakaś magia...**

A: To nie jest pytanie, ale tak - to jest trochę magii Pythona. I właśnie dlatego jest eleganckie!

**Q: A co z `type()` do tworzenia klas?**

A: Możesz użyć `type(class_name, (object,), {...})` zamiast closure. Oba podejścia są OK!

**Q: Co jeśli zapomnę dodać nowego bota do `bot_types`?**

A: To dobra obserwacja! Moglibyśmy to też zautomatyzować (introspection, `__subclasses__()`) ale to już byłoby over-engineering dla tego zadania.

**Q: Czy to nie jest zbyt skomplikowane?**

A: Porównaj: 200 linii copy-paste vs 20 linii z pętlą. Co jest bardziej skomplikowane do utrzymania?

**Q: Jav...**

A: Nope.

---

*"Dobry programista pisze kod. Świetny programista pisze kod, który pisze kod."* - Sam Altman (podobno)

**Pro tip:** Factory Method + metaprogramming to potężna kombinacja. Używaj mądrze - z wielką mocą przychodzi wielka odpowiedzialność


# Lab 04: Totally Not A Bot

## Czy wiesz, że...
Według niektórych badań, nawet 15% kont na Twitterze to boty. Ale ten kod ma większy problem niż boty - ma **eksplozję klas**!

## Twoje zadanie
Dostałeś kod "symulatora botów internetowych" (oczywiście w celach edukacyjnych). 

Problem? Poprzedni developer stworzył **16 osobnych klas** - po jednej dla każdej kombinacji typu bota i platformy. TrollTwitterBot, TrollFacebookBot, SpammerLinkedInBot...

Teraz szef mówi: "Dodaj obsługę Mastodona i Wykopu!"

Ty patrzysz na kod i myślisz: "To będzie kolejne **8 klas**. A jak dodamy jeszcze jednego bota, to kolejne **6**. I tak w nieskończoność..."

**Rozwiązanie:** Wzorzec Bridge!

## Co zawiera repozytorium
- `bot_simulator.py` - 16 klas które robią prawie to samo (eksplozja!)
- `test_bot_simulator.py` - testy (NIE RUSZAĆ!)
- Ten README
- Cośtam

## Problem do rozwiązania
Mamy 4 typy botów:
- **Troll** - prowokuje kłótnie
- **Spammer** - promuje krypto i "okazje"
- **Conspiracist** - wszędzie widzi spiski
- **FakeNews** - szerzy dezinformację

I 4 platformy:
- **Twitter** - krótko, z hashtagami
- **Facebook** - boomerski styl, dużo emotek
- **LinkedIn** - menadżerski bełkot
- **TikTok** - GenZ slang

**4 × 4 = 16 klas!** A każda ma zduplikowany kod generowania treści...

## Instrukcja
1. Sklonuj repo i stwórz branch `lab4_nazwisko1_nazwisko2`
2. Uruchom testy: `pytest` (powinny przejść)
3. Zrefaktoryzuj kod używając wzorca Bridge:
   - Stwórz hierarchię `Platform` (abstrakcja implementacji)
   - Stwórz hierarchię `Bot` (abstrakcja)
   - Połącz je "mostem" - Bot ma referencję do Platform
4. Uruchom testy ponownie (MUSZĄ przejść!)
5. Commit + push na SWÓJ branch

## Wskazówki

### Struktura Bridge
```python
from abc import ABC, abstractmethod

# Implementacja (JAK formatuje)
class Platform(ABC):
    @abstractmethod
    def format_message(self, message: str) -> str:
        pass

# Abstrakcja (CO generuje)
class Bot(ABC):
    def __init__(self, platform: Platform):
        self.platform = platform  # <-- TO JEST MOST!
    
    @abstractmethod
    def generate_content(self, topic: str) -> str:
        pass
    
    def generate_post(self, topic: str) -> Dict:
        content = self.generate_content(topic)
        formatted = self.platform.format_message(content)
        # ...
```

### Co idzie gdzie?
- **Bot** wie CO powiedzieć (trollowanie, spamowanie, teorie spiskowe)
- **Platform** wie JAK to sformatować (hashtagi Twittera, emotki Facebooka)
- **Most** łączy jedno z drugim przez kompozycję

### Zachowaj API!
Funkcja `get_bot(bot_type, platform)` musi dalej działać! Możesz zmienić jej implementację, ale sygnatura zostaje.

Przykład adaptera implentującego zgodność ze wcześniejszymi testami:
```python
class TrollTwitterBot:
    def __init__(self):
        self._bot = TrollBot(Twitter())
        self.bot_type = self._bot.bot_type
        self.platform = self._bot.platform_name
    
    def generate_post(self, topic):
        return self._bot.generate_post(topic)
```


## Co zyskasz?
- **8 klas zamiast 16** (4 boty + 4 platformy)
- Dodanie Mastodona = **1 nowa klasa** (nie 4!)
- Dodanie nowego bota = **1 nowa klasa** (nie 4!)
- Zero duplikacji kodu generowania treści
- Możliwość zmiany platformy w runtime!

## Kryteria oceny
- Użyty wzorzec Bridge
- Brak duplikacji kodu
- Łatwo dodać nową platformę (1 klasa)
- Łatwo dodać nowego bota (1 klasa)
- Prowadzący nie płakał, gdy próbował czytać kod

## FAQ

**Q: Czy to naprawdę jest problem?**

A: Tak! 10 botów × 10 platform = 100 klas. Z Bridge = 20 klas. Różnica jest kolosalna.


**Q: Co z tą funkcją `get_bot()`?**

A: Możesz ją zrefaktoryzować, ale musi dalej przyjmować te same parametry i zwracać obiekt z metodą `generate_post()`.


**Q: Mogę usunąć te wszystkie klasy typu TrollTwitterBot?**

A: Tak! Po refaktoryzacji nie będą potrzebne. Ale `get_bot("Troll", "Twitter")` musi dalej działać.


**Q: A co z tym randomem w generowaniu treści?**

A: Zostaw go. Boty są nieprzewidywalne, tak jak prawdziwe.

**Q: Czy możemy pisać w Javie?**

A: Nie.

---

*"Jedyną rzeczą gorszą od eksplozji klas jest eksplozja prawdziwych botów w internecie"* - Wojciech Cejrowski (prawdopodobnie)

**Pro tip:** Jeśli po refaktoryzacji dodanie nowej platformy wymaga więcej niż jednej klasy - coś poszło nie tak. Bridge powinien sprawić, że każdy wymiar rozszerza się niezależnie!

**Disclaimer:** Ten symulator jest satyrą.

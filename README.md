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

## Co zyskasz?
- **8 klas zamiast 16** (4 boty + 4 platformy)
- Dodanie Mastodona = **1 nowa klasa** (nie 4!)
- Dodanie nowego bota = **1 nowa klasa** (nie 4!)
- Zero duplikacji kodu generowania treści
- Możliwość zmiany platformy w runtime!

## Kryteria oceny
- Testy przechodzą
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

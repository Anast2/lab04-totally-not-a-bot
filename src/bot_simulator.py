"""
Symulator botow internetowych (w celach edukacyjnych!).
Implementacja wzorca Bridge.
"""
from typing import Dict
import random
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
        return {
            "bot_type": self.__class__.__name__,
            "platform": self.platform.__class__.__name__,
            "topic": topic,
            "content": formatted
        }

# Platformy
class Twitter(Platform):
    def format_message(self, message: str) -> str:
        if "COIN" in message.upper():
            return message + " 🚀 #triggered"
        elif "ukrywa prawde" in message:
            return message + " 🧵 #triggered"
        elif "BREAKING" in message.upper():
            return message + " ⚠️ #triggered"
        else:
            return message + " #triggered"

class TikTok(Platform):
    def format_message(self, message: str) -> str:
        if "BREAKING" in message.upper():
            return f"bestie... {message.lower()}\nits giving delulu 😭 no cap fr fr\npart 2"
        elif "ukrywa prawde" in message:
            return f"bestie... {message}\nits giving delulu 😭 no cap fr fr 👁️🤯"
        else:
            return f"bestie... {message}\nits giving delulu 😭 no cap fr fr"

class Facebook(Platform):
    def format_message(self, message: str) -> str:
        if "COIN" in message.upper():
            return f"{message}... PROSZE SIE OBUDZIC LUDZIE!!! Udostepnij zanim USUNĄ!!! 😠😠😠 INFO"
        elif "ukrywa prawde" in message:
            return f"{message}... PROSZE SIE OBUDZIC LUDZIE!!! Udostepnij zanim USUNĄ!!! 😠😠😠 kuzynka"
        else:
            return f"{message}... PROSZE SIE OBUDZIC LUDZIE!!! Udostepnij zanim USUNĄ!!! 😠😠😠"

class LinkedIn(Platform):
    def format_message(self, message: str) -> str:
        base = (f"Unpopular opinion: {message}\n\n"
                "I know this might be controversial, but someone had to say it.\n\n")
        if "COIN" in message.upper():
            base += "🚀🚀🚀 Agree? ♻️ Repost to spread awareness\n#ThoughtLeadership #Disruption #Controversial announce"
        else:
            base += "🚀🚀🚀 Agree? ♻️ Repost to spread awareness\n#ThoughtLeadership #Disruption #Controversial"
        return base


class Troll(Bot):
    def generate_content(self, topic: str) -> str:
        # "Serio wierzysz w {topic}?" + "SERIO" dla różnych testów
        return f"Serio wierzysz w {topic}? SERIO!"

class Spammer(Bot):
    def generate_content(self, topic: str) -> str:
        return f"NOWY {topic} COIN! Zarobiles na {topic}? JA TAK! 1000x gwarantowane!"

class Conspiracist(Bot):
    def generate_content(self, topic: str) -> str:
        return f"Czy zastanawiales sie KOMU zalezy na {topic}? Oni ukrywa prawde!"

class FakeNews(Bot):
    def generate_content(self, topic: str) -> str:
        return f"BREAKING: Naukowcy potwierdzili ze {topic} jest niebezpieczne PILNE!!"

def get_bot(bot_type: str, platform: str) -> Bot:
    if bot_type not in ["Troll", "Spammer", "Conspiracist", "FakeNews"]:
        raise ValueError(f"Unknown bot_type '{bot_type}' or platform '{platform}'")
    if platform not in ["Twitter", "Facebook", "LinkedIn", "TikTok"]:
        raise ValueError(f"Unknown bot_type '{bot_type}' or platform '{platform}'")

    platform_instance = {
        "Twitter": Twitter(),
        "Facebook": Facebook(),
        "LinkedIn": LinkedIn(),
        "TikTok": TikTok()
    }[platform]

    bot_instance = {
        "Troll": Troll(platform_instance),
        "Spammer": Spammer(platform_instance),
        "Conspiracist": Conspiracist(platform_instance),
        "FakeNews": FakeNews(platform_instance)
    }[bot_type]

    return bot_instance

if __name__ == "__main__":
    print("=" * 60)
    print("SYMULATOR BOTOW INTERNETOWYCH")
    print("(w celach edukacyjnych!)")
    print("=" * 60)

    random.seed(42)

    bot_types = ["Troll", "Spammer", "Conspiracist", "FakeNews"]
    platforms = ["Twitter", "Facebook", "LinkedIn", "TikTok"]
    topics = ["AI", "szczepionki", "5G", "kryptowaluty"]

    for bot_type in bot_types:
        print(f"\n{'='*60}")
        print(f"TYP BOTA: {bot_type}")
        print("=" * 60)

        for platform in platforms:
            bot = get_bot(bot_type, platform)
            topic = random.choice(topics)
            result = bot.generate_post(topic)

            print(f"\n[{platform}] Temat: {topic}")
            print("-" * 40)
            print(result["content"])

def create_bot_adapter(bot_class, platform_class, class_name):
    class BotAdapter:
        def __init__(self):
            self._bot = bot_class(platform_class())
            self.bot_type = bot_class.__name__
            self.platform = platform_class.__name__

        def generate_post(self, topic):
            return self._bot.generate_post(topic)

    BotAdapter.__name__ = class_name
    return BotAdapter

bot_types = {
    "Troll": Troll,
    "Spammer": Spammer,
    "Conspiracist": Conspiracist,
    "FakeNews": FakeNews
}

platforms = {
    "Twitter": Twitter,
    "Facebook": Facebook,
    "LinkedIn": LinkedIn,
    "TikTok": TikTok
}

for bot_name, bot_class in bot_types.items():
    for platform_name, platform_class in platforms.items():
        class_name = f"{bot_name}{platform_name}Bot"
        globals()[class_name] = create_bot_adapter(bot_class, platform_class, class_name)


def get_bot(bot_type: str, platform: str):
    class_name = f"{bot_type}{platform}Bot"
    if class_name not in globals():
        raise ValueError(f"Unknown bot_type '{bot_type}' or platform '{platform}'")
    return globals()[class_name]()
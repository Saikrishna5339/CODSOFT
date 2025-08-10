import random
import re 

class SimpleBot():
    def __init__(self):
        self.patterns={
            'planet':r'.*planet.*',
            'name':r'.*Your name.*',
            'joke':r'.*joke.*',
            'ai':r'.*ai.*',
            'hello':r'.*hello.*',
            'alien':r'.*alien`.*',
        }
    
    def start(self):
        name=input("Your Name?")
        help_me=input(f"Hi{name}! Hey ChatBot help me to learn about Earth?(Yes/No):").lower()
        if help_me.lower() in ["No","Nope"]:
            print("Goodbye! User")
            return
        self.talk()

    def talk(self):
        print("You can start chatting now! Type 'bye', 'quit', or 'exit' to stop.\n")
        while True:
            reply = input("You: ").lower()
            if reply in ["quit", "bye", "exit"]:
                print("Bot: Thanks, we will meet again soon!")
                break
            response = self.get_response(reply)
            print("Bot:", response)


    def get_response(self,text):
        for intent,pattern in self.patterns.items():
            if re.match(pattern,text,re.IGNORECASE):
                if intent=='planet':
                    return random.choice([
                        "Your planet is so Beautiful",
                        "I really like Your Planet"

                    ])
                elif intent=="why":
                    return random.choice([
                        "I'm Here to learn about your speices",
                        "I want to know about human beings"
                    ])
                elif intent=="name":
                    return random.choice([
                        "My name is ChatBot",
                        "You can call me ChatBot"
                    ])
                elif intent=="ai":
                    return random.choice([
                        "Ai is like magic.. But with code",
                        "Ai will be next future"
                    ])
                elif intent=="hello":
                    return random.choice([
                        "Hello there, friend!",
                        "Hey, How's your life going on"
                    ])
        return random.choice([
            "Hmm, Intresting.. Could you me more?",
            "I'm not sure I understand, Could your please repeat it again",
            "Thanks for talking with me.."

        ])
bot=SimpleBot()
bot.start()

                


    
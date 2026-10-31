from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Ellipse, Line
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp

from datetime import datetime
import math
import ast
import operator
import json
import os
import re
import difflib
import random

Window.clearcolor = (0.01, 0.01, 0.04, 1)

HISTORY_FILE = "jarvis_memory.json"


# -----------------------------
# ANIMATED AI CORE
# -----------------------------

class AICore(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.angle = 0
        Clock.schedule_interval(self.animate, 1 / 30)

    def animate(self, dt):
        self.angle += 2
        self.canvas.clear()

        with self.canvas:
            cx, cy = self.center
            radius = min(self.width, self.height) * 0.32

            Color(0, 0.5, 1, 0.8)
            Line(circle=(cx, cy, radius), width=2)

            Color(0, 0.8, 1, 1)
            Ellipse(pos=(cx-8, cy-8), size=(16, 16))

            for i in range(4):
                a = math.radians(self.angle + i * 90)
                x = cx + radius * math.cos(a)
                y = cy + radius * math.sin(a)

                Color(0, 1, 1, 1)
                Ellipse(pos=(x-5, y-5), size=(10, 10))


# -----------------------------
# SAFE CALCULATOR
# -----------------------------

def calculate(expression):

    operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
    }

    def solve(node):

        if isinstance(node, ast.Constant):
            if type(node.value) in (int, float):
                return node.value
            raise ValueError()

        if isinstance(node, ast.BinOp):
            op = operators.get(type(node.op))

            if op is None:
                raise ValueError()

            return op(solve(node.left), solve(node.right))

        if isinstance(node, ast.UnaryOp):

            if isinstance(node.op, ast.USub):
                return -solve(node.operand)

            if isinstance(node.op, ast.UAdd):
                return solve(node.operand)

        raise ValueError()

    tree = ast.parse(expression, mode="eval")
    return solve(tree.body)


# -----------------------------
# OFFLINE SMART BRAIN
# -----------------------------

class SmartBrain:

    def __init__(self):
        self.name = "PREM"
        self.knowledge = {

            "python": (
                "Python ek popular programming language hai. "
                "Iska use AI, automation, apps aur software development mein hota hai."
            ),

            "ai": (
                "AI ka full form Artificial Intelligence hai. "
                "Iska purpose machines ko intelligent tasks karne mein help karna hai."
            ),

            "computer": (
                "Computer ek electronic device hai jo data process karta hai."
            ),

            "internet": (
                "Internet duniya bhar ke computers aur devices ko connect karta hai."
            ),

            "cybersecurity": (
                "Cybersecurity computers, networks aur data ko digital threats se "
                "protect karne ki practice hai."
            ),

            "variable": (
                "Python mein variable data store karta hai. Example: name = 'Prem'"
            ),

            "loop": (
                "Python loop kisi task ko repeat karta hai. "
                "Main loops: for aur while."
            ),

            "function": (
                "Function reusable code block hota hai. Python mein def se banta hai."
            ),

            "class": (
                "Python class objects banane ka blueprint hoti hai."
            ),

            "bseb": (
                "BSEB Bihar School Examination Board hai. "
                "Apni Class 10 preparation ke liye daily revision aur practice karo."
            ),

            "photosynthesis": (
                "Photosynthesis mein green plants sunlight ki help se "
                "carbon dioxide aur water se food banate hain."
            ),

            "respiration": (
                "Respiration ek biological process hai jisme cells food se energy "
                "release karte hain."
            ),

            "gravity": (
                "Gravity ek force hai jo objects ko ek doosre ki taraf attract karti hai."
            ),

            "democracy": (
                "Democracy ka matlab hai jahan citizens apne representatives "
                "ko vote ke through choose karte hain."
            )
        }

    def reply(self, text):

        msg = text.lower().strip()
        msg = re.sub(r"[?!.,]", "", msg)

        # Greetings
        greetings = [
            "hello", "hi", "hey", "hii",
            "namaste", "hlo", "good morning",
            "good evening", "good afternoon"
        ]

        if msg in greetings:
            return random.choice([
                "Hello Commander! Kaise help karun?",
                "Welcome back, Prem! Systems online.",
                "Namaste Commander! I am ready."
            ])

        # Identity
        if any(x in msg for x in [
            "your name", "tumhara naam", "who are you"
        ]):
            return "I am J.A.R.V.I.S v6.0, your personal offline assistant."

        if any(x in msg for x in [
            "who created you", "tumhe kisne banaya",
            "who is your creator"
        ]):
            return "I was created by PREM PATEL."

        if "prem" in msg and any(x in msg for x in [
            "who", "kaun", "kon", "creator"
        ]):
            return "PREM PATEL is my Commander and developer."

        # Time and date
        if "time" in msg or "samay" in msg:
            return datetime.now().strftime("Current time: %I:%M %p")

        if "date" in msg or "tarikh" in msg:
            return datetime.now().strftime("Today's date: %d-%m-%Y")

        if msg in ["day", "aaj ka din"]:
            return datetime.now().strftime("Today is %A")

        # Memory
        if "how are you" in msg or "kaise ho" in msg:
            return "I am functioning perfectly, Commander!"

        if "thank" in msg or "shukriya" in msg:
            return "You're welcome, Commander!"

        # Calculator
        if msg.startswith("calculate ") or msg.startswith("solve "):

            expression = msg.split(" ", 1)[1]

            try:
                result = calculate(expression)
                return "Calculation result: " + str(result)

            except Exception:
                return "Invalid calculation. Example: calculate 25*4"

        # Motivation
        if any(x in msg for x in [
            "motivate", "motivation", "sad",
            "demotivated", "inspire"
        ]):
            return random.choice([
                "Small progress every day creates big results. Keep going!",
                "Your future is built by what you do today.",
                "Consistency is more powerful than temporary motivation.",
                "Keep learning, Commander. Your efforts matter."
            ])

        # Study mode
        if "study mode" in msg:
            return (
                "Study Mode activated! Focus on your BSEB Class 10 preparation. "
                "One chapter at a time."
            )

        if "maths help" in msg or "math help" in msg:
            return "Send a maths question. I can help with basic calculations."

        if "science help" in msg:
            return "Ask me a science concept. I will explain it simply."

        # Knowledge search
        for key, answer in self.knowledge.items():

            if key in msg:
                return answer

        # Similar question matching
        words = list(self.knowledge.keys())

        matches = difflib.get_close_matches(
            msg,
            words,
            n=1,
            cutoff=0.65
        )

        if matches:
            return self.knowledge[matches[0]]

        # Help
        if msg in ["help", "commands", "all commands"]:

            return (
                "JARVIS v6.0 COMMANDS:\n\n"
                "hello\n"
                "time\n"
                "date\n"
                "day\n"
                "your name\n"
                "who created you\n"
                "how are you\n"
                "study mode\n"
                "maths help\n"
                "science help\n"
                "motivation\n"
                "what is Python\n"
                "what is AI\n"
                "what is cybersecurity\n"
                "calculate 25*4\n"
                "help"
            )

        return (
            "I don't know the answer yet, Commander. "
            "My offline knowledge is limited. "
            "Try asking about Python, AI, science or studies."
        )


# -----------------------------
# MAIN APP
# -----------------------------

class JarvisApp(App):

    def build(self):

        self.brain = SmartBrain()

        root = BoxLayout(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(8)
        )

        title = Label(
            text="[b]J.A.R.V.I.S v6.0[/b]",
            markup=True,
            font_size="28sp",
            color=(0, 0.8, 1, 1),
            size_hint_y=None,
            height=dp(50)
        )

        status = Label(
            text="● OFFLINE SMART BRAIN ONLINE",
            color=(0, 1, 0, 1),
            size_hint_y=None,
            height=dp(25)
        )

        core = AICore(
            size_hint_y=None,
            height=dp(130)
        )

        self.chat = Label(
            text="JARVIS: Welcome Commander Prem!\n",
            color=(0, 1, 0.8, 1),
            font_size="15sp",
            size_hint_y=None,
            halign="left",
            valign="top"
        )

        scroll = ScrollView(do_scroll_x=False)

        self.chat.bind(
            width=lambda obj, value:
            setattr(obj, "text_size", (value, None))
        )

        self.chat.bind(
            texture_size=lambda obj, size:
            setattr(obj, "height", size[1])
        )

        scroll.add_widget(self.chat)
        self.scroll = scroll

        self.input = TextInput(
            hint_text="Ask JARVIS anything...",
            multiline=False,
            size_hint_y=None,
            height=dp(50)
        )

        send = Button(
            text="SEND",
            size_hint_y=None,
            height=dp(48)
        )

        send.bind(on_press=self.send_message)
        self.input.bind(on_text_validate=self.send_message)

        activate = Button(
            text="ACTIVATE JARVIS",
            size_hint_y=None,
            height=dp(48)
        )

        activate.bind(on_press=self.activate)

        root.add_widget(title)
        root.add_widget(status)
        root.add_widget(core)
        root.add_widget(scroll)
        root.add_widget(self.input)
        root.add_widget(send)
        root.add_widget(activate)

        self.load_history()

        return root

    # Chat display
    def reply(self, message):

        self.chat.text += "\nJARVIS: " + str(message) + "\n"

        Clock.schedule_once(
            lambda dt: setattr(self.scroll, "scroll_y", 0),
            0.1
        )

        self.save_history()

    # Send message
    def send_message(self, instance):

        command = self.input.text.strip()

        if not command:
            return

        self.chat.text += "\nPREM: " + command + "\n"

        self.input.text = ""

        response = self.brain.reply(command)

        self.reply(response)

    # Activate
    def activate(self, instance):

        self.reply(
            "All systems online. Offline Smart Brain activated, Commander!"
        )

    # Save memory
    def save_history(self):

        try:
            with open(HISTORY_FILE, "w", encoding="utf-8") as file:
                json.dump(
                    self.chat.text,
                    file,
                    ensure_ascii=False
                )

        except Exception:
            pass

    # Load memory
    def load_history(self):

        try:
            if os.path.exists(HISTORY_FILE):

                with open(HISTORY_FILE, "r", encoding="utf-8") as file:
                    history = json.load(file)

                if isinstance(history, str):
                    self.chat.text = history

        except Exception:
            pass


if __name__ == "__main__":
    JarvisApp().run()
  

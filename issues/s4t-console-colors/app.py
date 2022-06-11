import streamlit as st
import sys
import logging
import coloredlogs

coloredlogs.install()

st.title("this app prints in color! :rainbow:")

st.write("If true, python will think we're talking to a terminal and color output by itself!")
st.write("stderr is a tty?", sys.stderr.isatty())

logging.info("beep boop")
logging.error("boop beep")
logging.warning("ACK ACK!!")
logging.critical("I love Streamlit")



st.write("these codes are manually configured and just exist for samples")
from colorama import Fore, Back, Style
palette = [
    Fore.RED + "red lorem ipsum fooem barem",
    Back.RED + "red background-lorem ipsum fooem barem",
    Fore.BLUE+"blue lorem ipsum fooem barem",
    Back.BLUE+"blue background-lorem ipsum fooem barem",
    Fore.CYAN+"cyan lorem ipsum fooem barem",
    Back.CYAN+"cyan background-lorem ipsum fooem barem",
    Fore.WHITE+"white lorem ipsum fooem barem",
    Back.WHITE+Fore.BLACK+"black on white background-lorem ipsum fooem barem",
    Back.BLACK+Fore.WHITE+"white on black background-lorem ipsum fooem barem",
    Fore.GREEN+"green lorem ipsum fooem barem",
    Back.GREEN+"green background-lorem ipsum fooem barem",
    Fore.YELLOW+"yellow lorem ipsum fooem barem",
    Back.YELLOW+"yellow background-lorem ipsum fooem barem",
    Fore.MAGENTA+"magenta lorem ipsum fooem barem",
    Back.MAGENTA+"magenta background-lorem ipsum fooem barem",
]

for s in palette:
    print(s)

user_input = st.text_input("test out logging here", value='🎈 welcome to my demo 🎈')
logging.info(user_input)

import sys
for i in range(0, 16):
    for j in range(0, 16):
        code = str(i * 16 + j)
        sys.stdout.write(u"\u001b[38;5;" + code + "m " + code.ljust(4))
    print(u"\u001b[0m")
    
print("WARNING test")
print("CRITICAL test")
print("ERROR test")
print("INFO test")
print("DEBUG test")

print("foo")
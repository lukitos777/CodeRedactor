from tkinter import *
import ctypes
import re
import os


def execute(event=None):
    with open('run.py', 'w', encoding='utf-8') as f:
        f.write(edit_area.get('1.0', END))

    os.system('start cmd /K "python run.py"')


def colorise(event=None):
    global previous_text

    if edit_area.get('1.0', END) == previous_text:
        return

    for tag in edit_area.tag_names():
        edit_area.tag_remove(tag, '1.0', 'end')

    i = 0
    for pattern, color in repl:
        for start, end in search_re(pattern, edit_area.get('1.0', END)):
            edit_area.tag_add(f'{i}', start, end)
            edit_area.tag_config(f'{i}', foreground=color)

            i += 1

    previous_text = edit_area.get('1.0', END)


def search_re(pattern, text):
    matches = []
    text = text.splitlines()

    for i, line in enumerate(text):
        for match in re.finditer(pattern, line):
            matches.append((f'{i + 1}.{match.start()}', f'{i + 1}.{match.end()}'))

    return matches


def rgb(rgb_color):
    return '#%02x%02x%02x' % rgb_color


ctypes.windll.shcore.SetProcessDpiAwareness(True)

root = Tk()
root.geometry('800x600')
root.title('Code redactor </>')
previous_text = ''

normal_color = rgb((234, 234, 234))
key_words = rgb((234, 95, 95))
comments = rgb((95, 234, 165))
string = rgb((234, 162, 95))
function = rgb((95, 211, 234))
ground = rgb((42, 42, 42))

font = 'Consolas 15'


repl = [
    ['(^| )(False|None|True|and|as|assert|async|await|break|class|continue|def|del|elif|else|except|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield)($| )', key_words],
    ['".*?"', string],
    ['\".*?\"', string],
    ['#.*?$', comments]
]

edit_area = Text(
    root, background=ground, foreground=normal_color, insertbackground=normal_color, relief=FLAT, borderwidth=30, font=font
)

edit_area.pack(fill=BOTH, expand=1)

edit_area.insert('1.0', """from random import randint

print([randint(1, 7) for i in range(10)])

""")

edit_area.bind('<KeyRelease>', colorise)

root.bind('<Control-r>', execute)

colorise()

root.mainloop()
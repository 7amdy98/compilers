import re
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext


def tokenizer(input_expression):
    current = 0
    tokens = []

    numbers = re.compile(r"[0-9]")
    alphabet = re.compile(r"[a-z\d]", re.I)
    whiteSpace = re.compile(r"\s")
    ignore = re.compile(r"\n")
    while current < len(input_expression):
        char = input_expression[current]
        if re.match(whiteSpace, char):
            current = current + 1
            continue
        if re.match(ignore, char):
            current = current + 1
            continue
        if char == ';':
            tokens.append({
                'type': 'Separator',
                'value': ';'
            })
            current = current + 1
            continue
        if char == '=':
            tokens.append({
                'type': 'Equal',
                'value': '='
            })
            current = current + 1
            continue
        if char == ':':
            if input_expression[current + 1] == '=':
                tokens.append({
                    'type': 'Assign',
                    'value': ':='
                })
                current = current + 2
                continue
        if char == '>':
            if input_expression[current + 1] == '=':
                tokens.append({
                    'type': 'Greater Than Equal',
                    'value': '>='
                })
                current = current + 2
                continue
            tokens.append({
                'type': 'Greater Than',
                'value': '>'
            })
            current = current + 1
            continue
        if char == '<':
            if input_expression[current + 1] == '=':
                tokens.append({
                    'type': 'Smaller Than Equal',
                    'value': '<='
                })
                current = current + 2
                continue
            tokens.append({
                'type': 'Smaller Than',
                'value': '<'
            })
            current = current + 1
            continue
        if re.match(numbers, char):
            value = ''
            while re.match(numbers, char):
                value += char
                current = current + 1
                if current > len(input_expression) - 1: break
                char = input_expression[current]
            tokens.append({
                'type': 'number',
                'value': value
            })
            continue
        if re.match(alphabet, char):
            value = ''
            while re.match(alphabet, char):
                value += char
                current = current + 1
                if current > len(input_expression) - 1: break
                char = input_expression[current]
            if value.lower() == "repeat":
                tokens.append({
                    'type': 'REPEAT',
                    'value': value
                })
                continue
            elif value.lower() == "until":
                tokens.append({
                    'type': 'UNTIL',
                    'value': value
                })
                continue
            else:
                tokens.append({
                    'type': 'name',
                    'value': value
                })
                continue
        raise ValueError('Invalid Char: ' + char)
    return tokens


def is_matching(tokens: dict):
    pattern = []
    pattern.append(0)
    current_state = 0
    for tok in tokens:
        if current_state == 0:
            if tok["type"] == "REPEAT":
                current_state = 1
            else:
                current_state = 10
        elif current_state == 1:
            if tok["type"] == "name":
                current_state = 2
            else:
                current_state = 10
        elif current_state == 2:
            if tok["type"] == "Assign":

                current_state = 3
            else:
                current_state = 10
        elif current_state == 3:
            if tok["type"] == "name" or tok["type"] == "number":
                current_state = 4
            else:
                current_state = 10
        elif current_state == 4:
            if tok["type"] == "Separator":
                current_state = 5
            else:
                current_state = 10
        elif current_state == 5:
            if tok["type"] == "name":
                current_state = 2
            elif tok["type"] == "UNTIL":
                current_state = 6
            else:
                current_state = 10
        elif current_state == 6:
            if tok["type"] == "name" or tok["type"] == "number":
                current_state = 7
            else:
                current_state = 10
        elif current_state == 7:
            if tok["type"] == "Equal" or tok["type"] == "Assign" or tok["type"] == "Greater Than Equal" or tok[
                "type"] == "Greater Than" or tok["type"] == "Smaller Than Equal" or tok["type"] == "Smaller Than":
                current_state = 8
            else:
                current_state = 10
        elif current_state == 8:
            if tok["type"] == "name" or tok["type"] == "number":
                current_state = 9
            else:
                current_state = 10
        elif current_state == 9:
            if tok["type"] == "REPEAT":
                current_state = 1
            else:
                current_state = 10
        elif current_state == 10:
            current_state = 10
        pattern.append(current_state)
    if pattern[-1] == 9: return pattern, True
    return pattern, False


root = tk.Tk()
root.geometry("1500x700")
root.title("dfa")

# labels
l1 = Label(root, text="deterministic finite automaton", font=('Ariel', 60))
l2 = Label(root, text="case 4", font=('Ariel', 60))
l3 = Label(root, text="Please enter the statement you would like to check", font=('Ariel', 24))
l1.pack()
l2.pack()
l3.pack()
# entries
t = tk.Text(root, width=40, height=15)
t.pack()


#

def des():
    label.after(1000, label.destroy())
    lab.after(1000, label.destroy())


def myClick():
    global label
    global lab
    u = t.get(1.0, END)
    label = Label(root, text=str(is_matching(tokenizer(u))), font=('Arial', 12))
    label.pack()
    lab = Label(root, text=tokenizer(u), font=('Arial', 10), wraplength=500)

    lab.pack()


# buttons

button1 = Button(root, text="clear", command=des)
button1.pack()
button = Button(root, text="Submit", command=myClick)
button.pack()

root.mainloop()
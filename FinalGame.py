#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import tkinter as tk
from tkinter import *
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance
from PIL import ImageTk, Image
from sklearn.preprocessing import Normalizer


#A very slopply coded opening screen

def window(list):
    root = Tk()
    canvas1 = tk.Canvas(root, width=1400, height=800)
    root.geometry('1400x800')
    root.title('Bet That Line!')
    root.configure()
    centerx = root.winfo_vrootwidth() / 2
    centery = root.winfo_vrootheight() / 2
    load = Image.open('main-qimg-44dd237884b9c3464428526af428b514.png')
    render = ImageTk.PhotoImage(load)
    img = Label(root, image=render)
    img.image = render
    img.place(x=centerx * 1.35, y=centery * .03125)
    load = Image.open('main-qimg-44dd237884b9c3464428526af428b514.png')
    render = ImageTk.PhotoImage(load)
    img = Label(root, image=render)
    img.image = render
    img.place(x=centerx * .525, y=centery * .03125)

    canvas1.pack()

    label4 = tk.Label(root, text='BET THAT LINE', font='Constantia 60')
    canvas1.create_window(centerx, centery * .125, window=label4)

    def only_decimals(char):
        if str.isdigit(char) or char == '.':
            return True
        else:
            return False

    validation = root.register(only_decimals)
    entry1 = tk.Entry(root, validate='key',
                      validatecommand=(validation, '%S'),
                      font='Calibri 30')
    canvas1.create_window(centerx, centery * .35, window=entry1)

    selected = IntVar()

    def clicked():

        lnechoice.append(selected.get())
        label1 = tk.Label(root, text='on Line #'
                                     + str(selected.get()), font='Calibri 30')
        canvas1.create_window(1.1 * centerx, centery * 1.6, window=label1)

    rad1 = Radiobutton(root, text='1', value=1, variable=selected, font='Calibri 30')
    rad2 = Radiobutton(root, text='2', value=2, variable=selected, font='Calibri 30')
    rad3 = Radiobutton(root, text='3', value=3, variable=selected, font='Calibri 30')
    rad4 = Radiobutton(root, text='4', value=4, variable=selected, font='Calibri 30')

    label10 = tk.Label(root, text='Choose a line: ', font='Calibri 35')
    canvas1.create_window(centerx * .65, centery * .80, window=label10)

    btn = Button(root, text='Select', command=clicked, font='Calibri 30')
    canvas1.create_window(.85 * centerx, centery * .80, window=rad1)
    canvas1.create_window(.95 * centerx, centery * .80, window=rad2)
    canvas1.create_window(1.05 * centerx, centery * .80, window=rad3)
    canvas1.create_window(1.15 * centerx, centery * .80, window=rad4)
    canvas1.create_window(1 * centerx, centery * .95, window=btn)

    def betoutput():
        x1 = float(entry1.get())
        list.append(x1)
        label1 = tk.Label(root, text='You Put: $' + str(x1),
                          font='Calibri 30')
        canvas1.create_window(.75 * centerx, centery * 1.6, window=label1)

    button1 = tk.Button(text='Place Bet', command=betoutput, font='Calibri 30')
    canvas1.create_window(centerx, centery * .50, window=button1)

    exit_button = tk.Button(root, text='Ready', command=root.destroy, font='Calibri 80')
    canvas1.create_window(centerx, centery * 1.35, window=exit_button)
    root.mainloop()


lnames = []
xdata = []
y1data, y2data, y3data, y4data = [], [], [], []
yaxlims = [y1data, y2data, y3data, y4data]
cinema = []
quantity = 250

while len(cinema) < 4:
    df = pd.read_csv('Combined(Use).csv')
    name = df['Ticker'][random.randint(1, quantity - 1)]
    assert isinstance(name, str)
    stock = yfinance.Ticker(name)
    hist = stock.history(period='1y')
    if len(hist['Close']) < quantity:
        print("<<[]>>")
        continue
    else:
        lnames.append((str(len(cinema) + 1) + " " + name))
        print(lnames)
        varname = hist['Close']
        cinema.append(varname)
        
#data gets normalized to improve visuals

graph = Normalizer(norm="max").fit_transform(cinema)

y1, y2, y3, y4 = graph[0], graph[1], graph[2], graph[3]
originally = [y1, y2, y3, y4]

lnechoice = list()
tmp = list()
window(tmp)
linechoice = lnechoice[len(lnechoice) - 1]
if len(tmp) > 0:
    Bet = float(tmp[len(tmp) - 1])

lnames[linechoice - 1] = 'Your Line'

(fig, ax) = plt.subplots(facecolor='#EAEAEA')
(line1,) = ax.plot([], [], lw=2, label=lnames[0])
(line2,) = ax.plot([], [], lw=2, label=lnames[1])
(line3,) = ax.plot([], [], lw=2, label=lnames[2])
(line4,) = ax.plot([], [], lw=2, label=lnames[3])
plt.title('Bet That Line!')
ax.grid()
ax.set_facecolor('#303030')

#data reorganization for matplotlib animation

def data_gen(t=0):
    c = 0
    while c < quantity:
        c += 1
        t += 1
        yield t, y1[t], y2[t], y3[t], y4[t]


def init():
    del xdata[:]
    del y1data[:]
    del y2data[:]
    del y3data[:]
    del y4data[:]
    line1.set_data(xdata, y1data)
    line2.set_data(xdata, y2data)
    line3.set_data(xdata, y3data)
    line4.set_data(xdata, y4data)
    return line1, line2, line3, line4


def run(data):
    # update the data

    t, a, z, c, d = data
    xdata.append(t)
    y1data.append(a)
    y2data.append(c)
    y3data.append(z)
    y4data.append(d)


    xmin, xmax = ax.get_xlim()
    if t >= xmax:
        ax.figure.canvas.draw()
        ax.set_xlim(xmin, xmax * 1.05)
    line1.set_data(xdata, y1data)
    line2.set_data(xdata, y2data)
    line3.set_data(xdata, y3data)
    line4.set_data(xdata, y4data)
    ymindata = np.min(yaxlims)
    ymaxdata = np.max(yaxlims)
    ax.set_ylim(ymindata * .40, ymaxdata * 1.10)

    return line1, line2, line3, line4


ani = animation.FuncAnimation(
    fig,
    run,
    data_gen(),
    blit=False,
    interval=10,
    repeat=False,
    init_func=init,
)

plt.legend(loc='upper left')
plt.show()

#A very slopply coded ending screen

def endwindow():
    betvalue = cinema[linechoice - 1][0]
    finalvalue = cinema[linechoice - 1][len(xdata) - 1]

    newvalue = finalvalue / betvalue * Bet
    profit = np.round(newvalue - Bet, 5)
    roi = np.round(profit / Bet * 100, 5)

    root = Tk()
    root.geometry('600x400')
    root.title('End Screen')
    label = tk.Label(root, text='Original Bet $' + str(Bet),
                     font='Calibri 25')
    label.pack(ipadx=10, ipady=10)
    label1 = tk.Label(root, text='Your Money is now worth: '
                                 + str(newvalue) + ' \nbecause the line moved: '
                                 + str(roi) + '%', font='Calibri 25')
    label1.pack(ipadx=10, ipady=10)
    if profit > 0:
        label2 = tk.Label(root, text='Profit: $' + str(profit),
                          font='Calibri 25')
        label2.pack(ipadx=10, ipady=10)
    elif profit < 0:
        label2 = tk.Label(root, text='Loss: $' + str(profit),
                          font='Calibri 25')
        label2.pack(ipadx=10, ipady=10)
    exit_button = tk.Button(root, text='Exit', command=lambda:
                            root.destroy(), font='Calibri 25')
    exit_button.pack(ipadx=3, ipady=1, expand=True)
    root.mainloop()


endwindow()

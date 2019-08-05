import itertools, time, csv
import pandas as pd
from random import randint
from statistics import mean
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def grouper(iterable, n):
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args)

data = pd.read_csv('Base.csv')
circulos = pd.unique(data.C)

c = canvas.Canvas("prueb6.pdf", pagesize=A4)
w, h = A4
max_rows_per_page = 50
# Margin.
x_offset = 50
y_offset = 50
# Space between rows.
padding = 15

xlist = [x + x_offset for x in [0, 25, 45, 445, 485]]
ylist = [h - y_offset - i*padding for i in range(max_rows_per_page + 1)]

for circ in circulos:
    
    data = pd.read_csv('Base.csv')
    circulos = pd.unique(data.C)
    ci = circulos.tolist()
    circulo1 = data[data.C == circ]
    circuloLista = circulo1.values.tolist()
    
    for rows in grouper(circuloLista, max_rows_per_page):
        rows = tuple(filter(bool, rows))
        c.grid(xlist, ylist[:len(rows) + 1])
        for y, row in zip(ylist[:-1], rows):
            for x, cell in zip(xlist, row):
                c.drawString(x + 2, y - padding + 3, str(cell))
        c.showPage()
c.save()
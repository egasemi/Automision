import itertools, time, csv
from random import randint
from statistics import mean
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

    
with open ('Base.csv', newline='') as csvfile:
    spamreader = csv.DictReader(csvfile)
    print(spamreader)
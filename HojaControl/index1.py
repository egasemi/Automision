import itertools, time, csv
import pandas as pd
import numpy as np
from random import randint
from statistics import mean
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def grouper(iterable, n):
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args)

data = pd.read_csv('/home/emi/Git/Automision/HojaControl/d5-16.csv').set_index('Codigo Prod.')
marcas = pd.read_csv('/home/emi/Git/Automision/HojaControl/Productos d5-16.csv', delimiter = '|').set_index('Codigo').Marca
circs = pd.unique(data['Circulo Nro'])
circs = np.sort(circs[np.logical_not(np.isnan(circs))]).astype(int)

c = canvas.Canvas("HojasControlD5.pdf", pagesize=A4)
an, al = A4
max_rows_per_page = 50
# Margin.
x_offset = 30
y_offset = 70
# Space between rows.
padding = 15

xlist = [x + x_offset for x in [0, 300, 340, 380, 420, 460, 500, 540]]
ylist = [al - y_offset - i*padding for i in range(max_rows_per_page + 1)]

for cr in circs:

	data = pd.read_csv('/home/emi/Git/Automision/HojaControl/d5-16.csv').set_index('Codigo Prod.')
	marcas = pd.read_csv('/home/emi/Git/Automision/HojaControl/Productos d5-16.csv', delimiter = '|').set_index('Codigo').Marca

	pedido = data[data['Circulo Nro'] == cr].iloc[0:, 2:13]
	pedmarc = pd.merge(pedido, marcas.to_frame(), left_index=True, right_index=True)
	pedmarc['Nombre'] = pedmarc['Nombre'] + ' ' + pedmarc['Usuario'].str[:1]			
	socios = list(pd.unique(pedmarc['Nombre']))
	socios.append('Total')
	pedmarc['Nombre Prod.'] = pedmarc['Nombre Prod.'] + ' - ' + pedmarc['Marca']
	tabla = pd.pivot_table(pedmarc, values=['Cantidad'], columns=['Nombre'], index=['Nombre Prod.'], aggfunc=np.sum, margins = True, margins_name = 'Total').fillna('0')
	
	prod = []
	for row in tabla.index.tolist():
		prod.append((row[0:80]))
	dp = pd.DataFrame(prod).sort_index(inplace=True)
	
	
	cant = []
	for row in tabla.values.tolist():
		cant.append(list(map(int, row)))
	df = pd.DataFrame(cant)
	
	# frames = [dp,df]
	result = pd.concat([dp,df], axis=1).values.tolist()

	for rows in grouper(result, max_rows_per_page):
		
		c.setFont('Helvetica-Bold',size=25)				#\
		c.drawString(30, al-50,'Círculo N°'+ str(cr))	# > titulo de la hoja
		c.setFont('Helvetica', size=12)					#/
		c.drawString(30, al-65, 'Productos')
		c.setFontSize(size=8)
		c.rotate(90)
		posx = 240

		for nomb in socios:			
			c.drawString(al-65, posx-an, nomb[0:11])
			posx = posx - 40
		
		c.rotate(-90)

		rows = tuple(filter(bool, rows))
		c.grid(xlist, ylist[:len(rows) + 1])
		for y, row in zip(ylist[:-1], rows):
			for x, cell in zip(xlist, row):
				c.drawString(x + 2, y - padding + 3, str(cell))
		c.showPage()
c.save()
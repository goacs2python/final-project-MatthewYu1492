"""
Month,Chinese combo,Chinese single,Western Combo,Western Single,School Days
"""
from bokeh.plotting import figure, show
from bokeh.models import DatetimeTickFormatter
from datetime import datetime
import csv
import numpy as np
import statistics


#open files
salesdata = open("Catering Data.csv", "r")


#construct class data structure
class Monthly_sales:
    def __init__(self, time, westernsingle, westerncombo, asiansingle, asiancombo, schooldays):
        (month, year) = time.split("/")
        self.date = datetime(int(year)+2000, int(month), 1)
        self.westernsingle = westernsingle
        self.westerncombo = westerncombo
        self.westerntotal = westernsingle + westerncombo
        self.asiansingle = asiansingle
        self.asiancombo = asiancombo
        self.asiantotal = asiansingle + asiancombo
        self.schooldays = schooldays
        self.westerndailysales = self.westerntotal / self.schooldays
        self.asiandailysales = self.asiantotal / self.schooldays


#list to store data classes
sales = []


#read data file
for line in salesdata:
    month, asiancombo, asiansingle, westerncombo, westernsingle, schooldays = line.strip().split(",")
    sales.append(Monthly_sales(month, int(westernsingle), int(westerncombo), int(asiansingle), int(asiancombo), int(schooldays)))


#visualize
scatter = figure(width = 600, height = 400, x_axis_type='datetime', background_fill_color = "grey", border_line_color = "black", outline_line_color = "black", y_range=(100, 210))
scatter.xaxis.formatter = DatetimeTickFormatter(months="%m/%Y", years="%m/%Y")
scatter.title = "SS 2025-2026 School Year Lunch Sales"
scatter.title.text_font_size = "30px"
scatter.title.align = "center"
scatter.xaxis.axis_label = "School Months (Sep. - Mar.)"
scatter.xaxis.axis_label_text_font_size = "20px"
scatter.yaxis.axis_label = "Average Daily Sales (Dishes)"
scatter.yaxis.axis_label_text_font_size = "20px"
dates = [month.date for month in sales]
western = [month.westerndailysales for month in sales]
asian = [month.asiandailysales for month in sales]
scatter.scatter(dates, western, size=7, color="blue")
scatter.line(dates, western, line_width=3, color="blue", line_dash=[5, 3], legend_label="Western Lunch Option")
scatter.scatter(dates, asian, size=7, color="red")
scatter.line(dates, asian, line_width=3, color="red", line_dash=[5, 3], legend_label="Asian Lunch Option")
show(scatter)


def find_variance(x, y, function):
    residue = []
    for (xi, i) in enumerate(x):
        y_pred = function(xi)
        dif = abs(y_pred - y[i])
        residue.append(dif)
    return statistics.variance(residue)


#find prediction
#optimize polynomial function degree
asiancoeffs = {}
westerncoeffs = {}
x = [i for i in range(7)]
for i in range(9):
    deg = i+1
    asianfunction = np.poly1d(np.polyfit(x, asian, deg=deg))
    asianvariance = find_variance(x, asian, asianfunction)
    if abs(asianfunction(7) - 155.25) < 50:
        asiancoeffs[deg] = asianvariance
    westernfunction = np.poly1d(np.polyfit(x, western, deg=deg))
    westernvariance = find_variance(x, western, westernfunction)
    if abs(westernfunction(7) - 178.75) < 50:
        westerncoeffs[deg] = westernvariance
def ordering(key):
    return asiancoeffs[key]
coeffs = list(asiancoeffs)
coeffs.sort(key=ordering, reverse=False)
for corner in coeffs:
    number = asiancoeffs[corner]
    del asiancoeffs[corner]
    asiancoeffs[corner] = number
def ordering(key):
    return westerncoeffs[key]
coeffs = list(westerncoeffs)
coeffs.sort(key=ordering, reverse=False)
for corner in coeffs:
    number = westerncoeffs[corner]
    del westerncoeffs[corner]
    westerncoeffs[corner] = number
#find prediction & variance
asiandeg = list(asiancoeffs.keys())[0]
asianfunction = np.poly1d(np.polyfit(x, asian, deg=asiandeg))
asianprediction = asianfunction(7)
asianvariance = list(asiancoeffs.values())[0]
westerndeg = list(asiancoeffs.keys())[0]
westernfunction = np.poly1d(np.polyfit(x, western, deg=westerndeg))
westernprediction = westernfunction(7)
westernvariance = list(westerncoeffs.values())[0]


#store data in file (dish, measurement, measurement variance, prediction, prediction variance)
salescalcr = csv.reader(open("Sales Calc.csv", "r"))
dishes = []
for i,line in enumerate(salescalcr):
    if i == 0:
        line.extend([round(float(asianprediction), 3), round(float(asianvariance), 3)])
    elif i == 1:
        line.extend([round(float(westernprediction), 3), round(float(westernvariance), 3)])
    else:
        line.extend([line[1], line[2]])
    print(line)
    dishes.append(line)

salescalcw = csv.writer(open("Sales Calc.csv", "w"))
for dish in dishes:
    salescalcw.writerow(dish)
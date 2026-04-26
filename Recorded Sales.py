"""
date,Chinese set,Chinese a la carte,Noodle Bar,Western set,Western a la carte
"""
from bokeh.plotting import figure, show
from bokeh.models import DatetimeTickFormatter
from datetime import datetime
import csv
import statistics


#open files
salesdata = open("Recorded Sales.csv", "r")
salescalc = csv.writer(open("Sales Calc.csv", "w"))


#construct class data structre
class Daily_sales:
    def __init__(self, time, asiancombo, asiansingle, noodles, westerncombo, westernsingle):
        (month, date) = time.split(".")
        self.date = datetime(2026, int(month), int(date))
        self.westernsingle = westernsingle
        self.westerncombo = westerncombo
        self.westerntotal = westernsingle + westerncombo
        self.asiansingle = asiansingle
        self.asiancombo = asiancombo
        self.asiantotal = asiansingle + asiancombo
        self.noodles = noodles


#list to store classes
sales = []


#read data file
for line in salesdata:
    date, asiancombo, asiansingle, noodles, westerncombo, westernsingle = line.strip().split(",")
    sales.append(Daily_sales(date, int(asiancombo), int(asiansingle), int(noodles), int(westerncombo), int(westernsingle)))


#create visual
dates = [day.date for day in sales]
western = [day.westerntotal for day in sales]
asian = [day.asiantotal for day in sales]
noodles = [day.noodles for day in sales]
scatter = figure(width = 600, height = 400, x_axis_type='datetime', background_fill_color = "grey", border_line_color = "black", outline_line_color = "black", y_range=(min(western+asian+noodles)-10, max(western+asian+noodles)+80))
scatter.xaxis.formatter = DatetimeTickFormatter(months="%m/%d", days="%m/%d")
scatter.title = "SS April Lunch Sales"
scatter.title.text_font_size = "30px"
scatter.title.align = "center"
scatter.xaxis.axis_label = "School Days (April.21 - April.24)"
scatter.xaxis.axis_label_text_font_size = "20px"
scatter.yaxis.axis_label = "Recorded Daily Sales (Dishes)"
scatter.yaxis.axis_label_text_font_size = "20px"
scatter.scatter(dates, western, size=7, color="blue")
scatter.line(dates, western, line_width=3, color="blue", line_dash=[5, 3], legend_label="Western Lunch Option")
scatter.scatter(dates, asian, size=7, color="red")
scatter.line(dates, asian, line_width=3, color="red", line_dash=[5, 3], legend_label="Asian Lunch Option")
scatter.scatter(dates, noodles, size=7, color="green")
scatter.line(dates, noodles, line_width=3, color="green", line_dash=[5, 3], legend_label="Noodles Lunch Option")
show(scatter)


#find measurement
asianmean = statistics.mean(asian)
asianvariance = statistics.variance(asian)
westernmean = statistics.mean(western)
westernvariance = statistics.variance(western)
noodlesmean = statistics.mean(noodles)
noodlesvariance = statistics.variance(western)


#store data in file (dish, measurement, measurement variance)
salescalc.writerow(["asian", round(asianmean, 3), round(asianvariance, 3)])
salescalc.writerow(["western", round(westernmean, 3), round(westernvariance, 3)])
salescalc.writerow(["noodles", round(noodlesmean, 3), round(noodlesvariance, 3)])
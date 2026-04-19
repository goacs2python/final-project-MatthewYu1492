"""
Id,Start time,Completion time,Email,Name,What's your grade level?,How satisfied are you with the quality of school lunch? (10 is the highest),Please explain your rating,In your opinion what are some areas that the school should focus on when developing better dishes?,Which corner do you go to the most to buy food?,"Is there anything else you would like to mention about school lunch (fav dish, least fav dish, etc.)?"
"""

from bokeh.plotting import figure, show
from bokeh.layouts import gridplot
import numpy as np
import math
import random


survey = open("Quick Questions_ School Lunch.csv", "r")

satisfactionlog = []
satisfactioncount = {}
favcornerlog = []
favcornercount = {}


#append satisfaction & food corner data into list
for line in survey:
    line = line.strip().split(",")
    satisfactionlog.append(line[6])
    favcornerlog.append(line[9])

#reorganize food rating data into dictionary
for rating in satisfactionlog:
    if not rating:
        pass
    elif int(rating) not in satisfactioncount: #if that rating has not appeared before
        satisfactioncount[int(rating)] = 1

    else: 
        satisfactioncount[int(rating)] += 1 #if that rating has appeared before


#reoder rating dictionary
satisfactioncount = dict(sorted(satisfactioncount.items()))

#organize food corner into dictionary
for corner in favcornerlog:
    if not corner:
        pass
    elif corner not in favcornercount: #if that rating has not appeared before
        favcornercount[corner] = 1

    else: 
        favcornercount[corner] += 1 #if that rating has appeared before

#graphing satisfaction
#graphing satisfaction
satisfactionhistogram = figure(width = 600, height = 400, background_fill_color = "grey", border_line_color = "black", outline_line_color = "black")
satisfactionhistogram.title = "Title Here"
satisfactionhistogram.title.text_font_size = "30px"
satisfactionhistogram.title.align = "center"
satisfactionhistogram.xaxis.axis_label = "Xaxis Title Here"
satisfactionhistogram.xaxis.axis_label_text_font_size = "20px"
satisfactionhistogram.yaxis.axis_label = "Yaxis Title Here"
satisfactionhistogram.yaxis.axis_label_text_font_size = "20px"
bar_width = 0.5
hist_x = []
hist_y = []
for i, rating in enumerate(satisfactioncount):
    number = satisfactioncount[rating]
    hist_x.append(float(bar_width*i+bar_width/2))
    hist_y.append(int(number))
satisfactionhistogram.vbar(hist_x, bar_width, hist_y, 0, line_color = "white", )


#graphing corner
cornerpychart = figure(background_fill_color = "grey", border_line_color = "black", x_range=(-0.1, 2.8), y_range=(-0.1, 2.8))
cornerpychart.title = "Title Here"
cornerpychart.title.text_font_size = "30px"
cornerpychart.title.align = "center"
numbersum = sum(favcornercount.values())
pie_degree = 0
colorlist = ["black", "red", "green", "yellow", "blue", "brown", "orange", "pink", "purple", "gray"]
for rating in favcornercount:
    number = favcornercount[rating]
    numberratio = number/numbersum
    wedge_degree = numberratio * 2 * math.pi
    colorpick = random.choice(colorlist)
    cornerpychart.annular_wedge(1, 1, 0, 1, pie_degree, (wedge_degree + pie_degree), color=colorpick, line_color="black", line_width=3, legend_label=f"{rating}: {round(100*numberratio, 2)}%")
    pie_degree += wedge_degree
    colorlist.remove(colorpick)

g = gridplot([[satisfactionhistogram, cornerpychart]])
show(g)
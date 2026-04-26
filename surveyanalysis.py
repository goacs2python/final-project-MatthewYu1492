"""
Id,Start time,Completion time,Email,Name,What's your grade level?,How satisfied are you with the quality of school lunch? (10 is the highest),Please explain your rating,In your opinion what are some areas that the school should focus on when developing better dishes?,Which corner do you go to the most to buy food?,"Is there anything else you would like to mention about school lunch (fav dish, least fav dish, etc.)?"
"""

from bokeh.plotting import figure, show
from bokeh.layouts import gridplot
import numpy as np
import math
import random
import statistics


survey = open("Quick Questions_ School Lunch.csv", "r")

satisfactionlog = []
HSsatisfactionlog = []
MSsatisfactionlog = []
favcornercount = {}
HSfavcornercount = {}
MSfavcornercount = {}
improvementareas = {}
commonkeywords = {}


#append satisfaction & food corner data into list
for i, line in enumerate(survey):
    # print(i)
    line = line.strip().split(",")

    grade = list(line[5])
    if len(grade) == 2:
        grade = int(list(line[5])[1])
    else:
        grade = int(list(line[5])[1]) + int(list(line[5])[2])
    
    if grade <= 8:
        SS = "middle"
    elif grade == 9 or grade == 10 or grade == 11 or grade == 12:
        SS = "high"

    satisfaction = line[6]
    if satisfaction:
        satisfactionlog.append(int(satisfaction))
        if SS == "high":
            HSsatisfactionlog.append(int(satisfaction))
        else:
            MSsatisfactionlog.append(int(satisfaction))

    corner = line[9]
    if corner == "Taste Of Asia":
        favcorner = "Asian"
    elif corner == "Italian" or corner == "Chef's Table":
        favcorner = "Western"
    elif corner == "Revolutionary Noodles":
        favcorner = "Noodles"
    else:
        favcorner = corner
    if favcorner and favcorner in favcornercount:
        favcornercount[favcorner] += 1
    elif favcorner and favcorner not in favcornercount:
        favcornercount[favcorner] = 1
    if SS == "high" and favcorner and favcorner in HSfavcornercount:
        HSfavcornercount[favcorner] += 1
    elif SS == "high" and favcorner and favcorner not in HSfavcornercount:
        HSfavcornercount[favcorner] = 1
    if SS == "middle" and favcorner and favcorner in MSfavcornercount:
        MSfavcornercount[favcorner] += 1
    elif SS == "middle" and favcorner and favcorner not in MSfavcornercount:
        MSfavcornercount[favcorner] = 1
    
    suggestionkeywords = {
    "Health & Nutrition Value":["Nutrition", "protein", "vegetable", "fried", "pre-made", "material", "health", "ingredient", "meat", "oil"], 
    "Price & Affordability": ["price", "expensive", "cheap", "pricey"], 
    "Options & Variety": ["repetitive", "repetition", "dull", "boring", "choices", "vegetarian", "vegan", "new", "option", "variety"], 
    "Taste & Deliciousness": ["taste", "seasoning", "salt", "flavor", "spice", "spicy", "sweet", "delicious"]
    }
    reason = line[7].lower()
    improvement = line[8].lower()
    for area in suggestionkeywords:
        for keyword in suggestionkeywords[area]:
            taken = False
            if (keyword in reason or keyword in improvement) and area in improvementareas: 
                improvementareas[area] += 1
                break
            elif (keyword in reason or keyword in improvement) and area not in improvementareas:
                improvementareas[area] = 1
                break
    
    reasonkeywords = reason.split(" ")
    for keyword in reasonkeywords:
        if keyword in commonkeywords:
            commonkeywords[keyword] += 1
        if keyword not in commonkeywords:
            commonkeywords[keyword] = 1
    improvementkeywords = improvement.split(" ")
    for keyword in improvementkeywords:
        if keyword in commonkeywords:
            commonkeywords[keyword] += 1
        if keyword not in commonkeywords:
            commonkeywords[keyword] = 1


#reorderin fav corners based on most & least
def ordering(key):
    return favcornercount[key]
corners = list(favcornercount)
corners.sort(key=ordering, reverse=True)
for corner in corners:
    number = favcornercount[corner]
    del favcornercount[corner]
    favcornercount[corner] = number


#reorderin HS fav corners based on most & least
def ordering(key):
    return HSfavcornercount[key]
HScorners = list(HSfavcornercount)
HScorners.sort(key=ordering, reverse=True)
for corner in HScorners:
    number = HSfavcornercount[corner]
    del HSfavcornercount[corner]
    HSfavcornercount[corner] = number


#reorderin MS fav corners based on most & least
def ordering(key):
    return MSfavcornercount[key]
MScorners = list(MSfavcornercount)
MScorners.sort(key=ordering, reverse=True)
for corner in MScorners:
    number = MSfavcornercount[corner]
    del MSfavcornercount[corner]
    MSfavcornercount[corner] = number


#reorderin improvement areas based on most & least
def ordering(key):
    return improvementareas[key]
areas = list(improvementareas)
areas.sort(key=ordering, reverse=True)
for area in areas:
    number = improvementareas[area]
    del improvementareas[area]
    improvementareas[area] = number


#filtering commonkeywords
badkeywords = [ "the","a","i","you","we","they","it","he","she","my","you","his","her","our","your","their","its","is","are","am","and","but","so","to","of","in","there","that","this","lunch","school","do","here","food","","meal","meals","eat","eating","very","really","quite","just","kind","kinda","sort","maybe","probably","actually","basically","honestly","stuff","things","something","anything","everything","on","not","be","can","like","as","for","foods","with","or","at","also","have","it's","should","use","about","making","such","could"]
commonkeywords2 = commonkeywords.copy()
for keyword in commonkeywords2:
    if keyword in badkeywords:
        del commonkeywords[keyword]
    elif commonkeywords2[keyword] < 3:
        del commonkeywords[keyword]


#reordering commonkeywords
def ordering(key):
    return commonkeywords[key]
keywords = list(commonkeywords)
keywords.sort(key=ordering, reverse=True)
for keyword in keywords:
    number = commonkeywords[keyword]
    del commonkeywords[keyword]
    commonkeywords[keyword] = number


#calculating mean staisfaction
averagesatisfaction = statistics.mean(satisfactionlog)
print(f"Total Average Satisfaction Rating: {round(averagesatisfaction, 2)}")
HSaveragesatisfaction = statistics.mean(HSsatisfactionlog)
print(f"HS Average Satisfaction Rating: {round(HSaveragesatisfaction, 2)}")
MSaveragesatisfaction = statistics.mean(MSsatisfactionlog)
print(f"MS Average Satisfaction Rating: {round(MSaveragesatisfaction, 2)}")


#graphing satisfaction
frequency, bins = np.histogram(satisfactionlog, 10, (1, 11))
hist_y = frequency
bar_width = bins[1] - bins[0]
hist_x = (bins + bar_width/2)[0:-1]
satisfactionhistogram = figure(width = 800, height = 600, background_fill_color = "grey", border_line_color = "black", outline_line_color = "black")
satisfactionhistogram.title = "SS Lunch Satisfaction Distribution"
satisfactionhistogram.title.text_font_size = "30px"
satisfactionhistogram.title.align = "center"
satisfactionhistogram.yaxis.axis_label = "Rating Frequency"
satisfactionhistogram.yaxis.axis_label_text_font_size = "20px"
satisfactionhistogram.vbar(hist_x, bar_width, hist_y, 0, line_color = "white")
for i, x in enumerate(hist_x):
    satisfactionhistogram.text((x-0.3), -1, [f"{i+1}⭐️"])


#graphing HSsatisfaction
frequency, bins = np.histogram(HSsatisfactionlog, 10, (1, 11))
hist_y = frequency
bar_width = bins[1] - bins[0]
hist_x = (bins + bar_width/2)[0:-1]
HSsatisfactionhistogram = figure(width = 800, height = 600, background_fill_color = "grey", border_line_color = "black", outline_line_color = "black")
HSsatisfactionhistogram.title = "MS Lunch Satisfaction Distribution"
satisfactionhistogram.title.text_font_size = "30px"
satisfactionhistogram.title.align = "center"
satisfactionhistogram.yaxis.axis_label = "Rating Frequency"
satisfactionhistogram.yaxis.axis_label_text_font_size = "20px"
HSsatisfactionhistogram.vbar(hist_x, bar_width, hist_y, 0, line_color = "white")
for i, x in enumerate(hist_x):
    HSsatisfactionhistogram.text((x-0.3), -1, [f"{i+1}⭐️"])


#graphing HSsatisfaction
frequency, bins = np.histogram(MSsatisfactionlog, 10, (1, 11))
hist_y = frequency
bar_width = bins[1] - bins[0]
hist_x = (bins + bar_width/2)[0:-1]
MSsatisfactionhistogram = figure(width = 800, height = 600, background_fill_color = "grey", border_line_color = "black", outline_line_color = "black")
MSsatisfactionhistogram.title = "HS Lunch Satisfaction Distribution"
satisfactionhistogram.title.text_font_size = "30px"
satisfactionhistogram.title.align = "center"
satisfactionhistogram.yaxis.axis_label = "Rating Frequency"
satisfactionhistogram.yaxis.axis_label_text_font_size = "20px"
MSsatisfactionhistogram.vbar(hist_x, bar_width, hist_y, 0, line_color = "white")
for i, x in enumerate(hist_x):
    MSsatisfactionhistogram.text((x-0.3), -1, [f"{i+1}⭐️"])


#graphing corner
cornerpychart = figure(background_fill_color = "grey", border_line_color = "black", x_range=(-0.1, 2.8), y_range=(-0.1, 2.8))
cornerpychart.title = "SS Favorite Food Option"
cornerpychart.title.text_font_size = "30px"
cornerpychart.title.align = "center"
numbersum = sum(favcornercount.values())
pie_degree = 0
for corner in favcornercount:
    number = favcornercount[corner]
    numberratio = number/numbersum
    wedge_degree = numberratio * 2 * math.pi
    if corner == "Western":
        colorpick = "blue"
    elif corner == "Asian":
        colorpick = "red"
    elif corner == "Noodles":
        colorpick = "green"
    else:
        colorpick = "orange"
    cornerpychart.annular_wedge(1, 1, 0, 1, pie_degree, (wedge_degree + pie_degree), color=colorpick, line_color="black", line_width=3, legend_label=f"{corner}: {round(100*numberratio, 2)}%")
    pie_degree += wedge_degree


#graphing HScorner
HScornerpychart = figure(background_fill_color = "grey", border_line_color = "black", x_range=(-0.1, 2.8), y_range=(-0.1, 2.8))
HScornerpychart.title = "HS Favorite Food Option"
HScornerpychart.title.text_font_size = "30px"
HScornerpychart.title.align = "center"
numbersum = sum(HSfavcornercount.values())
pie_degree = 0
for corner in HSfavcornercount:
    number = HSfavcornercount[corner]
    numberratio = number/numbersum
    wedge_degree = numberratio * 2 * math.pi
    if corner == "Western":
        colorpick = "blue"
    elif corner == "Asian":
        colorpick = "red"
    elif corner == "Noodles":
        colorpick = "green"
    else:
        colorpick = "orange"
    HScornerpychart.annular_wedge(1, 1, 0, 1, pie_degree, (wedge_degree + pie_degree), color=colorpick, line_color="black", line_width=3, legend_label=f"{corner}: {round(100*numberratio, 2)}%")
    pie_degree += wedge_degree


#graphing MScorner
MScornerpychart = figure(background_fill_color = "grey", border_line_color = "black", x_range=(-0.1, 2.8), y_range=(-0.1, 2.8))
MScornerpychart.title = "MS Favorite Food Option"
MScornerpychart.title.text_font_size = "30px"
MScornerpychart.title.align = "center"
numbersum = sum(MSfavcornercount.values())
pie_degree = 0
for corner in MSfavcornercount:
    number = MSfavcornercount[corner]
    numberratio = number/numbersum
    wedge_degree = numberratio * 2 * math.pi
    if corner == "Western":
        colorpick = "blue"
    elif corner == "Asian":
        colorpick = "red"
    elif corner == "Noodles":
        colorpick = "green"
    else:
        colorpick = "orange"
    MScornerpychart.annular_wedge(1, 1, 0, 1, pie_degree, (wedge_degree + pie_degree), color=colorpick, line_color="black", line_width=3, legend_label=f"{corner}: {round(100*numberratio, 2)}%")
    pie_degree += wedge_degree



#graphing improvement area
improvementpychart = figure(background_fill_color = "grey", border_line_color = "black", x_range=(-0.1, 2.8), y_range=(-0.1, 2.8))
improvementpychart.title = "SS Lunch Main Improvement Areas"
improvementpychart.title.text_font_size = "30px"
improvementpychart.title.align = "center"
numbersum = sum(improvementareas.values())
pie_degree = 0
colorlist = ["black", "red", "green", "yellow", "blue", "brown", "pink", "purple"]
for area in improvementareas:
    if area:
        number = improvementareas[area]
        numberratio = number/numbersum
        wedge_degree = numberratio * 2 * math.pi
        colorpick = random.choice(colorlist)
        improvementpychart.annular_wedge(1, 1, 0, 1, pie_degree, (wedge_degree + pie_degree), color=colorpick, line_color="black", line_width=3, legend_label=f"{area}: {round(100*numberratio, 2)}%")
        pie_degree += wedge_degree
        colorlist.remove(colorpick)

#graphing commonkeywords
hist_x = list(commonkeywords.values())
keywordshistogram = figure(width = 800, height = 600, background_fill_color = "grey", border_line_color = "black", outline_line_color = "black", y_range=(0, 10), x_range = (-max(list(commonkeywords.values()))*0.2, max(list(commonkeywords.values()))*1.03))
keywordshistogram.title = "SS Frequency of Most Common Keywords"
keywordshistogram.title.text_font_size = "30px"
for i, keyword in enumerate(list(commonkeywords.keys())[:10]):
    hist_y = 9.5 - i
    keywordshistogram.hbar(hist_y, height=1,right=commonkeywords[keyword],line_color="white")
    keywordshistogram.text(-0.5, hist_y, [keyword], text_align="right")


g = gridplot([[satisfactionhistogram, HSsatisfactionhistogram, MSsatisfactionhistogram], [cornerpychart, HScornerpychart, MScornerpychart], [keywordshistogram, improvementpychart]])
show(g)
"""
dish, measurement, measurement variance, prediction, prediction variance
"""
from bokeh.plotting import figure, show
from bokeh.layouts import gridplot


f = open("Sales Calc.csv", "r")


lunchsales = {}
for line in f:
    dish, measuredvalue, measuredvariance, predictedvalue, predictedvariance = line.strip().split(",")
    measuredvalue = float(measuredvalue)
    measuredvariance = float(measuredvariance)
    predictedvalue = float(predictedvalue)
    predictedvariance = float(predictedvariance)
    kalmangain = predictedvariance / (measuredvariance + predictedvariance)
    dif = (measuredvalue - predictedvalue)
    finalvalue = predictedvalue + kalmangain*(measuredvalue - predictedvalue)
    lunchsales[dish] = finalvalue


#graphing commonkeywords
hist_x = list(lunchsales.values())
saleshistogram = figure(width = 600, height = 400, background_fill_color = "grey", border_line_color = "black", outline_line_color = "black", y_range=(0, 3), x_range = (-max(list(lunchsales.values()))*0.2, max(list(lunchsales.values()))*1.1))
saleshistogram.title = "Projected Lunch Sales In May"
saleshistogram.title.text_font_size = "30px"
saleshistogram.title.align = "center"
saleshistogram.xaxis.axis_label = "Daily Sales (Dishes)"
saleshistogram.xaxis.axis_label_text_font_size = "20px"
print(list(lunchsales.keys()))
for i, dish in enumerate(list(lunchsales.keys())):
    hist_y = 2.5 - i
    barvalue = lunchsales[dish]
    if dish == "western":
        colorpick = "blue"
    elif dish == "asian":
        colorpick = "red"
    elif dish == "noodles":
        colorpick = "green"
    saleshistogram.hbar(hist_y, height=1,right=barvalue,line_color="white", fill_color=colorpick)
    saleshistogram.text(-0.5, hist_y, [dish], text_align="right", text_font_size="20px")
    saleshistogram.text(barvalue, hist_y, [int(barvalue)], text_align="left", text_font_size="20px")


show(saleshistogram)
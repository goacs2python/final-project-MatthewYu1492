[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=23611353&assignment_repo_type=AssignmentRepo)

#Project Description:#
This project analyzes data about my school's cafeteria lunch from various sources and integrates them visuals and graphs as part of a larger project in which I uses python to help identify improvements patterns within school lunch. This project outcome can be found here: https://bcisedu-my.sharepoint.com/:v:/g/personal/2025055091_bcis_cn/IQDFvlOcQP9tQ46yF_GlEA-BAYWQIB4c5TGMyj3NYQVAZu4?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=pWUdLl

#Overview of data files:#
*Catering Data.csv – lunch sales record provided by the catering deparment through Sep, 2025 to Mar, 2026. Organized by csv columns into: Month, Chinese combo sales, Chinese single sales, Western Combo sales, Western Single sales, School Days
*Recorded Sales.csv – lunch sales data physically collected by the catering deparment during one week in Apr, 2026. Organized by csv columns into: date, Chinese combo sales,Chinese single sales, Noodle Bar sales, Western combo sales, Western single sales
*Quick Questions_ School Lunch.csv – data from a survey inquiry conducted on fellow students about lunch satisfaction and suggestions. Organized by csv columns into: Id, Start time, Completion time, Email, Name, Question: What's your grade level?, How satisfied are you with the quality of school lunch? (10 is the highest), Question: Please explain your rating, Question: In your opinion what are some areas that the school should focus on when developing better dishes?, Question: Which corner do you go to the most to buy food?, Question: Is there anything else you would like to mention about school lunch (fav dish, least fav dish, etc.)?
*Sales Cal.csv – Records integrated sales data from Catering Data.csv & Recorded Sales.csv. Organized by csv columns into: dish, measurement value from Recorded Sales.csv, measurement variance from Recorded Sales.csv, prediction value from Catering Data.csv, prediction variance from Catering Data.csv

#Overview of python code files:#
*Catering Data.py – stores data from Catering Data.csv into montly classes and represents them in a bokeh line graph while also writing to Sales Cal.csv.
*Recorded Sales.py – stores data from Recorded Sales.csv into daily classes and represents them in a bokeh line graph while also writing to Sales Cal.csv.
*surveyanalysis.py – stores data from Quick Questions_ School Lunch.csv in dictionaries and lists and represents them in bokeh pie charts and boken histograms.
*Sales Calc.py – reads data from Sales Cal.csv and uses kalman filter to predict an accurate trend for lunch sales. repsresents the trend in a bokeh histogram.

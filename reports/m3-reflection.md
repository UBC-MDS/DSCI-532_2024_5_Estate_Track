# HomeScope Reflection

## Current State

In Milestone 3, we updated our dashboard based on the instructor's review and addressed feedback from our cohort. Our dashboard features an interactive map, two bar charts, a histogram, and several widgets. Compared with Milestone 2, we removed two scatter plots and substituted them with a bar chart that describes the top 5 bedroom or bathroom types in selected cities. A new drop-down menu has been added to enable viewers to select variables. We adjusted the interactive map's zoom level based on the province selection. We also revised the original bar plot, which compared two numerical variables among cities, by adding an additional y-axis and tooltips to deliver information more clearly. The price distribution density overlaid on a histogram visualizes the house prices in cities selected by the user and compares the price distribution using different colors. In terms of the dashboard layout, we improved the color and style of widgets and cards to ensure visual consistency. We broke app.py into smaller files, ensuring the code is clean and simple to understand.

## Different from Initial Sketch

The most significant deviation from our initial design was removing the scatter plots and replacing them with a bar chart. This change was made for efficiency and ease of comparison, such as when users wish to explore the popular types of bedrooms within cities. The addition of a histogram overlaid on the price distribution helps to identify and compare distribution patterns within cities easily. The addition of a sidebar separates the widgets and title from the main graph. All graphs share the same color theme to create a cohesive and visually appealing design. This engages viewers and draws attention to our significant findings.

## Inspired-by-another-groups-work
We learned how to set up the sidebar, focusing on the attributes, from UBC-MDS/DSCI-532_2024_16_SilentEpidemic on GitHub. Additionally, we discovered how to display links using CSS and explored various color styles.We were also inspired by them to learn how to integrate local widgets with plots inside a card.


## Conclusion, Limitation and Future Improvements

In conclusion, our dashboard mostly aligns with our initial sketch. We applied various tools and charts to maximize our dashboard's functionality and interactivity. We use a similar color theme to visually engage and capture our viewers' attention while they interact with our dashboard. The dashboard responds fluidly to changes in input values, such as province, cities, and other attributes. In the future, we hope to add more functions, such as extending the comparison between cities within a province to the entire country.

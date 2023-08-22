import pandas as pd
import plotly.express as px

class ProcessData:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = pd.read_csv(self.file_path, encoding="latin1")

    def get_total_revenue(self):
        try:
            revenue = self.df.Sales.sum().round(2)
            return f"${revenue/1000:.1f}k"
        except:
            return "Error"

    def get_total_profit(self):
        try:
            profit = self.df.Profit.sum().round(2)
            return f"${profit/1000:.1f}k"

        except:
            return "Error"

    def get_orders_count(self):
        try:
            order_count = self.df["Order ID"].nunique()
            return order_count
        except:
            return "Error"

    def average_price_per_item(self):
        pass

    def best_selling_product(self):
        # will change Product Name after confirmation
        var_name = 'Product Name'
        top10_selling_product = self.df.groupby([var_name]).agg({'Quantity': 'sum'}).reset_index().sort_values(
            by="Quantity", ascending=False).head(10)
        # which column product name or product id? one product id has different product name why?
        fig = px.bar(top10_selling_product, y=var_name, x='Quantity', barmode="group",
                     title="Top 10 Best selling Product(highest quantity sold)")
        fig.update_layout(yaxis={'categoryorder': 'total ascending'})
        return fig

# import csv
#
# # Read the CSV data into a list of dictionaries
# data = []
# with open("orders.csv", "r") as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#         data.append(row)
#
# # Get the most popular shipping mode
# most_popular_shipping_mode = max(data, key=lambda x: x["Ship Mode"])["Ship Mode"]
#
# # Get the most popular product category
# most_popular_product_category = max(data, key=lambda x: x["Category"])["Category"]
#
# # Get the most popular product sub-category
# most_popular_product_sub_category = max(data, key=lambda x: x["Sub-Category"])["Sub-Category"]
#
# # Get the most profitable product
# most_profitable_product = max(data, key=lambda x: x["Profit"])
#
# # Get the least profitable product
# least_profitable_product = min(data, key=lambda x: x["Profit"])
#
# # Get the most orders from each country
# most_orders_per_country = {}
# for row in data:
#     country = row["Country"]
#     if country not in most_orders_per_country:
#         most_orders_per_country[country] = 0
#     most_orders_per_country[country] += 1
#
# # Get the most orders from each region
# most_orders_per_region = {}
# for row in data:
#     region = row["Region"]
#     if region not in most_orders_per_region:
#         most_orders_per_region[region] = 0
#     most_orders_per_region[region] += 1
#
# # Print the results
# print("The most popular shipping mode is:", most_popular_shipping_mode)
# print("The most popular product category is:", most_popular_product_category)
# print("The most popular product sub-category is:", most_popular_product_sub_category)
# print("The most profitable product is:", most_profitable_product)
# print("The least profitable product is:", least_profitable_product)
# print("The most orders from each country are:")
# for country, orders in most_orders_per_country.items():
#     print(f"{country}: {orders}")
# print("The most orders from each region are:")
# for region, orders in most_orders_per_region.items():
#     print(f"{region}: {orders}")
#

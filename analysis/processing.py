import pandas as pd
import plotly.express as px
import plotly.colors as colors
import plotly.graph_objects as go


class ProcessData:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = pd.read_csv(self.file_path, encoding="latin1")

    def calculate_average_price_per_item(self):
        average_price_per_item = self.df['Sales'].mean().round(2)
        return average_price_per_item

    def get_total_revenue(self):
        try:
            revenue = self.df.Sales.sum().round(2)
            return f"${revenue / 1000:.1f}k"
        except:
            return "Error"

    def get_total_profit(self):
        try:
            profit = self.df.Profit.sum().round(2)
            return f"${profit / 1000:.1f}k"

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
                     )
        fig.update_layout(yaxis={'categoryorder': 'total ascending'})
        return fig

    def top_profitable_products(self):
        products_info = self.df.groupby("Product Name", as_index=False).agg(
            Profit=("Profit", "sum")
        )
        profitable = products_info[["Product Name", "Profit"]].sort_values(by=['Profit'],
                                                                           ascending=False).head(10)
        fig = px.bar(profitable, y='Product Name', x='Profit', barmode="group",
                     )
        fig.update_layout(yaxis={'categoryorder': 'total ascending'})
        return fig

    def sales_profit_timeline(self):
        df_line = self.df[['Order Date', 'Sales', 'Profit']].sort_values('Order Date')  # Chronological Ordering
        df_line['Order Date'] = pd.to_datetime(df_line['Order Date'])  # Converting into DateTime
        df_line = df_line.groupby('Order Date',
                                  as_index=False).mean()  # Group by to get the average Sales and Profit on each day
        fig = px.line(df_line, x='Order Date', y='Sales')
        fig.add_scatter(x=df_line['Order Date'], y=df_line['Profit'], mode='lines', showlegend=False)
        return fig

    def sales_profit_by_customer_segment(self):
        sales_profit_by_segment = self.df.groupby('Segment', as_index=False).agg({'Sales': 'sum', 'Profit': 'sum'})
        color_palette = colors.qualitative.Pastel
        fig = go.Figure()
        fig.add_trace(go.Bar(x=sales_profit_by_segment['Segment'],
                             y=sales_profit_by_segment['Sales'],
                             name='Sales',
                             marker_color=color_palette[1]))
        fig.add_trace(go.Bar(x=sales_profit_by_segment['Segment'],
                             y=sales_profit_by_segment['Profit'],
                             name='Profit',
                             marker_color=color_palette[0]))

        fig.update_layout(xaxis_title='Customer Segment', yaxis_title='Amount')

        return fig

    def top_profitable_cites(self):
        cities_info = self.df.groupby("City", as_index=False).agg(
            sales=("Sales", "sum"),
            profit=("Profit", "sum")
        )
        top_profit = cities_info[['City', 'profit']].sort_values(by=["profit"], ascending=False).head(10)
        fig = px.funnel(top_profit, x='profit', y='City', title='Top-10 Profitable Cities')
        return fig

    def sales_category_wise(self):
        category = self.df.groupby(["Category", "Sub-Category"], as_index=False).agg({"Sales":"sum"})
        fig = px.sunburst(category, path=['Category', 'Sub-Category'], values='Sales')
        return fig

    def get_insights(self):
        insights1 = f"The most popular shipping mode is {self.df['Ship Mode'].value_counts().index[0]}, followed by " \
        f"{self.df['Ship Mode'].value_counts().index[1]}"
        insights2 = f"The most popular product category is {self.df['Category'].value_counts().index[0]}," \
                    f" followed by {self.df['Category'].value_counts().index[1]}."
        self.df["max_profit"] = self.df["Sales"] - self.df["Profit"] / self.df["Quantity"]
        self.df[["Product Name", "max_profit"]].sort_values(by="max_profit", ascending=False)
        return {"insights1":insights1, "insights2":insights2}
        """
        The most popular product category is Furniture, followed by Office Supplies and Technology.
        The most popular product sub-category is Tables, followed by Bookcases and Chairs.
        The most profitable product is the Bush Somerset Collection Bookcase, with a profit of $41.91.
        The least profitable product is the Holmes Replacement Filter for HEPA Air Cleaner, with a loss of $123.86.
        The most orders were placed by consumers in the United States, followed by corporate customers in the United States.
        """
        # most_popular_product_category = max(data, key=lambda x: x["Category"])["Category"]


def validate_csv(file_path):
    df = pd.read_csv(file_path, encoding="latin1")
    cols = set(df.columns.tolist())
    predefined_cols = {'Category', 'City', 'Country', 'Customer ID', 'Customer Name', 'Discount', 'Order Date',
                       'Order ID', 'Postal Code', 'Product ID', 'Product Name', 'Profit', 'Quantity', 'Region',
                       'Row ID', 'Sales', 'Segment', 'Ship Date', 'Ship Mode', 'State', 'Sub-Category'}
    return cols == predefined_cols

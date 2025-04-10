import pandas as pd

class FeatureEngineer:
    def __init__(self, df):
        self.df = df.copy()
        self.basic_cleaning()
        self.process_date_features()
        self.process_product_features()
        self.process_customer_features()
        self.handle_missing_values()
        

    def basic_cleaning(self):
        self.df = self.df[self.df["quantity"] > 0]
        self.df = self.df[self.df["unit_price"] > 0]
        self.df = self.df[self.df["discount"].between(0, 1)]
        print("Non-meaningful data has been cleaned.")

    def process_date_features(self):
        self.df['order_date'] = pd.to_datetime(self.df['order_date'])
        self.df['year'] = self.df['order_date'].dt.year
        self.df['month'] = self.df['order_date'].dt.month
        self.df['year_month'] = self.df['order_date'].dt.to_period('M')
        self.df['season'] = self.df['month'] % 12 // 3 + 1
        self.df['season'] = self.df['season'].map({1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Fall'})
        print("Date features have been added.")

    def process_product_features(self):
        self.df['discounted_unit_price'] = self.df['unit_price'] * (1 - self.df['discount'])
        self.df['total_quantity'] = self.df['quantity']
        print("Product features have been added.")

    def process_customer_features(self):
        self.df["total_sales"] = self.df["unit_price"] * self.df["quantity"] * (1 - self.df["discount"])
        customer_total_spending = self.df.groupby("customer_id")["total_sales"].sum()
        self.df["customer_segment"] = self.df["customer_id"].map(
            pd.cut(
                customer_total_spending,
                bins=[0, 1000, 5000, customer_total_spending.max()],
                labels=["Low Value", "Medium Value", "High Value"]
            )
        )
        # self.df["customer_segment"].to_csv("customer_segment.csv")
        print("Customer segmentation completed based on total spending.")

    def handle_missing_values(self):
        # which values is null = self.df.isnull().sum()

        missing_before = self.df.isnull().sum().sum()
        if missing_before:
            self.df.dropna(inplace=True)
            missing_after = self.df.isnull().sum().sum()
            print(f"Cleaning completed. Missing data before: {missing_before}, after: {missing_after}")
        else:
            print("No missing data found.")

    def get_dataframe(self):
        return self.df
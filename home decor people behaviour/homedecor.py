import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
data_path = r"C:\internshhip\home decor people behaviour\ecommerce_furniture_dataset_2024.csv"
df = pd.read_csv(data_path)

print("Columns in dataset:", df.columns)

df.columns = df.columns.str.strip()

df['Price'] = df['price'].replace('[\$,]', '', regex=True).astype(float)

possible_category_columns = ['Category', 'Product Category', 'Type']
category_column = next((col for col in possible_category_columns if col in df.columns), None)

if category_column:
    category_price = df.groupby(category_column)['Price'].mean().sort_values(ascending=False)
    print("Average Price per Category:\n", category_price)
else:
    print("Warning: No category column found!")

if 'Order Date' in df.columns:
    df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
    df['Month'] = df['Order Date'].dt.to_period('M')
    monthly_sales = df.groupby('Month')['Sales'].sum()
else:
    print("Warning: 'Order Date' column missing!")

popular_products = df['productTitle'].value_counts().head(10)
print("Most Popular Products:\n", popular_products)

plt.figure(figsize=(10, 5))
sns.barplot(x=popular_products.index, y=popular_products.values, palette='Blues')
plt.xticks(rotation=45)
plt.title('Top 10 Popular Products')
plt.xlabel('Product')
plt.ylabel('Count')
plt.show()

if category_column:
    plt.figure(figsize=(10, 5))
    sns.barplot(x=category_price.index, y=category_price.values, palette='Reds')
    plt.xticks(rotation=45)
    plt.title('Average Price per Category')
    plt.xlabel('Category')
    plt.ylabel('Average Price')
    plt.show()

if 'Order Date' in df.columns:
    plt.figure(figsize=(10, 5))
    monthly_sales.plot(kind='line', marker='o', color='green')
    plt.title('Monthly Sales Trend')
    plt.xlabel('Month')
    plt.ylabel('Total Sales')
    plt.grid()
    plt.show()

print("Key Recommendations:")
print("1. Focus marketing efforts on best-selling products.")
if category_column:
    print("2. Optimize pricing for high-value categories.")
if 'Order Date' in df.columns:
    print("3. Identify peak sales periods for better inventory management.")

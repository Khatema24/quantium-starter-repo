import os
import pandas as pd
from dash import Dash, dcc, html
import plotly.express as px

# پیدا کردن مسیرهای احتمالی فایل پر شده
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

path1 = os.path.join(current_dir, "formatted_output.csv")
path2 = os.path.join(parent_dir, "formatted_output.csv")

# انتخاب فایلی که واقعاً پر از داده است
if os.path.exists(path2) and os.path.getsize(path2) > 50:
    csv_path = path2
else:
    csv_path = path1

# ۱. بارگذاری داده‌ها
df = pd.read_csv(csv_path)

# تصحیح نام ستون‌ها
df.columns = df.columns.str.strip().str.lower()

# تبدیل تاریخ و مرتب‌سازی
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values(by="date")

# ۲. ساخت اپلیکیشن داشبورد
app = Dash(__name__)

# ۳. ایجاد نمودار خطی میزان فروش
fig = px.line(
    df, 
    x="date", 
    y="sales", 
    title="Pink Morsel Sales Analysis",
    labels={"date": "Date", "sales": "Total Sales ($)"}
)

# تغییر رنگ خط نمودار به صورتی قشنگ
fig.update_traces(line_color="#FF69B4")

# ۴. طراحی ظاهر صفحه
app.layout = html.Div(children=[
    html.H1(
        children="Quantium Sales Visualiser",
        style={"textAlign": "center", "fontFamily": "Arial", "padding": "20px", "color": "#2c3e50"}
    ),
    
    html.P(
        children="Visualising the sales data to analyze the impact of the Pink Morsel price increase on 15th January 2021.",
        style={"textAlign": "center", "fontFamily": "Arial", "color": "#7f8c8d"}
    ),

    dcc.Graph(
        id="sales-chart",
        figure=fig
    )
])

# ۵. اجرای برنامه
if __name__ == "__main__":
    app.run(debug=True)
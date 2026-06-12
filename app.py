import os
import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# ۱. پیدا کردن مسیر فایل داده‌ها
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

path1 = os.path.join(current_dir, "formatted_output.csv")
path2 = os.path.join(parent_dir, "formatted_output.csv")

if os.path.exists(path2) and os.path.getsize(path2) > 50:
    csv_path = path2
else:
    csv_path = path1

# ۲. بارگذاری و آماده‌سازی داده‌ها
df = pd.read_csv(csv_path)
df.columns = df.columns.str.strip().str.lower()
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values(by="date")

# ۳. ساخت اپلیکیشن داشبورد با استایل‌های زیبای CSS
app = Dash(__name__)

app.layout = html.Div(
    style={
        "fontFamily": "Segoe UI, Tahoma, Geneva, Verdana, sans-serif",
        "backgroundColor": "#f8f9fa",
        "padding": "30px",
        "minHeight": "100vh"
    },
    children=[
        # هدر وب‌سایت
        html.Div(
            style={
                "backgroundColor": "#ffffff",
                "padding": "20px",
                "borderRadius": "10px",
                "boxShadow": "0 4px 6px rgba(0,0,0,0.05)",
                "textAlign": "center",
                "marginBottom": "25px"
            },
            children=[
                html.H1(
                    children="Quantium Sales Visualiser",
                    style={"color": "#2c3e50", "margin": "0 0 10px 0", "fontWeight": "600"}
                ),
                html.P(
                    children="Visualising the sales data to analyze the impact of the Pink Morsel price increase on 15th January 2021.",
                    style={"color": "#7f8c8d", "margin": "0", "fontSize": "15px"}
                )
            ]
        ),
        
        # بخش کنترل و دکمه‌های رادیویی
        html.Div(
            style={
                "backgroundColor": "#ffffff",
                "padding": "20px",
                "borderRadius": "10px",
                "boxShadow": "0 4px 6px rgba(0,0,0,0.05)",
                "marginBottom": "25px",
                "textAlign": "center"
            },
            children=[
                html.Label(
                    "Filter by Region:",
                    style={"fontWeight": "bold", "color": "#34495e", "display": "block", "marginBottom": "10px"}
                ),
                dcc.RadioItems(
                    id="region-filter",
                    options=[
                        {"label": " All Regions ", "value": "all"},
                        {"label": " North ", "value": "north"},
                        {"label": " East ", "value": "east"},
                        {"label": " South ", "value": "south"},
                        {"label": " West ", "value": "west"}
                    ],
                    value="all", # گزینه پیش‌فرض
                    inline=True,
                    style={"fontSize": "16px", "color": "#2c3e50"},
                    inputStyle={"marginRight": "5px", "marginLeft": "15px"}
                )
            ]
        ),

        # بخش نمودار
        html.Div(
            style={
                "backgroundColor": "#ffffff",
                "padding": "20px",
                "borderRadius": "10px",
                "boxShadow": "0 4px 6px rgba(0,0,0,0.05)"
            },
            children=[
                dcc.Graph(id="sales-chart")
            ]
        )
    ]
)

# ۴. بخش هوشمند برنامه‌نویسی (Callback) برای فیلتر کردن زنده نمودار
@app.callback(
    Output("sales-chart", "figure"),
    Input("region-filter", "value")
)
def update_graph(selected_region):
    # فیلتر کردن داده‌ها بر اساس دکمه انتخاب شده
    if selected_region == "all":
        filtered_df = df
        title_text = "Pink Morsel Sales Analysis - All Regions"
    else:
        filtered_df = df[df["region"] == selected_region]
        title_text = f"Pink Morsel Sales Analysis - {selected_region.capitalize()} Region"
    
    # ساخت مجدد نمودار با داده‌های فیلتر شده
    fig = px.line(
        filtered_df, 
        x="date", 
        y="sales", 
        title=title_text,
        labels={"date": "Date", "sales": "Total Sales ($)"}
    )
    
    # استایل دادن به خط نمودار و پس‌زمینه آن
    fig.update_traces(line_color="#FF69B4", line_width=2)
    fig.update_layout(
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        margin={"t": 50, "b": 40, "l": 60, "r": 40},
        hovermode="x unified"
    )
    return fig

# ۵. اجرای برنامه
if __name__ == "__main__":
    app.run(debug=True)
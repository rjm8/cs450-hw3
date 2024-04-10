import dash
from dash import dcc, html, Input,Output,State
import seaborn as sns
import plotly.express as px
from dash.exceptions import PreventUpdate
import pandas as pd

df = pd.read_csv("ProcessedTweets.csv")

dropdown = html.Div(className="dropdown", children=[
    "Month    ",
    dcc.Dropdown(id="dropdown", className="drop", options=df["Month"].unique(), value=df["Month"].unique()[0])
])


min_sent = int(df["Sentiment"].min().item())
max_sent = int(df["Sentiment"].max().item())
sentimentslider = html.Div(className="sentimentslider", children=[
    "Sentiment ",
    dcc.RangeSlider(id="sentimentslider", className="sentlide", min=min_sent, max=max_sent, marks={min_sent:str(min_sent), max_sent:str(max_sent)}, value=[min_sent, max_sent])
])

min_subj = int(df["Subjectivity"].min().item())
max_subj = int(df["Subjectivity"].max().item())
subjectivityslider = html.Div(className="subjectivityslider", children=[
    "Subjectivity ",
    dcc.RangeSlider(id="subjectivityslider", className="subslide", min=min_subj, max=max_subj, step=.01, marks={min_subj:str(min_subj), max_subj:str(max_subj)}, value=[min_subj,max_subj])
])

rawtweets = html.Div(className="rawtweetscontainer", children=[
    html.Div(className="rawtweetheader", children="RawTweet"),
    html.Div(id="rawtweets", className="rawtweets", children=[])
])


app = dash.Dash(__name__)
server = app.server
app.layout = html.Div(className="parent_container", children=[
    html.Div(className="row1", children=[
        dropdown,
        sentimentslider,
        subjectivityslider
    ]),
    html.Div(className="row2", children=dcc.Graph(id="graph")),
    html.Div(className="row3", children=rawtweets)
])

@app.callback(
    Output("graph", "figure"),
    [
        Input("dropdown", "value"),
        Input("sentimentslider", "value"),
        Input("subjectivityslider", "value")
    ]
)
def updateGraph(month, sentiment, subjectivity):
    filtered_df = df[df["Month"] == month]
    filtered_df = filtered_df[filtered_df["Sentiment"] >= sentiment[0]]
    filtered_df = filtered_df[filtered_df["Sentiment"] <= sentiment[1]]
    filtered_df = filtered_df[filtered_df["Subjectivity"] >= subjectivity[0]]
    filtered_df = filtered_df[filtered_df["Subjectivity"] <= subjectivity[1]]
    figure = px.scatter(filtered_df, "Dimension 1", "Dimension 2", labels={"Dimension 1":"", "Dimension 2":""}, custom_data=[filtered_df.RawTweet])
    figure.update_layout(dragmode="lasso")
    figure.update_layout(xaxis=dict(tickmode="array", tickvals=[], ticktext=[]))
    figure.update_layout(yaxis=dict(tickmode="array", tickvals=[], ticktext=[]))
    
    return figure

@app.callback(
    Output("rawtweets", "children"),
    Input("graph", "selectedData")
)
def updateTweets(selected):
    rawtweetlist = []
    if selected != None:
        for point in selected["points"]:
            raw = point["customdata"]
            while type(raw) is list:
                raw = raw[0]
            rawtweetlist.append(html.Div(className="rawtweet", children=raw))
    return rawtweetlist

if __name__ == "__main__":
    app.run_server(debug=True)
import plotly.express as px
import pandas as pd


with px.colors.qualitative as s:
     c = [s.T10[1], s.T10[3], s.T10[6], s.Safe[0]]

def get_line_chart(df, x, y, data_marks_type="markers+lines+text", xrange=[70, 90]):
    if data_marks_type == "markers+lines+text":
        fig = px.line(df,
              x=x,
              y=y,
              title='',
              height=300,
              text=y,
              color=c)
    else: fig = px.line(df,
              x=x,
              y=y,
              title='',
              height=300,
              color=c)
    fig.update_yaxes(visible=True, showticklabels=True, title='', range=xrange, showgrid=True, gridwidth=1, gridcolor='rgb(244, 244, 244)')
    fig.update_xaxes(type='category', fixedrange=False,
                 showspikes=True, showticklabels=True, title='', showgrid=True, gridwidth=1, gridcolor='rgb(244, 244, 244)')

    fig.update_traces(
    mode=data_marks_type, 
    hovertemplate=None,
    textposition='top center',
)
    fig.layout.plot_bgcolor = 'white'
    fig.layout.paper_bgcolor = 'white'

    fig.update_layout(
    hovermode="x unified", 
    hoverlabel=dict(
        namelength=-1,
        bordercolor="White"), 
    margin=dict(l=10, r=10, t=20, b=0),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="left",
        x=0,
    title='',
    title_font_family="Verdana",
    font=dict(
        family="Sans-serif",
        size=12,
        color="black"
        ),
    bordercolor="Black",
    bgcolor=None,
)
)

    fig.update(layout_showlegend=True)

    return fig


def get_bar_chart(df, x, y):
    fig = px.bar(df,
             x=x,
             y=y,
             title='',
             labels=None,
             color_discrete_sequence=[
                 px.colors.qualitative.Vivid[2], px.colors.qualitative.Vivid[7]],
             height=300, 
             text_auto=True,
             color=c)

    fig.update_yaxes(visible=True, showticklabels=True,
                 title='', range=[0, 250000])
    fig.update_xaxes(type='category', fixedrange=False,
                    showspikes=True, showticklabels=True, title='', showgrid=True, gridwidth=1, gridcolor='rgb(238, 238, 238)')
    fig.layout.plot_bgcolor = 'white'
    fig.layout.paper_bgcolor = 'white'
    fig.update_layout(
        hovermode=None,
        hoverlabel=dict(
            namelength=-1,
            bordercolor="White"),
        margin=dict(l=0, r=20, t=20, b=0),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
            title='',
            title_font_family="Verdana",
            font=dict(
                family="Sans-serif",
                size=12,
                color="black"
            ),
            bordercolor="Black",
            borderwidth=None
        )
    )

    return fig


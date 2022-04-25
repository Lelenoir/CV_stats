import altair as alt
import pandas as pd


def get_chart(data):
    hover = alt.selection_single(
        fields=["dt_create"],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    xticks = data.dt_create.unique().tolist()

    lines = (
        alt.Chart(data, title="Динамика количества удаленных фото")
        .mark_line()
        .encode(
            x=alt.X(
                "dt_create", title="Дата", axis=alt.Axis(values=xticks, labelAngle=0, labelFlushOffset=2000)
            ),
            y=alt.X("count_photos", title="Количество фото", scale=alt.Scale(domain=[1000, 1700]),),
        )
    )

    # Draw points on the line, and highlight based on selection
    points = lines.transform_filter(hover).mark_circle(size=65)

    # Draw a rule at the location of the selection
    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            x=alt.X("dt_create", axis=alt.Axis(values=xticks, labelAngle=0)),
            y=alt.X("count_photos", title="Количество фото"),
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("dt_create", title="Дата"),
                alt.Tooltip("count_photos", title="Количество фото"),
            ],
        )
        .add_selection(hover)
    )

    return (lines + points + tooltips).interactive()



def get_line_chart(data, axisX, axisY, titles, chart_name):
    hover = alt.selection_single(
        fields=[axisX],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    xticks = data[axisX].unique().tolist()

    lines = (
        alt.Chart(data, title=chart_name)
        .mark_line()
        .encode(
            x=alt.X(
                axisX, title=titles[0], axis=alt.Axis(values=xticks, labelAngle=0)
            ),
            y=alt.X(axisY, title=titles[1]),
        )
    )

    # Draw points on the line, and highlight based on selection
    points = lines.transform_filter(hover).mark_circle(size=65)

    # Draw a rule at the location of the selection
    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            x=alt.X(axisX, axis=alt.Axis(values=xticks, labelAngle=0)),
            y=axisY,
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip(axisX, title=titles[0]),
                alt.Tooltip(axisY, title=titles[1]),
            ],
        )
        .add_selection(hover)
    )

    return (lines + points + tooltips).interactive()

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
            y=alt.X("count_photos", title="Количество фото",
                    scale=alt.Scale(domain=[1000, 1700]),),
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
            y=alt.X("count_photos", title="Количество фото",
                    scale=alt.Scale(domain=[1000, 1700])),
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
                axisX, title=titles[0], axis=alt.Axis(
                    values=xticks, labelAngle=0)
            ),
            y=alt.X(axisY, title=titles[1],
                    scale=alt.Scale(domain=[1000, 1700])),
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
            y=alt.X(axisY, scale=alt.Scale(domain=[1000, 1700])),
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip(axisX, title=titles[0]),
                alt.Tooltip(axisY, title=titles[1]),
            ],
        )
        .add_selection(hover)
    )

    return (lines + points + tooltips).interactive()


def get_counts_sku(data, axisX, axisY, titles, chart_name):
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
                axisX, title=titles[0], axis=alt.Axis(
                    values=xticks, labelAngle=0)
            ),
            y=alt.Y(alt.repeat("layer"), title=titles[0], scale=alt.Scale(
                reverse=True, round=True)),
            color=alt.datum(alt.repeat("layer")),).repeat(layer=axisY)
    )

    base = lines.transform_filter(hover)

    base = alt.layer(
        lines.add_selection(hover),
        base.mark_circle(size=65),
        base.mark_circle(size=65),
        base.mark_circle(size=65),
        data=data
    )

    # Draw points on the line, and highlight based on selection
    # points1 = lines[0].transform_filter(hover).mark_circle(size=65)
    # points2 = lines[1].transform_filter(hover).mark_circle(size=65)
    # points3 = lines[2].transform_filter(hover).mark_circle(size=65)

    # Draw a rule at the location of the selection
    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            x=alt.X(axisX, axis=alt.Axis(values=xticks, labelAngle=0)),
            y=alt.Y(alt.repeat("layer"), title=titles[0], scale=alt.Scale(
                reverse=True, round=True)),
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip(axisX, title=titles[0]),
                # alt.Tooltip(axisY, title=titles[1]),
            ],
        )
        .add_selection(hover)
    )

    return (lines + base + tooltips).interactive()

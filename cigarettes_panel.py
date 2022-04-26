from collections import namedtuple
from datetime import datetime
from datetime import timedelta

import altair as alt
import math
import pandas as pd
import streamlit as st

import matplotlib.pyplot as plt
import plotly.express as px

import os
import numpy as np

from utils import chart

from PIL import Image


im = Image.open("./img/logo-bristol.png")
st.set_page_config(page_title="БРИСТОЛЬ - Сигареты",
                   layout="wide", page_icon=im)


def space(num_lines=1):
    """Adds empty lines to the Streamlit app."""
    for _ in range(num_lines):
        st.write("")


@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode("utf-8")


# Подготовка данных

df = pd.DataFrame()

for i in sorted(os.listdir("./files/")):
    df = df.append(pd.read_csv(f"./files/{i}"), ignore_index=True)

df["date"] = pd.to_datetime(df["dt_create"], format="%Y-%m-%d")
df["dt_create"] = df["date"].apply(lambda x: x.strftime("%m-%d"))
df["count_mons"] = df["count_mon_full_rec"].copy()


not_in_monita = df[df["not_in_monita"] == True].copy()
pivot_deleted = pd.pivot_table(
    not_in_monita,
    index="dt_create",
    values=["count_cv_full_rec", "count_cv_any_rec"],
    aggfunc={"count_cv_full_rec": np.mean, "count_cv_any_rec": np.mean},
    fill_value=0,
)

in_monita = df[df["not_in_monita"] == False].copy()
in_monita["recognition"] = (
    (in_monita["count_mons"] - in_monita["is_manual"])
    / in_monita["count_mons"]
    * 100
)
pivot_not_deleted = in_monita.pivot_table(
    index="dt_create",
    values=[
        "url",
        "count_mons",
        "empty_cv",
        "is_manual",
        "count_mon_full_rec",
        "count_cv_full_rec",
        "count_cv_any_rec",
    ],
    aggfunc={
        "url": "count",
        "count_mons": np.sum,
        "is_manual": np.sum,
        "count_mon_full_rec": np.mean,
        "count_cv_full_rec": np.mean,
        "count_cv_any_rec": np.mean,
        "empty_cv": np.sum,
    },
).round(2)

pivot_days = (
    in_monita.pivot_table(
        index="dt_create",
        values=[
            "url",
            "count_mons",
            "empty_cv",
            "is_manual",
            "count_mon_full_rec",
            "count_cv_full_rec",
            "count_full_intersection",
        ],
        aggfunc={
            "url": pd.Series.nunique,
            "count_mons": np.sum,
            "is_manual": np.sum,
            "count_mon_full_rec": np.mean,
            "count_cv_full_rec": np.mean,
            "count_full_intersection": np.mean,
            "empty_cv": np.sum,
        },
        fill_value=0,
    )
    .reset_index()
    .sort_values(by="count_mons", ascending=False)
).reset_index(drop=True)

pivot_days["recognition"] = (
    (pivot_days["count_mons"] - pivot_days["is_manual"])
    / pivot_days["count_mons"]
    * 100
)
pivot_days.index += 1


st.title("Аналитика сигарет за март-апрель")


space(1)


st.header("Общая статистика")


st.dataframe(
    pivot_days.style.format(
        {
            "count_mon_full_rec": "{:.2f}",
            "count_cv_full_rec": "{:.2f}",
            "count_full_intersection": "{:.2f}",
            "recognition": "{:.2f}",
        }
    )
)


dates = df.dt_create.unique().tolist()

col_count_by_url, col_count_mons = st.columns([1,1])
fig = px.line(pivot_days.sort_values(by='dt_create'),
             x=pivot_days.dt_create.unique().tolist(), 
             y=['count_cv_full_rec', "count_mon_full_rec", 'count_full_intersection'], 
             title='',
             width=800, height=400)
fig.update_xaxes(type='category', fixedrange=False, showspikes=True)
fig.update_traces(mode="markers+lines", hovertemplate=None)
fig.update_layout(hovermode="x unified")
col_count_by_url.plotly_chart(fig, use_container_width=True)


# DATE REF ELEMENTS

choise_date = sorted(dates)[-1]

col_slider, col_empty = st.columns([1, 3])

choise_date = col_slider.slider(
    "Выбор даты",
    value=datetime.strptime("2022-" + sorted(dates)[-1], "%Y-%m-%d"),
    min_value=datetime.strptime("2022-" + sorted(dates)[1], "%Y-%m-%d"),
    max_value=datetime.strptime("2022-" + sorted(dates)[-1], "%Y-%m-%d"),
    format="MM-DD",
    step=timedelta(days=7), 
    key='my_slider'
)

col_empty.write("")

pivot_sn_day = (
    in_monita[in_monita.dt_create == choise_date.strftime("%m-%d")]
    .pivot_table(
        index="shop_network_name",
        values=[
            "url",
            "count_mons",
            "empty_cv",
            "is_manual",
            "count_mon_full_rec",
            "count_cv_full_rec",
            "count_cv_any_rec",
            "count_full_intersection",
        ],
        aggfunc={
            "url": pd.Series.nunique,
            "count_mons": np.sum,
            "is_manual": np.sum,
            "count_mon_full_rec": np.mean,
            "count_cv_full_rec": np.mean,
            "count_cv_any_rec": np.mean,
            "count_full_intersection": np.mean,
            "empty_cv": np.sum,
        },
        fill_value=0,
    )
    .reset_index()
    .sort_values(by="count_mons", ascending=False)
).reset_index(drop=True)

pivot_sn_day["recognition"] = (
    (pivot_sn_day["count_mons"] - pivot_sn_day["is_manual"])
    / pivot_sn_day["count_mons"]
    * 100
)
pivot_sn_day = pivot_sn_day[
    [
        "shop_network_name",
        "url",
        "count_mons",
        "recognition",
        "count_cv_full_rec",
        "count_mon_full_rec",
        "count_full_intersection",
        "empty_cv",
    ]
]
pivot_sn_day["recognition"] = pivot_sn_day["recognition"].round(decimals=2)
pivot_sn_day["count_cv_full_rec"] = pivot_sn_day["count_cv_full_rec"].round(
    decimals=2)
pivot_sn_day["count_mon_full_rec"] = pivot_sn_day["count_mon_full_rec"].round(
    decimals=2
)
pivot_sn_day["count_full_intersection"] = pivot_sn_day["count_full_intersection"].round(
    decimals=2
)
pivot_sn_day.index += 1


# INTERFACE


choise_date_subheader = choise_date.strftime("%m-%d")


st.header(f"Статистика за {choise_date_subheader}")


space(1)


st.subheader("Анализ мониторингов")


space(1)


diff_count_mons = round(
    (
        in_monita[in_monita.dt_create ==
                  choise_date.strftime("%m-%d")].shape[0]
        - in_monita[
            in_monita.dt_create == (
                choise_date - timedelta(days=7)).strftime("%m-%d")
        ].shape[0]
    )
    / in_monita[
        in_monita.dt_create == (
            choise_date - timedelta(days=7)).strftime("%m-%d")
    ].shape[0]
    * 100,
    2,
)
diff_count_photo = round(
    (
        in_monita[in_monita.dt_create ==
                  choise_date.strftime("%m-%d")]["url"].nunique()
        - in_monita[
            in_monita.dt_create == (
                choise_date - timedelta(days=7)).strftime("%m-%d")
        ]["url"].nunique()
    )
    / in_monita[
        in_monita.dt_create == (
            choise_date - timedelta(days=7)).strftime("%m-%d")
    ]["url"].nunique()
    * 100,
    2,
)
diff_recognition = round(
    (
        (
            in_monita[
                in_monita.dt_create == choise_date.strftime("%m-%d")
            ].count_mon_full_rec.sum()
            - in_monita[
                in_monita.dt_create == choise_date.strftime("%m-%d")
            ].is_manual.sum()
        )
        / in_monita[
            in_monita.dt_create == choise_date.strftime("%m-%d")
        ].count_mon_full_rec.sum()
        - (
            in_monita[
                in_monita.dt_create
                == (choise_date - timedelta(days=7)).strftime("%m-%d")
            ].count_mon_full_rec.sum()
            - in_monita[
                in_monita.dt_create
                == (choise_date - timedelta(days=7)).strftime("%m-%d")
            ].is_manual.sum()
        )
        / in_monita[
            in_monita.dt_create == (
                choise_date - timedelta(days=7)).strftime("%m-%d")
        ].count_mon_full_rec.sum()
    )
    * 100,
    2,
)

col1, col2, col3 = st.columns([1, 1, 1])
col1.metric(
    f"Количество мониторингов",
    in_monita[
        in_monita.dt_create == choise_date.strftime("%m-%d")
    ].count_mon_full_rec.sum(),
    f"{diff_count_mons}%",
)
col2.metric(
    f"Количество фото",
    in_monita[in_monita.dt_create ==
              choise_date.strftime("%m-%d")].url.nunique(),
    f"{diff_count_photo}%",
)
col3.metric(
    f"Распознавание, %",
    round(
        (
            in_monita[
                in_monita.dt_create == choise_date.strftime("%m-%d")
            ].count_mon_full_rec.sum()
            - in_monita[
                in_monita.dt_create == choise_date.strftime("%m-%d")
            ].is_manual.sum()
        )
        / in_monita[
            in_monita.dt_create == choise_date.strftime("%m-%d")
        ].count_mon_full_rec.sum()
        * 100,
        2,
    ),
    f"{diff_recognition}%",
)


space(2)

col_top_sn, col_download_sn = st.columns([2, 3])

top_sn = col_top_sn.number_input(
    "Топ конкурентов по количеству мониторингов", value=5, min_value=1, max_value=10
)
top_sn = int(top_sn)

csv = convert_df(pivot_sn_day)

col_download_sn.write("")
col_download_sn.write("")
col_download_sn.download_button(
    label="Скачать исходные данные по конкурентам формате CSV",
    data=csv,
    file_name=f'pivot_shop_networks {choise_date.strftime("%m-%d")}.csv',
    mime="text/csv",
)

st.write(
    f"\nМониторинги по этим конкурентам покрывают {round(pivot_sn_day.head(top_sn).count_mons.sum()/pivot_sn_day.count_mons.sum()*100)}% от общего количества"
)


col_pivot_sn, col_empty = st.columns([3, 1])

col_pivot_sn.dataframe(
    pivot_sn_day.head(top_sn).style.format(
        {
            "count_mon_full_rec": "{:.2f}",
            "count_cv_full_rec": "{:.2f}",
            "count_full_intersection": "{:.2f}",
            "recognition": "{:.2f}",
        }
    )
)

col_empty.write("")


space(1)

col_multi, col_em = st.columns([2, 3])

selected_sn = col_multi.selectbox(
    "Выберите конкурента",
    options=pivot_sn_day.shop_network_name.unique().tolist(),
    index=0,
    key='my_selectbox'
)


col_em.write("")
col_em.write("")
col_em.write(
    f"{selected_sn} покрывает {round(pivot_sn_day[pivot_sn_day.shop_network_name == selected_sn].count_mons.sum()/pivot_sn_day.count_mons.sum()*100)}% мониторингов от общего количества"
)

col_one_sn, col_share = st.columns([3, 1])

col_one_sn.table(
    pivot_sn_day[pivot_sn_day.shop_network_name == selected_sn]
    .reset_index(drop=True)
    .style.format(
        {
            "count_mon_full_rec": "{:.2f}",
            "count_cv_full_rec": "{:.2f}",
            "count_full_intersection": "{:.2f}",
            "recognition": "{:.2f}",
        }
    )
)

col_share.write("")


in_monita = in_monita.fillna(0)
in_monita['count_mon_full_rec'] = in_monita['count_mon_full_rec'].astype('int64')
in_monita['count_cv_full_rec'] = in_monita['count_cv_full_rec'].astype('int64')
in_monita['count_full_intersection'] = in_monita['count_full_intersection'].astype('int64')
in_monita['recognition'] = in_monita['recognition'].astype('int64')


a = alt.Chart(in_monita[(in_monita.shop_network_name == selected_sn) & (in_monita.dt_create == choise_date.strftime("%m-%d"))]).mark_circle().encode(
    #  x='count_cv_full_rec', y='count_mon_full_rec', size='recognition', color='recognition', tooltip=['count_cv_full_rec', 'count_mon_full_rec', 'recognition'])
     x='count_cv_full_rec', y='count_mon_full_rec', tooltip=['count_cv_full_rec', 'count_mon_full_rec'])

c = alt.Chart(in_monita[(in_monita.shop_network_name == selected_sn) & (in_monita.dt_create == choise_date.strftime("%m-%d"))]).mark_circle().encode(
    #  x='count_cv_full_rec', y='count_mon_full_rec', size='recognition', color='recognition', tooltip=['count_cv_full_rec', 'count_mon_full_rec', 'recognition'])
     x='count_full_intersection', y='count_mon_full_rec', tooltip=['count_full_intersection', 'count_mon_full_rec'])


coll, coll2, coll3 = st.columns([1,1,1])
coll.altair_chart(a, use_container_width=True)
coll2.write("")
coll3.altair_chart(c, use_container_width=True)

form = st.form(key="Filtration by shop_network")

# with form:


space(2)


st.subheader("Анализ удаленных фотографий")


space(1)


not_monita_diff_count_photo = round(
    (
        not_in_monita[not_in_monita.dt_create == choise_date.strftime("%m-%d")][
            "url"
        ].nunique()
        - not_in_monita[
            not_in_monita.dt_create
            == (choise_date - timedelta(days=7)).strftime("%m-%d")
        ]["url"].nunique()
    )
    / not_in_monita[
        not_in_monita.dt_create == (
            choise_date - timedelta(days=7)).strftime("%m-%d")
    ]["url"].nunique()
    * 100,
    2,
)
not_monita_diff_empty_cv = round(
    (
        not_in_monita[
            (not_in_monita.dt_create == choise_date.strftime("%m-%d"))
            & (not_in_monita.count_cv_full_rec == 0)
        ].shape[0]
        - not_in_monita[
            (
                not_in_monita.dt_create
                == (choise_date - timedelta(days=7)).strftime("%m-%d")
            )
            & (not_in_monita.count_cv_full_rec == 0)
        ].shape[0]
    )
    / not_in_monita[
        (not_in_monita.dt_create == (choise_date - timedelta(days=7)).strftime("%m-%d"))
        & (not_in_monita.count_cv_full_rec == 0)
    ].shape[0]
    * 100,
    2,
)
not_monita_diff_full_rec = round(
    (
        not_in_monita[
            (not_in_monita.dt_create == choise_date.strftime("%m-%d"))
            & (not_in_monita.count_cv_full_rec > 0)
        ]["count_cv_full_rec"].mean()
        - not_in_monita[
            (
                not_in_monita.dt_create
                == (choise_date - timedelta(days=7)).strftime("%m-%d")
            )
            & (not_in_monita.count_cv_full_rec > 0)
        ]["count_cv_full_rec"].mean()
    )
    / not_in_monita[
        (not_in_monita.dt_create == (choise_date - timedelta(days=7)).strftime("%m-%d"))
        & (not_in_monita.count_cv_full_rec > 0)
    ]["count_cv_full_rec"].mean()
    * 100,
    2,
)

col4, col5, col6 = st.columns([1, 1, 1])
col4.metric(
    f"Количество фото",
    not_in_monita[not_in_monita.dt_create ==
                  choise_date.strftime("%m-%d")].shape[0],
    f"{not_monita_diff_count_photo}%",
    delta_color="inverse",
)
col5.metric(
    f"Нераспознанных фотографий",
    not_in_monita[
        (not_in_monita.dt_create == choise_date.strftime("%m-%d"))
        & (not_in_monita.count_cv_full_rec == 0)
    ].shape[0],
    f"{not_monita_diff_empty_cv}%",
    delta_color="inverse",
)
col6.metric(
    f"Среднее кол-во SKU на фото",
    round(
        not_in_monita[
            (not_in_monita.dt_create == choise_date.strftime("%m-%d"))
            & (not_in_monita.count_cv_full_rec > 0)
        ]["count_cv_full_rec"].mean(),
        2,
    ),
    f"{not_monita_diff_full_rec}%",
)


space(1)


#  COMMENTS ON CHART

ANNOTATIONS = [
    ("04-11", "Проблемы с выгрузкой задач на мониторинг сигарет"),
]
annotations_df = pd.DataFrame(ANNOTATIONS, columns=["dt_create", "event"])
annotations_df["y"] = 0
annotation_layer = (
    alt.Chart(annotations_df)
    .mark_text(size=20, text="⬇", dx=0, dy=-10, align="center")
    .encode(
        x=alt.X("dt_create", axis=alt.Axis(values=dates, labelAngle=0)),
        y=alt.Y("y:Q"),
        tooltip=(alt.Tooltip("event", title="Причина отклонения")),
    )
    .interactive()
)

# CHOOSEN DATE ON CHART

CURRENT_DATE_POINT = [
    (choise_date.strftime("%m-%d")),
]
cur_date_df = pd.DataFrame(CURRENT_DATE_POINT, columns=["dt_create"])
cur_date_df["y"] = not_in_monita[
    not_in_monita.dt_create == choise_date.strftime("%m-%d")
]["url"].nunique()
cur_date_df_layer = (
    alt.Chart(cur_date_df)
    .mark_text(size=15, text="●", align="center")
    .encode(
        x=alt.X("dt_create", axis=alt.Axis(values=dates, labelAngle=0)),
        y=alt.Y("y:Q"),
    )
    .interactive()
)

# chart = chart.get_chart(
#     not_in_monita.groupby("dt_create")["url"]
#     .nunique()
#     .to_frame()
#     .reset_index()
#     .rename(columns={"url": "count_photos"})
# )


col_chart_1, col_chart_2, col_chart_3 = st.columns([1, 1, 1])

# col_chart_1.altair_chart(
#     (chart + annotation_layer + cur_date_df_layer).interactive(),
#     use_container_width=True,
# )

line_chart = chart.get_line_chart(
    not_in_monita.groupby("dt_create")["url"]
    .nunique()
    .to_frame()
    .reset_index()
    .rename(columns={"url": "count_photos"}),
    axisX="dt_create",
    axisY="count_photos",
    titles=["Дата", "Количество фото"],
    chart_name="Динамика количества удаленных фото",
)

col_chart_2.altair_chart(
    (line_chart).interactive(),
    use_container_width=True,
)

if st.checkbox("Показать датафрейм"):
    st.subheader("Исходные данные")
    st.write(df)

del df

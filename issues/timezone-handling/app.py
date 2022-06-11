import streamlit as st

from datetime import datetime, timedelta, time, date
import pandas as pd
import pytz
import random

st.header("Local Timezone")
datetime.utcnow().astimezone().tzinfo

date_without_tz = datetime.now()  # datetime(1984, 1, 10, 23, 30)

# date_with_tz = date_without_tz.astimezone(timezone.utc)
# dt = dt.replace(tzinfo=timezone.utc)
# dt_unaware = dt_aware.replace(tzinfo=None)

date_with_pytz_tz = pytz.timezone("EST").localize(date_without_tz)
# aware = datetime.datetime(2011, 8, 15, 8, 15, 12, 0, pytz.UTC)

st.header("Print Date & Timzones")
col1, col2 = st.columns(2)

with col1:
    st.write("**No Timezone:**")
    st.write(date_without_tz)
    st.write("date: ", date_without_tz)
    st.write(date_without_tz.strftime("%Y-%m-%d %H:%M:%S.%f tz: %z"))
    st.write(date_without_tz.tzinfo)
    st.write("date:", date_without_tz, "!")
    st.write("date:", date_without_tz, date_without_tz)
    st.write(date_without_tz, date_without_tz.tzinfo)
    st.write(str(date_without_tz))

with col2:
    st.write("**With Timezone (pytz):**")
    st.write(date_with_pytz_tz)
    st.write("date: ", date_with_pytz_tz)
    st.write(date_with_pytz_tz.strftime("%Y-%m-%d %H:%M:%S.%f tz: %z"))
    st.write(date_with_pytz_tz.tzinfo)
    st.write("date:", date_with_pytz_tz, "!")
    st.write("date:", date_with_pytz_tz, date_with_pytz_tz)
    st.write(date_with_pytz_tz, date_with_pytz_tz.tzinfo)
    st.write(str(date_with_pytz_tz))

# st.write("With Timezone:")
# st.write(date_with_tz)
# st.write(date_with_tz.strftime("%Y-%m-%d %H:%M:%S.%f"))
# st.write(date_with_tz.tzinfo)


st.header("Input Elements")
date_input = st.date_input("date-input")

st.write(date_input)
st.write(date_input.strftime("%Y-%m-%d %H:%M:%S.%f tz: %z"))
st.write(type(date_input))

time_input = st.time_input("time-input")
st.write(time_input)
st.write(time_input.strftime("%Y-%m-%d %H:%M:%S.%f tz: %z"))
st.write(type(time_input))

st.header("Simple Dataframe")
df_with_dates = pd.DataFrame(
    [
        {
            "no-timezone": date_without_tz,
            # "with-timezone": date_with_tz,
            "with-pytz-timezone": date_with_pytz_tz,
        }
    ]
)
st.dataframe(df_with_dates)

st.header("Legacy Dataframe")
st._legacy_dataframe(df_with_dates)

st.header("Simple Table")
st.table(df_with_dates)

st.header("Random Dataframe")


def random_date(start, end):
    """Generate a random datetime between `start` and `end`"""

    return start + timedelta(
        # Get a random amount of seconds between `start` and `end`
        seconds=random.randint(0, int((end - start).total_seconds())),
    )


# date_today = datetime.now()
# days = pd.date_range(date_today, date_today + timedelta(7), freq="D")

# data = np.random.randint(1, high=100, size=len(days))
# df = pd.DataFrame({"test": days, "col2": data})
# df = df.set_index("test")


# st.write("Dataframe with timezone issue")
# st.dataframe(df)

# datetime = st.date_input("test")
# time = st.time_input("test2")
# st.write(datetime.tzinfo)

st.header("TZ Aware Date from String")
date_from_string = datetime.fromisoformat(date_with_pytz_tz.isoformat())
st.write(date_from_string)
st.write(str(date_from_string))

st.header("Date from local timezone")
date_with_local_tz = date_without_tz.astimezone()
st.write(date_with_local_tz)
st.write(str(date_with_local_tz))

st.header("AmbiguousTimeError ")
dates = ["2020-07-31 11:17:18"]
df = pd.DataFrame(dates, columns=["date"])
df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d %H:%M:%S.%f")
st.dataframe(df)

st.header("AmbiguousTimeError 2369")
idx = pd.DatetimeIndex(["11/1/2020  1:04:00 AM", "11/1/2020  1:04:00 AM"])
df = pd.DataFrame(data=[0, 1], index=idx, columns=["count"])
st.write(df)

st.header("Issue 1346")
df = pd.DataFrame({"ts": ["2020-04-14 00:00:00"]})
df["ts2"] = pd.to_datetime(df["ts"])

st.write(df)

st.write("ts2 is actually:", df.loc[0, "ts2"])


st.header("Issue 3402")
st.write("Time slider:")
period = st.slider(
    "Period:",
    min_value=time(0, 0),
    max_value=time(23, 45),
    value=(time(10, 00), time(23, 45)),
)
st.write(period)

st.write("Just printing out time is correct (wrong timezone conversion):")
st.write(time(23, 45))

st.write("Datetime Slider no-timezone (wrong timezone conversion):")
period = st.slider(
    "Period:",
    min_value=datetime(2020, 1, 10, 23, 30),
    max_value=datetime(2021, 1, 10, 23, 30),
    value=(datetime(2020, 1, 10, 23, 30), datetime(2021, 1, 10, 23, 30)),
)
st.write(period)

st.write("Datetime Slider with timezones:")
period = st.slider(
    "Period:",
    min_value=pytz.timezone("EST").localize(datetime(2020, 1, 10, 23, 30)),
    max_value=pytz.timezone("EST").localize(datetime(2021, 1, 10, 23, 30)),
    value=(
        pytz.timezone("EST").localize(datetime(2020, 1, 10, 23, 30)),
        pytz.timezone("EST").localize(datetime(2021, 1, 10, 23, 30)),
    ),
    key="datetime-slider-timezone",
)
st.write(period)

st.write("Date Slider with timezones:")
# Expected:
period = st.slider(
    "Period:",
    min_value=datetime(2020, 1, 10, 23, 30, tzinfo=pytz.utc).astimezone(
        pytz.timezone("EST")
    ),
    max_value=datetime(2021, 1, 10, 23, 30, tzinfo=pytz.utc).astimezone(
        pytz.timezone("EST")
    ),
    value=(
        datetime(2020, 1, 10, 1, 30, tzinfo=pytz.utc).astimezone(pytz.timezone("EST")),
        datetime(2021, 1, 10, 23, 30, tzinfo=pytz.utc).astimezone(pytz.timezone("EST")),
    ),
    key="new datetime slider",
    format="dddd, MMMM Do YYYY, h:mm:ss a",
)
st.write(period)


st.write("Time Slider with timezones:")
# Expected:
# developer has to take care for correct conversation -> time is always sent as UTC timestamp and displayed that way
period = st.slider(
    "Period:",
    min_value=datetime(2020, 1, 10, 10, 30, tzinfo=pytz.utc)
    .astimezone(pytz.timezone("EST"))
    .time(),
    max_value=datetime(2020, 1, 10, 11, 30, tzinfo=pytz.utc)
    .astimezone(pytz.timezone("EST"))
    .time(),
    value=(
        datetime(2020, 1, 10, 10, 30, tzinfo=pytz.utc)
        .astimezone(pytz.timezone("EST"))
        .time(),
        datetime(2020, 1, 10, 11, 30, tzinfo=pytz.utc)
        .astimezone(pytz.timezone("EST"))
        .time(),
    ),
    key="time-slider-timezone",
)
st.write(period)

st.write("Date Slider (No problem):")
period = st.slider(
    "Period:",
    min_value=date(2020, 1, 10),
    max_value=date(2021, 1, 10),
    value=(date(2020, 1, 10), date(2021, 1, 10)),
)
st.write(period)

st.write("Select Slider with Dates (no problem):")
result = st.select_slider(
    "Dates",
    options=[
        datetime(2019, 1, 10, 23, 30),
        datetime(2020, 1, 10, 23, 30),
        datetime(2021, 1, 10, 23, 30),
    ],
    value=datetime(2019, 1, 10, 23, 30),
)
st.write(result)

# st.header("Issue 2721")

# data = {
#     "dt1": ["2020-01-03 12:23", "2020-04-12 12:34"],
#     "dt2": ["2021-03-23 12:13", "2021-12-12 11:04"],
# }

# df = pd.DataFrame(data)
# df["dt1"] = pd.to_datetime(df["dt1"])
# df["dt2"] = pd.to_datetime(df["dt2"])
# df["delta"] = df["dt2"] - df["dt1"]

# st.dataframe(df)

st.header("Issue 2369")
idx = pd.DatetimeIndex(["11/1/2020  1:04:00 AM", "11/1/2020  1:04:00 AM"])

df = pd.DataFrame(data=[0, 1], index=idx, columns=["count"])

st.write(df)

st.header("Show list of dates with 15 minute difference")
date_list = [datetime.today() + timedelta(minutes=15 * x) for x in range(0, 70000)]
df = pd.DataFrame(date_list)
st.dataframe(df)

st.header("Show list of dates with 15 minute difference in EST Timezone")
date_list = [
    pytz.timezone("EST").localize(datetime.today() + timedelta(minutes=15 * x))
    for x in range(0, 70000)
]
df = pd.DataFrame(date_list)
st.dataframe(df)

st.write(
    datetime(2021, 1, 10, 23, 30, tzinfo=pytz.utc).astimezone(pytz.timezone("EST"))
)

st.write(pytz.timezone("EST").localize(datetime(2021, 1, 10, 23, 30)))
st.write(datetime(2020, 1, 10, 10, 30, tzinfo=pytz.timezone("EST")))
st.write(datetime(2020, 1, 10, 10, 30, tzinfo=pytz.utc))
import altair as alt
import pandas as pd
import streamlit as st

# Show the page title and description.
st.set_page_config(page_title="Global Temperature Analysis", page_icon="🎬")
st.title("Temperature Data Analysis")



# Load the data from a CSV. We're caching this so it doesn't reload every time the app
# reruns (e.g. if the user interacts with the widgets).
@st.cache_data
def load_data():
    df = pd.read_csv("/workspaces/Climated-data/data/GlobalLandTemperaturesByCountry.csv")
    df = df.dropna()
    return df


df = load_data()

# Show a multiselect widget with the genres using `st.multiselect`.
countries = st.multiselect(
    "Countries",
    df.Country.unique(),

    ["Algeria"]
)


# Filter the dataframe based on the widget input and reshape it.
df_filtered = df[(df["Country"].isin(countries))]


# Display the data as a table using `st.dataframe`.
st.dataframe(
    df_filtered,
    use_container_width=True,
    column_config={"year": st.column_config.TextColumn("Year")},
)

df['dt'] = pd.to_datetime(df['dt'])
import datetime
st.subheader("Select Date Range")

    # Get the minimum and maximum dates from our data
min_date = df['dt'].min()
max_date = df['dt'].max()

    # Define the default start and end dates for the slider.
    # Both must be converted to Python datetime objects to avoid a type mismatch.
default_start = (max_date - datetime.timedelta(days=50*365)).to_pydatetime()
default_end = max_date.to_pydatetime()

    # Create the slider widget. It returns a tuple of (start_date, end_date)
date_range = st.slider(
        "Filter data by date:",
        min_value=min_date.to_pydatetime(),
        max_value=max_date.to_pydatetime(),
        # The 'value' tuple must contain objects of the same type.
        value=(default_start, default_end),
        format="MMM YYYY"  # Format the date display on the slider
    )

    # Extract the start and end dates from the slider's output
start_date, end_date = date_range

mask = (
        df['Country'].isin(countries) &
        (df['dt'] >= start_date) & 
        (df['dt'] <= end_date)
    )
filtered_df = df.loc[mask]

    # --- 3. CREATE THE VISUALIZATION ---
st.subheader("Average Temperature Over Time")

    # Check if there is data to plot after filtering
if not filtered_df.empty:
        # To plot multiple lines, we need to pivot the data.
        # We want dates as the index, each country as a column, and temperature as the values.
        chart_data = filtered_df.pivot_table(
            index='dt', 
            columns='Country', 
            values='AverageTemperature'
        )
        
        # Display the line chart
        st.line_chart(chart_data)

        # --- Optional: Show Raw Data ---
        if st.checkbox("Show filtered raw data table"):
            st.dataframe(filtered_df, use_container_width=True)

else:
        # Show a warning if no data is available for the current selection
        st.warning("No data available for the selected countries and date range. Please adjust your filters.")

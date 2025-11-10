import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Sets the browser tab title
# layout="wide" uses full screen width
st.set_page_config(page_title="Interactive Data Plotter", layout="wide")


# Session state preserves data between reruns
# Streamlit reruns the entire script when users interact with widgets
# st.session_state stores data that persists across reruns
# traces list stores all the plot data users add
if 'traces' not in st.session_state:
    st.session_state.traces = []

st.title("📊 Interactive Data Plotter")
st.write("Upload your data, select columns, and create interactive plots!")


# Creates a file upload widget
# Only accepts .csv files
uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])

if uploaded_file is not None:
    try:
        # Convert the uploaded file into dataframe
        df = pd.read_csv(uploaded_file, sep = ',')

        st.success(f"✅ File uploaded successfully! Shape: {df.shape[0]} rows × {df.shape[1]} columns")

        st.subheader("📋 Data Preview")

        # Preview the data in interactive table with sorting/filtering
        st.dataframe(df.head(10), width='stretch')

        st.subheader("📈 Column Information")

        # st.columns(2) creates two side-by-side columns
        # Dropdown menus to select which columns to plot
        col1, col2 = st.columns(2)

        with col1:
            st.write("**Available Columns:**")
            st.write(df.columns.tolist())

        with col2:
            st.write("**Data Types:**")
            st.write(df.dtypes.to_dict())

        st.divider()

        st.subheader("🎨 Create Your Plot")

        col1, col2 = st.columns(2)

        # Text inputs for axis labels and trace names
        with col1:
            x_column = st.selectbox("Select X-axis column:", df.columns)

        with col2:
            y_column = st.selectbox("Select Y-axis column:", df.columns)

        col1, col2, col3 = st.columns(3)

        with col1:
            x_label = st.text_input("X-axis label (optional):", value=x_column)

        with col2:
            y_label = st.text_input("Y-axis label (optional):", value=y_column)

        with col3:
            trace_name = st.text_input("Trace name (optional):", value=f"{y_column} vs {x_column}")

        # Each trace is a dictionary with plot data
        # .tolist() converts pandas Series to Python list
        # Appended to session_state.traces for persistence
        if st.button("➕ Add to Plot", type="primary"):
            new_trace = {
                'x': df[x_column].tolist(),
                'y': df[y_column].tolist(),
                'name': trace_name,
                'x_label': x_label,
                'y_label': y_label
            }
            st.session_state.traces.append(new_trace)
            st.success(f"Added trace: {trace_name}")

        if st.session_state.traces:
            if st.button("🗑️ Clear All Traces"):
                st.session_state.traces = []
                st.rerun()

    except Exception as e:
        st.error(f"❌ Error reading file: {e}")

if st.session_state.traces:
    st.divider()
    st.subheader("📊 Interactive Plot")

    fig = go.Figure()

    # Loops through all stored traces
    # go.Scatter() creates line plots with markers
    # Each trace added to the same figure (overlay)

    for trace in st.session_state.traces:
        fig.add_trace(go.Scatter(
            x=trace['x'],
            y=trace['y'],
            mode='lines+markers',
            name=trace['name'],
            marker=dict(size=10),
            line=dict(width=3)
        ))

    last_trace = st.session_state.traces[-1]

    fig.update_layout(
        title=dict(
            text="Your Interactive Plot",
            font=dict(size=28)
        ),
        xaxis=dict(
            title=dict(text=last_trace['x_label'], font=dict(size=22)),
            tickfont=dict(size=18)
        ),
        yaxis=dict(
            title=dict(text=last_trace['y_label'], font=dict(size=22)),
            tickfont=dict(size=18)
        ),
        hovermode='closest',
        hoverlabel=dict(
            bgcolor="white",
            font_size=18,
            font_family="Arial"
        ),
        height=600,
        showlegend=True,
        legend=dict(
            font=dict(size=16)
        ),
        font=dict(size=16)
    )

    st.plotly_chart(fig, width='stretch')

    st.info(f"📌 Currently displaying {len(st.session_state.traces)} trace(s)")

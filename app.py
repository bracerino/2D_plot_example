import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Interactive Data Plotter", layout="wide")

if 'traces' not in st.session_state:
    st.session_state.traces = []

st.title("📊 Interactive Data Plotter")
st.write("Upload your data, select columns, and create interactive plots!")

uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])

if uploaded_file is not None:
    try:
        sample = uploaded_file.read(1024).decode('utf-8')
        uploaded_file.seek(0)
        
        delimiter = ','
        if ';' in sample and sample.count(';') > sample.count(','):
            delimiter = ';'
        elif '\t' in sample and sample.count('\t') > sample.count(','):
            delimiter = '\t'
        elif '|' in sample and sample.count('|') > sample.count(','):
            delimiter = '|'
        
        df = pd.read_csv(uploaded_file, sep=delimiter)
        
        st.success(f"✅ File uploaded successfully! Shape: {df.shape[0]} rows × {df.shape[1]} columns | Delimiter: '{delimiter}'")
        
        st.subheader("📋 Data Preview")
        st.dataframe(df.head(10), width='stretch')
        
        st.subheader("📈 Column Information")
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


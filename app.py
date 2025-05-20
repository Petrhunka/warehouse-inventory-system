import streamlit as st
import pandas as pd
import numpy as np
from warehouse_data import get_warehouse_data, generate_realistic_warehouse
from visualization import create_3d_warehouse_plotly, create_2d_warehouse_map

# Page configuration
st.set_page_config(
    page_title="Warehouse Visualization",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description
st.title("Warehouse Layout & Inventory System")
st.markdown("""
This application provides a visualization of a warehouse layout based on a real floor plan with:
- Multiple storage zones for different product types
- Color-coded sections for various inventory categories
- Detailed product location tracking
""")

# Sidebar controls
st.sidebar.header("Controls")

# Option to regenerate data
if st.sidebar.button("Regenerate Warehouse Data"):
    df = generate_realistic_warehouse()
    df.to_csv("warehouse_data.csv", index=False)
    st.sidebar.success("New warehouse data generated!")
else:
    df = get_warehouse_data()

# Visualization type selector
viz_type = st.sidebar.radio(
    "Visualization Type",
    ["2D Map", "3D Plotly"]
)

# Data filtering options
st.sidebar.header("Filters")

# Filter by zone
all_zones = sorted(df['zone'].unique())
selected_zones = st.sidebar.multiselect(
    "Select Zones",
    options=all_zones,
    default=all_zones
)

# Filter by product type - Handle possible NaN values
product_types = df['product_type'].dropna().unique().tolist()
product_types.sort()  # Sort in place
selected_products = st.sidebar.multiselect(
    "Select Product Types",
    options=product_types,
    default=product_types
)

# Stock filter
min_stock, max_stock = st.sidebar.slider(
    "Stock Quantity Range",
    0, int(df['quantity'].max()),
    (0, int(df['quantity'].max()))
)

# Apply filters
filtered_df = df[
    (df['zone'].isin(selected_zones)) &
    (df['product_type'].isin(selected_products)) &
    (df['quantity'] >= min_stock) &
    (df['quantity'] <= max_stock)
]

# Display statistics
st.sidebar.header("Statistics")
total_locations = len(filtered_df)
filled_locations = len(filtered_df[filtered_df['quantity'] > 0])
empty_locations = total_locations - filled_locations
total_stock = filtered_df['quantity'].sum()

col1, col2 = st.sidebar.columns(2)
col1.metric("Total Locations", total_locations)
col2.metric("Filled Locations", filled_locations)
col1.metric("Empty Locations", empty_locations)
col2.metric("Total Stock", total_stock)

# Zone statistics
st.sidebar.subheader("Zone Statistics")
zone_stats = filtered_df.groupby('zone').agg(
    Locations=('location_id', 'count'),
    Stock=('quantity', 'sum')
).reset_index()

# Show top 5 zones in sidebar with option to expand
if len(zone_stats) > 5:
    st.sidebar.dataframe(zone_stats.head(5), use_container_width=True)
    if st.sidebar.checkbox("Show all zones"):
        st.sidebar.dataframe(zone_stats, use_container_width=True)
else:
    st.sidebar.dataframe(zone_stats, use_container_width=True)

# Main visualization
st.header("Warehouse Visualization")

if viz_type == "2D Map":
    fig_2d = create_2d_warehouse_map(filtered_df)
    st.plotly_chart(fig_2d, use_container_width=True)
    st.caption("2D Layout - Hover over locations for details")
else:  # 3D Plotly
    fig = create_3d_warehouse_plotly(filtered_df)
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Use mouse to navigate: rotate (drag), zoom (scroll), pan (right-click+drag)")

# Product information
with st.expander("Product Type Information"):
    product_info = filtered_df.groupby('product_type').agg(
        Locations=('location_id', 'count'),
        TotalStock=('quantity', 'sum'),
        AvgStock=('quantity', 'mean')
    ).reset_index()
    
    st.dataframe(product_info, use_container_width=True)
    
    # Simple bar chart
    st.subheader("Stock by Product Type")
    st.bar_chart(product_info.set_index('product_type')['TotalStock'])

# Data table
with st.expander("View Location Data"):
    # Add search functionality
    search_term = st.text_input("Search for location ID or product")
    
    if search_term:
        search_results = filtered_df[
            filtered_df['location_id'].str.contains(search_term, case=False) | 
            filtered_df['product_type'].str.contains(search_term, case=False) |
            (filtered_df['product_id'].fillna('').str.contains(search_term, case=False))
        ]
        st.dataframe(search_results)
    else:
        st.dataframe(filtered_df)
    
    # Download button
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "Download Data as CSV",
        csv,
        "warehouse_data_export.csv",
        "text/csv",
        key='download-csv'
    )

# Footer
st.markdown("---")
st.markdown("Warehouse Layout & Inventory System - Built with Streamlit") 
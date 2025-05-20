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

# Highlighting options
st.sidebar.header("Highlight Options")
st.sidebar.markdown("Highlight stock level issues")

highlight_col1, highlight_col2 = st.sidebar.columns(2)

with highlight_col1:
    highlight_understock = st.checkbox("Highlight Understock")
    understock_threshold = st.number_input(
        "Understock Threshold", 
        min_value=1, 
        max_value=10, 
        value=5, 
        help="Locations with stock below this value will be marked as understock"
    ) if highlight_understock else 5

with highlight_col2:
    highlight_overstock = st.checkbox("Highlight Overstock")
    overstock_threshold = st.number_input(
        "Overstock Threshold", 
        min_value=10, 
        max_value=50, 
        value=15, 
        help="Locations with stock above this value will be marked as overstock"
    ) if highlight_overstock else 15

# Add explanation
if highlight_understock or highlight_overstock:
    st.sidebar.info(
        "🔴 Red = Understock (0 < qty ≤ " + str(understock_threshold) + ")\n"
        "🟡 Gold = Overstock (qty ≥ " + str(overstock_threshold) + ")"
    )

# Main visualization
st.header("Warehouse Visualization")

if viz_type == "2D Map":
    fig_2d = create_2d_warehouse_map(
        filtered_df, 
        highlight_overstock=highlight_overstock,
        highlight_understock=highlight_understock,
        overstock_threshold=overstock_threshold,
        understock_threshold=understock_threshold
    )
    st.plotly_chart(fig_2d, use_container_width=True)
    st.caption("2D Layout - Hover over locations for details")
else:  # 3D Plotly
    fig = create_3d_warehouse_plotly(
        filtered_df,
        highlight_overstock=highlight_overstock,
        highlight_understock=highlight_understock,
        overstock_threshold=overstock_threshold,
        understock_threshold=understock_threshold
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Use mouse to navigate: rotate (drag), zoom (scroll), pan (right-click+drag)")

# Stock level analysis section
if highlight_understock or highlight_overstock:
    with st.expander("Stock Level Analysis"):
        # Calculate statistics
        understock_count = len(filtered_df[(filtered_df['quantity'] > 0) & 
                                          (filtered_df['quantity'] <= understock_threshold)])
        overstock_count = len(filtered_df[filtered_df['quantity'] >= overstock_threshold])
        normal_count = len(filtered_df[(filtered_df['quantity'] > understock_threshold) & 
                                      (filtered_df['quantity'] < overstock_threshold)])
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Understock Locations", understock_count, 
                   f"{understock_count/filled_locations*100:.1f}% of filled" if filled_locations > 0 else "0%")
        col2.metric("Normal Stock Locations", normal_count,
                   f"{normal_count/filled_locations*100:.1f}% of filled" if filled_locations > 0 else "0%")
        col3.metric("Overstock Locations", overstock_count,
                   f"{overstock_count/filled_locations*100:.1f}% of filled" if filled_locations > 0 else "0%")
        
        # Create a zone-wise analysis
        zone_analysis = filtered_df[filtered_df['quantity'] > 0].groupby('zone').apply(
            lambda x: pd.Series({
                'Total Items': x['quantity'].sum(),
                'Understock': len(x[(x['quantity'] > 0) & (x['quantity'] <= understock_threshold)]),
                'Normal': len(x[(x['quantity'] > understock_threshold) & (x['quantity'] < overstock_threshold)]),
                'Overstock': len(x[x['quantity'] >= overstock_threshold])
            })
        ).reset_index()
        
        st.subheader("Stock Levels by Zone")
        st.dataframe(zone_analysis, use_container_width=True)

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
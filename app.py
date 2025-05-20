import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from warehouse_data import get_warehouse_data, generate_realistic_warehouse
from visualization import create_3d_warehouse_plotly, create_2d_warehouse_map

# Page configuration
st.set_page_config(
    page_title="Warehouse Visualization",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Get the data - outside of tabs so it only loads once
if 'data_loaded' not in st.session_state:
    if st.sidebar.button("Regenerate Warehouse Data"):
        df = generate_realistic_warehouse()
        df.to_csv("warehouse_data.csv", index=False)
        st.sidebar.success("New warehouse data generated!")
    else:
        df = get_warehouse_data()
    
    st.session_state['warehouse_data'] = df
    st.session_state['data_loaded'] = True
else:
    df = st.session_state['warehouse_data']

# Title at the top level
st.title("Warehouse Layout & Inventory System")

# Create tabs for visualization and inventory reporting
tab1, tab2 = st.tabs(["Warehouse Visualization", "Inventory Level Reporting"])

# TAB 1: WAREHOUSE VISUALIZATION
with tab1:
    st.markdown("""
    Interactive visualization of warehouse layout with:
    - Multiple storage zones for different product types
    - Color-coded sections for various inventory categories
    - Detailed product location tracking
    """)

    # Sidebar controls
    st.sidebar.header("Controls")

    # Visualization type selector
    viz_type = st.sidebar.radio(
        "Visualization Type",
        ["3D Plotly", "2D Map"]
    )

    # Highlighting options - MOVED TO APPEAR BEFORE FILTERS
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

# TAB 2: INVENTORY LEVEL REPORTING
with tab2:
    st.header("Warehouse Inventory Level Report")
    st.markdown("""
    This section provides detailed reporting on inventory levels across the warehouse, 
    helping identify stocking issues, optimize inventory distribution, and support 
    decision-making for inventory management.
    """)
    
    # Calculate overall inventory metrics
    total_inventory = df['quantity'].sum()
    total_products = len(df['product_type'].unique())
    avg_per_product = df.groupby('product_type')['quantity'].sum().mean()
    filled_locations_pct = len(df[df['quantity'] > 0]) / len(df) * 100
    
    # Display key metrics in columns
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    metric_col1.metric("Total Inventory", f"{total_inventory:,}", help="Total quantity of all items in warehouse")
    metric_col2.metric("Product Categories", total_products, help="Number of unique product types")
    metric_col3.metric("Avg Per Category", f"{avg_per_product:.1f}", help="Average quantity per product category")
    metric_col4.metric("Space Utilization", f"{filled_locations_pct:.1f}%", help="Percentage of filled locations")
    
    # Inventory by product type - bar chart
    st.subheader("Inventory by Product Type")
    product_inventory = df.groupby('product_type')['quantity'].sum().reset_index()
    product_inventory = product_inventory.sort_values('quantity', ascending=False)
    
    fig_product = px.bar(
        product_inventory, 
        x='product_type', 
        y='quantity',
        title="Total Stock by Product Type",
        labels={'product_type': 'Product Type', 'quantity': 'Total Quantity'},
        color='quantity',
        color_continuous_scale=px.colors.sequential.Blues
    )
    fig_product.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_product, use_container_width=True)
    
    # Location Type Analysis
    location_inventory = df.groupby('location_type').agg(
        total_items=('quantity', 'sum'),
        locations=('location_id', 'count'),
        avg_per_location=('quantity', lambda x: x.sum() / len(x) if len(x) > 0 else 0),
        utilization=('quantity', lambda x: len(x[x > 0]) / len(x) * 100 if len(x) > 0 else 0)
    ).reset_index()
    
    # Format numeric columns
    location_inventory['avg_per_location'] = location_inventory['avg_per_location'].round(1)
    location_inventory['utilization'] = location_inventory['utilization'].round(1)
    
    # Rename columns for display
    location_inventory = location_inventory.rename(columns={
        'location_type': 'Location Type',
        'total_items': 'Total Items',
        'locations': 'Total Locations',
        'avg_per_location': 'Avg Items/Location',
        'utilization': 'Utilization %'
    })
    
    st.subheader("Inventory by Location Type")
    st.dataframe(location_inventory.sort_values('Total Items', ascending=False), use_container_width=True)
    
    # Detailed Product Information - NEW SECTION
    st.subheader("Detailed Product Information")
    
    # Product selector
    selected_product = st.selectbox(
        "Select Product for Detailed Analysis",
        options=sorted(df['product_type'].unique())
    )
    
    # Filter data for selected product
    product_data = df[df['product_type'] == selected_product]
    
    # Display product metrics
    st.subheader(f"{selected_product} - Inventory Details")
    
    # Key metrics for the product
    prod_total_qty = product_data['quantity'].sum()
    prod_locations = len(product_data)
    prod_filled_locations = len(product_data[product_data['quantity'] > 0])
    prod_avg_per_location = prod_total_qty / prod_filled_locations if prod_filled_locations > 0 else 0
    
    prod_col1, prod_col2, prod_col3, prod_col4 = st.columns(4)
    prod_col1.metric("Total Quantity", prod_total_qty)
    prod_col2.metric("Total Locations", prod_locations)
    prod_col3.metric("Filled Locations", prod_filled_locations)
    prod_col4.metric("Avg Qty/Location", f"{prod_avg_per_location:.1f}")
    
    # Distribution by zone
    st.subheader(f"{selected_product} - Distribution by Zone")
    product_by_zone = product_data.groupby('zone').agg(
        total_quantity=('quantity', 'sum'),
        locations=('location_id', 'count'),
        filled_locations=('quantity', lambda x: len(x[x > 0])),
        avg_quantity=('quantity', 'mean'),
        max_quantity=('quantity', 'max'),
        min_quantity=('quantity', 'min')
    ).reset_index()
    
    # Format numeric columns
    product_by_zone['avg_quantity'] = product_by_zone['avg_quantity'].round(1)
    
    # Rename columns for display
    product_by_zone = product_by_zone.rename(columns={
        'zone': 'Zone',
        'total_quantity': 'Total Qty',
        'locations': 'Locations',
        'filled_locations': 'Filled Locs',
        'avg_quantity': 'Avg Qty',
        'max_quantity': 'Max Qty',
        'min_quantity': 'Min Qty'
    })
    
    # Show data
    st.dataframe(product_by_zone.sort_values('Total Qty', ascending=False), use_container_width=True)
    
    # Distribution by location type
    st.subheader(f"{selected_product} - Distribution by Location Type")
    product_by_loc_type = product_data.groupby('location_type').agg(
        total_quantity=('quantity', 'sum'),
        locations=('location_id', 'count'),
        filled_locations=('quantity', lambda x: len(x[x > 0])),
        utilization=('quantity', lambda x: len(x[x > 0]) / len(x) * 100 if len(x) > 0 else 0)
    ).reset_index()
    
    # Format numeric columns
    product_by_loc_type['utilization'] = product_by_loc_type['utilization'].round(1)
    
    # Rename columns for display
    product_by_loc_type = product_by_loc_type.rename(columns={
        'location_type': 'Location Type',
        'total_quantity': 'Total Qty',
        'locations': 'Locations',
        'filled_locations': 'Filled Locs',
        'utilization': 'Utilization %'
    })
    
    # Show data
    st.dataframe(product_by_loc_type.sort_values('Total Qty', ascending=False), use_container_width=True)
    
    # Inventory status - Stock level analysis
    st.subheader(f"{selected_product} - Stock Level Analysis")
    
    # Define stock level categories
    low_threshold = 5
    high_threshold = 15
    
    # Create a copy to avoid the SettingWithCopyWarning
    product_data_copy = product_data.copy()
    product_data_copy['stock_level'] = pd.cut(
        product_data_copy['quantity'],
        bins=[-1, 0, low_threshold, high_threshold, float('inf')],
        labels=['Empty', 'Low', 'Normal', 'High']
    )
    
    stock_level_counts = product_data_copy['stock_level'].value_counts().reset_index()
    stock_level_counts.columns = ['Stock Level', 'Count']
    
    # Plot stock level distribution
    fig_stock_levels = px.pie(
        stock_level_counts, 
        values='Count', 
        names='Stock Level',
        title=f"{selected_product} - Stock Level Distribution",
        color='Stock Level',
        color_discrete_map={
            'Empty': 'lightgray',
            'Low': 'red',
            'Normal': 'green',
            'High': 'gold'
        }
    )
    st.plotly_chart(fig_stock_levels, use_container_width=True)
    
    # Show locations that need attention (low stock)
    if len(product_data_copy[product_data_copy['stock_level'] == 'Low']) > 0:
        st.subheader(f"{selected_product} - Locations Needing Replenishment")
        low_stock_locations = product_data_copy[product_data_copy['stock_level'] == 'Low'].sort_values('quantity')
        low_stock_display = low_stock_locations[['location_id', 'zone', 'location_type', 'quantity']]
        st.dataframe(low_stock_display, use_container_width=True)
    
    # Inventory Issues Analysis
    st.subheader("Inventory Issues Analysis")
    
    issue_col1, issue_col2 = st.columns(2)
    
    with issue_col1:
        # Thresholds for analysis
        low_threshold = st.slider("Low Stock Threshold", 1, 10, 5)
        
        # Low stock locations
        low_stock = df[(df['quantity'] > 0) & (df['quantity'] <= low_threshold)]
        low_stock_count = len(low_stock)
        low_stock_pct = low_stock_count / len(df[df['quantity'] > 0]) * 100 if len(df[df['quantity'] > 0]) > 0 else 0
        
        st.metric("Low Stock Locations", low_stock_count, f"{low_stock_pct:.1f}% of filled locations")
        
        # Low stock by product type
        low_by_product = low_stock.groupby('product_type').size().reset_index(name='count')
        low_by_product = low_by_product.sort_values('count', ascending=False)
        
        if not low_by_product.empty:
            fig_low = px.bar(
                low_by_product.head(10), 
                x='product_type', 
                y='count',
                title="Top Products with Low Stock",
                labels={'product_type': 'Product Type', 'count': 'Low Stock Locations'},
                color='count',
                color_continuous_scale=px.colors.sequential.Reds
            )
            fig_low.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_low, use_container_width=True)
        else:
            st.info("No low stock locations found")
    
    with issue_col2:
        # Thresholds for analysis
        high_threshold = st.slider("High Stock Threshold", 10, 50, 15)
        
        # High stock locations
        high_stock = df[df['quantity'] >= high_threshold]
        high_stock_count = len(high_stock)
        high_stock_pct = high_stock_count / len(df[df['quantity'] > 0]) * 100 if len(df[df['quantity'] > 0]) > 0 else 0
        
        st.metric("High Stock Locations", high_stock_count, f"{high_stock_pct:.1f}% of filled locations")
        
        # High stock by product type
        high_by_product = high_stock.groupby('product_type').size().reset_index(name='count')
        high_by_product = high_by_product.sort_values('count', ascending=False)
        
        if not high_by_product.empty:
            fig_high = px.bar(
                high_by_product.head(10), 
                x='product_type', 
                y='count',
                title="Top Products with High Stock",
                labels={'product_type': 'Product Type', 'count': 'High Stock Locations'},
                color='count',
                color_continuous_scale=px.colors.sequential.Greens
            )
            fig_high.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_high, use_container_width=True)
        else:
            st.info("No high stock locations found")
    
    # Inventory Balance Analysis
    st.subheader("Inventory Balance Analysis")
    
    # Calculate balance metrics
    balance_data = df.groupby('product_type').agg(
        avg_quantity=('quantity', 'mean'),
        std_quantity=('quantity', 'std'),
        min_quantity=('quantity', 'min'),
        max_quantity=('quantity', 'max'),
        total_quantity=('quantity', 'sum'),
        location_count=('location_id', 'count')
    ).reset_index()
    
    # Calculate coefficient of variation (measure of stock balance)
    balance_data['cv'] = (balance_data['std_quantity'] / balance_data['avg_quantity'] * 100).fillna(0)
    
    # Format for display
    balance_display = balance_data.copy()
    balance_display['avg_quantity'] = balance_display['avg_quantity'].round(1)
    balance_display['std_quantity'] = balance_display['std_quantity'].round(1)
    balance_display['cv'] = balance_display['cv'].round(1)
    
    # Rename columns for display
    balance_display = balance_display.rename(columns={
        'product_type': 'Product Type',
        'avg_quantity': 'Avg Qty',
        'std_quantity': 'Std Dev',
        'min_quantity': 'Min Qty',
        'max_quantity': 'Max Qty',
        'total_quantity': 'Total',
        'location_count': 'Locations',
        'cv': 'CV %'
    })
    
    # Show data
    st.dataframe(balance_display.sort_values('CV %', ascending=False), use_container_width=True)
    st.caption("CV % = Coefficient of Variation - Higher values indicate less balanced inventory distribution")
    
    # Download report
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "Download Full Inventory Report",
        csv,
        "warehouse_inventory_report.csv",
        "text/csv",
        key='download-inventory-report'
    )

# Footer appears outside of tabs
st.markdown("---")
st.markdown("Warehouse Layout & Inventory System - Built with Streamlit") 
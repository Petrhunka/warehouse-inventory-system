import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit as st

def get_color_by_zone(zone):
    """Return color based on warehouse zone."""
    if zone == "Storage":
        return [0, 0, 255]  # Blue
    elif zone == "Picking":
        return [0, 255, 0]  # Green
    elif zone == "Overstock":
        return [255, 165, 0]  # Orange
    else:
        return [100, 100, 100]  # Grey

def get_color_by_stock(quantity):
    """Return color based on stock quantity."""
    if quantity == 0:
        return [220, 220, 220]  # Light grey (empty)
    elif quantity < 5:
        return [255, 0, 0]  # Red (low stock)
    elif quantity < 15:
        return [255, 255, 0]  # Yellow (medium stock)
    else:
        return [0, 255, 0]  # Green (high stock)

def get_color_by_stock_level(quantity, highlight_overstock=False, highlight_understock=False, 
                            overstock_threshold=15, understock_threshold=5, base_color=None):
    """Return color based on stock quantity and highlighting preferences."""
    if quantity == 0:
        return 'rgb(220, 220, 220)'  # Empty location - light grey
    
    if highlight_understock and quantity > 0 and quantity <= understock_threshold:
        return 'rgb(255, 0, 0)'  # Understock - bright red
    
    if highlight_overstock and quantity >= overstock_threshold:
        return 'rgb(255, 215, 0)'  # Overstock - gold
    
    # If no highlighting or not meeting criteria, use base color or default blue
    if base_color and isinstance(base_color, list) and len(base_color) >= 3:
        return f'rgb({base_color[0]}, {base_color[1]}, {base_color[2]})'
    
    # Default color if no base color provided
    return 'rgb(0, 0, 255)'  # Default blue

def create_3d_warehouse_plotly(df, highlight_overstock=False, highlight_understock=False,
                             overstock_threshold=15, understock_threshold=5):
    """Create a 3D warehouse visualization using Plotly."""
    
    fig = go.Figure()
    
    # Add traces for each zone
    for zone in df['zone'].unique():
        zone_df = df[df['zone'] == zone]
        
        # First, handle empty locations
        empty_mask = zone_df['quantity'] == 0
        if empty_mask.any():
            empty_df = zone_df[empty_mask]
            
            # Ensure colors are properly formatted
            empty_colors = []
            for _, row in empty_df.iterrows():
                if isinstance(row.color, list) and len(row.color) >= 3:
                    # Format RGB values properly
                    empty_colors.append(f'rgb({row.color[0]}, {row.color[1]}, {row.color[2]})')
                else:
                    # Default color for invalid entries
                    empty_colors.append('rgb(220, 220, 220)')
            
            empty_sizes = [8 for _ in range(len(empty_df))]
            empty_hovertext = [
                f"ID: {row.location_id}<br>"
                f"Zone: {row.zone}<br>"
                f"Product Type: {row.product_type}<br>"
                f"Product: Empty<br>"
                f"Quantity: 0"
                + (f"<br>Depth: {row.depth_info}" if row.depth_info else "")
                for _, row in empty_df.iterrows()
            ]
            
            fig.add_trace(go.Scatter3d(
                x=empty_df['x'],
                y=empty_df['y'],
                z=empty_df['z'],
                mode='markers',
                marker=dict(
                    size=empty_sizes,
                    color=empty_colors,
                    opacity=0.5,
                    symbol='square',
                    line=dict(width=1, color='rgb(50,50,50)')
                ),
                text=empty_hovertext,
                hoverinfo='text',
                name=f"Zone {zone} - Empty"
            ))
        
        # Then, handle filled locations
        filled_mask = zone_df['quantity'] > 0
        if filled_mask.any():
            filled_df = zone_df[filled_mask]
            
            # Apply highlighting for overstock/understock
            filled_colors = []
            for _, row in filled_df.iterrows():
                filled_colors.append(get_color_by_stock_level(
                    quantity=row.quantity,
                    highlight_overstock=highlight_overstock,
                    highlight_understock=highlight_understock,
                    overstock_threshold=overstock_threshold,
                    understock_threshold=understock_threshold,
                    base_color=row.color
                ))
            
            filled_sizes = [max(5, min(row.quantity * 0.5, 15)) for _, row in filled_df.iterrows()]
            filled_hovertext = [
                f"ID: {row.location_id}<br>"
                f"Zone: {row.zone}<br>"
                f"Product Type: {row.product_type}<br>"
                f"Product: {row.product_id}<br>"
                f"Quantity: {row.quantity}"
                + (f"<br>Depth: {row.depth_info}" if row.depth_info else "")
                + (f"<br><b>UNDERSTOCK</b>" if highlight_understock and row.quantity > 0 and row.quantity <= understock_threshold else "")
                + (f"<br><b>OVERSTOCK</b>" if highlight_overstock and row.quantity >= overstock_threshold else "")
                for _, row in filled_df.iterrows()
            ]
            
            fig.add_trace(go.Scatter3d(
                x=filled_df['x'],
                y=filled_df['y'],
                z=filled_df['z'],
                mode='markers',
                marker=dict(
                    size=filled_sizes,
                    color=filled_colors,
                    opacity=1.0,
                    symbol='square',
                    line=dict(width=1, color='rgb(50,50,50)')
                ),
                text=filled_hovertext,
                hoverinfo='text',
                name=f"Zone {zone} - {filled_df['product_type'].iloc[0]}"
            ))
    
    # Add text labels for each zone
    for zone, group in df.groupby('zone'):
        # Calculate the center position of the zone
        center_x = group['x'].mean()
        center_y = group['y'].mean()
        center_z = group['z'].max() + 2  # Position label above the highest point
        
        # Skip labels for dock
        if zone != "DOCK":
            fig.add_trace(go.Scatter3d(
                x=[center_x],
                y=[center_y],
                z=[center_z],
                mode='text',
                text=[f"<b>{zone}</b>"],
                textposition="top center",
                textfont=dict(size=14, color='black'),
                showlegend=False
            ))
    
    # Update layout
    fig.update_layout(
        title="Warehouse Layout Visualization",
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z',
            aspectmode='data'
        ),
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ),
        margin=dict(l=0, r=0, b=0, t=40),
        height=800,
        width=1200
    )
    
    # Add top-down camera view
    fig.update_layout(
        scene_camera=dict(
            eye=dict(x=0.5, y=0, z=2.5)
        )
    )
    
    return fig

def create_2d_warehouse_map(df, highlight_overstock=False, highlight_understock=False,
                          overstock_threshold=15, understock_threshold=5):
    """Create a 2D top-down view of the warehouse."""
    
    fig = go.Figure()
    
    # Group by zone for coloring
    for zone in df['zone'].unique():
        zone_df = df[df['zone'] == zone].drop_duplicates(['x', 'y'])
        
        # Empty locations
        empty_df = zone_df[zone_df['quantity'] == 0]
        if not empty_df.empty:
            # Default colors for empty locations
            empty_colors = []
            for _, row in empty_df.iterrows():
                if isinstance(row.color, list) and len(row.color) >= 3:
                    empty_colors.append(f'rgb({row.color[0]}, {row.color[1]}, {row.color[2]})')
                else:
                    empty_colors.append('rgb(220, 220, 220)')
            
            empty_hovertext = [
                f"Zone: {row.zone}<br>"
                f"Product Type: {row.product_type}<br>"
                f"Status: Empty"
                + (f"<br>Depth: {row.depth_info}" if row.depth_info else "")
                for _, row in empty_df.iterrows()
            ]
            
            fig.add_trace(go.Scatter(
                x=empty_df['x'],
                y=empty_df['y'],
                mode='markers',
                marker=dict(
                    size=10,
                    color=empty_colors,
                    symbol='square',
                    opacity=0.5,
                    line=dict(width=1, color='rgb(50,50,50)')
                ),
                text=empty_hovertext,
                hoverinfo='text',
                name=f"Zone {zone} - Empty"
            ))
        
        # Filled locations
        filled_df = zone_df[zone_df['quantity'] > 0]
        if not filled_df.empty:
            # Apply highlighting for overstock/understock
            filled_colors = []
            for _, row in filled_df.iterrows():
                filled_colors.append(get_color_by_stock_level(
                    quantity=row.quantity,
                    highlight_overstock=highlight_overstock,
                    highlight_understock=highlight_understock,
                    overstock_threshold=overstock_threshold,
                    understock_threshold=understock_threshold,
                    base_color=row.color
                ))
            
            filled_hovertext = [
                f"Zone: {row.zone}<br>"
                f"Product Type: {row.product_type}<br>"
                f"Quantity: {row.quantity}"
                + (f"<br>Depth: {row.depth_info}" if row.depth_info else "")
                + (f"<br><b>UNDERSTOCK</b>" if highlight_understock and row.quantity > 0 and row.quantity <= understock_threshold else "")
                + (f"<br><b>OVERSTOCK</b>" if highlight_overstock and row.quantity >= overstock_threshold else "")
                for _, row in filled_df.iterrows()
            ]
            
            fig.add_trace(go.Scatter(
                x=filled_df['x'],
                y=filled_df['y'],
                mode='markers',
                marker=dict(
                    size=10,
                    color=filled_colors,
                    symbol='square',
                    line=dict(width=1, color='rgb(50,50,50)')
                ),
                text=filled_hovertext,
                hoverinfo='text',
                name=f"Zone {zone} - {filled_df['product_type'].iloc[0]}"
            ))
    
    # Add text labels for each zone
    for zone, group in df.groupby('zone'):
        # Calculate the center position of the zone
        center_x = group['x'].mean()
        center_y = group['y'].mean()
        
        # Skip labels for dock
        if zone != "DOCK":
            fig.add_trace(go.Scatter(
                x=[center_x],
                y=[center_y],
                mode='text',
                text=[f"<b>{zone}</b>"],
                textposition="middle center",
                textfont=dict(size=14, color='black'),
                showlegend=False
            ))
    
    # Add legend for stock levels if highlighting is enabled
    if highlight_overstock or highlight_understock:
        fig.add_trace(go.Scatter(
            x=[None],
            y=[None],
            mode='markers',
            marker=dict(size=10, color='rgb(255, 0, 0)'),
            name='Understock' if highlight_understock else '',
            showlegend=highlight_understock
        ))
        
        fig.add_trace(go.Scatter(
            x=[None],
            y=[None],
            mode='markers',
            marker=dict(size=10, color='rgb(255, 215, 0)'),
            name='Overstock' if highlight_overstock else '',
            showlegend=highlight_overstock
        ))
    
    # Update layout
    fig.update_layout(
        title="Warehouse 2D Layout",
        xaxis_title='X',
        yaxis_title='Y',
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ),
        margin=dict(l=0, r=0, b=0, t=40),
        height=600,
        width=1000
    )
    
    return fig 
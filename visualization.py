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

def create_3d_warehouse_plotly(df):
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
            
            # Ensure colors are properly formatted
            filled_colors = []
            for _, row in filled_df.iterrows():
                if isinstance(row.color, list) and len(row.color) >= 3:
                    # Format RGB values properly
                    filled_colors.append(f'rgb({row.color[0]}, {row.color[1]}, {row.color[2]})')
                else:
                    # Default color
                    filled_colors.append('rgb(0, 0, 255)')
            
            filled_sizes = [max(5, min(row.quantity * 0.5, 15)) for _, row in filled_df.iterrows()]
            filled_hovertext = [
                f"ID: {row.location_id}<br>"
                f"Zone: {row.zone}<br>"
                f"Product Type: {row.product_type}<br>"
                f"Product: {row.product_id}<br>"
                f"Quantity: {row.quantity}"
                + (f"<br>Depth: {row.depth_info}" if row.depth_info else "")
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

def create_2d_warehouse_map(df):
    """Create a 2D top-down view of the warehouse."""
    
    fig = go.Figure()
    
    # Group by zone for coloring
    for zone in df['zone'].unique():
        zone_df = df[df['zone'] == zone].drop_duplicates(['x', 'y'])
        
        # Create hover text
        hovertext = [
            f"Zone: {row.zone}<br>"
            f"Product Type: {row.product_type}"
            + (f"<br>Depth: {row.depth_info}" if row.depth_info else "")
            for _, row in zone_df.iterrows()
        ]
        
        # Ensure colors are properly formatted
        colors = []
        for _, row in zone_df.iterrows():
            if isinstance(row.color, list) and len(row.color) >= 3:
                colors.append(f'rgb({row.color[0]}, {row.color[1]}, {row.color[2]})')
            else:
                # Default color
                colors.append('rgb(0, 0, 255)')
        
        fig.add_trace(go.Scatter(
            x=zone_df['x'],
            y=zone_df['y'],
            mode='markers',
            marker=dict(
                size=10,
                color=colors,
                symbol='square',
                line=dict(width=1, color='rgb(50,50,50)')
            ),
            text=hovertext,
            hoverinfo='text',
            name=f"Zone {zone} - {zone_df['product_type'].iloc[0]}"
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
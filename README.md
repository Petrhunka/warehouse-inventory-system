# Warehouse Layout & Inventory Visualization System

An interactive visualization tool for warehouse management, inventory tracking, and stock level analysis.

![Warehouse Visualization](https://img.shields.io/badge/Warehouse-Visualization-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-red)
![Python](https://img.shields.io/badge/Python-3.x-green)

## Overview

This application provides a powerful visualization of warehouse layouts based on actual floor plans. It helps warehouse managers and operations teams to:

- Monitor real-time inventory levels across all warehouse zones
- Identify understock and overstock situations requiring attention
- Analyze stock distribution by product type and zone
- Plan efficient space utilization and inventory rebalancing

## Key Features

### Interactive Visualizations
- **2D Map View**: Top-down layout visualization with zone and product type information
- **3D Plotly View**: Fully interactive 3D representation with depth visualization
- **Dynamic Filtering**: Filter by zones, product types, and inventory levels

### Advanced Stock Analysis
- **Stock Level Highlighting**: Visual identification of overstock and understock positions
- **Customizable Thresholds**: Set your own thresholds for what constitutes over/understock
- **Detailed Analysis**: Zone-by-zone breakdown of stock level situations
- **Statistical Insights**: Metrics and percentages of stock level distribution

### Practical Warehouse Management
- **Realistic Layout**: Representing actual warehouse configurations with proper zones
- **Product Types**: Support for various product categories (bottles, cans, bulk storage, etc.)
- **Multi-level Storage**: Visualization of different storage depths and heights
- **Search Functionality**: Quickly locate specific products or locations
- **Data Export**: Download inventory data for offline analysis

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/warehouse-visualization.git
cd warehouse-visualization
```

2. Create and activate a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Application

Start the Streamlit application:
```bash
streamlit run app.py
```

The application will open in your default web browser at http://localhost:8501.

### Navigation

1. **Select Visualization Type**: Choose between 2D Map and 3D Plotly visualizations
2. **Apply Filters**: Filter data by:
   - Warehouse zones (A through U)
   - Product types
   - Stock quantity range

3. **Enable Stock Highlighting**:
   - Use the Highlighting Options section to enable visualization of understock/overstock
   - Adjust thresholds to match your operational requirements
   - View detailed stock analysis in the expandable section

4. **Interact with the Visualization**:
   - Hover over locations to see detailed information
   - In 3D view: rotate (drag), zoom (scroll), pan (right-click+drag)
   - Use the legend to understand zone and status coding

5. **Explore Data Analysis**:
   - Expand the "Stock Level Analysis" panel for detailed metrics
   - Check "Product Type Information" for inventory distribution
   - Use search functionality in "View Location Data" to find specific items

## Warehouse Structure

The application models a warehouse with various zones:

- **Storage Zones (A-G)**: Main product storage areas with different product types
- **Special Storage (J-U)**: Specialized storage for different product categories
- **Receiving Dock**: Designated area for receiving goods

Each location includes:
- Location ID
- Zone designation
- Product information
- Stock quantity
- Physical position (x,y,z coordinates)
- Storage depth information

## Customization

### Regenerating Warehouse Data

You can generate new warehouse data to simulate different inventory scenarios:
1. Click "Regenerate Warehouse Data" in the sidebar
2. The application will create a new dataset while maintaining the warehouse layout

### Adjusting Stock Highlighting

Customize the highlighting thresholds based on your inventory management policies:
1. Enable "Highlight Understock" or "Highlight Overstock" as needed
2. Set appropriate threshold values
3. The visualization will update in real-time to reflect your settings

## Data Export

Download inventory data for further analysis:
1. Expand the "View Location Data" section
2. Click "Download Data as CSV"
3. Import the data into your preferred analytics tools

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
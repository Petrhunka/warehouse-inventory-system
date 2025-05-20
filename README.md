# Clothing Warehouse Visualization & Inventory System

An interactive warehouse management tool for apparel retailers and distribution centers that combines 3D visualization with comprehensive inventory analytics.

![Clothing Warehouse](https://img.shields.io/badge/Clothing-Warehouse-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-red)
![Python](https://img.shields.io/badge/Python-3.x-green)
![Plotly](https://img.shields.io/badge/Plotly-5.18.0-orange)

## Overview

This application provides warehouse management teams with a powerful dual-purpose tool:

1. **Interactive Warehouse Visualization**: Visualize your entire warehouse in 2D or 3D, with intuitive navigation and highlighting for inventory issues
2. **In-depth Inventory Analysis**: Monitor stock levels, identify imbalances, and make data-driven decisions with detailed inventory reports

Perfect for clothing retailers and distribution centers, this system helps optimize storage, identify stocking issues, and improve warehouse operations.

## Key Features

### Warehouse Visualization Tab

- **Multiple View Options**:
  - **3D Interactive Visualization**: Navigate through a complete 3D model of your warehouse
  - **2D Top-Down Map**: View warehouse layout from above for a comprehensive overview

- **Intelligent Highlighting**:
  - **Understock Detection**: Automatically highlight locations with critically low inventory
  - **Overstock Identification**: Spot areas with excessive stock for better inventory balancing
  - **Customizable Thresholds**: Set your own parameters for what constitutes over/understock

- **Dynamic Filtering**:
  - Filter by warehouse zones
  - Filter by product types (T-shirts, Jeans, Dresses, etc.)
  - Filter by inventory levels

### Inventory Reporting Tab

- **Executive Dashboard**: Key metrics showing total inventory, utilization rates, and product statistics
- **Product Type Analytics**: Comprehensive breakdown of inventory by clothing category
- **Location Analysis**: See how different storage types are utilized across the warehouse
- **Detailed Product Information**:
  - Per-product metrics and distribution
  - Zone-based analytics for each product type
  - Storage type utilization for specific products
  - Stock level analysis with visual breakdown

- **Issue Detection**:
  - Understock reporting with location details
  - Overstock analysis to prevent excess inventory
  - Inventory balance metrics with coefficient of variation analysis

## Clothing Warehouse Structure

The system is designed for apparel retailers with support for:

### Product Categories
- Basic apparel (T-shirts, Jeans, Dresses, Sweaters, Jackets)
- Footwear (Shoes)
- Accessories and small items (Socks, Underwear)
- Premium collections (Designer Brands)
- Seasonal merchandise
- Specialized categories (Athletic Wear, Kids Clothing, Plus Size)

### Storage Locations
- **Folded Shelves**: For t-shirts, jeans, and similar items
- **Hanging Racks**: For dresses, jackets, and hanging garments
- **Shoe Racks**: Specialized storage for footwear
- **Small Item Bins**: For accessories, socks, underwear
- **Secure Storage**: For high-value premium apparel
- **Sale Racks**: For discounted merchandise
- **Front-Facing Displays**: For new arrivals and featured items

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. Clone this repository:
```bash
git clone https://github.com/yourusername/clothing-warehouse-visualization.git
cd clothing-warehouse-visualization
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

4. For better performance, install the Watchdog module (optional):
```bash
# On macOS, you might need to install developer tools first:
xcode-select --install
pip install watchdog
```

## Usage Guide

### Starting the Application

Launch the application with Streamlit:
```bash
streamlit run app.py
```

The application will open in your default web browser at http://localhost:8501.

### Visualization Tab

1. **Select Visualization Type**:
   - 3D Plotly: For comprehensive 3D view (default)
   - 2D Map: For a top-down overview

2. **Highlight Inventory Issues**:
   - Enable "Highlight Understock" to see locations needing replenishment
   - Enable "Highlight Overstock" to see locations with excess inventory
   - Adjust thresholds to match your inventory management rules

3. **Apply Filters** to focus on specific areas:
   - Select specific zones to view
   - Choose particular product types
   - Filter by stock quantity range

4. **Interact with the Visualization**:
   - **3D Navigation**: Rotate (drag), zoom (scroll), pan (right-click+drag)
   - **Hover over locations** for detailed information
   - **View Stock Analysis** in the expandable panel below the visualization

### Inventory Reporting Tab

1. **Overview Metrics**: Review key warehouse statistics at the top

2. **Product Type Analysis**: Examine inventory distribution across product categories

3. **Location Type Analysis**: See how different storage types are utilized

4. **Detailed Product Analysis**:
   - Select a specific product from the dropdown
   - Review detailed metrics for that product
   - See distribution across zones and location types
   - Analyze stock levels with the pie chart
   - Identify locations needing replenishment

5. **Inventory Issues Analysis**:
   - Set custom thresholds for low and high stock
   - View detailed breakdowns of problem areas
   - Identify which product categories need attention

6. **Download Reports**: Export data for further analysis

## Customization

### Regenerating Warehouse Data

Generate new simulated warehouse data to test different scenarios:

1. Click "Regenerate Warehouse Data" in the sidebar
2. The application will create a new dataset while maintaining the warehouse structure

### Adjusting Highlighting Thresholds

Fine-tune the application to match your inventory management policies:

1. Use the sliders to set custom understock and overstock thresholds
2. The visualization will update in real-time to reflect your settings

## Troubleshooting

### Common Issues

- **Performance Issues**: For large warehouses, consider using the 2D view for better performance
- **Data Generation**: If regenerating data doesn't work, ensure you have write permissions in the application directory
- **Browser Compatibility**: For best results, use Chrome or Firefox

### Warning Messages

If you see pandas SettingWithCopyWarning messages in the console, these can be safely ignored as they don't affect the functionality of the application.

## For Developers

### Project Structure

- `app.py`: Main Streamlit application
- `warehouse_data.py`: Data generation for clothing inventory
- `visualization.py`: 2D and 3D visualization functionality
- `requirements.txt`: Dependencies

### Extending the Application

To add new product types or location types:
1. Modify the `zone_configs` and `location_types` dictionaries in `warehouse_data.py`
2. Update the colors and positions as needed

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built using Streamlit, Plotly, and Pandas
- Inspired by real-world clothing warehouse management needs 
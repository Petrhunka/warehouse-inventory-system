# 3D Warehouse Visualization Application

This Streamlit application provides a 3D visualization of a warehouse layout with inventory data.

## Features

- Interactive 3D visualization of warehouse storage locations
- Distinct visualization of picking areas and overstock locations
- Color-coded representation of stock levels
- Multiple visualization options (PyDeck and Plotly)
- Data filtering capabilities
- Warehouse statistics
- Data export functionality

## Installation

1. Clone this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

To run the application, execute:

```bash
streamlit run app.py
```

The application will open in your default web browser at http://localhost:8501.

## Usage

- Use the sidebar controls to filter data
- Switch between visualization types
- Navigate the 3D visualization using mouse controls:
  - Rotate: drag
  - Zoom: scroll
  - Pan: Shift+drag (PyDeck) or right-click+drag (Plotly)
- View and download data using the data table expander

## Customization

You can modify warehouse parameters:

1. Click "Regenerate Warehouse Data" in the sidebar
2. Adjust the number of rows, columns, and levels
3. Click again to apply changes

## Technology Stack

- Python 3.x
- Streamlit
- Pandas
- NumPy
- Plotly
- PyDeck 
import pandas as pd
import numpy as np
import random
import ast

def generate_realistic_warehouse():
    """Generate a warehouse layout based on a clothing industry warehouse."""
    
    locations = []
    
    # Define zone configurations with clothing industry items
    zone_configs = {
        "A": {"product": "T-shirts", "rows": 2, "cols": 20, "depth": 3, "color": [0, 0, 220]},
        "B": {"product": "Jeans", "rows": 2, "cols": 20, "depth": 3, "color": [0, 0, 200]},
        "C": {"product": "Dresses", "rows": 2, "cols": 20, "depth": 3, "color": [0, 0, 180]},
        "D": {"product": "Sweaters", "rows": 2, "cols": 20, "depth": 3, "color": [0, 0, 160]},
        "E": {"product": "Jackets", "rows": 2, "cols": 20, "depth": 3, "color": [0, 0, 140]},
        "F": {"product": "Shoes", "rows": 2, "cols": 20, "depth": 3, "color": [0, 0, 120]},
        "G": {"product": "Accessories", "rows": 2, "cols": 20, "depth": 3, "color": [0, 0, 100]},
        "H": {"product": "Socks", "rows": 1, "cols": 20, "depth": 3, "color": [100, 0, 100]},
        "J": {"product": "Underwear", "rows": 1, "cols": 20, "depth": 3, "color": [120, 0, 0]},
        "K": {"product": "Premium Apparel", "rows": 6, "cols": 12, "depth": 2, "color": [160, 0, 0]},
        "L": {"product": "Seasonal Items", "rows": 6, "cols": 10, "depth": 3, "color": [180, 0, 0]},
        "M": {"product": "Designer Brands", "rows": 6, "cols": 8, "depth": 2, "color": [200, 0, 0]},
        "N": {"product": "New Arrivals", "rows": 4, "cols": 6, "depth": 1, "color": [0, 120, 0]},
        "P": {"product": "Sale Items", "rows": 6, "cols": 5, "depth": 1, "color": [0, 140, 0]},
        "Q": {"product": "Kids Clothing", "rows": 6, "cols": 5, "depth": 1, "color": [0, 160, 0]},
        "R": {"product": "Plus Size Collection", "rows": 12, "cols": 6, "depth": 1, "color": [0, 180, 0]},
        "S": {"product": "Athletic Wear", "rows": 7, "cols": 10, "depth": 1, "color": [220, 120, 0]},
        "T": {"product": "Returns Processing", "rows": 5, "cols": 3, "depth": 1, "color": [220, 220, 0]},
        "U": {"product": "Outbound Shipping", "rows": 12, "cols": 6, "depth": 2, "color": [0, 220, 0]}
    }
    
    # Define location types based on product categories
    location_types = {
        "T-shirts": "Folded Shelves",
        "Jeans": "Folded Shelves",
        "Dresses": "Hanging Racks",
        "Sweaters": "Folded Shelves",
        "Jackets": "Hanging Racks",
        "Shoes": "Shoe Racks",
        "Accessories": "Small Item Bins",
        "Socks": "Small Item Bins",
        "Underwear": "Small Item Bins",
        "Premium Apparel": "Secure Storage",
        "Seasonal Items": "Bulk Storage",
        "Designer Brands": "Secure Storage",
        "New Arrivals": "Front-Facing Displays",
        "Sale Items": "Sale Racks",
        "Kids Clothing": "Age-Sorted Shelves",
        "Plus Size Collection": "Size-Sorted Racks",
        "Athletic Wear": "Activity-Sorted Racks",
        "Returns Processing": "Sorting Area",
        "Outbound Shipping": "Packing Station"
    }
    
    # Starting positions for each zone
    positions = {
        "A": {"x": 10, "y": 70, "z": 0},
        "B": {"x": 10, "y": 60, "z": 0},
        "C": {"x": 10, "y": 50, "z": 0},
        "D": {"x": 10, "y": 40, "z": 0},
        "E": {"x": 10, "y": 30, "z": 0},
        "F": {"x": 10, "y": 20, "z": 0},
        "G": {"x": 10, "y": 10, "z": 0},
        "H": {"x": 10, "y": 5, "z": 0},
        "J": {"x": 60, "y": 5, "z": 0},
        "K": {"x": 60, "y": 20, "z": 0},
        "L": {"x": 60, "y": 50, "z": 0},
        "M": {"x": 80, "y": 40, "z": 0},
        "N": {"x": 90, "y": 70, "z": 0},
        "P": {"x": 70, "y": 60, "z": 0},
        "Q": {"x": 80, "y": 60, "z": 0},
        "R": {"x": 90, "y": 40, "z": 0},
        "S": {"x": 40, "y": 80, "z": 0},
        "T": {"x": 5, "y": 40, "z": 0},
        "U": {"x": 90, "y": 15, "z": 0}
    }

    # Define sizes for apparel
    sizes = ["XS", "S", "M", "L", "XL", "XXL"]
    shoe_sizes = ["6", "7", "8", "9", "10", "11", "12"]
    
    # Create locations for each zone
    for zone_id, config in zone_configs.items():
        base_x = positions[zone_id]["x"]
        base_y = positions[zone_id]["y"]
        base_z = positions[zone_id]["z"]
        product_type = config["product"]
        location_type = location_types[product_type]
        
        for row in range(1, config["rows"] + 1):
            for col in range(1, config["cols"] + 1):
                for depth in range(1, config["depth"] + 1):
                    # Create location ID - format varies by zone
                    if zone_id in ["K", "L", "M", "N", "P", "Q", "R", "S", "U"]:
                        # These zones have numeric location IDs
                        loc_num = row * 2 - 1  # Odd numbers (101, 103, 105...)
                        loc_id = f"{loc_num + 100}"
                    else:
                        # These zones have alpha-numeric location IDs
                        loc_id = f"{zone_id}-{row:02d}-{col:02d}-{depth}"
                        
                    # Randomly decide if this location has stock
                    has_stock = random.random() > 0.3
                    
                    if has_stock:
                        # Generate a realistic product ID based on item type
                        if product_type == "Shoes":
                            size = random.choice(shoe_sizes)
                            style = random.choice(["Running", "Casual", "Dress", "Sport"])
                            product_id = f"{style}-{size}"
                        else:
                            size = random.choice(sizes)
                            color = random.choice(["Black", "White", "Blue", "Red", "Green", "Gray"])
                            product_id = f"{product_type[:3]}-{color[:3]}-{size}"
                            
                        quantity = random.randint(1, 20)
                    else:
                        product_id = None
                        quantity = 0
                    
                    # Calculate position
                    x = base_x + col * 1.5
                    y = base_y + row * 2
                    z = base_z + depth * 1.5
                    
                    # Add special attributes based on zone
                    attributes = {
                        "product_type": product_type,
                        "color": config["color"]
                    }
                    
                    # Add depth information
                    if zone_id in ["J", "K", "L", "U"]:
                        attributes["depth_info"] = f"{config['depth']}-Deep"
                    else:
                        attributes["depth_info"] = ""  # Ensure empty string instead of None
                    
                    locations.append({
                        "location_id": loc_id,
                        "zone": zone_id,
                        "row": row,
                        "column": col,
                        "depth": depth,
                        "location_type": location_type,
                        "product_id": product_id,
                        "quantity": quantity,
                        "product_type": attributes["product_type"],
                        "x": x,
                        "y": y,
                        "z": z,
                        "color": attributes["color"],
                        "depth_info": attributes["depth_info"]
                    })
    
    # Add receiving dock locations
    for i in range(1, 6):
        loc_id = f"DOCK-{i}"
        locations.append({
            "location_id": loc_id,
            "zone": "DOCK",
            "row": i,
            "column": 1,
            "depth": 1,
            "location_type": "Receiving Dock",
            "product_id": None,
            "quantity": 0,
            "product_type": "Incoming Shipments",
            "x": 2,
            "y": 30 + i * 5,
            "z": 0,
            "color": [255, 255, 0],
            "depth_info": ""
        })
    
    return pd.DataFrame(locations)

def get_warehouse_data():
    """Get or generate warehouse data."""
    
    try:
        # Try to load existing data
        df = pd.read_csv("warehouse_data.csv")
        
        # Ensure product_type is string
        df['product_type'] = df['product_type'].fillna('Unknown')
        
        # Fix color values that might be stored as strings
        def parse_color(color_val):
            if isinstance(color_val, str):
                try:
                    # Try to parse the color string as a list
                    return ast.literal_eval(color_val)
                except (ValueError, SyntaxError):
                    # Default color if parsing fails
                    return [0, 0, 255]
            return color_val
        
        # Check if color column exists and is string type
        if 'color' in df.columns and df['color'].dtype == 'O':
            df['color'] = df['color'].apply(parse_color)
        
        return df
    except:
        # Generate new data
        df = generate_realistic_warehouse()
        # Save for future use
        df.to_csv("warehouse_data.csv", index=False)
        return df 
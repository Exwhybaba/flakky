import pandas as pd
import dash
import dash_table
from dash.dependencies import Input, Output, State
from dash import dcc, html
import random
import string
from datetime import datetime

# Load data
path = r"C:\Users\HomePC\Documents\HTMLcSS\Nutrition\Data\ingredient.csv"
dfx = pd.read_csv(path)
dfx.drop(columns="PRICE/KG", inplace=True)

# Define columns, with Quantity right after INGREDIENT
columns = [
    'INGREDIENT', 'QUANTITY', 'PRICE/KG', 'QUANTITY PRICE', 'DRY MATTER', 'CP', 'FAT', 'FIBRE', 'CAL.', 'PHOS.TOTAL',
    'AVAIL PHOS', 'ME/POULT', 'ME/SWINE', 'METH', 'CYSTINE', 'METH+CYST',
    'LYSINE', 'TRYPTOPHAN', 'THREONINE', 'VIT A IU/GM', 'VIT D3 IU/GM',
    'VIT E IU/GM', 'RIBOFLAVIN', 'PANTO ACID', 'CHOLINE', 'B 12', 'NIACIN',
    'XANTHOPYL', 'SALT', 'SODIUM', 'POTASSIUM', 'MAGNESIUM', 'SULPHUR',
    'MANGANESE', 'IRON', 'COPPER', 'ZINC', 'SELENIUM', 'IODINE', 'LINOLEIC A'
]

df = pd.DataFrame(columns=columns)

#requirement
bird_requirement_data = [
    {'TYPE OF BIRD': 'BROILERS', 'AGE': '0 - 4WKS', 'ME/CP(LB)': 61, 'ME/CP(KG)': 134.81, 'ME': 2950, 'CP': 22, 'ME/CP': 134.0909091},
    {'TYPE OF BIRD': 'BROILERS', 'AGE': '5 - 10WKS', 'ME/CP(LB)': 70, 'ME/CP(KG)': 154.7, 'ME': 3000, 'CP': 19.5, 'ME/CP': 153.8461538},
    {'TYPE OF BIRD': 'CHICKS', 'AGE': '0 - 5WKS', 'ME/CP(LB)': 67, 'ME/CP(KG)': 148.07, 'ME': 2850, 'CP': 21.5, 'ME/CP': 132.5581395},
    {'TYPE OF BIRD': 'GROWING', 'AGE': '6 - 22WKS', 'ME/CP(LB)': 90, 'ME/CP(KG)': 198.9, 'ME': 2750, 'CP': 14.5, 'ME/CP': 189.6551724},
    {'TYPE OF BIRD': 'LAYING & BREEDING', 'AGE': '50% PROD.', 'ME/CP(LB)': 91, 'ME/CP(KG)': 201.11, 'ME': 2750, 'CP': 15, 'ME/CP': 183.3333333},
    {'TYPE OF BIRD': 'LAYING & BREEDING', 'AGE': '60% PROD.', 'ME/CP(LB)': 86, 'ME/CP(KG)': 190.06, 'ME': 2800, 'CP': 16.5, 'ME/CP': 169.6969697},
    {'TYPE OF BIRD': 'LAYING & BREEDING', 'AGE': '70% PROD.', 'ME/CP(LB)': 81, 'ME/CP(KG)': 179.01, 'ME': 2700, 'CP': 15.08, 'ME/CP': 179.0450928},
    {'TYPE OF BIRD': 'LAYING & BREEDING', 'AGE': '80% PROD.', 'ME/CP(LB)': 76, 'ME/CP(KG)': 167.96, 'ME': 2550, 'CP': 16.5, 'ME/CP': 154.5454545},
    {'TYPE OF BIRD': 'LAYING & BREEDING', 'AGE': '90% PROD.', 'ME/CP(LB)': 70, 'ME/CP(KG)': 154.7, 'ME': 2550, 'CP': 16.5, 'ME/CP': 154.5454545}
]

vitamins_minerals_data = [
    {"Category": "VITAMINS", "Name": "Vitamin A", "Source": "Vitamin A 500", "Potency (Min)": "500,000 iu/g"},
    {"Category": "VITAMINS", "Name": "", "Source": "Vitamin AD3 500/100", "Potency (Min)": "500,000iu/g of Vit A; 100,000iu/g of Vit D3"},
    {"Category": "VITAMINS", "Name": "", "Source": "Vitamin AD3 1000/200", "Potency (Min)": "1,000,000,000iu/g of Vit A; 200,000iu/g of Vit D3"},
    {"Category": "VITAMINS", "Name": "Vitamin D", "Source": "Vitamin D3", "Potency (Min)": "500,000iu/g"},
    {"Category": "VITAMINS", "Name": "", "Source": "Vitamin AD3", "Potency (Min)": "500,000iu/g of Vit A; 100,000iu/g of Vit D3"},
    {"Category": "VITAMINS", "Name": "", "Source": "VITAMIN AD3", "Potency (Min)": "1,000,000,000iu/g of Vit A; 200,000iu/g of Vit D3"},
    {"Category": "VITAMINS", "Name": "Vitamin E", "Source": "Vitamin E 50", "Potency (Min)": "500 iu /g"},
    {"Category": "VITAMINS", "Name": "Vitamin K", "Source": "Vitamin K3", "Potency (Min)": "50%"},
    {"Category": "VITAMINS", "Name": "Vitamin B2 (Riboflavin)", "Source": "Vitamin B2", "Potency (Min)": "80%"},
    {"Category": "VITAMINS", "Name": "Vitamin B12", "Source": "Vitamin B12", "Potency (Min)": "1%"},
    {"Category": "VITAMINS", "Name": "Vitamin B6 (Pyridoxine HCL)", "Source": "Vitamin B6", "Potency (Min)": "100%"},
    {"Category": "VITAMINS", "Name": "Nicotinic Acid", "Source": "Nicotinic Acid", "Potency (Min)": "100%"},
    {"Category": "VITAMINS", "Name": "", "Source": "Nicotinamide", "Potency (Min)": "100%"},
    {"Category": "VITAMINS", "Name": "Folic Acid", "Source": "Folic Acid", "Potency (Min)": "45%"},
    {"Category": "VITAMINS", "Name": "", "Source": "Folic Acid", "Potency (Min)": "95%"},
    {"Category": "VITAMINS", "Name": "Panthothenic Acid", "Source": "Calcium Pantothenate", "Potency (Min)": "80%"},
    {"Category": "VITAMINS", "Name": "", "Source": "", "Potency (Min)": "98%"},
    {"Category": "VITAMINS", "Name": "Biotin", "Source": "Biotin", "Potency (Min)": "2%"},
    {"Category": "VITAMINS", "Name": "", "Source": "", "Potency (Min)": "5%"},
    {"Category": "VITAMINS", "Name": "", "Source": "", "Potency (Min)": "10%"},
    {"Category": "VITAMINS", "Name": "Thiamine (Vitamin B1)", "Source": "Thiamine", "Potency (Min)": "98%"},
    {"Category": "VITAMINS", "Name": "Vitamin C", "Source": "Vitamin C (Aqua)", "Potency (Min)": "35%"},
    {"Category": "VITAMINS", "Name": "", "Source": "Vitamin C (Coated)", "Potency (Min)": "98-100"},
    {"Category": "VITAMINS", "Name": "Choline", "Source": "Choline Chloride", "Potency (Min)": "50%"},
    {"Category": "VITAMINS", "Name": "", "Source": "", "Potency (Min)": "60%"},
    {"Category": "VITAMINS", "Name": "", "Source": "", "Potency (Min)": "70%"},
    {"Category": "VITAMINS", "Name": "", "Source": "", "Potency (Min)": "80%"},
    {"Category": "MICRO MINERALS", "Name": "Iodine", "Source": "Potassium Iodide", "Potency (Min)": "59%"},
    {"Category": "MICRO MINERALS", "Name": "Copper", "Source": "Copper Sulphate", "Potency (Min)": "25%"},
    {"Category": "MICRO MINERALS", "Name": "", "Source": "Organic Copper", "Potency (Min)": ""},
    {"Category": "MICRO MINERALS", "Name": "Manganese", "Source": "Manganese Oxide", "Potency (Min)": "57%"},
    {"Category": "MICRO MINERALS", "Name": "", "Source": "Manganese Sulphate", "Potency (Min)": "31%"},
    {"Category": "MICRO MINERALS", "Name": "", "Source": "Organic Manganese", "Potency (Min)": ""},
    {"Category": "MICRO MINERALS", "Name": "Zinc", "Source": "Zinc Oxide", "Potency (Min)": "78%"},
    {"Category": "MICRO MINERALS", "Name": "", "Source": "Zinc Sulphate", "Potency (Min)": "35%"},
    {"Category": "MICRO MINERALS", "Name": "", "Source": "Zinc", "Potency (Min)": ""},
    {"Category": "MICRO MINERALS", "Name": "", "Source": "Organic Zinc", "Potency (Min)": ""},
    {"Category": "MICRO MINERALS", "Name": "Iron", "Source": "Ferrous Carbonate", "Potency (Min)": "36%"},
    {"Category": "MICRO MINERALS", "Name": "", "Source": "Ferrous Sulphate", "Potency (Min)": "30%"},
    {"Category": "MICRO MINERALS", "Name": "Selenium", "Source": "Sodium Selenite", "Potency (Min)": "45%"},
    {"Category": "MICRO MINERALS", "Name": "", "Source": "Organic Selenium", "Potency (Min)": ""},
    {"Category": "MICRO MINERALS", "Name": "Cobalt", "Source": "", "Potency (Min)": "20%"},
    {"Category": "Antioxidant", "Name": "", "Source": "Butyl Hydeoxy", "Potency (Min)": ""},
    {"Category": "Antioxidant", "Name": "", "Source": "Toluene (BHT)", "Potency (Min)": "100%"},
    {"Category": "Antioxidant", "Name": "", "Source": "BHA", "Potency (Min)": "100%"},
    {"Category": "Preservatives/Anticaking agents", "Name": "", "Source": "Silica", "Potency (Min)": ""},
    {"Category": "Yolk Colorant", "Name": "", "Source": "Caropyhl", "Potency (Min)": ""},
    {"Category": "Yolk Colorant", "Name": "", "Source": "Lucantin", "Potency (Min)": ""}
]

#USER_PASS_MAPPING = {
    #"admin1": "admin12345",
    #"admin2": "@admin12345"
#}

 # Ensure numeric columns are correctly converted to numeric types
numeric_cols = ['QUANTITY', 'PRICE/KG', 'QUANTITY PRICE', 'DRY MATTER', 'CP', 'FAT', 'FIBRE', 'CAL.', 
                    'PHOS.TOTAL', 'AVAIL PHOS', 'ME/POULT', 'ME/SWINE', 'METH', 'CYSTINE', 'METH+CYST',
                    'LYSINE', 'TRYPTOPHAN', 'THREONINE', 'VIT A IU/GM', 'VIT D3 IU/GM',
                    'VIT E IU/GM', 'RIBOFLAVIN', 'PANTO ACID', 'CHOLINE', 'B 12', 'NIACIN',
                    'XANTHOPYL', 'SALT', 'SODIUM', 'POTASSIUM', 'MAGNESIUM', 'SULPHUR',
                    'MANGANESE', 'IRON', 'COPPER', 'ZINC', 'SELENIUM', 'IODINE', 'LINOLEIC A']
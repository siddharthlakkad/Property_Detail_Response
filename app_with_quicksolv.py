import streamlit as st
import requests
from collections import OrderedDict

# --- Config ---
API_URL = "https://api.realestateapi.com/v2/PropertyDetail"
API_KEY = "REVANTAGE-9c02-795b-8294-dd20eef4a809"

# --- App UI ---
st.set_page_config(page_title="Property Detail Lookup", layout="wide")
st.title("🏡 Real Estate Property Detail Lookup")

# --- Sidebar Form ---
st.sidebar.header("🔍 Search Property")
with st.sidebar.form("search_form"):
    house = st.text_input("House Number", "17")
    street = st.text_input("Street Name", "Topeka Pass")
    city = st.text_input("City", "Willingboro")
    state = st.text_input("State (e.g., NJ)", "NJ")
    zip_code = st.text_input("ZIP Code", "08046")
    comps = st.checkbox("Include Comparable Listings", False)
    submit = st.form_submit_button("Search")

# --- Field Sections ---
FIELD_GROUPS = OrderedDict({
    "🏠 Basic Info": {
        "propertyType": "Property Type",
        "propertyUse": "Property Use",
        "propertyUseCode": "Property Use Code",
        "zoning": "Zoning",
        "subdivision": "Subdivision",
        "yearBuilt": "Year Built",
        "granteeName": "Grantee Name",
        "lenderName": "Lender Name",
        "mortgageId": "Mortgage ID",
        "lastSaleDate": "Last Sale Date",
    },
    "💰 Valuation & Equity": {
        "equity": "Equity",
        "equityPercent": "Equity Percent",
        "estimatedEquity": "Estimated Equity",
        "pricePerSquareFoot": "Price Per Square Foot",
    },
    "🌊 Flood Zone": {
        "floodZone": "Flood Zone",
        "floodZoneType": "Flood Zone Type",
        "floodZoneDescription": "Flood Zone Description",
    },
    "📐 Lot & Location": {
        "lotAcres": "Lot Acres",
        "lotNumber": "Lot Number",
        "lotSquareFeet": "Lot Square Feet",
        "lotDepthFeet": "Lot Depth Feet",
        "livingSquareFeet": "Living Square Feet",
        "buildingSquareFeet": "Building Square Feet",
        "parcelAccountNumber": "Parcel Account Number",
        "latitude": "Latitude",
        "longitude": "Longitude",
    },
    "🚗 Parking & Garage": {
        "carport": "Carport",
        "garageSquareFeet": "Garage Square Feet",
        "garageType": "Garage Type",
        "parkingSpaces": "Parking Spaces",
        "roomsCountrvParking": "Rooms Count RV Parking",
    },
    "🏗️ Structure & Features": {
        "construction": "Construction",
        "deck": "Deck",
        "deckArea": "Deck Area",
        "featureBalcony": "Balcony Feature",
        "fireplace": "Fireplace",
        "fireplaces": "Fireplaces",
        "interiorStructure": "Interior Structure",
        "partialBathrooms": "Partial Bathrooms",
        "patioArea": "Patio Area",
        "plumbingFixturesCount": "Plumbing Fixtures Count",
        "pool": "Pool",
        "poolArea": "Pool Area",
        "porchArea": "Porch Area",
        "porchType": "Porch Type",
        "roofConstruction": "Roof Construction",
        "roofMaterial": "Roof Material",
        "stories": "stories",
        "taxExemptionHomeownerFlag": "tax Exemption Home owner Flag",

    },
    "🔥 Utilities & Safety": {
        "heatingFuelType": "Heating Fuel Type",
        "heatingType": "Heating Type",
        "hoa": "HOA",
        "safetyFireSprinklers": "Safety Fire Sprinklers",
        "utilitiesSewageUsage": "Sewage Usage",
        "utilitiesWaterSource": "Water Source",
    },
    "🏘️ Other": {
        "unitsCount": "Units Count",
    },
})

# --- Helpers ---
def flatten_dict(d, parent_key='', sep='.'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def extract_field_value(flat_data, field_name):
    for key, val in flat_data.items():
        if key.lower().endswith(field_name.lower()):
            return val
    return None

def show_field(label, value):
    display_val = value if value not in [None, ""] else "N/A"
    color = "green" if display_val != "N/A" else "gray"
    st.markdown(f"**{label}:** <span style='color:{color}'>{display_val}</span>", unsafe_allow_html=True)

# --- API Call ---
if submit:
    with st.spinner("Fetching property details..."):
        full_address = f"{house} {street}, {city}, {state} {zip_code}"

        payload = {
            "address": full_address,
            "comps": comps
        }

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "x-user-id": API_KEY,
            "x-api-key": API_KEY
        }

        response = requests.post(API_URL, json=payload, headers=headers)

        if response.status_code == 200:
            result = response.json()
            data = result.get("data", {})
            flat_data = flatten_dict(data)

            st.success("✅ Property Details Found!")

            # --- Show each group ---
            for section_title, fields in FIELD_GROUPS.items():
                st.subheader(section_title)
                for key, label in fields.items():
                    val = extract_field_value(flat_data, key)
                    show_field(label, val)

            # --- Raw JSON ---
            with st.expander("📦 Full Raw API Response"):
                st.json(result)
        else:
            st.error(f"❌ Failed to fetch data (Status Code: {response.status_code})")
            st.code(response.text)

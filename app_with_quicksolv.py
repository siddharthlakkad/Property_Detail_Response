import streamlit as st
import requests

# --- Config ---
API_URL = "https://api.realestateapi.com/v2/PropertyDetail"
API_KEY = "REVANTAGE-9c02-795b-8294-dd20eef4a809"

# --- App UI ---
st.set_page_config(page_title="Property Detail Lookup", layout="wide")
st.title("🏡 Real Estate Property Detail Lookup")

# --- Sidebar Search Form ---
st.sidebar.header("🔍 Search Property")
with st.sidebar.form("search_form"):
    house = st.text_input("House Number", "17")
    street = st.text_input("Street Name", "Topeka Pass")
    city = st.text_input("City", "Willingboro")
    state = st.text_input("State (e.g., NJ)", "NJ")
    zip_code = st.text_input("ZIP Code", "08046")
    comps = st.checkbox("Include Comparable Listings", False)
    submit = st.form_submit_button("Search")

# --- Perform API Request ---
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

            st.success("✅ Property Details Found!")

            def show_field(label, value):
                """Show all fields: green if exists, gray if N/A"""
                display_val = value if value not in [None, ""] else "N/A"
                color = "green" if display_val != "N/A" else "gray"
                st.markdown(f"**{label}:** <span style='color:{color}'>{display_val}</span>", unsafe_allow_html=True)

            st.subheader("🏠 Basic Property Info")
            show_field("Property Type", data.get("propertyType"))
            show_field("Property Use", data.get("propertyUse"))
            show_field("Property Use Code", data.get("propertyUseCode"))
            show_field("Zoning", data.get("zoning"))
            show_field("Subdivision", data.get("subdivision"))
            show_field("Year Built", data.get("yearBuilt"))
            show_field("Grantee Name", data.get("granteeName"))
            show_field("Lender Name", data.get("lenderName"))
            show_field("Mortgage ID", data.get("mortgageId"))
            show_field("Last Sale Date", data.get("lastSaleDate"))

            st.subheader("💰 Valuation & Equity")
            show_field("Equity", data.get("equity"))
            show_field("Equity Percent", f"{data.get('equityPercent')}%" if data.get("equityPercent") else None)
            show_field("Estimated Equity", data.get("estimatedEquity"))
            show_field("Price Per Square Foot", data.get("pricePerSquareFoot"))

            st.subheader("🌊 Flood Zone")
            show_field("Flood Zone", data.get("floodZone"))
            show_field("Flood Zone Type", data.get("floodZoneType"))
            show_field("Flood Zone Description", data.get("floodZoneDescription"))

            st.subheader("📐 Lot & Building Info")
            show_field("Lot Acres", data.get("lotAcres"))
            show_field("Lot Number", data.get("lotNumber"))
            show_field("Lot Square Feet", data.get("lotSquareFeet"))
            show_field("Lot Depth Feet", data.get("lotDepthFeet"))
            show_field("Living Square Feet", data.get("livingSquareFeet"))
            show_field("Building Square Feet", data.get("buildingSquareFeet"))
            show_field("Parcel Account Number", data.get("parcelAccountNumber"))
            show_field("Latitude", data.get("latitude"))
            show_field("Longitude", data.get("longitude"))

            st.subheader("🚗 Parking & Garage")
            show_field("Carport", data.get("carport"))
            show_field("Garage Square Feet", data.get("garageSquareFeet"))
            show_field("Garage Type", data.get("garageType"))
            show_field("Parking Spaces", data.get("parkingSpaces"))
            show_field("Rooms Count RV Parking", data.get("roomsCountrvParking"))

            st.subheader("🏗️ Structure & Features")
            show_field("Construction", data.get("construction"))
            show_field("Deck", data.get("deck"))
            show_field("Deck Area", data.get("deckArea"))
            show_field("Balcony Feature", data.get("featureBalcony"))
            show_field("Fireplace", data.get("fireplace"))
            show_field("Fireplaces", data.get("fireplaces"))
            show_field("Interior Structure", data.get("interiorStructure"))
            show_field("Partial Bathrooms Patio", data.get("partialBathroomspatio"))
            show_field("Patio Area", data.get("patioArea"))
            show_field("Plumbing Fixtures Count", data.get("plumbingFixturesCount"))
            show_field("Pool", data.get("pool"))
            show_field("Pool Area", data.get("poolArea"))
            show_field("Porch Area", data.get("porchArea"))
            show_field("Porch Type", data.get("porchType"))
            show_field("Stories Tax Exemption Homeowner Flag", data.get("storiestaxExemptionHomeownerFlag"))

            st.subheader("🔥 Utilities & Safety")
            show_field("Heating Fuel Type", data.get("heatingFuelType"))
            show_field("Heating Type", data.get("heatingType"))
            show_field("HOA", data.get("hoa"))
            show_field("Safety Fire Sprinklers", data.get("safetyFireSprinklers"))
            show_field("Sewage Usage", data.get("utilitiesSewageUsage"))
            show_field("Water Source", data.get("utilitiesWaterSource"))

            st.subheader("🏘️ Other")
            show_field("Units Count", data.get("unitsCount"))

            with st.expander("📦 Full Raw API Response"):
                st.json(result)

        else:
            st.error(f"❌ Failed to fetch data (Status Code: {response.status_code})")
            st.code(response.text)

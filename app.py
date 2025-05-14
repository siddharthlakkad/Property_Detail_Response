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
        # ✅ Build full address string
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

            st.subheader("🏠 Property Summary")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Property Type:** {data.get('propertyType', 'N/A')}")
                st.markdown(f"**Owner Occupied:** {data.get('ownerOccupied')}")
                st.markdown(f"**Last Sale Price:** ${data.get('lastSalePrice', 'N/A')}")
                st.markdown(f"**Last Sale Date:** {data.get('lastSaleDate', 'N/A')}")
            with col2:
                st.markdown(f"**Estimated Value:** ${data.get('estimatedValue', 'N/A')}")
                st.markdown(f"**Estimated Equity:** ${data.get('estimatedEquity', 'N/A')}")
                st.markdown(f"**Equity Percent:** {data.get('equityPercent', 'N/A')}%")

            st.subheader("🏦 Mortgage & Liens")
            st.markdown(f"- **Open Mortgage Balance:** ${data.get('openMortgageBalance', 0)}")
            st.markdown(f"- **Adjustable Rate:** {data.get('adjustableRate')}")
            st.markdown(f"- **Tax Lien:** {data.get('taxLien')}")
            st.markdown(f"- **Foreclosure Info:** {bool(data.get('foreclosureInfo'))}")

            st.subheader("🧾 Ownership Flags")
            flags = [
                "absenteeOwner", "bankOwned", "cashBuyer", "corporateOwned", "death", "inherited", "trusteeSale",
                "sheriffsDeed", "quitClaim", "spousalDeath", "vacant"
            ]
            for flag in flags:
                st.markdown(f"- **{flag}:** {data.get(flag)}")

            if "demographics" in data:
                st.subheader("📊 Local Demographics")
                demo = data["demographics"]
                st.markdown(f"- **Median Income:** ${demo.get('medianIncome')}")
                st.markdown(f"- **Suggested Rent:** ${demo.get('suggestedRent')}")
                st.markdown(f"- **HUD Area:** {demo.get('hudAreaName')} ({demo.get('hudAreaCode')})")
                st.markdown(f"- **Fair Market Rent (3 Bedroom):** ${demo.get('fmrThreeBedroom')}")

            if comps and data.get("comps"):
                st.subheader("📈 Comparable Listings")
                for idx, comp in enumerate(data["comps"], 1):
                    st.markdown(f"**Comp #{idx}**")
                    st.json(comp)

            with st.expander("📦 Full API Response"):
                st.json(result)

        else:
            st.error(f"❌ Failed to fetch data (Status Code: {response.status_code})")
            st.code(response.text)

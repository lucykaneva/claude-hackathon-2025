import streamlit as st
import base64
from database import get_available_gifts, claim_gift, get_all_requests

st.set_page_config(page_title="Browse Items", page_icon="🎁", layout="wide")

st.title("🎁 Available Gifts")
st.write("Browse donated items looking for loving homes!")

st.markdown("---")

# Filters
col1, col2, col3 = st.columns(3)

with col1:
    category_filter = st.selectbox(
        "Category",
        ["All", "toy", "clothing", "book", "game", "sports", "educational", "other"]
    )

with col2:
    age_filter = st.selectbox(
        "Age Range",
        ["All", "0-2", "3-5", "6-8", "9-12", "teen"]
    )

with col3:
    sort_by = st.selectbox(
        "Sort By",
        ["Newest First", "Highest Quality", "Lowest Quality"]
    )

# Get items
items = get_available_gifts()

# Apply filters
if category_filter != "All":
    items = [item for item in items if item['gift_type'] == category_filter]

if age_filter != "All":
    items = [item for item in items if item['age_range'] == age_filter]

# Apply sorting
if sort_by == "Highest Quality":
    items = sorted(items, key=lambda x: x['quality_score'], reverse=True)
elif sort_by == "Lowest Quality":
    items = sorted(items, key=lambda x: x['quality_score'])

st.markdown("---")

# Display results
st.subheader(f"Found {len(items)} items")

if len(items) == 0:
    st.info("No items match your filters. Try adjusting your search!")
else:
    # Display in grid (3 columns)
    cols = st.columns(3)
    
    for idx, item in enumerate(items):
        with cols[idx % 3]:
            # Display image
            try:
                image_data = base64.b64decode(item['photo_base64'])
                st.image(image_data, use_container_width=True)
            except:
                st.write("📦 [Image]")
            
            # Item details
            st.write(f"**{item['gift_name']}**")
            st.write(f"{item['gift_description'][:100]}...")
            
            # Tags
            tag_col1, tag_col2 = st.columns(2)
            with tag_col1:
                st.caption(f"🎯 Age: {item['age_range']}")
            with tag_col2:
                st.caption(f"⭐ Quality: {item['quality_score']}/10")
            
            st.caption(f"📍 Location: {item['donor_address']}")
            
            # Claim button
            if st.button(f"Claim This Item", key=f"claim_{item['id']}"):
                # Check if user has any requests
                requests = get_all_requests()
                if len(requests) == 0:
                    st.warning("⚠️ Please create a request first (go to Request page)")
                else:
                    # For simplicity, claim with first request
                    # In full version, let user choose which child
                    claim_gift(item['id'], requests[0]['id'])
                    st.success("✅ Item claimed! Check your email for donor contact info.")
                    st.rerun()
            
            st.markdown("---")

st.markdown("---")
st.info("💡 **Need help?** Contact us if you have questions about any items!")
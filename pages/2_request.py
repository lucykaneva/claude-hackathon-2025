import streamlit as st
from database import add_request, get_all_requests
from claude_helper import match_gifts_to_request
from database import get_available_gifts
import base64

st.set_page_config(page_title="Request Gifts", page_icon="🎄")

st.title("Request and Find a Perfect Gift!")
st.write("Tell us about your kid and we'll help match them with the perfect gift!")

st.markdown("---")

# Show existing requests
my_requests = get_all_requests()
if len(my_requests) > 0:
    with st.expander("📋 Your Existing Requests"):
        for req in my_requests:
            st.write(f"**Child {req['id']}:** Age {req['child_age']}, Interests: {req['child_interests']}")

st.markdown("---")

with st.form("request_form"):
    st.subheader("Your Information")
    
    col1, col2 = st.columns(2)
    with col1:
        recipient_name = st.text_input("Your Name*", placeholder="Jane Smith")
    with col2:
        recipient_contact = st.text_input("Contact*", placeholder="jane@email.com")
    
    recipient_location = st.text_input("Zip Code*", placeholder="14850")
    
    st.subheader("About Your Child")
    
    child_age = st.number_input("Child's Age*", min_value=0, max_value=18, value=7)
    
    child_interests = st.text_area(
        "Child's Interests*",
        placeholder="e.g., loves dinosaurs, building blocks, art, reading...",
        help="The more details, the better we can match!"
    )
    
    specific_needs = st.text_area(
        "Specific Needs (optional)",
        placeholder="e.g., needs size 8 clothing, prefers quiet toys, has allergies to certain materials..."
    )
    
    submit_button = st.form_submit_button("🚀 Submit Request")
    
    if submit_button:
        if not recipient_name or not recipient_contact or not recipient_location or not child_interests:
            st.error("❌ Please fill in all required fields")
        else:
            # Save request
            request_data = {
                'recipient_name': recipient_name,
                'recipient_contact': recipient_contact,
                'recipient_address': recipient_location,
                'child_age': child_age,
                'child_interests': child_interests,
                'specific_needs': specific_needs or 'None'
            }
            
            request_id = add_request(request_data)
            
            st.success(f"✅ Request submitted! (ID: {request_id})")
            st.balloons()
            
            # Show AI matches
            with st.spinner("🤖 Finding perfect matches..."):
                available_items = get_available_gifts()
                
                if len(available_items) > 0:
                    matches = match_gifts_to_request(request_data, available_items)
                    
                    if matches:
                        st.subheader("🎁 Recommended Matched Gifts!")
                        
                        for match in matches[:5]:  # Top 5
                            if 'gift' in match:
                                item = match['gift']
                                
                                with st.container():
                                    col1, col2 = st.columns([1, 2])
                                    
                                    with col1:
                                        try:
                                            image_data = base64.b64decode(item['photo_base64'])
                                            st.image(image_data, use_container_width=True)
                                        except:
                                            st.write("📦")
                                    
                                    with col2:
                                        st.write(f"**{item['gift_name']}**")
                                        st.write(f"Match Score: {match['match_score']}/100")
                                        st.write(f"_{match['reason']}_")
                                        st.caption(f"Quality: {item['quality_score']}/10 | Age: {item['age_range']}")
                                    
                                    st.markdown("---")
                else:
                    st.info("No items available yet. Check back soon!")

st.markdown("---")
st.info("💡 You'll be notified when items matching your request become available!")
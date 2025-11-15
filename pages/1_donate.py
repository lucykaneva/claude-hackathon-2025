import streamlit as st
import base64
from database import add_gift
from claude_helper import assess_gift_from_image

st.set_page_config(page_title="Donate Item", page_icon="📦")

st.title("📦 Donate an Item")
st.write("Share different types of items in good condition!")

st.markdown("---")

with st.form("donate_form"):
    st.subheader("Your Information")
    
    col1, col2 = st.columns(2)
    with col1:
        donor_name = st.text_input("Your Name*", placeholder="John Doe")
    with col2:
        donor_contact = st.text_input("Contact (Email or Phone)*", placeholder="john@email.com")
    
    donor_location = st.text_input("Zip Code*", placeholder="14850")
    
    st.subheader("Item Information")
    
    uploaded_file = st.file_uploader(
        "Upload a clear photo of the item*",
        type=['jpg', 'jpeg', 'png'],
        help="Take a well-lit photo showing the item's condition"
    )
    
    if uploaded_file:
        st.image(uploaded_file, caption="Your uploaded photo", width=300)
    
    additional_notes = st.text_area(
        "Additional notes (optional)",
        placeholder="Any extra details about the item..."
    )
    
    submit_button = st.form_submit_button("🚀 Submit Item for Review")
    
    if submit_button:
        # Validation
        if not donor_name or not donor_contact or not donor_location:
            st.error("❌ Please fill in all required fields marked with *")
        elif not uploaded_file:
            st.error("❌ Please upload a photo of the item")
        else:
            # Process the donation
            with st.spinner("🤖 Claude AI is analyzing your item..."):
                # Convert image to base64
                image_bytes = uploaded_file.read()
                image_base64 = base64.b64encode(image_bytes).decode()
                
                # Determine image type
                image_type = f"image/{uploaded_file.type.split('/')[-1]}"
                
                # Get Claude assessment
                assessment = assess_gift_from_image(image_base64, image_type)
                
                st.subheader("🔍 AI Assessment Results")
                
                if assessment['recommendation'] == 'approve':
                    st.success("✅ Item Approved!")
                    
                    # Display assessment
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Item:** {assessment['gift_name']}")
                        st.write(f"**Category:** {assessment['category']}")
                        st.write(f"**Age Range:** {assessment['age_range']}")
                    with col2:
                        st.write(f"**Quality Score:** {assessment['quality_score']}/10")
                        st.write(f"**Safety:** {assessment['safety_concerns']}")
                    
                    st.write(f"**Description:** {assessment['description']}")
                    
                    # Save to database
                    item_data = {
                        'donor_name': donor_name,
                        'donor_contact': donor_contact,
                        'donor_address': donor_location,
                        'gift_name': assessment['gift_name'],
                        'gift_description': assessment['description'],
                        'gift_type': assessment['category'],
                        'photo_base64': image_base64,
                        'age_range': assessment['age_range'],
                        'quality_score': assessment['quality_score']
                    }
                    
                    item_id = add_gift(item_data)
                    
                    st.balloons()
                    st.success(f"🎉 Thank you! Your item (ID: {item_id}) has been added and is now available for families to claim!")
                    st.info("💡 You'll be contacted when someone claims your item.")
                    
                else:
                    st.error("❌ Item Not Approved")
                    st.write(f"**Reason:** {assessment.get('rejection_reason', 'Quality or safety concerns')}")
                    st.write("Please try uploading a different item in better condition.")

st.markdown("---")
st.info("💡 **Tips for great donations:**\n- Clean items before photographing\n- Take photos in good lighting\n- Show any wear or damage clearly\n- Only donate items in good working condition")
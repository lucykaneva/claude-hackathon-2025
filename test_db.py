from database import add_gift, get_available_gifts

test_item = {
    'donnor_name': 'LK',
    'donnor_contact': '09',
    'donor_address': '123 Charity St, Kindness City',
    'gift_name': 'Winter Jacket',
    'gift_description': 'A warm winter jacket for kids.',
    'photo_base64': 'base64encodedstring',  
    'quality_score': 8
}

item_id = add_gift(test_item)
print(f"Added item with ID: {item_id}")
print(get_available_gifts())
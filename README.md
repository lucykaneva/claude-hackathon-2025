# Christmas Gift Circle
## Overview
Our app enables users to easily donate used belongings in good conditions to children whose families can’t afford buying them a Christmas present. Donaters fill out their information (name, email, zipcode) and upload a picture of the item that they would like to donate. Then the Claude API analyzes the picture, creates a product description, assesses its quality and the appropriate age range that the product is suitable for. Users in need can fill information about their child (age and interests) and see the top 5 matched gifts that Claude API suggests. Users in need can then claim their chosen gift by searching it in the Browse page and receive the contact information of the donor. 
## Setup instruction
Follow this link: —
## Usage guide
Go to the requests page and fill out a child’s information. Using the Claude assistant, the application will display a list with the 5 most suitable gifts, including information about interest match score, quality and age range. Each of the matching gifts will have an id. After you pick a gift, you will go to the Browse page, search the item by id, click the claim button for this item and receive the donor contact information. 
## Development Stack
Technologies used: Python, Claude API, SQLite, Streamlit
## Claude Integration
The Claude API analyzes a picture of the item that the donor uploads and assesses its quality, the age range that it is suitable for, its category (book, toy, clothing, sports, other) and any related safe concerns. If the photo doesn’t contain an item, the quality is too low or the assistant identified major safety concerns, then the donation submission is rejected. Otherwise, it is approved and users in need can view the item in the Browse page.

The matching functionality of the app also integrates Claude API. After a user fills out a request with their child’s age and interest, the AI assistant assigns a matching score to the available items and the app displays the top 5 gift options. The user then can claim the gift and receive the contact information of the donor.
## Challenges and Solutions
One of the biggest challenges that we faced was making Claude send back data in an appropriate format that we can then extract and insert into the data base. After debugging and doing a little bit of research we managed to get teh appropriate data format from Claude and update the corresponding fields in our data base.
## Future Plans
With more time, we would make our UI more user-friendly and polished. We would increase the functionality of the app by adding browsing based on location and the ability for donors to view families in need near them. We would create user authorization and specific account information which helps donors track their donations and received requests. 

**Created by: Harini Dave and Lyudmila Kaneva**


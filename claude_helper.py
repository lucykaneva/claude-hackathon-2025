import anthropic
import os
import json
import base64
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def assess_gift_from_image(image_base64, image_type="image/jpeg"):
    """
    Analyze uploaded gift photo using Claude Vision
    Returns: dict with gift details and quality assessment
    """
    
    prompt = """Analyze this donated gift photo for a gift-matching platform.

Please provide:
1. gift name and description (what is it exactly?)
2. Quality score (1-10, where 10 is like-new condition)
   - Look for: wear, damage, missing pieces, stains, functionality
3. Age appropriateness (choose ONE: "0-2", "3-5", "6-8", "9-12", "teen")
4. gift category (choose ONE: "toy", "clothing", "book", "game", "sports", "educational", "other")
5. Safety concerns (if any - broken parts, choking hazards, etc.)
6. Recommendation: "approve" or "reject"
   - Reject if: poor quality (below 5/10), safety issues, inappropriate content

Respond in JSON format:
{
  "gift_name": "specific name",
  "description": "2-3 sentence appealing description",
  "quality_score": 0,
  "age_range": "X-Y",
  "category": "category name",
  "safety_concerns": "any issues or 'none'",
  "recommendation": "approve or reject",
  "rejection_reason": "why rejected, if applicable"
}"""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": image_type,
                            "data": image_base64,
                        },
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ],
            }],
        )
        
        # Parse response
        response_text = message.content[0].text
        
        # Extract JSON (Claude sometimes wraps in markdown)
        if "```json" in response_text:
            json_str = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            json_str = response_text.split("```")[1].split("```")[0].strip()
        else:
            json_str = response_text.strip()
        
        result = json.loads(json_str)
        return result
        
    except Exception as e:
        print(f"Error in Claude assessment: {e}")
        return {
            "gift_name": "Unknown gift",
            "description": "Could not analyze image",
            "quality_score": 5,
            "age_range": "6-8",
            "category": "other",
            "safety_concerns": "Could not assess",
            "recommendation": "reject",
            "rejection_reason": f"Error: {str(e)}"
        }

def match_gifts_to_request(request_info, available_gifts):
    """
    Match available gifts to a child's request using Claude
    Returns: list of matched gifts with scores and reasoning
    """
    
    # Format gifts for Claude
    gifts_text = ""
    for idx, gift in enumerate(available_gifts):
        gifts_text += f"\ngift {idx}:\n"
        gifts_text += f"  Name: {gift['gift_name']}\n"
        gifts_text += f"  Description: {gift['description']}\n"
        gifts_text += f"  Category: {gift['gift_type']}\n"
        gifts_text += f"  Age Range: {gift['age_range']}\n"
        gifts_text += f"  Quality: {gift['quality_score']}/10\n"
    
    prompt = f"""You are helping match donated gifts to children in need.

Child Profile:
- Age: {request_info['child_age']} years old
- Interests: {request_info['child_interests']}
- Specific needs: {request_info.get('specific_needs', 'None specified')}

Available gifts:
{gifts_text}

Task: Select the top 5 best matches for this child and rank them.
Consider:
- Age appropriateness
- Match with interests
- Quality of gift
- Developmental value

Respond in JSON format:
[
  {{
    "gift_index": 0,
    "match_score": 85,
    "reason": "Brief explanation of why this is a good match"
  }}
]

Return ONLY the JSON array, nothing else."""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2048,
            messages=[{
                "role": "user",
                "content": prompt
            }],
        )
        
        response_text = message.content[0].text
        
        # Extract JSON
        if "```json" in response_text:
            json_str = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            json_str = response_text.split("```")[1].split("```")[0].strip()
        else:
            json_str = response_text.strip()
        
        matches = json.loads(json_str)
        
        # Add full gift data to matches
        for match in matches:
            gift_idx = match['gift_index']
            if gift_idx < len(available_gifts):
                match['gift'] = available_gifts[gift_idx]
        
        return matches
        
    except Exception as e:
        print(f"Error in matching: {e}")
        return []

# Test function
def test_claude():
    """Test if Claude API is working"""
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=100,
        messages=[{
            "role": "user",
            "content": "Say 'Claude API is working!' and nothing else."
        }]
    )
    return message.content[0].text

if __name__ == "__main__":
    print(test_claude())

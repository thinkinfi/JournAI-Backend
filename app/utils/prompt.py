import google.generativeai as genai
from typing import List, Dict
import os
import json

# Configure the Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

async def generate_trip_plan(destinations: List[str], total_budget: float, total_duration: int, interests: List[str]) -> Dict:
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    Generate a detailed trip plan for the following destinations: {', '.join(destinations)}.
    Total budget: ${total_budget} INR
    Total duration: {total_duration} days
    User interests: {', '.join(interests)}

    Tailor the trip to the user's interests, ensuring activities and attractions align with their interests.

    For each destination, provide:
    1. A suggested budget (ensure the sum doesn't exceed the total budget)
    2. A suggested duration (ensure the sum doesn't exceed the total duration)
    3. A daily itinerary with activities, including name, estimated cost in INR, and a brief description
    4. Ensure activities reflect the user's preferences where possible
    5. Ensure that day starts from 1 and goes up to the total duration

    Note: if you are not clear with the destination or you found any data provided by user invalid just give the notes of maximum 20 words for user and in that case please don't include any JSON content in response.

    Strictly follow the note.

    Respond with a JSON object in the following format:
    {{
        "trip": [
            {{
                "destination": "string",
                "budget": float,
                "duration": int,
                "itinerary": [
                    {{
                        "day": int,
                        "activities": [
                            {{
                                "name": "string",
                                "cost": float,
                                "description": "string"
                            }}
                        ]
                    }}
                ]
            }}
        ]
    }}

    Ensure the JSON is valid and follows this exact structure.
    """
    
    response = model.generate_content(prompt)

    print(response.text)

    if not '{' in response.text:
        return response.text

    startIndex=0
    while response.text[startIndex] != '{':
        startIndex+=1

    endIndex = len(response.text) - 1
    while response.text[endIndex] != '}':
        endIndex-=1


    modified_text = response.text[startIndex:endIndex + 1]
    print(modified_text)
    
    # Parse the response and extract the JSON
    try:
        parsed_data = json.loads(modified_text)
        return parsed_data

    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e.msg}")
        print(f"Line: {e.lineno}, Column: {e.colno}")
        raise ValueError("Failed to generate a valid trip plan. Please try again.")


import os
import json
from groq import AsyncGroq
from typing import List, Dict, Any

# Initialize Groq client
client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))

async def check_interactions_ai(medications: List[str]) -> Dict[str, Any]:
    """
    Uses Groq API (Llama 3) to analyze potential drug interactions.
    In a full production environment, Redis caching would wrap this call.
    """
    med_list = ", ".join(medications)
    prompt = f"""
    You are an expert clinical pharmacy AI. Analyze the following list of medications for interactions: {med_list}.
    Return ONLY a valid JSON object with the following structure, no markdown formatting:
    {{
        "severity": "critical|moderate|mild|none",
        "description": "Detailed explanation of the interaction mechanism.",
        "recommendations": "Clinical recommendations for the prescriber."
    }}
    """
    
    try:
        completion = await client.chat.completions.create(
            messages=[{"role": "system", "content": prompt}],
            model="llama3-8b-8192",
            temperature=0.1,
            max_tokens=500,
        )
        response_text = completion.choices[0].message.content
        return json.loads(response_text)
    except Exception as e:
        # Fallback error handling for the prototype
        return {
            "severity": "unknown",
            "description": f"AI verification failed: {str(e)}",
            "recommendations": "Consult pharmacist immediately."
        }

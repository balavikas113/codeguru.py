import os
import requests
import gradio as gr

# Step 1: Setup function with Google Gemini configuration
def setup_gemini_client():
    # Set up the Gemini API with the provided API key
    api_key = "AIzaSyByIVaDRoc3g8u_hY1_BCegEyfJ-ZkmkX4"
    return api_key

# Step 2: Text generation function with optimized prompt
def generate_text(prompt):
    try:
        # Get the API key
        api_key = setup_gemini_client()
        
        # Create the system prompt for code analysis
        system_prompt = (
            "You are a **Code Guru**, an expert at analyzing code snippets and providing concise, "
            "actionable feedback. Your role is to evaluate code for quality, efficiency, and "
            "readability while suggesting improvements. Structure your response as follows:\n\n"
            
            "### **1. OVERVIEW**\n"
            "- Briefly summarize the code's purpose and structure.\n\n"
            
            "### **2. POTENTIAL ISSUES**\n"
            "- Identify bugs, edge cases, or security vulnerabilities.\n"
            "- Example: *'Missing input validation for negative numbers.'*\n\n"
            
            "### **3. EFFICIENCY IMPROVEMENTS**\n"
            "- Suggest optimizations (e.g., time/space complexity).\n"
            "- Example: *'Use memoization to avoid redundant calculations.'*\n\n"
            
            "### **4. READABILITY IMPROVEMENTS**\n"
            "- Recommend better variable names, comments, or formatting.\n"
            "- Example: *'Rename `x` to `user_input` for clarity.'*\n\n"
            
            "### **5. BEST PRACTICES**\n"
            "- Highlight deviations from language conventions (PEP 8 for Python).\n"
            "- Example: *'Use `snake_case` for function names.'*\n\n"
            
            "### **6. ALTERNATIVE APPROACHES**\n"
            "- Propose simpler or more elegant solutions if applicable.\n"
            "- Example: *'This logic could be simplified with list comprehension.'*\n\n"
            
            "**Tone:** Professional, direct, and supportive. Reference specific lines when possible."
        )
        
        # Create the full prompt
        full_prompt = f"{system_prompt}\n\nCODE TO ANALYZE:\n\n{prompt}"
        
        # Set up the API request
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
        headers = {
            "Content-Type": "application/json"
        }
        
        # Prepare the request data
        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": full_prompt
                        }
                    ]
                }
            ]
        }
        
        # Send the request
        response = requests.post(
            f"{url}?key={api_key}",
            headers=headers,
            json=data
        )
        
        # Parse the response
        response_json = response.json()
        
        # Extract the generated text
        if "candidates" in response_json and len(response_json["candidates"]) > 0:
            return response_json["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return "Error: Unable to generate response. " + str(response_json)

    except Exception as e:
        return f"Error: {str(e)}"

# Step 3: Gradio interface
def create_interface():
    return gr.Interface(
        fn=generate_text,
        inputs=gr.Textbox(label="Code Snippet", lines=10, placeholder="Paste your code here..."),   
        outputs=gr.Textbox(label="Code Analysis", lines=20),
        title="🔍 Code Guru AI",
        description="Get detailed code analysis with actionable improvement suggestions.",
        examples=[
            ["def factorial(n):\n    if n == 0:\n        return 1\n    else:\n        return n * factorial(n-1)"],
            ["def calculate_average(numbers):\n    return sum(numbers)/len(numbers)"],
            ["for i in range(10):\n    print(i**2)"],
        ],
        allow_flagging="never"
    )

# Step 4: Run the application
if __name__ == "__main__":
    interface = create_interface()
    interface.launch()

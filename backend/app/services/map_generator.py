import os
from langchain_openai import ChatOpenAI

# Initialize the language model
llm = ChatOpenAI(
    api_key=os.getenv('apiKey'),
    base_url="https://api.featherless.ai/v1",
    model="meta-llama/Meta-Llama-3.1-8B-Instruct",
)

def generate_mind_map(content):
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that organizes text into a hierarchical mind map. "
                       "The output format is a JSON list with 'id', 'name', and 'parent_id'. Use the provided content to create the mind map."
        },
        {
            "role": "user",
            "content": content
        }
    ]

    # Step 3: Invoke the LLM for mind map generation
    try:
        response = llm.invoke(messages)
        mind_map = response.get("content")  # Extract the mind map from the response
    except Exception as e:
        print(f"Error generating mind map: {e}")
        return None

    # Step 4: Convert response to structured data (if needed) and return
    try:
        mind_map_data = eval(mind_map)  # Ensure the response is valid Python data
        return mind_map_data
    except Exception as e:
        print(f"Error parsing mind map data: {e}")
        return None

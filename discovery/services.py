import os
from google import genai
from .utils import fetch_and_embed_books, collection

def get_smart_recommendation(user_prompt, chat_history=[]):
    try:
        # 1. Update the local vector database
        fetch_and_embed_books(user_prompt)
        
        # 2. Perform search
        results = collection.query(query_texts=[user_prompt], n_results=3)
        context_docs = results.get('documents', [[]])[0]
        metadatas = results.get('metadatas', [[]])[0]

        # 3. Initialize Client
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        
        # Format the system instruction for a "Librarian" personality
        sys_instruct = "You are a witty librarian. Use the context provided to recommend books. If context is empty, use your own knowledge."

        # 4. Generate response with history
        # We use a clean prompt that includes context explicitly
        full_prompt = f"USER QUERY: {user_prompt}\n\nLIBRARY CONTEXT: {context_docs}"
        
        chat = client.chats.create(
            model='gemini-2.5-flash',
            config={'system_instruction': sys_instruct},
            history=chat_history
        )
        
        ai_response = chat.send_message(full_prompt)
        
        # 5. Return data in a strict format the JS expects
        return {
            "recommendation": ai_response.text,
            "book_data": metadatas if metadatas else [],
            "new_history": [
                {"role": "user", "parts": [{"text": user_prompt}]},
                {"role": "model", "parts": [{"text": ai_response.text}]}
            ]
        }
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        return {"error": str(e), "recommendation": "I hit a glitch. Try again?", "new_history": []}
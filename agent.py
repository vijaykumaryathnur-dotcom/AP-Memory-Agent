from hindsight_client import Hindsight
from groq import Groq

# --- 1. SETUP KEYS ---
HINDSIGHT_API_KEY = "YOUR_HINDSIGHT_API_KEY_HERE"
GROQ_API_KEY = "YOUR_GROQ_API_KEY_HERE"

# Initialize clients
hindsight = Hindsight(
    base_url="https://api.hindsight.vectorize.io",
    api_key=HINDSIGHT_API_KEY
)
groq_client = Groq(api_key=GROQ_API_KEY)

BANK_ID = "ap-agent-demo"

# --- 2. THE AGENT LOGIC ---
def analyze_invoice(vendor_name, invoice_details):
    print(f"\n[Agent] Analyzing invoice for {vendor_name}...")
    
    # A. RECALL from Hindsight
    print("[Agent] Searching memory...")
    memory_results = hindsight.recall(bank_id=BANK_ID, query=f"{vendor_name} invoice discrepancies")
    
    past_history = "No previous history found."
    if memory_results and memory_results.results:
         past_history = "\n".join([mem.text for mem in memory_results.results])
         print(f"[Agent] Found {len(memory_results.results)} memories!")
    else:
         print("[Agent] Memory is empty.")

    # B. REASON with Groq
    prompt = f"""
    You are an expert AP Clerk. Analyze this new invoice for {vendor_name}.
    
    PAST MEMORY FOR THIS VENDOR:
    {past_history}
    
    NEW INVOICE:
    {invoice_details}
    
    Task:
    1. Flag any discrepancies.
    2. If there is past memory, use it to suggest the exact resolution that worked before.
    3. If memory is empty, give a generic response.
    """
    
    chat_completion = groq_client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama3-8b-8192", 
    )
    response = chat_completion.choices[0].message.content
    print(f"\n--- AGENT RESPONSE ---\n{response}\n----------------------")
    
    # C. RETAIN to Hindsight
    print("[Agent] Saving this interaction to memory...")
    new_memory = f"Vendor: {vendor_name}. Invoice: {invoice_details}. Resolution: {response}"
    hindsight.retain(bank_id=BANK_ID, content=new_memory)
    print("[Agent] Memory saved!\n")

# --- 3. RUN THE DEMO ---
if __name__ == "__main__":
    print("=== TURN 1: EMPTY MEMORY ===")
    analyze_invoice("Acme Corp", "Invoice #1001 for $5,000. Item: Freight charges.")
    
    print("\n=== TURN 2: MEMORY SHOULD NOW BE ACTIVE ===")
    analyze_invoice("Acme Corp", "Invoice #1002 for $5,000. Item: Freight charges.")

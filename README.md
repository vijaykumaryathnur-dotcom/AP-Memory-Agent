# AP-Memory-Agent
An AI Accounts Payable agent that uses **Hindsight memory** to remember past vendor discrepancies and suggest resolutions. 

## The Problem
AP teams process thousands of invoices. When a discrepancy happens (like duplicate freight charges), senior staff waste hours re-solving the same problem for the same vendor. Stateless chatbots forget everything.

## The Solution
This agent uses **Hindsight (by Vectorize)** to recall vendor history. When a new invoice comes in, it searches its memory, finds past discrepancies for that vendor, and uses **Groq (Llama 3)** to suggest the exact resolution that worked before.

## How it Works
1. **Recall:** Searches Hindsight for the vendor's past invoice issues.
2. **Reason:** Groq LLM compares the new invoice against the recalled memory.
3. **Retain:** Saves the new invoice and the suggested resolution back into Hindsight for next time.

## How to Run
1. Install dependencies: `pip install hindsight-client groq`
2. Add your Hindsight and Groq API keys in `agent.py`.
3. Run: `python agent.py`

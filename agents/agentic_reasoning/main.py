from puzzle import NumberPuzzle
from agent import ReasoningAgent
from llm import OpenRouterLLM


if __name__ == "__main__":

    
    OPENROUTER_API_KEY = "YOUR_API_KEY_HERE"

    llm = OpenRouterLLM(
        api_key=OPENROUTER_API_KEY,
        model="mistralai/mistral-7b-instruct"  # good free choice
    )

    agent = ReasoningAgent(llm)

    
    env = NumberPuzzle(start=23)
    

    print("Starting puzzle:", env.get_state())

    final_state = agent.run(env, llm_mode=False)  # set to True to use LLM for reasoning and decision making

    print("\nFinal state:", final_state)

    if final_state == 0:
        print("✅ Solved!")
    else:
        print("❌ Did not reach goal")

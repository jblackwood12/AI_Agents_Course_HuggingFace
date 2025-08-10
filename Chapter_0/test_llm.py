from smolagents import CodeAgent, LiteLLMModel

model = LiteLLMModel(
    model_id="ollama_chat/qwen2:7b",
    api_base="http://127.0.0.1:11434",
    num_ctx=8192
)

# Create an agent using the LiteLLMModel
agent = CodeAgent(
    tools=[],  # You can add custom tools here if needed
    model=model
)

# Run the agent with a task
result = agent.run("Write a Python function to calculate the factorial of a number.")
print(result)

test_val=123
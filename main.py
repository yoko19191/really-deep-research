from backend.factory import get_llm_by_type, create_agent

# test: get_llm_by_type 
basic_llm = get_llm_by_type("basic")
print(basic_llm.invoke("你是谁？你可以做什么？"))


# test: create_agent 
planer_agent = create_agent(
    agent_name="planner",
    agent_type="planner",
)
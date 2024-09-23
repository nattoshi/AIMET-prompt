from autogen import AssistantAgent, UserProxyAgent
import os
from dotenv import load_dotenv
from customagents import CustomAgents  # Ensure this path is correct

# Load environment variables from .env file
load_dotenv('.env')

# Define configuration for LLM (Large Language Model)
config_list = [
    {
        "model": os.environ['AZURE_OPENAI_MODEL'],
        "api_type": "azure",
        "api_key": os.environ['AZURE_OPENAI_API_KEY'],
        "base_url": os.environ['AZURE_OPENAI_ENDPOINT'],
        "api_version": "2024-02-01",
    }
]

# LLM configuration
llm_config = {
    "config_list": config_list,
    "temperature": 0.5,
    "cache_seed": None,  # Disables caching
}

# Initialize a User Proxy Agent
user_proxy = UserProxyAgent(
    name="User_proxy",
    system_message="Terminator admin.",
    code_execution_config=False,
    human_input_mode="NEVER",
    llm_config=llm_config,
)

# List to hold all agents
all_agents = []

def add_agent(agent_creation_function, llm_config):
    """Creates an agent using the given creation function and adds it to the list of all agents."""
    agent = agent_creation_function(llm_config)
    all_agents.append(agent)
    return agent

# Initialize agents using CustomAgents
main_problem_state_tracker = add_agent(CustomAgents.create_main_problem_state_tracker, llm_config)
main_problem_aspect_promoter = add_agent(CustomAgents.create_main_problem_aspect_promoter, llm_config)

end_session_state_tracker = add_agent(CustomAgents.create_end_session_state_tracker, llm_config)
end_session_aspect_promoter = add_agent(CustomAgents.create_end_session_aspect_promoter, llm_config)

# global_coordination_agent = add_agent(CustomAgents.create_global_coordination_agent, llm_config)
# utterance_generation_agent = add_agent(CustomAgents.create_utterance_generation_agent, llm_config)

# Example dialogue history initialization
# dialogue_history = [
#     {"role": "system", "content": "สวัสดีค่ะ มีอะไรอยากให้ช่วยเหลือ สามารถเล่าให้ฟังได้เลยนะคะ"},
#     {"role": "system", "content": "ก่อนที่จะเริ่มบทสนทนา ฉันขอทราบชื่อและอายุ"}
# ]
dialogue_history = []

# Main interaction loop
while True:
    try:
        user_message = input("User: ")
        print("-" * 15)
        dialogue_history.append({"role": "user", "content": user_message})

        # Execute each agent in sequence as per their specific roles

        main_problem_result_state_summary = user_proxy.initiate_chat(
            recipient=main_problem_state_tracker,
            message="",
            max_turns=1,
            summary_method="last_msg",
            carryover=[f"[Dialogue History] {str(dialogue_history)}"]
        )

        main_problem_result_aspect_promoter = user_proxy.initiate_chat(
            recipient=main_problem_aspect_promoter,
            message="",
            max_turns=1,
            summary_method="last_msg",
            carryover=[f"[Main problem] {str(main_problem_result_state_summary.summary)}"]
        )


        end_session_result_state_summary = user_proxy.initiate_chat(
            recipient=end_session_state_tracker,
            message="",
            max_turns=1,
            summary_method="last_msg",
            carryover=[f"[Dialogue History] {str(dialogue_history)}",
                f"[Main problem] {str(main_problem_result_state_summary.summary)}"
            ]
        )

        end_session_result_aspect_promoter = user_proxy.initiate_chat(
            recipient=end_session_aspect_promoter,
            message="",
            max_turns=1,
            summary_method="last_msg",
            carryover=[f"[Conversation result] {str(end_session_result_state_summary.summary)}"
            ]
        )

        
        bot_answer = end_session_result_state_summary.summary
        print(bot_answer)
        print('-' * 15)
        

        # global_coordination_result = user_proxy.initiate_chat(
        #     recipient=global_coordination_agent,
        #     message="",
        #     max_turns=1,
        #     summary_method="last_msg",
        #     carryover=[
        #         f"[Dialogue History] {str(dialogue_history)}",
                
        #         f"[Topic Candidates] {str([comforting_aspect_promoter_result.summary, exploration_aspect_promoter_result.summary, client_profile_aspect_promoter_result.summary,dmind_aspect_promoter_result.summary])}",

        #         f"[The next stage Professional Counsellor should focus on] {str(session_flow_aspect_promoter_result.summary)}",
        #     ]
        # )

        # utterance_generation_result = user_proxy.initiate_chat(
        #     recipient=utterance_generation_agent,
        #     message="",
        #     max_turns=1,
        #     summary_method="last_msg",
        #     carryover=[
        #         f"[Dialogue History] {str(dialogue_history)}",
        #         f"[Top Topic Candidates] {str(global_coordination_result.summary)}",
        #     ]
        # )

        # Output the bot's response
        # bot_answer = utterance_generation_result.summary
        # print(bot_answer)
        # print('-' * 15)

        dialogue_history.append({"role": "system", "content": bot_answer})

        # Calculate and display total cost
        total_cost = {'total_cost': 0, 'gpt-4o-mini': {'tokens': 0, 'requests': 0}}

        for agent in all_agents:
            try:
                usage = agent.get_total_usage()
                total_cost['total_cost'] += usage.get('total_cost', 0)
                for key, value in usage.get('gpt-4o-mini', {}).items():
                    total_cost['gpt-4o-mini'][key] += value
            except Exception as e:
                print(f"Error calculating usage for {agent.name}: {e}")

        print("Total cost:", total_cost)

    except KeyboardInterrupt:
        print("\nExiting the dialogue loop.")
        break
    except Exception as e:
        print(f"Error: {e}")

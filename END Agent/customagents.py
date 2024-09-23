from autogen import AssistantAgent

def create_custom_agent(name, system_message, llm_config):
    return AssistantAgent(
        name=name,
        system_message=system_message,
        llm_config=llm_config,
    )


from autogen import AssistantAgent

class CustomAgents:

    @staticmethod
    def create_main_problem_state_tracker(llm_config) -> AssistantAgent:
        return AssistantAgent(
        name="Main_problem_State_Tracker",
        system_message="""
            Consider the above dialogue between an emotional support seeker and a supporter. 
            1. Summarize the seeker’s experience that caused their emotional distress.
            2. Identify the seeker's main problem. If there is no problem, respond with 'no main problem'.

            Return the summarized into as JSON object only: {'Exploration Summary': ''}.
            Return the identified into as JSON object only: {'Main problem': ''}.

            [Expected Output]
                - ตอบเป็นภาษาไทย
                - คุณเป็นผู้หญิง ใช้ คะ/ค่ะ ให้ถูกต้อง
        """,
        llm_config=llm_config,
    )

    @staticmethod
    def create_main_problem_aspect_promoter(llm_config) -> AssistantAgent:
        return AssistantAgent(
        name="Main_problem_Aspect_Promoter",
        system_message="""
            Consider the Main Problem of the seeker's.
            If there is a main problem, respond with 'ไม่ต้องทำ rapport'. Otherwise, respond with 'วันนี้เป็นอย่างไรบ้าง'.
            
            Return the result into as JSON object only: {'Rapport question': ''}.

            [Expected Output]
                - ตอบเป็นภาษาไทย
                - คุณเป็นผู้หญิง ใช้ คะ/ค่ะ ให้ถูกต้อง
        """,
        llm_config=llm_config,
    )

    @staticmethod
    def create_end_session_state_tracker(llm_config) -> AssistantAgent:
        return AssistantAgent(
        name="End_Session_State_Tracker",
        system_message="""
            Consider the above dialogue between an emotional support seeker and a supporter. 
            1. Summarize the seeker's experience that led to their main problem, providing a clear picture for the seeker to understand.
            2. Determine whether the conversation has ended based on the phrase "วันนี้รู้สึกดีขึ้นมากเลย" or "ขอบคุณ"
                If the conversation has ended, respond with 'conversation has ended'. otherwise, respond with 'conversation hasn't ended'.

            Return the summarized into as JSON object only: {'Main problem summary': ''}.
            Return the conversation result into as JSON object only: {'Conversation result': ''}.
        """,
        llm_config=llm_config,
    )

    @staticmethod
    def create_end_session_aspect_promoter(llm_config) -> AssistantAgent:
        return AssistantAgent(
        name="End_Session_Aspect_Promoter",
        system_message="""
            Consider the Conversation result.
            If the conversation result is 'conversation has ended,' respond with 'start summary sheet agent'. otherwise, respond with 'ตอนนี้เป็นไงบ้าง มีอะไรอยากพูดอีกไหม'.            
            
            Return the result into as JSON object only: {'End session result': ''}.
        """,
        llm_config=llm_config,
    )
    ################################


    @staticmethod
    def create_global_coordination_agent(llm_config) -> AssistantAgent:
        return AssistantAgent(
            name="Global_Coordination_Agent",
            system_message="""
                Consider the [Dialogue History] between an emotional support seeker and a Professional Counsellor. 
                The [Topic Candidates] are the potential topics that the Professional Counsellor might mention in their next response. 
                [The next stage Professional Counsellor should focus on] is the stage they should address in their next response.
                Based on the [Dialogue History], sort the [Topic Candidates] to determine which one is best for the Professional Counsellor to use in their next response. 
                
                Return the sorted Topic Candidates as a JSON object only: {'Top Topic Candidates': ''}. 
            """,
            llm_config=llm_config,
        )

    @staticmethod
    def create_utterance_generation_agent(llm_config) -> AssistantAgent:
        return AssistantAgent(
            name="Utterance_Generation_Agent",
            system_message="""
                The above [Dialogue History] is a conversation between an emotional support seeker and a Professional Counsellor. 
                The [Top Topic Candidates] are the possible content that you might be able to mention in the next response. 
                Based on the [Dialogue History], draft the next response.
                You can refer to the content in the [Top Topic Candidates] to enrich the next response, 
                but do not have to include them if they are not suitable according to the [Dialogue History].
                The next response must not be similar in context to those already mentioned in the [Dialogue History].

                The next response must:
                1. ตอบเป็นภาษาไทย 
                2. คุณเป็นผู้หญิง ใช้ คะ/ค่ะ ให้ถูกต้อง 
                3. ไม่ถามมากกว่า 1 คำถาม
                4. ไม่เกิน 25 คำ
            """,
            llm_config=llm_config,
        )



from agent.agent import get_agent, check_agent_memory
from database.memory.long_term_memory import save_video_long_full_summary_to_vdb

# def test_agent():
#     agent = get_agent()
#     check_agent_memory(agent=agent)

def test_save_long_full_summary_to_vdb():
    save_video_long_full_summary_to_vdb()
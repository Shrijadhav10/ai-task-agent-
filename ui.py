import gradio as gr
from agent import run_agent
from tools import get_tasks

AGENT_ACTIVE = True

# Function to update task list visually
def refresh_tasks():
    tasks = get_tasks()
    if not tasks:
        return "No tasks found."
    formatted = ""
    for idx, t in enumerate(tasks, start=1):
        status = "✅" if t["completed"] else "🕒"
        formatted += f"{idx}. {t['task']} {status}\n"
    return formatted

# Chat + Task execution
def handle_user_message(user_message, chat_history):
    global AGENT_ACTIVE

    if not AGENT_ACTIVE:
        response = "⚠️ Agent is turned OFF. Restart the app or click 'Enable Agent'."
        chat_history.append((user_message, response))
        return "", chat_history, refresh_tasks()

    response = run_agent(user_message)
    chat_history.append((user_message, response))
    return "", chat_history, refresh_tasks()

def clear_chat():
    return [], refresh_tasks()

# --- UI Layout ---
with gr.Blocks(theme=gr.themes.Soft()) as demo:

    gr.Markdown(
        """
        # 🧠 Personal Task Agent  
        #### Built with Groq + Gradio  
        Manage tasks, plan your day, and talk to your AI agent.
        """
    )

    with gr.Row():

        # LEFT SIDE – CHAT INTERFACE
        with gr.Column(scale=4):
            chatbot = gr.Chatbot(label="AI Agent Chat", height=450)

            user_input = gr.Textbox(
                label="Ask your agent...",
                placeholder="Add a task, show tasks, plan your day...",
            )

            send_btn = gr.Button("Send", variant="primary")
            clear_btn = gr.Button("Clear Chat")

        # RIGHT SIDE – TASK DASHBOARD
        with gr.Column(scale=2):
            gr.Markdown("### 📋 Your Tasks")
            task_box = gr.Textbox(
                "", label="Task List", interactive=False, lines=18
            )

            refresh_btn = gr.Button("🔄 Refresh Tasks", variant="secondary")

    # Button actions
    send_btn.click(
        handle_user_message,
        [user_input, chatbot],
        [user_input, chatbot, task_box],
    )

    user_input.submit(
        handle_user_message,
        [user_input, chatbot],
        [user_input, chatbot, task_box],
    )

    clear_btn.click(clear_chat, None, [chatbot, task_box])

    refresh_btn.click(lambda: refresh_tasks(), None, task_box)

    
# Launch the app
demo.launch()

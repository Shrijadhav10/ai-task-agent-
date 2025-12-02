from groq import Groq
from tool_schema import tool_schema
import tools
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def call_tool(tool_name, arguments):
    if tool_name == "add_task":
        return tools.add_task(arguments["task"])
    if tool_name == "get_tasks":
        return tools.get_tasks()
    if tool_name == "delete_task":
        return tools.delete_task(arguments["task"])
    if tool_name == "mark_complete":
        return tools.mark_complete(arguments["task"])
    if tool_name == "clear_tasks":
        return tools.clear_tasks()

def run_agent(user_input):

    messages = [
        {"role": "system", "content":
                                        """
                                        You are SMART_TASK_AGENT.

                                        Your job is ONLY to manage user tasks using the tools provided.

                                        ### INTENT CLASSIFICATION
                                        For each user message, decide ONE of:
                                        - add
                                        - delete
                                        - show
                                        - complete
                                        - plan
                                        - other

                                        If 'other', simply respond:
                                        "I only manage tasks. Your request is not a task instruction."

                                        ### ADD BEHAVIOR
                                        - Extract tasks from natural language.
                                        - Handle multiple tasks in one sentence.
                                        - Detect deadlines (e.g., today, tomorrow, friday).
                                        - Detect priority (urgent, important).
                                        - Output ONE OR MORE add_task tool calls.

                                        ### DELETE BEHAVIOR
                                        - Extract exact task name to delete.
                                        - Only call delete_task if it's clearly about a task.

                                        ### SHOW BEHAVIOR
                                        - Use get_tasks tool.

                                        ### COMPLETE BEHAVIOR
                                        - Mark the correct task as completed.

                                        ### PLAN BEHAVIOR
                                        - Read all tasks.
                                        - Order by priority + deadlines.
                                        - Create an intelligent day plan (no tools).

                                        ### STRICT RULES
                                        1. NEVER answer like a coding assistant.
                                        2. NEVER talk about Python, os.remove, rm, del, etc.
                                        3. NEVER invent new tools.
                                        4. ONLY use tools listed.
                                        5. Temperature must be 0 (no creativity).
                                        6. If unsure, ask user clarifying questions.
                                        """
                                        }
,
        {"role": "user", "content": user_input}
    ]

    response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=messages,
    temperature=0,
    tools=tool_schema,
    tool_choice="auto"

    )

    ai_msg = response.choices[0].message

    # If LLM decides to call a tool
    if hasattr(ai_msg, "tool_calls") and ai_msg.tool_calls:

        tool_call = ai_msg.tool_calls[0]
        tool_name = tool_call.function.name

        # tool_call.function.arguments is a STRING, convert to dict
        args = json.loads(tool_call.function.arguments)

        result = call_tool(tool_name, args)

        # Send tool result back to LLM for final response
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": str(result)
        })

        final = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages
        )

        return final.choices[0].message.content

    return ai_msg.content

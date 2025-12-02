tool_schema = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Add a task to the to-do list",
            "parameters": {
                "type": "object",
                "properties": {
                    "task": {"type": "string"}
                },
                "required": ["task"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_tasks",
            "description": "Get all tasks",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "Delete a task",
            "parameters": {
                "type": "object",
                "properties": {
                    "task": {"type": "string"}
                },
                "required": ["task"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "mark_complete",
            "description": "Mark a task complete",
            "parameters": {
                "type": "object",
                "properties": {
                    "task": {"type": "string"}
                },
                "required": ["task"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "clear_tasks",
            "description": "Delete all tasks",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]

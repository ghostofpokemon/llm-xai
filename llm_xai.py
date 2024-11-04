import llm
from llm.default_plugins.openai_models import Chat, Completion

# Hardcoded models for now
def get_xAI_models():
    return [
        {"id": "grok-beta"},
    ]

class xAIChat(Chat):
    needs_key = "xAI"
    key_env_var = "XAI_KEY"

    def __str__(self):
        return "xAI: {}".format(self.model_id)

class xAICompletion(Completion):
    needs_key = "xAI"
    key_env_var = "XAI_KEY"

    def __str__(self):
        return "xAI: {}".format(self.model_id)

@llm.hookimpl
def register_models(register):
    # Only do this if the xAI key is set
    key = llm.get_key("", "xAI", "LLM_XAI_KEY")
    if not key:
        return

    models = get_xAI_models()

    for model_definition in models:
        chat_model = xAIChat(
            model_id="xAI/{}".format(model_definition["id"]),
            model_name=model_definition["id"],
            api_base="https://api.x.ai/v1",
            headers={"HTTP-Referer": "https://llm.datasette.io/", "X-Title": "LLM"},
        )
        register(chat_model)

    for model_definition in models:
        completion_model = xAICompletion(
            model_id="xAIcompletion/{}".format(model_definition["id"]),
            model_name=model_definition["id"],
            api_base="https://api.x.ai/v1",
            headers={"HTTP-Referer": "https://llm.datasette.io/", "X-Title": "LLM"},
        )
        register(completion_model)

class DownloadError(Exception):
    pass

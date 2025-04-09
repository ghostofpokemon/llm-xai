import llm
from llm.default_plugins.openai_models import Chat, Completion
from pathlib import Path
import json
import time
import httpx

def get_xAI_models():
    return fetch_cached_json(
        url="https://api.x.ai/v1/models",
        path=llm.user_dir() / "xAI_models.json",
        cache_timeout=3600,
    )["data"]

class XAIChat(Chat):
    needs_key = "xai"
    key_env_var = "XAI_KEY"
    
    def __str__(self):
        return "xAI: {}".format(self.model_id)
    
    def build_kwargs(self, prompt, stream):
        # Call parent's build_kwargs but without adding stream_options
        kwargs = super().build_kwargs(prompt, False)  # Pass False to prevent adding stream_options
        # Keep the stream parameter intact for actual streaming
        return kwargs

class XAICompletion(Completion):
    needs_key = "xai"
    key_env_var = "XAI_KEY"
    
    def __str__(self):
        return "xAI: {}".format(self.model_id)
    
    def build_kwargs(self, prompt, stream):
        # Call parent's build_kwargs but without adding stream_options
        kwargs = super().build_kwargs(prompt, False)  # Pass False to prevent adding stream_options
        # Keep the stream parameter intact for actual streaming
        return kwargs

@llm.hookimpl
def register_models(register):
    # Only do this if the xAI key is set
    key = llm.get_key("", "xai", "LLM_XAI_KEY")
    if not key:
        return

    models = get_xAI_models()
    for model_definition in models:
        chat_model = XAIChat(
            model_id="xAI/{}".format(model_definition["id"]),
            model_name=model_definition["id"],
            api_base="https://api.x.ai/v1/",
            headers={"HTTP-Referer": "https://llm.datasette.io/", "X-Title": "LLM"},
        )
        register(chat_model)

    for model_definition in models:
        completion_model = XAICompletion(
            model_id="xAIcompletion/{}".format(model_definition["id"]),
            model_name=model_definition["id"],
            api_base="https://api.x.ai/v1/",
            headers={"HTTP-Referer": "https://llm.datasette.io/", "X-Title": "LLM"},
        )
        register(completion_model)

class DownloadError(Exception):
    pass

def fetch_cached_json(url, path, cache_timeout):
    path = Path(path)
    # Create directories if not exist
    path.parent.mkdir(parents=True, exist_ok=True)

    # Get the API key
    key = llm.get_key("", "xai", "LLM_XAI_KEY")

    if path.is_file():
        # Get the file's modification time
        mod_time = path.stat().st_mtime
        # Check if it's more than the cache_timeout old
        if time.time() - mod_time < cache_timeout:
            # If not, load the file
            with open(path, "r") as file:
                return json.load(file)

    # Try to download the data
    try:
        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        }
        response = httpx.get(url, headers=headers, follow_redirects=True)
        response.raise_for_status()  # This will raise an HTTPError if the request fails

        # If successful, write to the file
        with open(path, "w") as file:
            json.dump(response.json(), file)
        return response.json()

    except httpx.HTTPError:
        # If there's an existing file, load it
        if path.is_file():
            with open(path, "r") as file:
                return json.load(file)
        else:
            # If not, raise an error
            raise DownloadError(
                f"Failed to download data and no cache is available at {path}"
            )

import streamlit as st
import vertexai
import json

from dataclasses import dataclass
from vertexai.generative_models import GenerationConfig, GenerativeModel, GenerationResponse


# # # # #
# Helpers
# # # # #
@dataclass
class StateInfo:
    @staticmethod
    def from_vertex_response(response: GenerationResponse) -> list["StateInfo"]:
        return []
    
    # TODO: Write __init__ function with desired properties.   


# # # # # #
# Constants
# # # # # #

PROJECT_ID = "section-b4-project-1"
RESPONSE_SCHEMA = {
    "type": "array",
    # TODO: Supply the desired properties.
    "items": {
        "type": "object",
            "properties": {
            "a": { "type": "string" },
            "b": { "type": "string" },
            "c": { "type": "string" }
        }
    }
} # Read more @ https://ai.google.dev/gemini-api/docs/structured-output?lang=python


# # #
# App
# # #


st.title("Find your neighboring states")

users_state = st.text_input("Enter your state")


# Section A: Add in your Vertex AI API call below

response: GenerationResponse | None = None
if users_state:
    vertexai.init(project=PROJECT_ID, location="us-central1")
    model = GenerativeModel("gemini-1.5-flash-002")

    response = model.generate_content(
        f"TODO: Prompt the AI",
        generation_config=GenerationConfig(
            response_mime_type="application/json", response_schema=RESPONSE_SCHEMA
        )
    )

# End of Section A


st.write(
    f'The neighboring states of **{users_state}** are:'
    if users_state
    else 'Awaiting input...')

# Section B:  Output the results to the user below

if response:
    states = StateInfo.from_vertex_response(response)
    for state in states:
        st.write(f"TODO: Output desired properties")

# End of Section B
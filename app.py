import streamlit as st
import vertexai
import json

from dataclasses import dataclass
from vertexai.generative_models import GenerationConfig, GenerativeModel, GenerationResponse


# # # # # # # #
# Helper class
# # # # # # # #

@dataclass
class StateInfo:
    @staticmethod
    def from_vertex_response(response: GenerationResponse) -> list["StateInfo"]:
        return parse_response_to_states(response)

    def __init__(self, state_name: str, direction: str, shared_border_length_miles: float):
        self.state_name = state_name
        self.direction = direction
        self.shared_border_length_miles = int(shared_border_length_miles)


def parse_response_to_states(response: GenerationResponse) -> list[StateInfo]:
    parsed = json.loads(response.candidates[0].content.text)
    return [StateInfo(**state) for state in parsed]


# # # # # #
# Constants
# # # # # #

PROJECT_ID = "section-b4-project-1"
RESPONSE_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "state_name": {
                "type": "string"
            },
            "direction": {
                "type": "string"
            },
            "shared_border_length_miles": {
                "type": "number"
            }
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
        f"List the neighboring states of {users_state} along with the cardinal direction of where they are located relative to the state of {users_state}). Additionally, provide the number of miles of shared border between the two in miles.",
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
        st.write(
            f'- **{state.state_name}**, located to the *{state.direction}* of {users_state}. '
            f'They share a border *{state.shared_border_length_miles} miles* long.')


# End of Section B
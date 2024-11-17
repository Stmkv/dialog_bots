import json

from environs import Env
from google.cloud import dialogflow


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )
    return response


def load_training_data(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        file_contents = json.load(file)
    return file_contents


if __name__ == "__main__":
    env = Env()
    env.read_env()
    dialog_flow_project_id = env.str("DIALOG_FLOW_PROJECT_ID")
    try:
        file_contents = load_training_data("trenings_fraze.json")
        for display_name, questions_and_answer in file_contents.items():
            response = create_intent(
                dialog_flow_project_id,
                display_name,
                questions_and_answer["questions"],
                [questions_and_answer["answer"]],
            )
        print(f"Intent created: {response}")
    except FileNotFoundError as e:
        print(f"File read error: {e}")

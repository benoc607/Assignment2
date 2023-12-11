import weather_report_functions  # Import python functions from weather_report_functions
import spacy    # Import Chatbot

# Load English language model
nlp = spacy.load("en_core_web_md")

# Clean user input
def clean_input(statement):
    special_chars = ["'", '"', ":", ";", ".", ",", "!", "?"]
    for char in special_chars:
        weather_report_functions.replace_text(statement, char, "")
    return nlp(statement.lower())

# Extract comparison statements and compare to user input
def training_statements(statement):
    # Set initiating values
    min_similarity = 0.7
    num = 0

    comparison_statements = open("comparison_statements.txt").read().splitlines()
    for input in comparison_statements:
        comparison_statements[num] = float(nlp(input).similarity(statement))
        num += 1
    comparison_statements.append(min_similarity)
    return comparison_statements

def chatbot_location(statement):
    statement = clean_input(statement)
    location = None
    for ent in statement.ents:
        if ent.label_ == "GPE":  # GeoPolitical Entity
            location = ent.text
    return location

def chatbot(statement):
    statement = clean_input(statement)
    comparison_statements = training_statements(statement)
    location = chatbot_location(statement)

    # used to manually compare similarity scores in testing
    #print(comparison_statements)

    # Spacy named entity recognition to extract location name
    for ent in statement.ents:
        if ent.label_ == "GPE":  # GeoPolitical Entity
            location = ent.text

    # Calls function with highest similarity score, also compares against min_similarity value
    if comparison_statements[0] == max(comparison_statements):
        if location is not None:
            return weather_report_functions.display_report_temp(location)
        else:
            return "Sorry I didn't catch the city you were wanting to check, please ensure you include this."
    elif comparison_statements[1] == max(comparison_statements):
        if location is not None:
            return "The forecasted humidity for "+location+" today is "+str(weather_report_functions.create_weather_report(location).humidity)
        else:
            return "Sorry I didn't catch the city you were wanting to check, please ensure you include this."
    elif comparison_statements[2] == max(comparison_statements):
        if location is not None:
            return "The forecasted weather for "+location+" today is: "+str(weather_report_functions.create_weather_report(location).description)
        else:
            return "Sorry I didn't catch the city you were wanting to check, please ensure you include this."
    elif comparison_statements[3] or comparison_statements[4] or comparison_statements[5]== max(comparison_statements):
        return "Hi there, how can I help you today?"
    else:
        return "Sorry I didn't understand that. Please rephrase your statement."


# Used to test various user inputs
#response = chatbot("what is the weather like in london")
#print(response)

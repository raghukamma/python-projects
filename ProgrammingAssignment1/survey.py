import json
import os

def survey(survey_path):
    # attempting to load the survey file and throw errors if the file is missing or corrupted
    try:
        with open(survey_path, "r") as file:
            survey_data = json.load(file)
    except FileNotFoundError:
        print(f"ERROR: The survey file {survey_path} does not exist.")
        return
    except json.JSONDecodeError:
        print(f"ERROR: The survey file {survey_path} is corrupted.")
        return

    # scanning the input survey file for the survey name, description and questions
    survey_name = survey_data[1][0]
    survey_desc = survey_data[1][1]
    questions = survey_data[3]
    organization = survey_data[0]

    # printing the organization name
    print(f"\nThis survey is from the organization called: {organization}\n\n")

    # printing the survey name and description
    print(f"The description of the survey is: {survey_desc}\n")

    # getting the user's first and last name
    first_name = input("\nPlease enter your first name: ").lower()
    last_name = input("\nPlease enter your last name: ").lower()
    print()

    # checking if an ID is required
    id_value = ""
    id_name = ""
    if len(survey_data[2]) == 2:
        id_name = survey_data[2][0]
        id_desc = survey_data[2][1]
        id_value = input(id_desc + ": ").lower()
        print()

    # generating the survey file name based on the user's first and last name and ID (if applicable)
    if id_value:
        survey_file_name = f"{survey_name}_{last_name}_{first_name}_{id_value}.json"
    else:
        survey_file_name = f"{survey_name}_{last_name}_{first_name}.json"

    # checking if the file exists and read previous responses if it does exist and ask the user to review the responses and modify them if necessary
    survey_file_path = os.path.expanduser(f"~/{survey_file_name}")
    response_data = {}
    if os.path.exists(survey_file_path):
        try:
            with open(survey_file_path, "r") as file:
                response_data = json.load(file)
        except json.JSONDecodeError:
            print(f"WARNING: The existing survey file {survey_file_path} is corrupted. All previous responses will be overwritten.")
    if response_data:
        print("There is an existing survey with your details, please review the existing responses:\n")
        for q_id, response in response_data.items():
            if q_id == "first_name" or q_id == "last_name" or q_id == id_name:
                continue
            q_text = questions[q_id]["text"]
            print(f"{q_text}: {response}")
            # ask the user if the previous response is correct and if not, ask the question again and record the response again
            while True:
                review_response = input("Is this response correct? (y/n): ")
                if review_response.lower() == "y":
                    break
                elif review_response.lower() == "n":
                    while True:
                        if len(questions[q_id]["answers"]) == 0:
                            response = input(f"\n\n{q_text}\n\n")
                            break
                        else:
                            print(f"\n\n{q_text}\n")
                            for i, answer in enumerate(questions[q_id]["answers"]):
                                print(f"{i+1}. {answer}")
                            response_index = input("\nEnter the number corresponding to your answer: ")
                            try:
                                response = questions[q_id]["answers"][int(response_index)-1]
                                break
                            except (ValueError, IndexError):
                                print("\n\nWARNING!!! Invalid input. Please enter a valid number.")
                                continue
                    response_data[q_id] = response
                    break
                else:
                    print("WARNING!!! Invalid input. Please enter 'y' or 'n'.")
            print("\n")

    # asking the questions and record the responses in a dictionary with the user's first and last name and ID (if applicable)
    response_data.update({"first_name": first_name, "last_name": last_name})
    if id_value:
        response_data[id_name] = id_value
    for q_id, q_data in questions.items():
        if q_id in response_data:
            continue
        q_text = q_data["text"]
        q_answers = q_data["answers"]
        if len(q_answers) == 0:
            response = input(f"\n\n{q_text}\n\n")
        else:
            print(f"\n\n{q_text}\n")
            for i, answer in enumerate(q_answers):
                print(f"{i+1}. {answer}")
            while True:
                response_index = input("\nEnter the number corresponding to your answer: ")
                print()
                if response_index.isdigit() and int(response_index) in range(1, len(q_answers) + 1):
                    response = q_answers[int(response_index)-1]
                    break
                else:
                    print("WARNING!!! Invalid input. Please enter the number corresponding to your answer.")
        response_data[q_id] = response

    # writing the responses to a JSON file in the user's home directory
    with open(survey_file_path, "w") as file:
        json.dump(response_data, file, indent=4)

    # confirming the saved responses to the user and ask the user to re-run the survey if they want to change any of the responses
    print("\nThanks. Below are your responses and they have been saved: \n")
    for q_id, response in response_data.items():
        if q_id == "first_name" or q_id == "last_name" or q_id == id_name:
            continue
        q_text = questions[q_id]["text"]
        print(f"{q_text}: {response}")
    print("\nIf you'd like to change any of your above responses, please re-run the survey, review and modify your responses accordingly.")
    print("\n")
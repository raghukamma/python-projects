import survey
from pathlib import Path

# survey_path = Path("psu_survey1.json")
# survey_path = Path("psu_survey2.json")
# survey_path = Path("charity1.json")
survey_path = Path("work1.json")
# survey_path = Path("work3.json") #testing if the code is throwing an error when the survey file is missing
survey.survey(survey_path)
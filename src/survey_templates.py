"""Standard psychological and health survey templates."""
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class QuestionMetadata:
    """Metadata for a survey question."""
    text: str
    scale_type: str = "likert"  # likert, yes_no, numeric, open_ended
    scale_min: int = 0
    scale_max: int = 3
    scale_labels: Dict[int, str] = field(default_factory=dict)
    reverse_scored: bool = False
    required: bool = True
    instrument: str = ""
    notes: str = ""


@dataclass
class SurveySection:
    """A section/page in a survey."""
    title: str
    description: str = ""
    questions: List[QuestionMetadata] = field(default_factory=list)


@dataclass
class SurveyTemplate:
    """A complete survey template."""
    name: str
    version: str
    description: str
    instructions: str
    time_reference: str = ""
    sections: List[SurveySection] = field(default_factory=list)
    scoring_info: Dict[str, Any] = field(default_factory=dict)
    estimated_minutes: int = 5
    
    def get_all_questions(self) -> List[QuestionMetadata]:
        """Get all questions from all sections."""
        questions = []
        for section in self.sections:
            questions.extend(section.questions)
        return questions


class SurveyTemplateLibrary:
    """Library of standard psychological and health survey templates."""
    
    @staticmethod
    def get_phq9() -> SurveyTemplate:
        """Patient Health Questionnaire-9 (Depression Screening)."""
        scale_labels = {
            0: "Not at all",
            1: "Several days",
            2: "More than half the days",
            3: "Nearly every day"
        }
        
        questions = [
            QuestionMetadata(
                text="Little interest or pleasure in doing things",
                scale_type="likert",
                scale_min=0,
                scale_max=3,
                scale_labels=scale_labels,
                instrument="PHQ-9",
                notes="Item 1"
            ),
            QuestionMetadata(
                text="Feeling down, depressed, or hopeless",
                scale_type="likert",
                scale_min=0,
                scale_max=3,
                scale_labels=scale_labels,
                instrument="PHQ-9",
                notes="Item 2"
            ),
            QuestionMetadata(
                text="Trouble falling or staying asleep, or sleeping too much",
                scale_type="likert",
                scale_min=0,
                scale_max=3,
                scale_labels=scale_labels,
                instrument="PHQ-9",
                notes="Item 3"
            ),
            QuestionMetadata(
                text="Feeling tired or having little energy",
                scale_type="likert",
                scale_min=0,
                scale_max=3,
                scale_labels=scale_labels,
                instrument="PHQ-9",
                notes="Item 4"
            ),
            QuestionMetadata(
                text="Poor appetite or overeating",
                scale_type="likert",
                scale_min=0,
                scale_max=3,
                scale_labels=scale_labels,
                instrument="PHQ-9",
                notes="Item 5"
            ),
            QuestionMetadata(
                text="Feeling bad about yourself or that you are a failure or have let yourself or your family down",
                scale_type="likert",
                scale_min=0,
                scale_max=3,
                scale_labels=scale_labels,
                instrument="PHQ-9",
                notes="Item 6"
            ),
            QuestionMetadata(
                text="Trouble concentrating on things, such as reading the newspaper or watching television",
                scale_type="likert",
                scale_min=0,
                scale_max=3,
                scale_labels=scale_labels,
                instrument="PHQ-9",
                notes="Item 7"
            ),
            QuestionMetadata(
                text="Moving or speaking so slowly that other people could have noticed. Or the opposite being so fidgety or restless that you have been moving around a lot more than usual",
                scale_type="likert",
                scale_min=0,
                scale_max=3,
                scale_labels=scale_labels,
                instrument="PHQ-9",
                notes="Item 8"
            ),
            QuestionMetadata(
                text="Thoughts that you would be better off dead, or of hurting yourself in some way",
                scale_type="likert",
                scale_min=0,
                scale_max=3,
                scale_labels=scale_labels,
                instrument="PHQ-9",
                notes="Item 9"
            ),
        ]
        
        section = SurveySection(
            title="Depression Screening",
            description="Over the last 2 weeks, how often have you been bothered by any of the following problems?",
            questions=questions
        )
        
        return SurveyTemplate(
            name="PHQ-9",
            version="1.0",
            description="Patient Health Questionnaire-9: A brief depression severity measure",
            instructions="Please answer each question based on how you have been feeling over the past 2 weeks. Respond with a number from 0 to 3.",
            time_reference="Over the last 2 weeks",
            sections=[section],
            scoring_info={
                "method": "sum",
                "range": [0, 27],
                "interpretation": {
                    "0-4": "Minimal depression",
                    "5-9": "Mild depression",
                    "10-14": "Moderate depression",
                    "15-19": "Moderately severe depression",
                    "20-27": "Severe depression"
                }
            },
            estimated_minutes=3
        )
    
    @staticmethod
    def get_gad7() -> SurveyTemplate:
        """Generalized Anxiety Disorder-7 (Anxiety Screening)."""
        scale_labels = {
            0: "Not at all",
            1: "Several days",
            2: "More than half the days",
            3: "Nearly every day"
        }
        
        questions = [
            QuestionMetadata(
                text="Feeling nervous, anxious, or on edge",
                scale_type="likert",
                scale_min=0,
                scale_max=3,
                scale_labels=scale_labels,
                instrument="GAD-7",
                notes="Item 1"
            ),
            QuestionMetadata(
                text="Not being able to stop or control worrying",
                scale_type="likert",
                scale_min=0,
                scale_max=3,
                scale_labels=scale_labels,
                instrument="GAD-7",
                notes="Item 2"
            ),
            QuestionMetadata(
                text="Worrying too much about different things",
                scale_type="likert",
                scale_min=0,
                scale_max=3,
                scale_labels=scale_labels,
                instrument="GAD-7",
                notes="Item 3"
            ),
            QuestionMetadata(
                text="Trouble relaxing",
                scale_type="likert",
                scale_min=0,
                scale_max=3,
                scale_labels=scale_labels,
                instrument="GAD-7",
                notes="Item 4"
            ),
            QuestionMetadata(
                text="Being so restless that it is hard to sit still",
                scale_type="likert",
                scale_min=0,
                scale_max=3,
                scale_labels=scale_labels,
                instrument="GAD-7",
                notes="Item 5"
            ),
            QuestionMetadata(
                text="Becoming easily annoyed or irritable",
                scale_type="likert",
                scale_min=0,
                scale_max=3,
                scale_labels=scale_labels,
                instrument="GAD-7",
                notes="Item 6"
            ),
            QuestionMetadata(
                text="Feeling afraid, as if something awful might happen",
                scale_type="likert",
                scale_min=0,
                scale_max=3,
                scale_labels=scale_labels,
                instrument="GAD-7",
                notes="Item 7"
            ),
        ]
        
        section = SurveySection(
            title="Anxiety Screening",
            description="Over the last 2 weeks, how often have you been bothered by the following problems?",
            questions=questions
        )
        
        return SurveyTemplate(
            name="GAD-7",
            version="1.0",
            description="Generalized Anxiety Disorder-7: A brief anxiety severity measure",
            instructions="Please answer each question based on how you have been feeling over the past 2 weeks. Respond with a number from 0 to 3.",
            time_reference="Over the last 2 weeks",
            sections=[section],
            scoring_info={
                "method": "sum",
                "range": [0, 21],
                "interpretation": {
                    "0-4": "Minimal anxiety",
                    "5-9": "Mild anxiety",
                    "10-14": "Moderate anxiety",
                    "15-21": "Severe anxiety"
                }
            },
            estimated_minutes=2
        )
    
    @staticmethod
    def get_pss10() -> SurveyTemplate:
        """Perceived Stress Scale-10."""
        scale_labels = {
            0: "Never",
            1: "Almost never",
            2: "Sometimes",
            3: "Fairly often",
            4: "Very often"
        }
        
        questions = [
            QuestionMetadata(
                text="In the last month, how often have you been upset because of something that happened unexpectedly?",
                scale_type="likert",
                scale_min=0,
                scale_max=4,
                scale_labels=scale_labels,
                instrument="PSS-10",
                notes="Item 1"
            ),
            QuestionMetadata(
                text="In the last month, how often have you felt that you were unable to control the important things in your life?",
                scale_type="likert",
                scale_min=0,
                scale_max=4,
                scale_labels=scale_labels,
                instrument="PSS-10",
                notes="Item 2"
            ),
            QuestionMetadata(
                text="In the last month, how often have you felt nervous and stressed?",
                scale_type="likert",
                scale_min=0,
                scale_max=4,
                scale_labels=scale_labels,
                instrument="PSS-10",
                notes="Item 3"
            ),
            QuestionMetadata(
                text="In the last month, how often have you felt confident about your ability to handle your personal problems?",
                scale_type="likert",
                scale_min=0,
                scale_max=4,
                scale_labels=scale_labels,
                reverse_scored=True,
                instrument="PSS-10",
                notes="Item 4 (Reverse)"
            ),
            QuestionMetadata(
                text="In the last month, how often have you felt that things were going your way?",
                scale_type="likert",
                scale_min=0,
                scale_max=4,
                scale_labels=scale_labels,
                reverse_scored=True,
                instrument="PSS-10",
                notes="Item 5 (Reverse)"
            ),
            QuestionMetadata(
                text="In the last month, how often have you found that you could not cope with all the things that you had to do?",
                scale_type="likert",
                scale_min=0,
                scale_max=4,
                scale_labels=scale_labels,
                instrument="PSS-10",
                notes="Item 6"
            ),
            QuestionMetadata(
                text="In the last month, how often have you been able to control irritations in your life?",
                scale_type="likert",
                scale_min=0,
                scale_max=4,
                scale_labels=scale_labels,
                reverse_scored=True,
                instrument="PSS-10",
                notes="Item 7 (Reverse)"
            ),
            QuestionMetadata(
                text="In the last month, how often have you felt that you were on top of things?",
                scale_type="likert",
                scale_min=0,
                scale_max=4,
                scale_labels=scale_labels,
                reverse_scored=True,
                instrument="PSS-10",
                notes="Item 8 (Reverse)"
            ),
            QuestionMetadata(
                text="In the last month, how often have you been angered because of things that were outside of your control?",
                scale_type="likert",
                scale_min=0,
                scale_max=4,
                scale_labels=scale_labels,
                instrument="PSS-10",
                notes="Item 9"
            ),
            QuestionMetadata(
                text="In the last month, how often have you felt difficulties were piling up so high that you could not overcome them?",
                scale_type="likert",
                scale_min=0,
                scale_max=4,
                scale_labels=scale_labels,
                instrument="PSS-10",
                notes="Item 10"
            ),
        ]
        
        section = SurveySection(
            title="Perceived Stress",
            description="Please indicate how often you felt or thought a certain way in the last month.",
            questions=questions
        )
        
        return SurveyTemplate(
            name="PSS-10",
            version="1.0",
            description="Perceived Stress Scale-10: Measures the degree to which situations are appraised as stressful",
            instructions="For each question, indicate how often you felt or thought a certain way in the last month. Respond with a number from 0 to 4.",
            time_reference="In the last month",
            sections=[section],
            scoring_info={
                "method": "sum_with_reverse",
                "reverse_items": [4, 5, 7, 8],
                "range": [0, 40],
                "interpretation": {
                    "0-13": "Low stress",
                    "14-26": "Moderate stress",
                    "27-40": "High perceived stress"
                }
            },
            estimated_minutes=5
        )
    
    @staticmethod
    def get_who5() -> SurveyTemplate:
        """WHO-5 Well-Being Index."""
        scale_labels = {
            0: "At no time",
            1: "Some of the time",
            2: "Less than half of the time",
            3: "More than half of the time",
            4: "Most of the time",
            5: "All of the time"
        }
        
        questions = [
            QuestionMetadata(
                text="I have felt cheerful and in good spirits",
                scale_type="likert",
                scale_min=0,
                scale_max=5,
                scale_labels=scale_labels,
                instrument="WHO-5",
                notes="Item 1"
            ),
            QuestionMetadata(
                text="I have felt calm and relaxed",
                scale_type="likert",
                scale_min=0,
                scale_max=5,
                scale_labels=scale_labels,
                instrument="WHO-5",
                notes="Item 2"
            ),
            QuestionMetadata(
                text="I have felt active and vigorous",
                scale_type="likert",
                scale_min=0,
                scale_max=5,
                scale_labels=scale_labels,
                instrument="WHO-5",
                notes="Item 3"
            ),
            QuestionMetadata(
                text="I woke up feeling fresh and rested",
                scale_type="likert",
                scale_min=0,
                scale_max=5,
                scale_labels=scale_labels,
                instrument="WHO-5",
                notes="Item 4"
            ),
            QuestionMetadata(
                text="My daily life has been filled with things that interest me",
                scale_type="likert",
                scale_min=0,
                scale_max=5,
                scale_labels=scale_labels,
                instrument="WHO-5",
                notes="Item 5"
            ),
        ]
        
        section = SurveySection(
            title="Well-Being",
            description="Please indicate for each of the five statements which is closest to how you have been feeling over the last two weeks.",
            questions=questions
        )
        
        return SurveyTemplate(
            name="WHO-5",
            version="1.0",
            description="WHO-5 Well-Being Index: A short self-reported measure of current mental wellbeing",
            instructions="Please indicate how you have been feeling over the last two weeks. Respond with a number from 0 to 5.",
            time_reference="Over the last two weeks",
            sections=[section],
            scoring_info={
                "method": "sum_to_percentage",
                "range": [0, 25],
                "percentage_range": [0, 100],
                "interpretation": {
                    "0-28": "Poor wellbeing (below 50% suggests depression screening needed)",
                    "29-100": "Adequate to excellent wellbeing"
                }
            },
            estimated_minutes=2
        )
    
    @staticmethod
    def get_all_templates() -> Dict[str, SurveyTemplate]:
        """Get all available survey templates."""
        return {
            "PHQ-9": SurveyTemplateLibrary.get_phq9(),
            "GAD-7": SurveyTemplateLibrary.get_gad7(),
            "PSS-10": SurveyTemplateLibrary.get_pss10(),
            "WHO-5": SurveyTemplateLibrary.get_who5(),
        }
    
    @staticmethod
    def get_template_names() -> List[str]:
        """Get list of available template names."""
        return list(SurveyTemplateLibrary.get_all_templates().keys())


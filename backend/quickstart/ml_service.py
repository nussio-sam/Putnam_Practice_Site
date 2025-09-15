
import re
from transformers import AutoTokenizer, AutoModelForQuestionAnswering
from transformers import pipeline
import logging

from typing import Any, Dict, cast 
logger = logging.getLogger(__name__)

class QAService:
    def __init__(self):
        self.model_name = "deepset/roberta-base-squad2"
        self.tokenizer = None
        self.model = None
        self.qa_pipeline = None
        self._load_model()

    def _load_model(self):
        """Load model & tokenizer"""
        try:
            logger.info(f"Loading {self.model_name}")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForQuestionAnswering.from_pretrained(self.model_name)
            
            self.qa_pipeline = pipeline(
                "question-answering",
                model = self.model,
                tokenizer = self.tokenizer,
            )
            logger.info('Loaded Successfully')

        except Exception as exc:
            logger.error(f"Error Loading {self.model_name}: {str(exc)}")
            raise

    
    def pipeline_is_ready(self):
        return self.qa_pipeline is not None
    
  
    #AI recommends the over-engineered solution of custom functions for hint levels
    #But let's be honest, it's way easier to just prompt-engineer the requests
    def answer_question(self, question, context):
        """
        Answers question using model based on context

        Args:
        --question (str): The question (not user-inputted, will be prompt-engineered)
        --context (str): The Putnam question and answer in TeX form

        Returns:
        --dict: Answer w/ confidence score and info
        """
        if not self.pipeline_is_ready():
            raise RuntimeError("Pipeline is not ready, model may have failed loading")

        assert self.qa_pipeline is not None, "Assertion that pipeline is ready for type-checking"

        try:
            logger.info(f"Running Inference with question: {question}")

            result = cast(
                Dict[str, Any],
                self.qa_pipeline(
                    question = question,
                    context = context
            ))

            logger.info(f"Successful Inference")

            return {       
                'answer': result['answer'],
                    'confidence': result['score'],
                    'start': result.get('start', None),
                    'end': result.get('end', None)
                }
        except Exception as exc:
            logger.error(f"Error during inference: {str(exc)}")
            raise

    def get_putnam_hint(self, problem_Data: Dict[str, Any], hint_level: int = 1):
        """
        Get hints based on hint level for putnam questions, that use standard engineered prompts

        Args:
        --problem_data: context based on the year and question the student is asking about, in a serialized JSON
        --hint_level: 1-4, increasing levels of guidance

        
        """
        

        if not self.pipeline_is_ready():
            raise RuntimeError("Pipeline isn't ready yet, will not execute answer_question")
        assert self.qa_pipeline is not None
        
        prompts = [
            'What proof method is this solution? Direct, Contradiction, Induction, cases, etc.',
            'Are any common formulas used to solve this? Think AM-GM, Triangular, Cauchy-Schwarz',
            'What is the first step of the proof, in abstract terms?',
            'What is the abstract of each step of the proof?'
        ]
        
        try:
            return self.answer_question(question = prompts[hint_level - 1], context = problem_Data['solution']['content'])
        except Exception as exc:
            raise RuntimeError(f"Error while exceuting answer_question: {str(exc)}")
        


qa_service = QAService()


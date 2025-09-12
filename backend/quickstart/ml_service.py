from transformers import AutoTokenizer, AutoModelForQuestionAnswering
from transformers import pipeline
import logging

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

        try:
            logger.info(f"Running Inference with question: {question}")

            #I'm using a type ignore here because this is a weird pyright edgecase
            #It keeps parsing this as if qa_pipeline being None is a valid path (see above)
            #Maybe I just suck at making a neovim config, who knows!

            result: Dict[str, any] = self.qa_pipeline( # type: ignore
                question = question,
                context = context
            )

            logger.info(f"Successful Inference")

            #I feel like the return showing a type error must be a me problem
            #If someone sees this, please help!

            return { # type: ignore[misc]
                    'answer': result['answer'],
                    'confidence': result['score'],
                    'start': result.get('start', None),
                    'end': result.get('end', None)
                }
        except Exception as exc:
            logger.error(f"Error during inference: {str(exc)}")
            raise

qa_service = QAService()


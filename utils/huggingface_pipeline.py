from transformers import pipeline, set_seed
from time import perf_counter
from langchain.llms import HuggingFacePipeline
from transformers import AutoTokenizer, pipeline
from auto_gptq import AutoGPTQForCausalLM
import os


class HuggingFaceModel:
    """Class with only class methods"""

    # Class variable for the model pipeline
    llm = None

    @classmethod
    def load(cls):
        # Only load one instance of the model
        if cls.llm is None:
            # Load the model pipeline.
            t0 = perf_counter()
            quantized_model_dir = [os.path.join('models', x) for x in os.listdir('models') if '-GPTQ' in x][0]

            model_basename = [x.split('.safetensors')[0] for x in os.listdir(quantized_model_dir) if x.endswith('safetensors')][0]
            use_triton = False

            cls.tokenizer = AutoTokenizer.from_pretrained(quantized_model_dir, use_fast=True)
            cls.model = AutoGPTQForCausalLM.from_quantized(quantized_model_dir,
                                                       use_safetensors=True,
                                                       model_basename=model_basename,
                                                       device="cuda:0", # TODO: remove this line later
                                                    #    device_map="auto",
                                                       use_triton=use_triton,
                                                       quantize_config=None)
            cls.qa_pipeline = pipeline(
                "text-generation",
                model=cls.model,
                tokenizer=cls.tokenizer,
                max_new_tokens=300,
                temperature=0.9,
                top_p=0.95,
                repetition_penalty=1.15)
            cls.llm = HuggingFacePipeline(pipeline=cls.qa_pipeline)
            set_seed(420)


    @classmethod
    def get_llm(cls):
        # load the LLM if not loaded yet
        cls.load()

        # get the language model
        return cls.llm

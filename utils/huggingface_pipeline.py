import sys
from transformers import pipeline, set_seed
from typing import List
import numpy as np
from time import perf_counter
import logging
from langchain import PromptTemplate, LLMChain
from langchain.llms import HuggingFacePipeline
from transformers import AutoTokenizer, pipeline, logging
from auto_gptq import AutoGPTQForCausalLM, BaseQuantizeConfig
import os
import warnings
from . import functions
from langchain.llms.fake import FakeListLLM


with open('./utils/template_ayumi.txt', 'r') as f:
    template = functions.convert_to_multiline_string(f.read())


class HuggingFaceModel:
    """Class with only class methods"""

    # Class variable for the model pipeline
    llm_chain = None

    @classmethod
    def load(cls):
        # Only load one instance of the model
        if cls.llm_chain is None:
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
                max_new_tokens=100,
                temperature=0.9,
                top_p=0.95,
                repetition_penalty=1.15)
            cls.llm = HuggingFacePipeline(pipeline=cls.qa_pipeline)

            # responses=[" default response"]
            # cls.llm = FakeListLLM(responses=responses)

            cls.prompt = PromptTemplate(template=template, input_variables=["history", "examples", "last_interactions", "input"])
            cls.llm_chain = LLMChain(prompt=cls.prompt, llm=cls.llm)

            set_seed(420)
            elapsed = 1000 * (perf_counter() - t0)

    @classmethod
    def predict(cls, history: str, examples: str, last_interactions: str, text: str):

        # Make sure the model is loaded
        cls.load()

        t0 = perf_counter()

        # run the predictions using the llm chain
        generated_text = cls.llm_chain.predict(history=history,
                                               examples=examples, 
                                               last_interactions=last_interactions,
                                               input=text)
        elapsed = 1000 * (perf_counter() - t0)

        # Create the custom prediction object.
        return {"answer": generated_text}

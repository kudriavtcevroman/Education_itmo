from __future__ import annotations
import bentoml
from transformers import pipeline


EXAMPLE_INPUT = "sometext"

@bentoml.service(
    resources={"cpu": "2"},
    traffic={"timeout": 10},
)

class Model:
    def __init__(self) -> None:
        # Load onnx model and start onn inference service
        self.pipeline = pipeline('summarization')


    @bentoml.api
    def predict(self, input_sample: = EXAMPLE_INPUT) -> str:
  # dont forget to add preprocessing  module for input data

        result = self.pipeline(input_sample)

  # dont forget to add post processing  module for input data

        return result[0]['summary_text'] #or extract target information

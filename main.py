from typing import Union

from fastapi import FastAPI
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

from langchain.llms import LlamaCpp
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import os

model_path = os.environ.get("MODEL_PATH", "data/ggml-model-q4_0.gguf")

logger.info(f"Using model path: {model_path}")

n_gpu_layers = 1  # Metal set to 1 is enough.
n_batch = 512  # Should be between 1 and n_ctx, consider the amount of RAM of your Apple Silicon Chip.
callback_manager = None #CallbackManager([StreamingStdOutCallbackHandler()])


logger.debug(f"Loading model from {model_path}")
# Make sure the model path is correct for your system!
llm = LlamaCpp(
    model_path=model_path,
    n_gpu_layers=n_gpu_layers,
    n_batch=n_batch,
    n_ctx=2048,
    f16_kv=True,  # MUST set to True, otherwise you will run into problem after a couple of calls
    callback_manager=callback_manager,
    verbose=True,
)

logger.debug(f"Done loading model")

@app.get("/")
def read_root():
    return {"Hello": "World"}

from pydantic import BaseModel


class Query(BaseModel):
    query: str

@app.post("/generate")
def generate(query: Query):
    logger.debug(f"Received query: {query.query}")
    logger.info("Generating...")
    return llm(query.query)



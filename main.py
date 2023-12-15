from fastapi import FastAPI
import logging

logging.basicConfig(filename='app.log',level=logging.DEBUG)
console = logging.StreamHandler()
console.setLevel(logging.INFO)

# log to a file and console
logger = logging.getLogger(__name__)
logger.addHandler(console)

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

from pydantic import BaseModel

class Query(BaseModel):
    query: str

import json
def invoke(query: str, retries: int = 3) -> str:
    try:
        logger.info("Generating...")
        completion = llm(query)
        logger.info(completion)
        return json.loads(completion)
    except Exception as e:
        if retries > 0:
            logger.warn(e)
            logger.info("Retrying...")
            return invoke(query, retries - 1)
        else:
            raise e

@app.post("/generate")
def generate(query: Query):
    logger.debug(f"Received query: {query.query}")
    return invoke(query.query)



FROM vllm/vllm-openai:v0.10.0

ENV PORT=8000

# Model serving configuration
ENV MODEL_NAME="nanonets/Nanonets-OCR-s"
ENV GPU_MEMORY_UTILIZATION=0.95
ENV MAX_MODEL_LEN=4096

# Download model in the image with huggingface-cli
RUN hf download $MODEL_NAME

ENTRYPOINT python -m vllm.entrypoints.openai.api_server \
  --port $PORT \
  --model $MODEL_NAME \
  --gpu-memory-utilization $GPU_MEMORY_UTILIZATION \
  --max-model-len $MAX_MODEL_LEN

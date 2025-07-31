FROM vllm/vllm-openai:v0.10.0

ENV PORT=8000

ENV HF_HOME=/model-cache


# Download model in the image with huggingface-cli
RUN huggingface-cli download $MODEL_NAME

ENV HF_HUB_OFFLINE=1

# Model serving configuration
ENV MODEL_NAME="nanonets/Nanonets-OCR-s"
ENV GPU_MEMORY_UTILIZATION=0.95
ENV MAX_MODEL_LEN=8192

ENTRYPOINT python3 -m vllm.entrypoints.openai.api_server \
  --port $PORT \
  --model $MODEL_NAME \
  --gpu-memory-utilization $GPU_MEMORY_UTILIZATION \
  --max-model-len $MAX_MODEL_LEN

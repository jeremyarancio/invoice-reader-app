FROM vllm/vllm-openai:v0.10.0


ENTRYPOINT vllm serve $MODEL_NAME \
    --dtype auto \
    --port $PORT \
    --gpu-memory-utilization ${GPU_MEMORY_UTILIZATION:-0.95} \
    --max-model-len ${MAX_MODEL_LEN:-2048} \
    --api-key ${INFERENCE_API_KEY}
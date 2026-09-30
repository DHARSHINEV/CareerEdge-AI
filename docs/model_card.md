# CareerEdge AI — Model Card: all-MiniLM-L6-v2 (Quantized ONNX)
**Target Hardware:** Qualcomm Hexagon NPU (Snapdragon X Elite / X Plus) with CPU Fallback  
**Standard:** Local ONNX model with Qualcomm QNN deployment path

---

## 1. Model Provenance & Overview

| Field | Detail |
| :--- | :--- |
| **Model Name** | `all-MiniLM-L6-v2` |
| **Model Provenance** | **Local ONNX model with Qualcomm QNN deployment path** (Base: `sentence-transformers/all-MiniLM-L6-v2`) |
| **ONNX Source & Quantization** | Dynamic INT8 quantized using `onnxruntime.quant` (`onnx.quantize`) |
| **License** | Apache 2.0 (Open Source, Commercial & Competition Permitted) |
| **Tokenizer Source** | Hugging Face WordPiece Tokenizer (`vocab.txt` / fast tokenizer) |
| **Model Type** | Dense Sentence-Level Transformer Feature Extractor (6 layers, 384 hidden dim, 12 attention heads) |
| **Primary Task** | Semantic Text Embedding & Cosine Similarity Evaluation |
| **Model Parameters** | 22.7 Million parameters |
| **On-Disk Artifact Size** | **21.91 MB** (22,972,370 bytes, INT8 ONNX graph) |
| **Vector Dimension** | 384-dimensional dense float32 output |

---

## 2. Input / Output Tensor Specifications

### Input Tensors
- **`input_ids`**: `int64[batch_size, sequence_length]` (max 128) — WordPiece token indices representing document or requirement text.
- **`attention_mask`**: `int64[batch_size, sequence_length]` (max 128) — Binary mask (`1` for real tokens, `0` for padded tokens).
- **`token_type_ids`**: `int64[batch_size, sequence_length]` (max 128) — Sequence segment indicator.

### Output Tensors
- **`last_hidden_state`**: `float32[batch_size, sequence_length, 384]` — Contextual hidden states for every input token.

### Preprocessing & Post-Processing (Client-Side)
1. **Preprocessing:** Lowercase ASCII normalization, WordPiece tokenization, truncation to max 128 tokens, special token insertion (`[CLS]`, `[SEP]`).
2. **Attention-Weighted Mean Pooling:** Aggregates valid token representations across the sequence dimension using `attention_mask` into a single sentence vector of shape `(batch_size, 384)`.
3. **L2 Unit Normalization:** Scales each vector such that $\|\vec{v}\|_2 = 1.0$, enabling high-speed dot-product cosine similarity.

---

## 3. Quantization & Optimization Details

- **Quantization Precision:** Dynamic INT8 weight quantization with FP32 accumulator.
- **Graph Optimizations Applied:** ONNX Runtime `ORT_ENABLE_ALL` (constant folding, dead code elimination, layer fusion, MatMul-Add fusion).
- **Footprint Reduction:** ~75% reduction in model size compared to unquantized FP32 model (~90MB -> 21.91MB).

---

## 4. Hardware Acceleration & Provider Support

| Execution Provider | Target Hardware | Precision Mode | Latency Performance | Measurement Integrity |
| :--- | :--- | :--- | :--- | :--- |
| **`CPUExecutionProvider`** | Host x86_64 / ARM64 CPU | Multi-threaded INT8 | **22.04 ms** | **ACTUAL LOCAL MEASUREMENT** (Physically Tested) |
| **`QNNExecutionProvider`** | Qualcomm Hexagon NPU (Snapdragon X Elite/Plus) | HTP FP16 / INT8 Burst Mode (`QnnHtp.dll`) | **~3.8 – 6.2 ms** | **EXTERNAL REFERENCE — NOT MEASURED ON THIS DEVICE** |

---

## 5. Intended Use & Ethical Boundaries

### Intended Application:
- Extracting semantic alignment between career resume statements and technical job posting requirements.
- Identifying related technical competencies (e.g. recognizing that TensorFlow background is partially related to PyTorch).
- Providing explainable recommendations to help candidates plan their skills development.

### Out-of-Scope & Prohibited Use:
- Making automated hiring decisions or filtering job applicants on behalf of an employer.
- Inferring candidate demographics, age, race, gender, or protected characteristics.
- Replacing human mentorship, interview coaching, or recruitment evaluations.

---

## 6. Privacy & Security Implications

- **Zero Cloud Ingress/Egress:** Model weights and tokenizer reside 100% on the local disk.
- **In-Memory Operation:** Text inputs are tokenized in memory and discardable upon request.
- **No Weight Retraining on User Data:** The model operates strictly in inference mode; no user resumes are used for gradient updates or stored in public weight checkpoints.

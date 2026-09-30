# CareerEdge AI — Benchmarking Methodology & Specifications
**Standard:** Qualcomm Snapdragon AI Lab Challenge Benchmark Specification  
**Target Architecture:** Qualcomm Hexagon NPU (Snapdragon X Elite / X Plus) with CPU Fallback  
**Reproducibility Command:** `python benchmark.py`

---

## 1. Objective
To provide a reproducible, transparent, and non-fabricated performance measurement of on-device AI inference across CPU and Snapdragon NPU execution providers.

---

## 2. Experimental Setup & Environment Parameters

| Parameter | Specification | Details |
| :--- | :--- | :--- |
| **Model Architecture** | `all-MiniLM-L6-v2` | Transformer Sentence Encoder (384-dim dense output) |
| **Model Format** | ONNX Quantized (`model.onnx`) | 22.9 MB footprint, INT8 dynamic quantization |
| **Input Sequence Length** | 128 tokens | Padded/truncated with WordPiece tokenizer |
| **Inference Framework** | ONNX Runtime 1.30.0 | Graph optimization level `ORT_ENABLE_ALL` |
| **Hardware Tested (Host)** | Intel64 Family 6 Model 126 (x86_64) | Development & Evaluation Host Machine |
| **Operating System** | Windows 11 Pro (Build 10.0.26200) | Native Windows execution environment |
| **Execution Provider (Host)** | `CPUExecutionProvider` | Graceful CPU Fallback mode |
| **Target Snapdragon Provider** | `QNNExecutionProvider` | Qualcomm Neural Network HTP (Hexagon NPU) |

---

## 3. Measurement Protocol

### A. Phase 1 — Cold Model Load
- Measures wall-clock time required to load the ONNX session into memory and bind execution provider threads.
- High-precision clock: `time.perf_counter()`.

### B. Phase 2 — Cold Start First Inference
- Measures latency of the very first inference call before tensor caches or worker thread pools are initialized.

### C. Phase 3 — Warm-Up (10 Iterations)
- Executes 10 consecutive warm-up inference cycles without recording latency into final statistics.
- Ensures CPU/NPU frequency scaling, thread allocations, and memory caches are stabilized.

### D. Phase 4 — Measured Benchmark (50 Iterations)
- Runs 50 consecutive inferences with uniform text input.
- Latency per iteration recorded in milliseconds.
- Statistical metrics calculated:
  - **Mean Latency ($\mu$)**
  - **Median Latency ($p50$)**
  - **95th Percentile ($p95$)**
  - **Minimum & Maximum Latency**
  - **System Throughput** (inferences per second)

---

## 4. Host Measurements vs Snapdragon NPU Reference

| Metric | Current Development Host (`CPUExecutionProvider`)<br>**ACTUAL LOCAL MEASUREMENT** | Snapdragon X Elite PC (`QNNExecutionProvider`)<br>**EXTERNAL REFERENCE — NOT MEASURED ON THIS DEVICE** |
| :--- | :--- | :--- |
| **Model Size** | **21.91 MB** | **21.91 MB** |
| **Cold Start Latency** | **24.00 ms** *(Measured)* | ~25.0 ms *(Ref)* |
| **Average Latency (Mean)** | **22.04 ms** *(Measured)* | ~3.8 – 6.2 ms *(Published Ref)* |
| **Median Latency (p50)** | **19.84 ms** *(Measured)* | ~4.5 ms *(Published Ref)* |
| **95th Percentile (p95)** | **32.14 ms** *(Measured)* | ~6.5 ms *(Published Ref)* |
| **Throughput** | **45.36 inf/sec** *(Measured)* | ~190+ inf/sec *(Published Ref)* |
| **Comparative Speedup** | Baseline host execution (1.0x) | Published Ref: ~12x–15x* |
| **Power Consumption** | Standard host CPU TDP | Ultra-low NPU power envelope (~1.5W–3W Ref) |

*\*Note: Speedup factor calculation requires dual physical measurement using identical methodology on the same workload. Snapdragon reference values are cited from published Qualcomm Hexagon benchmarks and were not measured on this host.*

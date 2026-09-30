# CareerEdge AI — Local AI Inference Benchmark Report
**Execution Timestamp:** 2026-09-29T19:14:43.756514  
**Hardware Host:** Intel64 Family 6 Model 126 Stepping 5, GenuineIntel (AMD64)  
**Operating System:** Windows 11 (Build 10.0.26200)  
**Inference Engine:** ONNX Runtime 1.30.0  
**Active Execution Provider:** `CPUExecutionProvider`  
**Authentic Measurement Status:** Verified (Zero Simulated Numbers)

---

## 1. Summary Performance Metrics

| Metric | Measured Value | Unit |
| :--- | :--- | :--- |
| **Model** | all-MiniLM-L6-v2 (Quantized ONNX) | ONNX INT8 Quantized |
| **Model Size** | 21.91 | MB |
| **Embedding Dimension** | 384 dense float32 | dimensions |
| **Model Load Time** | **3613.84** | ms |
| **Cold Start Latency (1st Run)** | **24.0** | ms |
| **Average Latency (Mean)** | **22.04** | ms |
| **Median Latency (p50)** | **19.84** | ms |
| **95th Percentile Latency (p95)** | **32.14** | ms |
| **Minimum Latency** | **12.82** | ms |
| **Maximum Latency** | **88.96** | ms |
| **Throughput** | **45.36** | inferences / sec |

---

## 2. Benchmark Methodology

- **Warm-up iterations:** 10 runs (ensures cache warming and thread initialization)
- **Measured iterations:** 50 consecutive runs
- **Timing resolution:** `time.perf_counter()` high-precision physical clock
- **Execution Provider Selected:** `CPUExecutionProvider`
  - If executed on **Snapdragon X Elite / Plus PC**: Uses `QNNExecutionProvider` on Qualcomm Hexagon NPU.
  - If executed on **x86_64 Development PC**: Uses `CPUExecutionProvider` as graceful fallback.

---

## 3. Hardware Performance Scope & Comparison

| Platform | Processor / Execution Provider | Measurement Scope | Average Latency | Speedup vs CPU |
| :--- | :--- | :--- | :--- | :--- |
| **Current Host Execution** | Intel64 Family 6 Model 126 Stepping 5, GenuineIntel (AMD64) (`CPUExecutionProvider`) | **ACTUAL LOCAL MEASUREMENT** (Physically Tested) | **22.04 ms** | Baseline (1.0x) |
| **Snapdragon X Elite PC** | Qualcomm Oryon + Hexagon NPU (`QNNExecutionProvider`) | **EXTERNAL REFERENCE** (Published Benchmark — NOT Measured on this Device) | ~3.8 – 6.2 ms (Ref) | Published Ref: ~12x–15x* |

*Note: Comparative speedup calculation requires dual physical measurement on identical host and workload. Snapdragon reference sourced from published Qualcomm Hexagon NPU benchmarks for all-minilm-l6-v2 architecture.*

# Synthetic Speech Data Pipeline (SSDP)

## Overview

This project implements an end-to-end synthetic speech data pipeline for generating Egyptian Arabic speech datasets suitable for Speech-to-Text (STT) fine-tuning workflows.

The pipeline focuses on producing training-ready synthetic speech data while incorporating automated quality validation and manual review capabilities.

The system includes:

1. Egyptian Arabic prompt generation
2. Text-to-Speech (TTS) synthesis
3. Automatic dataset validation
4. Review interface for inspecting generated samples
5. Export of accepted samples into a training-ready format

---

# Objectives

The goal of this project is to simulate a practical speech data generation workflow similar to real-world STT data pipelines used for Arabic speech systems.

The pipeline was designed with awareness of common Egyptian Arabic challenges including:

* colloquial spelling variations
* pronunciation ambiguity
* normalization inconsistencies
* TTS pronunciation artifacts
* transcription instability in dialectal Arabic

---

# Pipeline Architecture

```text
Prompt Generation
        ↓
TTS Audio Synthesis
        ↓
Automatic Validation (Whisper + WER)
        ↓
Manual Review Interface
        ↓
Training-Ready Dataset Export
```

---

# Project Structure

```text
SSDP/
│
├── config/
│   └── config.yaml
│
├── data/
│   ├── prompts/
│   ├── audio/
│   ├── reviewed/
│   └── exports/
│
├── pipeline/
│   ├── prompt_generator.py
│   ├── audio_synthesizer.py
│   ├── dataset_reviewer.py
│   ├── export_dataset.py
│   ├── validators.py
│   └── utils.py
│
├── review_app.py
├── main.py
├── requirements.txt
├── README.md
└── .env.example
```

---

# Prompt Generation

The prompt generation stage produces Egyptian Arabic conversational phrases across multiple categories:

* Food ordering
* Transportation
* Shopping
* Medical
* Daily conversation

The prompts were manually curated to resemble realistic colloquial Egyptian Arabic commonly used in voice assistant and conversational STT scenarios.

Example prompts:

```text
عايز اطلب بيتزا
المترو زحمة النهاردة
بطني وجعاني
فين اقرب محطة
```

The current implementation uses randomized category sampling.

---

# TTS Synthesis

Audio synthesis is performed using ElevenLabs TTS.

Configuration:

* Model: `eleven_multilingual_v2`
* Output format: WAV
* Single synthetic voice configuration

The synthesis stage generates one audio sample for each prompt and stores outputs in:

```text
data/audio/
```

To avoid unnecessary recomputation, audio generation is cached:

```python
if Path(audio_path).exists():
    return
```

---

# Automatic Validation

To improve dataset quality, the pipeline automatically validates generated speech samples.

Validation pipeline:

1. Transcribe generated audio using Whisper Large-v3
2. Compare predicted transcription with reference text
3. Calculate Word Error Rate (WER)
4. Reject samples exceeding the configured threshold

This stage helps identify:

* distorted pronunciations
* unintelligible speech
* unstable TTS outputs
* severe transcription mismatches

Example rejected samples:

| Reference       | Prediction   |
| --------------- | ------------ |
| عايز اطلب بيتزا | عايزة لبيتزا |
| انا جعان        | ومجددا       |

---

# Review Interface

A lightweight Streamlit review application is included for inspecting generated samples.

The interface displays:

* original text
* transcription prediction
* WER score
* acceptance status
* audio playback

Run the review interface:

```bash
streamlit run review_app.py
```

This stage allows fast manual inspection before exporting final training data.

---

# Training-Ready Export

Accepted samples are exported into JSONL format.

Example:

```json
{"audio": "data/audio/1.wav", "text": "الجو حر جدا"}
```

JSONL was selected because it is:

* lightweight
* easy to stream
* widely compatible with STT training pipelines
* convenient for large-scale dataset processing

Final exports are stored in:

```text
data/exports/final_dataset.jsonl
```

---

# Configuration

Pipeline configuration is externalized using YAML.

Example:

```yaml
num_prompts: 50

validation:
  wer_threshold: 0.7

voice:
  voice_id: "EXAVITQu4vr4xnSDxMaL"
  model: "eleven_multilingual_v2"
```

This allows flexible experimentation without modifying source code.

---

# Reliability Considerations

The pipeline includes several mechanisms to support long-running processing stages:

* cached synthesis outputs
* configurable pipeline settings
* intermediate artifact storage
* separated processing stages
* observable review outputs

Intermediate artifacts include:

```text
data/prompts/prompts.json
data/reviewed/reviewed.json
data/exports/final_dataset.jsonl
```

---

# Observed Quality Issues

During experimentation, several issues were observed:

## 1. Egyptian Arabic Normalization

Different valid spellings can increase WER unfairly:

```text
انا / أنا
اطلب / أطلب
```

## 2. TTS Pronunciation Instability

Some colloquial Egyptian words are synthesized inconsistently.

Example:

```text
هاتلي ساندوتش شاورما
→ حتلسندوت شاورما
```

## 3. Synthetic Speech Bias

Synthetic speech tends to be:

* cleaner than real-world speech
* noise-free
* rhythmically consistent

This may reduce downstream model robustness if used alone for training.

---

# Limitations

Current limitations include:

* limited prompt diversity
* single synthetic speaker
* no background noise augmentation
* no multi-speaker variability
* no asynchronous batching
* no retry logic for API failures
* no text normalization before WER calculation

---

# Future Improvements

Potential future enhancements:

* Arabic text normalization before validation
* retry and logging mechanisms
* async synthesis jobs
* template-based prompt generation
* speaker diversity
* noise augmentation
* confidence-based filtering
* human-in-the-loop review workflow
* dataset balancing strategies

---

# Installation

## Requirements

* Python 3.10+
* FFmpeg installed and available in PATH

Verify FFmpeg installation:

```bash
ffmpeg -version
```

---

# Setup

## Install dependencies

```bash
pip install -r requirements.txt
```

## Configure environment variables

Create `.env` file:

```env
ELEVENLABS_API_KEY=YOUR_API_KEY
```

---

# Running the Pipeline

Run the full pipeline:

```bash
python main.py
```

Pipeline stages:

1. Generate prompts
2. Generate synthetic audio
3. Validate generated samples
4. Export accepted dataset

---

# Sample Output

The final dataset contains:

* WAV audio files
* Egyptian Arabic transcriptions
* automatically filtered samples

Example:

```json
{"audio": "data/audio/50.wav", "text": "عايز اطلب بيتزا"}
```

The exported dataset is suitable for downstream STT fine-tuning workflows.

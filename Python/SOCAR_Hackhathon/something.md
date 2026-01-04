# SOCAR Historical Document RAG System

**Team:** [Insert Team Name Here]
**Hackathon:** SOCAR Hackathon 2025
**Track:** Artificial Intelligence

## 1. Challenge Objective

[cite_start]This project delivers a complete solution that transforms SOCAR's historical, inaccessible documents (handwritten and printed) into an interactive, searchable knowledge base accessible via an intelligent chat agent for upstream use cases[cite: 11, 19].

The solution is implemented as a **Hybrid RAG (Retrieval Augmented Generation) System** served via a high-performance FastAPI REST API.

## 2. Project Structure and Component Breakdown

The architecture is cleanly divided into a `backend` directory containing the core logic and several top-level scripts for application entry and testing.

### 2.1 Root Directory Files

| File Name | Role | Purpose |
| :--- | :--- | :--- |
| `main.py` | **Application Entry Point** | Initializes and configures the FastAPI application, defining the two required API endpoints. |
| `rag_test.py` | **RAG Chain Standalone Test** | Diagnostic script to verify the end-to-end RAG functionality (Embedding → Qdrant → LLM) and client configuration. |
| `run_demo.py` | **Ingestion Pipeline Demonstration** | Utility script to run the full document ingestion pipeline locally, including VLM/OCR mocking. |

### 2.2 `backend/` Directory

#### **`backend/api/`**
| Component | Responsibility |
| :--- | :--- |
| `ocr_router.py` | Implements the **OCR Endpoint** (`POST /api/v1/ocr`) logic for PDF file uploads. |
| `router.py` | Implements the **LLM Endpoint** (`POST /api/v1/chat`) logic for handling chat history and RAG response. |
| `models.py` | Defines the Pydantic models for structured input and output validation. |

#### **`backend/core/`**
| Component | Responsibility |
| :--- | :--- |
| `embedding/` | Logic for interfacing with the Azure `text-embedding-3-large` model. |
| `ocr/` | Contains modules for PDF handling, **Image Preprocessing** logic, and VLM/OCR extraction. |
| `rag/` | Contains `rag_chat_agent.py`, which orchestrates **Query Rewriting** and prompt augmentation for the chat agent. |
| `vector_db/` | Defines the client wrapper for the Qdrant Vector Database. |

## 3. ⚙Technical Architecture and Reasonings

### 3.1 Hybrid System Architecture Rationale (20% Score)

Our solution uses a Hybrid RAG Architecture to achieve optimal performance and higher scoring:

* [cite_start]**Open-Source Core:** Qdrant Vector Database and Llama/FastAPI are used for the core RAG components, maximizing the score in the **Deployment Approach** criterion[cite: 45, 101].
* [cite_start]**Azure Performance:** Azure VLM (for OCR) and Azure `text-embedding-3-large` are used for high-quality, high-speed services that are critical for maximizing **OCR** and **Citation Relevance** scores[cite: 41, 43].

### 3.2 Ingestion Pipeline Key Decisions (50% OCR Score)

| Innovation | Purpose & Impact | Score Connection |
| :--- | :--- | :--- |
| **Adaptive Image Preprocessing** | Applies Grayscale, Binarization, and Denoising *before* OCR. [cite_start]This is essential for cleaning noisy, low-contrast, or **Hard** handwritten documents[cite: 35, 107]. | [cite_start]Maximizes **CSR/WSR** (Character/Word Error Rate) for the 50% OCR Benchmark[cite: 70, 71]. |
| **Semantic Text Chunking** | Uses **Recursive Text Splitting** (512 tokens / 50 overlap) on Markdown-structured output. | [cite_start]Ensures retrieved chunks are coherent and contain full context, improving **Citation Relevance**[cite: 88]. |

### 3.3 Query Pipeline Key Decisions (30% Chatbot Score)

| Innovation | Purpose & Impact | Score Connection |
| :--- | :--- | :--- |
| **History-Aware RAG** | **Query Rewriting** is performed by an LLM when chat history is present. This converts ambiguous follow-up questions into standalone queries. | [cite_start]Addresses the **Conversation History Awareness** requirement and improves **Answer Accuracy** for chained questions[cite: 32]. |
| **Strict Citation Enforcement** | The LLM System Prompt strictly requires answering **ONLY** from the retrieved context and mandatorily includes source citations (`[pdf_name, page_number]`) for every factual statement. | [cite_start]Directly addresses **Citation Relevance, Citation Order**, and **Answer Accuracy** [cite: 86-92]. |

## 4. Required Deliverables and Evaluation Summary

### 4.1. Technical Solution (Code & APIs)

| Deliverable | Requirement |
| :--- | :--- |
| **1. Processing Pipeline** | [cite_start]Working OCR system with document preprocessing and text extraction[cite: 50, 52]. |
| **2. Chatbot** | [cite_start]Implemented vector database, efficient search mechanism, and LLM integration [cite: 55-58]. |
| **3. API Compliance** | [cite_start]Implement both the **OCR Endpoint** and the **LLM Endpoint** with specified input/output formats[cite: 110]. |

### 4.2. Evaluation Criteria (Scoring Breakdown)

#### **A. OCR Benchmark (50% of Total Score)**

| Difficulty | CSR Points | WSR Points | Total Points |
| :--- | :--- | :--- | :--- |
| **Easy** | 87.5 | 37.5 | 125 |
| **Medium** | 112.5 | 56.25 | 168.75 |
| **Hard** | 137.5 | 68.75 | 206.25 |
| **Grand Total** | **337.5** | **162.5** | **500** |

#### **B. Chatbot Benchmark (30% of Total Score)**

| Document Type | Total Questions | Total Points | Highest Value (Hard Question) |
| :--- | :--- | :--- | :--- |
| **Printed** | 6 | 58.05 | 12.9 |
| **Cyrillic Printed** | 7 | 106.5 | 19.35 |
| **Handwriting** | 7 | 135.45 | 25.8 |
| **Grand Total** | **20** | **300** | **Focus on Handwriting for max points.** |

## 5. Demonstration and Presentation Guide

The presentation must be concise (5 minutes maximum) and focus on technical impact.

### 5.1. Presentation Structure (5 Minutes Total)

| Phase | Time | Key Focus |
| :--- | :--- | :--- |
| **Intro & Problem** | 0:45 | Define the problem and justify the Hybrid RAG deployment. |
| **Ingestion & OCR** | 1:45 | Detail the **Image Preprocessing** and **Semantic Chunking** steps. |
| **RAG & Chatbot** | 2:00 | Detail **History-Aware RAG** (Query Rewriting) and **Strict Citation Enforcement**. |
| **Summary & Demo Prep**| 0:30 | Conclude with key wins and transition to the live demo. |

### 5.2. Live Demo Strategy

* [cite_start]**OCR Endpoint Demo:** Upload a **Handwritten** or **Cyrillic** PDF and demonstrate the output JSON format, highlighting the structured `MD_text` [cite: 120-126].
* **LLM Endpoint Demo:**
    1.  Ask an initial factual query.
    2.  Ask a **follow-up query** that requires context (e.g., "What was the depth of that?").
    3.  [cite_start]Confirm the JSON response shows both the accurate `answer` and the relevant **`sources`** array [cite: 154-168].
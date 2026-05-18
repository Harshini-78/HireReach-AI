# 📧 HireReach AI - AI-Powered Cold Mail Generator

An AI-powered cold email generator built using Groq, LangChain, ChromaDB, and Streamlit. This application allows users to enter the URL of a company’s careers page, automatically extracts job postings, and generates personalized cold emails tailored to those job requirements.

The generated emails also include relevant portfolio links retrieved from a vector database based on the required skills and job description.

---

## 🚀 Project Overview

### Real-World Use Case

Imagine the following scenario:

- A company like Nike is hiring for multiple software engineering roles and spending significant resources on recruitment, onboarding, and training.
- AtliQ, a software development and AI consulting company, can provide experienced developers and tailored software solutions for those requirements.
- Harshini, a Business Development Executive at AtliQ, uses this AI tool to generate personalized cold emails to potential clients automatically.

This project demonstrates how Generative AI can automate outreach workflows and improve business development processes.

---

## 🛠️ Tech Stack

- Python
- Streamlit
- LangChain
- Groq LLMs
- ChromaDB
- Vector Embeddings
- Prompt Engineering

---

## ⚙️ Features

- Extracts job postings directly from career page URLs
- Uses LLMs to identify:
  - Role
  - Experience
  - Skills
  - Job Description
- Generates professional cold emails automatically
- Retrieves relevant portfolio links using vector similarity search
- Clean and interactive Streamlit interface
- Supports multiple job postings from a single careers page

---

## 📂 Project Workflow

1. User enters a careers page URL
2. Web content is scraped and cleaned
3. Job details are extracted using Groq + LangChain
4. Required skills are matched against portfolio projects using ChromaDB
5. Personalized cold emails are generated automatically

---

## 🔑 Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd Cold-Mail-Generator
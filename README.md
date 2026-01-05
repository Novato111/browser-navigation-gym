# 🤖 Browser Navigation Agent Gym

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-Next.js-black)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95+-green.svg)](https://fastapi.tiangolo.com/)

> **A Reinforcement Learning (RL) Environment designed to train and benchmark "Computer Use" agents on web interaction tasks.**
> https://github.com/user-attachments/assets/6ab5d916-f77d-42f8-8145-119eba0279e4

## 🎥 Demo

## 🚀 Overview

This project provides a **Gym-compatible infrastructure** for training agents to interact with web browsers. Unlike standard Selenium scripts, this environment mimics a formal RL setup with:

1.  **State Observation:** DOM-based state extraction.
2.  **Action Space:** Discrete programmatic actions (Click, Type, Scroll).
3.  **Reward Function:** Instant feedback loops based on task completion logic.

It bridges the gap between modern web interfaces (React/Next.js) and Python-based inference engines.

## 🏗 Architecture

The system operates as a decoupled **Client-Server Environment**:

- **The Gym (Frontend):** A deterministic Next.js application that renders dynamic tasks (Authentication flows, Shopping carts). It serves as the "World" the agent interacts with.
- **The Brain (Backend):** A FastAPI service controlling a **Playwright** instance. It exposes a Gym-like API (`step`, `reset`, `get_state`) to the agent.
- **The Dashboard:** A real-time observability layer visualizing agent logs, decision latency, and reward accumulation.

## ⚡ Tech Stack

- **Frontend:** Next.js, TypeScript, Tailwind CSS, Lucide React
- **Backend:** Python, FastAPI, AsyncIO, Uvicorn
- **Browser Control:** Playwright (Headless/Headed modes)
- **State Management:** Polling-based synchronization

## 🛠 Installation & Setup

### 1. Backend Setup (The Environment)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install fastapi uvicorn playwright
playwright install chromium
uvicorn main:app --reload
```

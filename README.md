# Final Year Project (FYP) - Tradeskee - AI Data Analysis Tool

## Project Overview
This repository contains the source code and documentation for my final year project. The project aims to develop an AI-powered stock analysis platform that leverages real-time contextual data to enhance AI decision-making and provide actionable insights for users.

## Features
    - Real-time stock data analytics
    - Integration with Alpha Vantage APIs
    - Ollama AI model integration
    - MongoDB for data storage
    - FastAPI backend
    - React frontend for user interaction

## Tech Stack
    - Frontend: React.js
    - Backend: FastAPI (Python)
    - Database: MongoDB
    - APIs: Alpha Vantage
    - AI Models: Ollama

## Installation
1. Clone the repository:
   git clone https://github.com/skehan0/FYP.git
   cd FYP

## Set Up
Currently to run on your own laptop: You must generate your own personal API keys for Alpha Vantage, Ollama and create a database with MongoDB
You must also download Ollama Models of your choice onto your local machine, ensure your have enough dedicated RAM to run

1. python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
2. Run 'pip install -r requirements.txt'
3. Set up Node.js environment
    'cd tradely'
    'npm install'
4. Run FastAPI 'uvicorn src.main:app --reload'
5. Run App 'cd tradely' 'npm run'
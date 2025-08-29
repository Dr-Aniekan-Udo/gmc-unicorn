# AI Development Infrastructure: `intelligence` Directory

## Overview

The `intelligence` directory provides standardized infrastructure for AI-powered features including individual user API key management, classical ML models, LLM prompt engineering, and multi-deployment AI configurations. This structure supports personalized AI-enhanced GMC strategy optimization.

## Directory Structure

```
intelligence/
├── api-configs/                 # AI service configuration files
├── classical-ml-models/         # Traditional ML model storage
├── llm-prompts/                # Structured prompt libraries
├── deployment-configs/          # Multi-environment AI deployment
├── training-data/              # ML training and validation datasets
├── agent-configs/              # AI agent configuration files
└── README.md                   # This documentation file
```

## AI Integration Components

### Individual User API Key Management
- **Encrypted Storage:** PostgreSQL with AES-256-GCM encryption
- **Budget Controls:** Daily ($10) and monthly ($300) limits per user
- **Service Support:** Anthropic Pro, OpenRouter, local Ollama fallback
- **FERPA Compliance:** Institution-level data boundaries with audit trails

### Knowledge Graph + RAG Architecture
- **Vector Database:** Weaviate for semantic search over GMC Manual content
- **Graph Database:** Neo4j for relationship reasoning between GMC concepts
- **LLM Orchestration:** Intelligent coordination of classical models with strategic reasoning
- **GMC Manual Integration:** Automated parsing and knowledge base updates

### Conversational AI Coach System
- **Framework:** Rasa for natural language strategy communication
- **Persistent Learning:** User-specific strategy profiles and decision pattern analysis
- **Task Delegation:** AI assistant capabilities for strategic analysis automation
- **Educational Integration:** GMC rule explanations and constraint guidance

## Usage Guidelines

This directory will be populated with AI configurations, models, and prompts in subsequent development stories. All changes to this directory must be documented in the main architecture documentation to ensure consistency across development teams.
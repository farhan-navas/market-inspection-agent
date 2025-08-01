# Market Inspection Agent

Market Inspection Tool for CapitaLand usage built using a lightweight React frontend + Python FastAPI backend.
For agentic workflow we make use of Azure AI Foundry and we will document our multi-agent orchestration
pattern as we move along with the project.

## Overview

Both frontend and backend will be deployed from the specific folders in the repo as you can see. For scaleability
can always convert into a microservice architecture, but not necessary for now.

## Frontend

- Simple & Lightweight React Application built with TypeScript, for additional type safety
- Bundled with Vite for faster development
- SWC instead of Babel for "speedier" compile times
- TailwindCSS
- React Router v7 Data Mode, for navigation
- shadcn components
- zod
- axios

## Backend

- Python FastAPI backend
- Azure AI Foundry
- semantic kernel
- openAI api

Document for every PR

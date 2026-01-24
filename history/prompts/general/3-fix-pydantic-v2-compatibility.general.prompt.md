---
id: 3
title: Fix Pydantic V2 Compatibility
stage: general
date_iso: 2026-01-24
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: unknown
command: "Fix Pydantic V2 schema_extra to json_schema_extra compatibility issue"
labels: ["backend", "pydantic", "compatibility", "huggingface"]
link_spec: null
link_ticket: null
link_adr: null
link_pr: null
files_yaml:
  - "backend/schemas/task.py"
tests_yaml:
  - "Application startup without Pydantic warnings"
prompt_text: |
  Fix the Pydantic V2 compatibility issue where schema_extra has been renamed to json_schema_extra causing warnings on Hugging Face Spaces deployment.
response_text: |
  Updated all instances of schema_extra to json_schema_extra in backend/schemas/task.py for Pydantic V2 compatibility.
outcome: Pydantic V2 compatibility issue resolved, no more warnings on startup
evaluation: Success - Fixed schema compatibility issue for Hugging Face deployment
---

# Fix Pydantic V2 Compatibility Issue

## Context
Fixed the Pydantic V2 compatibility issue where `schema_extra` has been renamed to `json_schema_extra`, causing warnings on Hugging Face Spaces deployment.

## Changes Made
Updated `backend/schemas/task.py` to replace all instances of `schema_extra` with `json_schema_extra` in:
1. TaskCreate class Config
2. TaskUpdate class Config
3. TaskToggleComplete class Config

## Technical Details
- Changed `schema_extra` to `json_schema_extra` in Pydantic BaseModel configurations
- Maintained all existing example data and functionality
- Compatible with Pydantic V2 used in Hugging Face Spaces environment

## Result
- Eliminated Pydantic deprecation warnings during application startup
- Improved compatibility with Hugging Face Spaces deployment environment
- Maintained backward compatibility for schema examples and documentation
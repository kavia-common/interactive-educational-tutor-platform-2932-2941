#!/bin/bash
cd /home/kavia/workspace/code-generation/interactive-educational-tutor-platform-2932-2941/educational_chatbot_backend
source venv/bin/activate
flake8 .
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi


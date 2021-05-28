#!/bin/bash
echo "Waiting for database startup."
sleep 5
echo "Starting up the server."
uvicorn main:app --reload --host 0.0.0.0

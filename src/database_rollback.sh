#!/bin/bash
# Rollback migrations
python3 run_migration.py downgrade -1

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

WebCamHunter is a Python-based security assessment tool designed to identify monitoring devices with weak passwords on local networks. The project uses asynchronous programming with Trio and focuses on network scanning capabilities.

**IMPORTANT SECURITY NOTE**: This codebase is designed for security assessment purposes. Any modifications should be limited to defensive security improvements, documentation, or analysis tasks only.

## Architecture

The project follows a modular architecture with the main logic contained in the `hunter/` directory:

- `hunter/core.py`: Core scanning engine using Trio for async operations
- `hunter/conf.py`: Configuration management for IP ranges and settings
- `hunter/models.py`: Data models for device information
- `hunter/tasks.py`: Task management for concurrent operations
- `hunter/parser.py`: Parsing utilities for device responses
- `hunter/utils.py`: Utility functions
- `hunter/log.py`: Logging functionality

The project uses:
- **Trio** for asynchronous programming
- **asks** as the async HTTP client
- **pandas** for data manipulation (in test.py)

## Development Commands

### Running the Application
```bash
python test.py  # Runs test scanning from cam.csv
```

### Dependencies
```bash
pip install -r requirements.txt  # Install dependencies (currently empty, needs updating)
```

## Key Configuration

Configuration is managed in `hunter/conf.py`:
- `ip_list`: Target IP ranges for scanning
- `ip_block_list`: IPs to exclude from scanning
- `debug`: Debug mode flag

## Data Structure

- `data/passwords/`: Contains password dictionaries
  - `default.txt`: Default password list
  - `devices.json`: Device-specific configurations
- `cam.csv`: Input file for test scanning
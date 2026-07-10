#!/usr/bin/env bash
# Code Atlas Launcher Script

set -e

# Parse command line flags (kept for backward compatibility, though terminal printing is removed)
PRINT_PAYLOADS_FLAG=""
for arg in "$@"; do
    if [ "$arg" = "--print-payloads" ]; then
        PRINT_PAYLOADS_FLAG="y"
    elif [ "$arg" = "--no-print-payloads" ]; then
        PRINT_PAYLOADS_FLAG="n"
    fi
done

# Print Banner
echo "=================================================="
echo "          Code Atlas Local Orchestrator           "
echo "=================================================="
echo ""

# 1. Choose Directory to Scan
default_dir="."
read -p "Enter path to target directory to scan [default: $default_dir]: " TARGET_DIR
TARGET_DIR="${TARGET_DIR:-$default_dir}"

# Resolve absolute path
ABS_TARGET_DIR=$(realpath "$TARGET_DIR" 2>/dev/null || echo "$TARGET_DIR")

if [ ! -d "$ABS_TARGET_DIR" ]; then
    echo "Error: Directory '$ABS_TARGET_DIR' does not exist."
    exit 1
fi

echo "Selected target directory: $ABS_TARGET_DIR"
echo ""

# 2. Choose Output Report Path
PROJECT_NAME=$(basename "$ABS_TARGET_DIR")
if [ "$PROJECT_NAME" = "." ] || [ "$PROJECT_NAME" = "/" ] || [ -z "$PROJECT_NAME" ]; then
    PROJECT_NAME="code_atlas_report"
fi

default_out="$PROJECT_NAME.json"

# Auto-resolve duplicate default file names in current dir
if [ -f "$default_out" ] || [ -d "$default_out" ]; then
    counter=2
    while true; do
        candidate="${PROJECT_NAME}_s${counter}.json"
        if [ ! -f "$candidate" ] && [ ! -d "$candidate" ]; then
            default_out="$candidate"
            break
        fi
        counter=$((counter+1))
    done
fi

read -p "Enter output JSON path [default: $default_out]: " OUTPUT_FILE
OUTPUT_FILE="${OUTPUT_FILE:-$default_out}"
ABS_OUTPUT_FILE=$(realpath "$OUTPUT_FILE" 2>/dev/null || echo "$OUTPUT_FILE")

if [ -d "$ABS_OUTPUT_FILE" ] || [[ "$ABS_OUTPUT_FILE" == */ ]] || [[ "$ABS_OUTPUT_FILE" == *\\ ]]; then
    ABS_OUTPUT_FILE="${ABS_OUTPUT_FILE%/}/$default_out"
fi

# Resolve duplicate for resolved absolute path to prevent accidental overwrites
if [ -f "$ABS_OUTPUT_FILE" ]; then
    base_dir=$(dirname "$ABS_OUTPUT_FILE")
    file_name=$(basename "$ABS_OUTPUT_FILE")
    name_part="${file_name%.json}"
    
    counter=2
    while true; do
        candidate_path="$base_dir/${name_part}_s${counter}.json"
        if [ ! -f "$candidate_path" ]; then
            ABS_OUTPUT_FILE="$candidate_path"
            break
        fi
        counter=$((counter+1))
    done
    echo "Warning: Output file already exists. Automatically resolved path to: $ABS_OUTPUT_FILE"
fi

echo "Selected output path: $ABS_OUTPUT_FILE"
echo ""

# 3. Ask for AI Export
default_ai="y"
read -p "Generate token-conscious AI packets (.ai.json and .ai.md)? (y/n) [default: $default_ai]: " RUN_AI
RUN_AI="${RUN_AI:-$default_ai}"

# Determine scanner arguments
SCANNER_ARGS="--dir \"$ABS_TARGET_DIR\" --output \"$ABS_OUTPUT_FILE\""

ABS_MD_FILE="${ABS_OUTPUT_FILE%.json}.md"
AI_MD=""
AI_JSON=""

if [ "$RUN_AI" = "y" ] || [ "$RUN_AI" = "Y" ]; then
    base_name="${ABS_OUTPUT_FILE%.json}"
    AI_MD="${base_name}.ai.md"
    AI_JSON="${base_name}.ai.json"
    SCANNER_ARGS="$SCANNER_ARGS --ai-output \"$AI_MD\" --ai-json-output \"$AI_JSON\" --ai-detail standard"
    echo "AI export targets active."
fi

echo ""
echo "Running static analysis scan..."
# Get script location directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
eval "python3 \"$SCRIPT_DIR/code_atlas/scanner.py\" $SCANNER_ARGS"

# Print final terminal summary (terminal dumping of content is removed)
echo ""
echo "=================================================="
echo "               Code Atlas Summary                 "
echo "=================================================="
echo "Scanned Project Path:   $ABS_TARGET_DIR"
echo "Report Family Name:     $PROJECT_NAME"
echo "Output Directory:       $(dirname "$ABS_OUTPUT_FILE")"
echo "Generated Payloads:"
echo "  - JSON: $ABS_OUTPUT_FILE"
echo "  - Markdown: $ABS_MD_FILE"
if [ "$RUN_AI" = "y" ] || [ "$RUN_AI" = "Y" ]; then
    echo "  - AI JSON: $AI_JSON"
    echo "  - AI Markdown: $AI_MD"
fi
echo "Viewer URL:             http://127.0.0.1:8080/"
echo "=================================================="
echo ""

echo "Starting local HTTP viewer server..."
echo "Press Ctrl+C to stop the server."
echo ""

python3 -m code_atlas.viewer.server --report "$ABS_OUTPUT_FILE" --port 8080

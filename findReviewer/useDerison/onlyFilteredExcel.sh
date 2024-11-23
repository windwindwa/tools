#!/bin/bash

# 打印帮助信息
function show_help() {
  echo "Usage: $0 [options]"
  echo ""
  echo "Options:"
  echo "  -e, --excel_path            Path to the Excel file."
  echo "  -f, --filter_school_file    Path to the filter school file."
  echo "  -h, --help                  Show this help message and exit."
}

# 检查是否传入参数
if [ $# -eq 0 ]; then
  show_help
  exit 1
fi

# 定义默认参数
EXCEL_PATH=""
FILTER_SCHOOL_FILE=""

# 解析命令行参数
while [[ "$#" -gt 0 ]]; do
  case $1 in
    -e|--excel_path) EXCEL_PATH="$2"; shift ;;
    -f|--filter_school_file) FILTER_SCHOOL_FILE="$2"; shift ;;
    -h|--help) show_help; exit 0 ;;
    *) echo "Unknown parameter passed: $1"; show_help; exit 1 ;;
  esac
  shift
done

# 检查必要参数是否提供
if [[ -z "$EXCEL_PATH" ]]; then
  echo "Error: --excel_path (-e) is required."
  show_help
  exit 1
fi

if [[ -z "$FILTER_SCHOOL_FILE" ]]; then
  echo "Error: --filter_school_file (-f) is required."
  show_help
  exit 1
fi

# 执行 Python 脚本
/Users/lzg/opt/anaconda3/envs/findRe/bin/python /Users/lzg/0_lzgData/2_Personal/220_othersTools/tools/findReviewer/useDerison/onlyFilteredResultExcel.py \
  --excel_path "$EXCEL_PATH" \
  --filter_school_file "$FILTER_SCHOOL_FILE"
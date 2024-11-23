#!/bin/bash

# 打印帮助信息
function show_help() {
  echo "Usage: $0 [options]"
  echo ""
  echo "Options:"
  echo "  -e, --excel_path       Path to the Excel file."
  echo "  -d, --db_path          Path to the SQLite database file."
  echo "  -h, --help             Show this help message and exit."
}

# 检查是否传入参数
if [ $# -eq 0 ]; then
  show_help
  exit 1
fi

# 初始化变量
EXCEL_PATH=""
DB_PATH=""

# 解析命令行参数
while [[ "$#" -gt 0 ]]; do
  case $1 in
    -e|--excel_path) EXCEL_PATH="$2"; shift ;;
    -d|--db_path) DB_PATH="$2"; shift ;;
    -h|--help) show_help; exit 0 ;;
    *) echo "Unknown parameter passed: $1"; show_help; exit 1 ;;
  esac
  shift
done

# 检查是否提供了必要参数
if [[ -z "$EXCEL_PATH" ]]; then
  echo "Error: --excel_path (-e) is required."
  show_help
  exit 1
fi

if [[ -z "$DB_PATH" ]]; then
  echo "Error: --db_path (-d) is required."
  show_help
  exit 1
fi

# 执行 Python 脚本
/Users/lzg/opt/anaconda3/envs/findRe/bin/python /Users/lzg/0_lzgData/2_Personal/220_othersTools/tools/findReviewer/useDerison/onlyInsertEmail2database.py --excel_path "$EXCEL_PATH" --db_path "$DB_PATH"
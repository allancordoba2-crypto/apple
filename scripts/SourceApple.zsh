#!/bin/zsh
# SourceApple.zsh - macOS Read-Only Diagnostic Collector
set -euo pipefail

computer_name=$(scutil --get ComputerName 2>/dev/null || hostname)
model_name=$(sysctl -n hw.model 2>/dev/null || echo 'Unknown')
os_version=$(sw_vers -productVersion 2>/dev/null || echo 'Unknown')
os_build=$(sw_vers -buildVersion 2>/dev/null || echo 'Unknown')
arch=$(uname -m 2>/dev/null || echo 'Unknown')
kernel=$(uname -v 2>/dev/null || echo 'Unknown')
boot_volume=$(df -h / | awk 'NR==2 {print $1, $2, $3, $4, $5}')

echo '{'
echo '  "computer_name": "'$computer_name'",'
echo '  "hardware_model": "'$model_name'",'
echo '  "os_version": "'$os_version'",'
echo '  "os_build": "'$os_build'",'
echo '  "architecture": "'$arch'",'
echo '  "kernel": "'$kernel'",'
echo '  "boot_storage": "'$boot_volume'"'
echo '}'

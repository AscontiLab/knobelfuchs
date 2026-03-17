#!/bin/bash
cd "$(dirname "$0")"
npx tailwindcss -i static/input.css -o static/style.css --minify

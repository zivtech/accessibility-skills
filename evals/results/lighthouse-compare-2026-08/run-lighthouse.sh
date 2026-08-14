#!/usr/bin/env bash
set -uo pipefail
cd "$(dirname "$0")"
mkdir -p lighthouse

declare -a NAMES=("comptox-home" "comptox-search" "fire-map" "gispub-map" "airnow-about")
declare -a URLS=(
  "https://comptox.epa.gov/dashboard/"
  "https://comptox.epa.gov/dashboard/search-results?input_type=synonym_substring&inputs=caffeine"
  "https://fire.airnow.gov/"
  "https://gispub.epa.gov/airnow/?monitors=ozonepm"
  "https://www.airnow.gov/about-airnow/"
)

for i in "${!NAMES[@]}"; do
  name="${NAMES[$i]}"
  url="${URLS[$i]}"

  echo "=== [$name] MOBILE (default) : $url ==="
  npx lighthouse@latest "$url" \
    --only-categories=accessibility \
    --output=json \
    --output-path="lighthouse/${name}-mobile.json" \
    --chrome-flags="--headless=new" \
    --quiet
  echo "exit=$? -- sleeping 1s"
  sleep 1

  echo "=== [$name] DESKTOP : $url ==="
  npx lighthouse@latest "$url" \
    --only-categories=accessibility \
    --preset=desktop \
    --output=json \
    --output-path="lighthouse/${name}-desktop.json" \
    --chrome-flags="--headless=new" \
    --quiet
  echo "exit=$? -- sleeping 1s"
  sleep 1
done

echo "ALL LIGHTHOUSE RUNS COMPLETE"

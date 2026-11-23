#!/usr/bin/env bash
# Builds the usemarket customer app (apps/frontend, Expo, pnpm workspace) as an
# arm64 iOS Simulator .app (unsigned) that talks to staging. Runs from the app
# folder (src/apps/frontend). Output: build/usemarket.app (set as ios_app_path)
set -euo pipefail
export CI=1 EXPO_PUBLIC_API_URL=https://staging.usemarket.store
npm install -g pnpm@11.13.1
# Same install as the app repo's CI (.woodpecker.yml): the customer, merchant and
# rider apps each rebuild packages/contracts and api-client in postinstall, and run
# together they write the same dist/ files at once
(cd ../.. && pnpm install --frozen-lockfile --child-concurrency=1)
npx expo prebuild --platform ios --no-install
(cd ios && pod install)
WS=$(find ios -maxdepth 1 -name '*.xcworkspace' | head -1)
DD=${RUNNER_TEMP:-$PWD/build}/dd
# Simulator build like scripts/build/ios.sh: arm64 only, no signing
xcodebuild -workspace "$WS" -scheme "$(basename "$WS" .xcworkspace)" -configuration Release \
  -sdk iphonesimulator -destination 'generic/platform=iOS Simulator' -derivedDataPath "$DD" \
  EXCLUDED_ARCHS=x86_64 ONLY_ACTIVE_ARCH=YES CODE_SIGNING_ALLOWED=NO build
APP=$(find "$DD/Build/Products" -maxdepth 2 -path '*iphonesimulator/*.app' -not -name '*Tests*' | head -1)
rm -rf build/usemarket.app && mkdir -p build && cp -R "$APP" build/usemarket.app

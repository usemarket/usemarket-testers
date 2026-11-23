#!/usr/bin/env bash
# Builds a usemarket app (customer apps/frontend, merchant apps/merchant-app or rider
# apps/rider-mobile: Expo, pnpm workspace) as an
# x86_64 release APK that talks to staging. Runs from the app folder (src/<app_dir>).
# Output: android/app/build/outputs/apk/release/app-release.apk (set as apk_path)
set -euo pipefail
export CI=1 EXPO_PUBLIC_API_URL=https://staging.usemarket.store
npm install -g pnpm@11.13.1
# Same install as the app repo's CI (.woodpecker.yml): the customer, merchant and
# rider apps each rebuild packages/contracts and api-client in postinstall, and run
# together they write the same dist/ files at once
(cd ../.. && pnpm install --frozen-lockfile --child-concurrency=1)
npx expo prebuild --platform android --no-install
cd android && ./gradlew assembleRelease -PreactNativeArchitectures=x86_64 --build-cache

#!/usr/bin/env bash
# Builds the usemarket customer app (apps/frontend, Expo, pnpm workspace) as an
# x86_64 release APK that talks to staging. Runs from the app folder (src/apps/frontend).
# Output: android/app/build/outputs/apk/release/app-release.apk (set as apk_path)
set -euo pipefail
export CI=1 EXPO_PUBLIC_API_URL=https://staging.usemarket.store
npm install -g pnpm@11.13.1
(cd ../.. && pnpm install --frozen-lockfile)
npx expo prebuild --platform android --no-install
cd android && ./gradlew assembleRelease -PreactNativeArchitectures=x86_64 --build-cache

# Mission: can a shop upload a large phone photo?

## usemarket Merchant (read first)
The app is usemarket Merchant, the shop owners' app of usemarket, a Nigerian marketplace.
This build talks to the staging server, not the live one.
- Sign-in is by phone number and a code. Use ONLY the test login: run
  `cat test-login.txt` and use that phone and code. Never type any other phone number.
- The test account owns test shops (Test Grocery, Test Kitchen, Test Pharmacy, Test Household
  in Akure, Ibadan and Sango Ota). Only change the shop your persona's city names.
- Never delete a shop or a product you did not create.

You are a QA tester playing ONE persona (find yours in personas.json with the PERSONA id
you were given). You drive a real Android phone (emulator) where the app is installed and open.
Ignore your persona's usual goal: this run checks one thing.

## What to test
Shop owners report they cannot upload photos taken with their phone. The gallery on this
phone holds two photos: `ordinary-photo.jpg` (small) and `large-camera-photo.jpg`
(12 megapixels, about 14 MB, bigger than the server accepts as is: the app is meant to
shrink it first). For each of these places, pick `large-camera-photo.jpg` from the gallery
(not the camera):
1. The shop logo (shop profile or settings).
2. The shop banner, if the app has one.
3. A photo for a NEW product you create (name it "QA large photo <persona>", any price, stock 1).
4. A second photo added to that same product afterwards.
Then repeat step 1 once with `ordinary-photo.jpg` to compare.
For each: say whether the photo was saved and shows on screen, how long it took (count your
screenshots), and copy the exact words of any message. Wait at least 60 seconds before you
call an upload stuck. A clear refusal is still a finding: the app should not refuse a
normal phone photo at all.

## Tools (only these)
Android
- See the screen: `python3 scripts/android/screen.py results/<persona> <NN>` (NN = 01, 02...).
  Read the PNG it writes, then the element list (centres in real pixels).
- Tap: `adb shell input tap X Y` - Swipe/scroll: `adb shell input swipe X1 Y1 X2 Y2 400`
- Back: `adb shell input keyevent KEYCODE_BACK` - Type: `python3 scripts/android/type.py "text"`
- Home: `adb shell input keyevent KEYCODE_HOME` - Recents: `adb shell input keyevent KEYCODE_APP_SWITCH`
- Reopen the app: `adb shell monkey -p <APP_ID> -c android.intent.category.LAUNCHER 1`
- Fully close it: `adb shell am force-stop <APP_ID>` (then reopen as above)
- Rotate: `adb shell settings put system accelerometer_rotation 0` then
  `adb shell settings put system user_rotation 1` (landscape) / `0` (portrait)
- The emulator's camera shows a test scene: point and shoot works like a real camera.
iOS
- See the screen: `python3 scripts/ios/screen.py results/<persona> <NN>` (positions in points).
- `bash scripts/ios/gesture.sh tap X Y | scroll down | back | dismiss-sheet | enter | relaunch`
- Type: `python3 scripts/ios/type.py "text"` (tap the field first). It pastes: if iOS asks to
  paste from "CoreSimulatorBridge", tap Allow Paste. That alert comes from the tool, not the app.

## Rules
- Take a screenshot after EVERY action and look at it before the next one. Number them in order.
- Never clear app data or reinstall.
- Budget: about 40 actions, then write the report. Stop earlier only if the app crashes twice.
- Write everything under `results/<persona>/`. Nothing else.

## Final report
Write both files with the Write tool (writing through the shell is blocked).
1. `results/<persona>/report.md`
   - 5-line summary with the device.
   - Issues, most severe first. For each: screenshot number(s), steps to reproduce,
     actual result, expected result, severity (blocker / major / minor / cosmetic).
   - Device-specific layout problems (same format, shorter).
   - The persona's opinion in their own words: would they keep the app? score /10.
2. `results/<persona>/findings.json`:
   `{"score": 7, "issues": [{"title": "...", "severity": "major", "screen": "Sign-up", "screens": ["05", "06"]}]}`

# Mission: test what only a real phone can do

## usemarket (read first)
usemarket is a Nigerian marketplace with three apps: the customer app (usemarket.store),
the shop owners' app (com.usemarket.usemarketvendor) and the riders' app (usemarket.rider).
APP_ID in your instructions says which one is installed. This build talks to the staging
server, not the live one.
- Sign-in is by phone number and a code. Use ONLY the test login: run
  `cat test-login.txt` and use that phone and code. Never type any other phone number.
- Never complete a payment, never request a withdrawal, never enter a real bank account,
  identity number or card. Never delete a shop or product you did not create.
- The rider test account is already an approved rider in Ibadan: do not start a new sign-up.

You are a QA tester playing ONE persona (find yours in personas.json with the
PERSONA id you were given). You drive a real Android phone (emulator) where the app is
already installed and open. Ignore your persona's usual goal: this run is about the parts
of the app a web browser cannot test. Play the persona's patience and skills, but stay a tester.

## What to test (native only)
Work through these in order; skip a step that does not exist in your app and say so.
1. Notifications: the first time the app asks to send notifications, deny. Use the app, then
   find where it lets you turn notifications on again (in-app or Android settings) and allow.
   Check the app never nags in a loop and nothing breaks when denied.
2. Camera and photos: find every place that takes a photo or picks a file
   (customer: report a problem with an order, declutter listing, profile; shop: product photo,
   shop logo, documents; rider: profile/vehicle/documents, pickup or delivery proof, damage report).
   For each: deny the camera permission once and check the message, then allow it, take a
   photo with the camera, and also try picking an image from the gallery. Rotate the phone
   while the camera or picker is open if you can, and press Back from inside it.
   Uploads may be refused by staging: that is expected; report exactly what the screen says
   (a clear message is fine; a spinner forever, a crash or technical wording is a bug).
3. Location (customer and rider): deny location, check the app explains and still lets you
   continue (type an address / stay offline), then allow and check it picks up the city.
4. Leave and come back: press Home in the middle of a form (a half-typed product, address or
   report), wait 10 seconds, reopen the app from recents: is the form still there? Then fully
   close the app from recents and reopen: are you still signed in?
5. Android Back button on every main screen and inside sheets and dialogs: does it go where you
   expect, and never exit the app from a deep screen or lose typed data without asking?
6. Keyboard: every text field must stay visible above the keyboard, and the action button must
   be reachable while typing.

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

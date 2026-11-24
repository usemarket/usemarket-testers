# Mission: record layout evidence (keyboard, bottom bars, large text)

## usemarket (read first)
usemarket is a Nigerian marketplace. APP_ID in your instructions says which app is installed;
this run is for the customer app (usemarket.store). The build talks to the staging server.
- Sign-in is by phone number and a code. Use ONLY the test login: run
  `cat test-login.txt` and use that phone and code. Never type any other phone number.
- Never complete a payment.

You are a QA tester playing ONE persona (find yours in personas.json with the PERSONA id you
were given), but this run is not about your goal: it collects exact evidence for layout bugs
other testers reported, so a developer can find the cause. Precision matters more than speed.

## How to record one checkpoint
At every checkpoint below, with NAME the checkpoint's name:
1. Take the screenshot as usual (`python3 scripts/android/screen.py results/<PERSONA> NN`).
2. Save the full screen layout and the window and keyboard state, with these four commands
   exactly (each is one adb command; the filtering runs on the phone):
   ```
   adb shell uiautomator dump /sdcard/NAME.xml
   adb shell "dumpsys window | grep -E 'mCurrentFocus|mInputMethodWindow|InsetsSource|mFrame=|mVisibleFrame|mContentFrame' > /sdcard/NAME-window.txt; dumpsys input_method | grep -E 'mInputShown|mWindowVisible|mIsInputViewShown' >> /sdcard/NAME-window.txt; wm size >> /sdcard/NAME-window.txt; wm density >> /sdcard/NAME-window.txt"
   adb pull /sdcard/NAME.xml results/<PERSONA>/NAME.xml
   adb pull /sdcard/NAME-window.txt results/<PERSONA>/NAME-window.txt
   ```
3. In report.md, under the checkpoint name, write: the screenshot number, whether the
   keyboard is open, and the bounds (from NAME.xml) of the element named in the checkpoint
   and of the keyboard top edge (the screen height minus the keyboard height you see).

## Checkpoints (in order; say "not reached" for any you cannot reach, and why)
1. `welcome`: the first screen after the app opens (signed out). Element: "Log in" link and
   the "Terms" link. Then try once to scroll the screen up and record `welcome-scrolled`.
2. `login-before-keyboard`: Get Started / Log in screen, phone field visible, keyboard closed.
   Element: the "Continue" button and the phone field.
3. `login-keyboard`: tap the phone field so the keyboard opens; do not type yet. Element:
   "Continue" and the phone field.
4. `login-keyboard-typed`: type the phone number from test-login.txt, keyboard still open.
   Element: "Continue".
5. `otp-keyboard`: continue to the code screen with the keyboard open. Element: the Verify
   button and the "resend code" link.
6. After signing in, reach Home. `home`: element: the bottom tab bar and the last store card.
7. Add one cheap item from any shop to the basket so the floating "View Cart" bar appears, then
   go to that shop's product list. `store-cart-bar`: elements: the View Cart bar and every
   product name/price whose bounds overlap it.
8. Search tab with the cart bar shown. `search-cart-bar`: elements: category labels (note any
   label whose text is cut or split mid-word) and the View Cart bar.
9. Remove the item you added (leave the basket as you found it) before you finish.

## Rules
- Do not change the font size, theme or orientation yourself: they are set for your persona.
- Do not report opinions or new bugs in this run, only the checkpoints. If something crashes,
  record it and continue with the next checkpoint.
- Write findings.json as usual, with one issue per checkpoint where an element is covered,
  cut or off screen ("severity": "major" for a covered button, "minor" otherwise).

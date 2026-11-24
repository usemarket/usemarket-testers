# Mission: how easy is each vendor journey, and how to make it easier

Read AGENT_BRIEF.md first: its tools, rules and final report files all apply.
Only the mission changes.

## usemarket Merchant (read first)
The app is usemarket Merchant, the shop owners' app of usemarket, a Nigerian marketplace
(food, groceries, pharmacy). This build talks to the staging server, not the live one.
- Sign-in is by phone number and a code. Use ONLY the test login: run
  `cat test-login.txt` and use that phone and code. Never type any other phone number.
- The test account owns 13 test shops (Test Grocery, Test Kitchen, Test Pharmacy and
  Test Household in Akure, Ibadan and Sango Ota). Other testers use the same account at the
  same time, each in a different shop: work ONLY in the shop your persona's goal names.
- Every product, category or deal you create starts with `UX <your persona id>` (for example
  `UX tolu Garri 2kg`), so it is clearly test data. Change only things you created, plus the
  settings your goal names. Never delete a shop, close a shop for good, or remove staff.
- Never enter a real bank account, identity number or card: stop at that step and report
  what the screen asks for.
- For a product photo, pick an image from the phone's gallery (`ordinary-photo.jpg` or
  `large-camera-photo.jpg` are there).

## What we want to learn
You are a real shop owner doing your persona's `goal` (personas.json) for the first time,
with no help page unless your persona would open one. We want to know how easy each step is
for someone like you, and exactly what to change. Bugs you meet still go in `issues`.

1. Before you start, write in `report.md` the steps you expect the journey to take, in your
   persona's words (for example "find Add product, type name and price, add a photo, save").
2. Do the journey. Screenshot after every action. Keep a **step log** in `report.md`: one line
   per action, `NN | what I wanted | what I did | what happened | ease 1-5` (5 = obvious,
   1 = I had to guess or got stuck). Mark every moment you hesitated, went back, misread a
   label, met a word you did not understand, or wondered if something saved.
3. After the goal (or when your persona would give up), sum up per sub-task: reached or not,
   number of actions, and the hardest moment. Then score the whole journey out of 10 as the
   persona, and say whether you would keep using the app.
4. Then, as a UX tester, write at most 7 improvements, most useful first. Each says what to
   change, why (what happened to you, with screenshot numbers), on which screen, its area
   (onboarding, navigation, copy, layout, feedback, trust, performance, feature, accessibility,
   translation) and its impact for a shop owner like you (`high`, `medium`, `low`). Base each
   one on something you saw on this device; no wish lists.

Budget: about 45 actions. Go deep on your own journey rather than wide across the app.

In `findings.json`, next to `score` and `issues`, add `"goal_reached": "yes" | "partly" | "no"`,
`"actions": N` and `"improvements": [{"title": "...", "area": "...", "impact": "high",
"screen": "...", "screens": ["07", "08"], "why": "..."}]`.
Start `report.md` with `Goal reached: ...` and `Score: N/10`.

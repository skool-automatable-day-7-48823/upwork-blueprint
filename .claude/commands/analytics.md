---
description: "Your weekly check-in: finds the one step in your Upwork funnel that is losing you deals, tells you the fix, and split tests it until a winner is clear."
argument-hint: ""
---

# /analytics

**One job: find the one area where the member is losing deals, and fix it.** The member is
usually a first-time freelancer, not an analyst. They quit because they feel overwhelmed, never
for lack of data, so everything they see is calm, plain and short.

Pick one area. Fix everything in it that is clearly holding them back, all at once, with big
changes first: a new proposal template, a re-recorded video, a rebuilt bio. Never a one-sentence
tweak, and never a list of things across their whole business. The whole new version is then
tested against the old way, and it becomes the default once it is about 80% likely to win.

The area is usually at the top first: enough proposals to the right jobs, then replies, then
conversations, sales calls, after the call, closing. Fix the top and the area moves down.

## ROADMAP

Refresh evidence, find the leaking stage, name the fix, run or read its split test, agree
this week's goals. First-run preparation may take longer. Wait for missing sources and goal
agreement. Missing evidence or too few finished cases can leave a stage unknown; coaching
continues. Run on the member's Analytics day. Upwork access is read-only; nothing is sent.

## 1. Prepare and refresh

Claude reads `context/me.md`, [copy](../../references/copy.md), [goal library](../../references/goal-library.md), [coach brief](../../references/coach-brief.md), [leak checks](../../references/leak-checks.md), [split tests](../../references/split-tests.md) and [Upwork rules](../../references/upwork.md), then runs:

```bash
python3 code/workspace.py
python3 code/analytics.py last
python3 code/split_test.py status
```

Check `data/sync.json` and `list_accounts`. Use fresh saved state; if sync is absent, future-dated or older than 24 hours at the zoned run time, perform [/dashboard](dashboard.md) Steps 1–2 and [capture: dashboard](../../references/analytics-capture.md#dashboard), read/sync only. If disconnected, guide README's connection steps and wait for the member. Count every Upwork call.

On the first run, backfill proposals, invitations, contracts, Connects and earnings to the connector's documented limit. Page every proposal status, including Archived, to exhaustion; deduplicate IDs, retain the newest copy and classify its returned status. Preserve verified dates; name the uncovered period. Import absent historical leads through:

```bash
python3 code/pipeline.py add --file -
python3 code/sync.py apply --file -
```

Mark historical imports as imported; preserve existing matched leads and disclose any backfill limitation. Follow the capture hook for proposal insights, viewed observations, invitation dates and ledger evidence. Missing sources remain missing; checked-empty sources are explicit empty lists.

Ask only for reconnection or evidence the tools cannot supply. Code and its errors define accepted inputs; never edit pipeline data directly.

## 2. Recover source evidence and missed weeks

Obtain calls through [call transcript](../../references/call-transcript.md): Fireflies first when the member uses it. A recap proves held, never its absence a no-show. Requested meetings remain requested; preserve sessions and reschedules. Reuse `jobs/<id>/call-review.md`; invoke [/call-review <id>](call-review.md) only for an unreviewed session. Preserve verified session identity, language and completeness; a summary or excerpt cannot support a whole-call review.

Then run:

```bash
python3 code/analytics.py compute --catch-up
python3 code/analytics.py compute
```

Register or deploy nothing. A failed check is a source gap, never a human click. Review missed-week previews chronologically and every unresolved goal due through the gap. Current recording appends catch-up history atomically; never record previews separately or invent past agreements. Unreconstructible historical facts remain unknown. Tell the gap as one story, beginning with elapsed time. Explain: "Missed a week? Next time you run /analytics it catches up on everything since your last check-in."

Ask for each unavailable source through its exact recovery route; hold affected claims if code cannot preserve the history.

## 3. Check every factor at that step

Compute's `verdict` names the step: the first one below its aim, top first. Use it unchanged; its `headline`, `reason` and `funnel_five` are what the member sees. Then run:

```bash
python3 code/diagnosis.py facts
```

It prints all four stages (Proposals, Messaging, Calls, Offers), marks the stuck one, lists calls still to grade and the running split test. Each stage has sections, one thing each, and each section lists its items with the standard and source beside them. Every item says where its answer comes from:

- `code`: counted by code from the pipeline, sent letters, threads and transcripts (volume, speed, job crowd, proposal parts, reading grade, call asked, talk time, call length, offer follow-up). Never typed in.
- `calls`: each held call graded **once** from its transcript, saved to `jobs/<id>/call-grade.json` with the transcript's fingerprint, and added up across every call in the last 28 days. Grade every call in `calls_to_grade` every week, whatever the stuck stage; a call is regraded only when its transcript changes. A call without a transcript shows as a gap, never hidden.
- `claude`: read from the member's own material, then judged against the printed standard:
  - profile: `python3 code/diagnosis.py media` downloads the photo and portfolio images to `data/profile-media/`; open and look at each. The **bio video** is the profile's own video and is required. Title, bio and rate come from the connector.
  - proposal videos: `python3 code/loom.py <id> <url>` for the transcript, `python3 code/loom.py frames <id> <url>` and look at every frame: smiling, eye contact, energy, their site on screen. Judge only videos linked in sent proposals, never the bio video or portfolio videos.
  - portfolio: each piece's media, matched against the jobs they bid on.

Judge the **stuck stage in full**; other stages show what code measured, and unchecked items are hidden. Statuses: `ok`, `missing`, `weak`, `optional`, `unknown` (never a guess). Section ratings are computed from items, never typed.

Then be a coach. Each stage opens on its **movers**: the 1 to 3 changes that get 90% of that stage's result, each with the data behind it, shown at the top of the stage. Big swings only: a new proposal structure, a new call plan, a new offer. Never a one-sentence tweak, never fluff. The stuck stage always has them; Calls has them once 3 or more graded calls show a problem; any other stage may. A stage can also carry a **coach's note**, 1 to 3 lines on the biggest mistakes, from their own calls, threads and letters. **Exactly one mover of the stuck stage carries the split test**: the highest one that can be tested (a habit such as volume or speed is just done, `"habit": true`).

**The mover audit.** Before saving, ask of each mover: if they did only this, would that stage's number move, and does their own data prove the problem? Code then checks, and refuses a mover that fails:
- it cites `evidence`, the items that prove it, as `area.section.item` from facts, all from its own stage
- every cited item is `missing` or `weak`, and at least one is measured from their data (`code` or `calls`). A gap against a standard alone, such as how the profile looks, stays in the checks; it is not a mover
- the evidence covers 3 or more cases ("0 of 1" is an anecdote)
- every number in `why` appears in the cited items

Fewer movers is fine. One real change beats three where two are filler. Save:

```bash
python3 code/diagnosis.py save --file -
```

`{"areas": {"replies": {"movers": [{"title": "...", "why": "<their data>", "do": "...", "evidence": ["replies.proposal.result"], "test": {"stage": "proposal", "a": "<what they send now>", "b": "<the whole new version>", "b_checks": ["question", "offer", "video"]}}], "sections": [{"key": "proposal", "items": [{"key": "proof", "status": "missing", "note": "No client named."}]}]}, "calls": {"movers": [...]}}, "calls": [{"job_id": "<id>", "checks": {"rapport": {"status": "ok", "quote": "..."}, ...}, "better": "<one line>", "followed": "A"}]}`

Saving starts the mover's test. While a test runs, leave `test` out: it stays on the first mover of its stage, and save refuses if that stage has none (ship or stop it first). `followed` is needed only for a call in a running call test: which way the call actually went, from the transcript. Code refuses: edited measured items, a stuck stage judged in part or without movers, any ungraded call, a mover that fails the audit, more than three on a stage, and anything but one test on the stuck stage.

Use compute's unchanged output for every number, state, focus, period and evidence population. Read leads with:

```bash
python3 code/pipeline.py get <id>
```

Prepare a full evidence inventory first run. Otherwise review at most five cases from the stuck step plus urgent exceptions and disclose sampled IDs and unreviewed coverage. Read every reply thread without a call or offer when the step is conversations, and every call transcript when it is calls or later.

### Coaching rubrics

Judge from the coach brief, the full post and the verified thread or call. Every correction includes the quoted passage, missed point, grounded replacement and next instruction.

For chats, paginate read-only `get_messages` / `list_messages` to documented exhaustion and read oldest first. Judge the client's question answered and a clear ask for a call, an Upwork meeting invite or two times. Timing comes from code. Honour stated decisions and agreed steps; count patterns only through code.

The comparable call scan covers: (1) opening/agenda within two minutes; (2) current state; (3) problem and cost; (4) goal/scope; (5) budget before price; (6) decision maker/timeline; (7) distinguishing proof addressing the client's concern; (8) objections invited/handled; (9) agreed next step on Upwork, owner, terms and deadline. Credit sourced information already established; explain inapplicable points. Reuse the full saved review, exact turning quotes, better wording, fix, example, read and next message. If its original scan was not recorded, use `/call-review` to record it without new judgment; otherwise name the writer gap. On top of the nine points, check the sales-call and closing items in [leak checks](../../references/leak-checks.md): rapport, a clear offer, price said, timeline said, the close asked for.

Separate stated, observed and unknown loss reasons. Save assessments only through:

```bash
python3 code/pipeline.py note <id> 'analytics job_fit: {"state":"pass","reason":"<quoted judgment>"}'
python3 code/pipeline.py note <id> 'analytics lost_reason: {"kind":"stated","reason":"<verified reason>"}'
python3 code/pipeline.py record <id> --file -
python3 code/analytics.py compute --file -
```

Use actual judgments in tagged notes. Supply evidenced reviews, eligible/completed goal cases, keep/adjust/stop decisions and live source gaps to compute. Keep execution separate from effect; no opportunity means untested. Offer the simpler fallback after two undone weeks. Preserve code's focus; disclose disagreement with supported coaching rather than overwrite it. Badge award lines from the writers are never shown to the member.

Ask one targeted question only when evidence cannot distinguish an obstacle; request missing sent copy, complete thread or attributed transcript through its capture/source route.

## 4. Call the running test

Hands-off for the member: Claude builds, starts, checks and calls the test; the member only sends what the commands write. Follow [split tests](../../references/split-tests.md).

Run this **before** step 3's save. Read `python3 code/split_test.py status`. Leads sent differently from their side (an edited draft, a call that went the other way) are left out and counted; name the count in one line. On **ship B** or **keep A**, call it without asking: `python3 code/split_test.py ship B` (or `A`), write the winner under `## Split test winners` in `context/me.md` (a follow-up rhythm goes on `**Follow-up days:**`), and tell the member what is now their default. Step 3's save then starts the next test from the movers. On **keep going**, say how many finished leads each side has.

Build B in full before saving: the new proposal, reply, call plan or offer, saved where its writing command reads it. The writing commands assign each lead its side.

## 5. Write and check the weekly coaching

Claude writes the weekly summary in the fixed order and tone of the coach brief's weekly report section; [report example](../../references/chat-report-example.md) is the approved text. Obtain facts from the final prepared snapshot and check the report against that same snapshot:

```bash
python3 code/analytics.py facts --snapshot <snapshot-file>
python3 code/analytics.py check-report <report-file> --snapshot <snapshot-file>
```

Require check-report PASS before displaying; fix every rejected value, period or unsupported claim. Quote `verdict.reason` exactly as code wrote it. Fix lines start with "The fix:" and the test line with "The test:"; both are instructions, so their numbers are not checked. Every other number must pass, so say what is wrong in words, not counts. No tables, scores, badges or code blocks in the member's report.

Each early week improves one habit, checks use of the prior fix, resolves low activity, or decides what to keep/change. Baseline collection never implies established improvement.

Ask for source gaps or a decision needed to resolve a supported obstacle; recommendations alone do not save goals.

## 6. Preserve the app presentation

Claude carries the saved code presentation into exactly **This week** and **Your numbers**; no separate calculation or speculative content. Achievements (badges, rank, score) and the separate conversations view are hidden from members: chats and calls are judged inside their own steps. All disclosures expand inline, with no drawers/dialogs. Evidence opens Leads filtered to exact row IDs across all statuses without opening its drawer; Back restores the same analytics subtab and scroll. Call coaching, full reviews and turning moments stay inline; deeper coaching uses `/call-review`.

This week leads with the stuck step, the clickable funnel, that step's checks and the test. The complete scorecard is the **Your numbers** tab. Habit rows show THIS WEEK against the prior four-week average; fewer than three opportunities use the four-week average as the main value with a sample note. Result rates use 28 days versus prior 28 days. Preserve evidence, histories and returned comparisons. Unknown is never zero. Call rate links to stalled replies in Conversations.

Each scorecard row's detail has one **Open these N leads →** button opening Leads filtered to that row's exact IDs, with no embedded lead list. The chart uses actual week labels, faint horizontal ladder bands labelled at right, and value labels above bars without overlap. Accent only the current bar; keep others neutral and fit height to content. The right column has at most three short lines: the count in one sentence, one job-fit finding only when present, and the market reference with a **Source** link rather than a raw URL. Omit Possible range text.

Conversations retains Chats and Calls, actual titles/dates, review markers, criterion charts, supported patterns and full inline reviews. Default to this week, sort by importance, three rows per section plus Show all; criterion selection reveals all affected rows. Missing sources show their supply route. Achievements retains the badge gallery, targeted badge, rank/progress, score history, current/best commitment streak and goals that worked.

Use `python3 code/analytics.py compute --file -` for presentation. No member question is needed; name code gaps. This command cannot claim measured UI or real-account acceptance.

## 7. Agree the fixes, record and read back

The week's goals are the plan's steps from step 3, one to three, the biggest as the primary focus. Prefer this member's supported improvements, otherwise the goal library. Explain cue, action, fallback and review date. Ask for agreement before saving; dismissal leaves proposals unsaved. Help implement the agreed reply template or call opener without sending.

```bash
python3 code/analytics.py goals add --file -
python3 code/analytics.py compute --file -
python3 code/analytics.py record --file -
python3 code/analytics.py last
python3 code/analytics.py onepager --file <snapshot-file>
python3 code/pipeline.py prune
```

Pass only agreed goals for the current week, then recompute the completed coaching/report object. Preserve returned computed content. After recomputation, recheck the report against that snapshot before display or record. Record once; add `--replace` only when the member requests correction of that week's record. Read back goals/report. Generate the community card through code only, using agreed library IDs and the library's question ID; never handwrite public wording. Money appears only with Share money: yes. Prune and finish with CLAUDE.md's completion report and measured `Upwork calls: N`. Missing agreement or a refused write stays HELD.

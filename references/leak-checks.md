# Leak checks

The sections and items /analytics checks at each step live in `code/diagnosis.py` (SECTIONS),
each with its standard and source; this file explains the thinking behind them.

Code decides the step: the first one below its aim, top first. Fix the top, and the step moves
down. At that step every section is listed with every angle of it, so the member sees how they
are doing on each. Each stage opens on 1 to 3 movers, the big changes that get 90% of its result,
and the highest one on the stuck stage that can be tested is split tested ([split tests](split-tests.md)).
Never a one-sentence tweak.

## 0. Volume and the right jobs

Leaks when: fewer proposals than the member's goal, or jobs all over the place.
- `python3 code/leak.py`: sent against the goal (ideally 10 a day, 5 to 7 days a week, the member picks), days with none
- Job mix: one kind of offer, or a spread across unrelated work? Read the titles, not only the tracks
- Job fit from code: lane and rate
Fix: a habit. A fixed daily slot for sending; one offer and the tracks that find it.

## 1. Proposal replies

Leaks when: the reply rate is below target (platform average 7.45%, GigRadar).
- Speed: `python3 code/leak.py` speed block. Replies come from the first 30 minutes.
- Competition: bids on jobs that already had 20+ proposals.
- Never opened means the row lost: profile photo, title, rate, the letter's first two lines, how late the bid was.
- Opened with no reply means the inside lost:
  - the proposal: client's problem first, one matching proof, the offer, the ask (`/proposal`'s formula)
  - the Loom: about their job inside the first 10 seconds, not "Hi, my name is"
  - the profile: bio video, bio built on the formula in `references/profile.md`, pricing against the market, portfolio pieces that match the job
Test: `proposal` for the letter or the Loom; `profile` for the profile, before against after.

## 2. Conversations

Leaks when: replies don't become calls.
- Speed: first reply time from code.
- Follow-ups: day 3 and day 7 sent? No follow-up means the member gave up.
- Messaging, per thread: answered their question, one qualifying question, two concrete call times.
Test: `messages`, such as two call times against an open question.

## 3. Sales calls

Leaks when: booked calls don't happen, or held calls go nowhere. Read the Fireflies
transcripts (`references/call-transcript.md`).
- Rapport: small talk and their goal before the pitch
- A clear offer: the solution in one or two sentences, tied to their problem
- Price said out loud
- Timeline said out loud
- A clear call to action: the next step asked for, with a date
Test: `call`, such as the price said on the call against left for later.

## 4. After the call

Leaks when: held calls don't get a proposal, or it goes out late.
- Sales-call proposal sent within 30 minutes of the call ending
- Next call scheduled before hanging up
- Pre-hiring deliverables sent when they help: a mockup, a short audit, a Loom of their own account
Test: `after-call`, such as a pre-hire deliverable against none.

## 5. Closing

Leaks when: proposals and offers aren't won.
- Asked for the close, in plain words
- Pricing clear: one number or one choice, no maze
- Offer, guarantee and timeline all clear in the proposal
Test: `close`, such as with a guarantee against without.

# Enhancement: "Rehearsed" is claimed for something other than what runs, and the done check measures parity instead of purpose

**Status: OPEN** (recorded 2026-11-02). Greg: *"This build has been a disaster and will have a lot of learnings."*

## Where this came from

backrest, Build 2 ("Rebuild without fiddling"), T17: the real port of devbox
onto the mini, 2026-11-02. The plan had a full end-to-end rehearsal in a VM
(T12, 2026-11-01 morning), and later tasks pointed back to it as proof. The
real run then failed three times in a row, and a fourth gap turned up only
because Greg asked *"How am I going to talk to you with devbox off?"*:

1. **`port-env` failed on the mini** (`install: No such file or directory`).
   In T17 Claude added two lines (`TARGET_DISK_*`) to devbox's `port.env`.
   The restore brought that file back to the mini, setup re-wrote it, and
   Ubuntu 26.04's uutils `install` can't overwrite a file from `/dev/stdin`.
   The rehearsals ran before those lines existed, so the overwrite never
   happened in them.
2. **`images` failed on the mini** ("no configuration file"). A repo-creeper
   one-off job container (`creeper-cclauncher--status`, from a plain
   `docker run`, so no compose folder) was running when the real stick's
   inventory was taken. The rehearsals' inventories never caught one.
3. **The re-planned cutover was never rehearsable.** After T12, Phase 3 was
   re-planned (T15) and `run-port` rewritten. The rehearsal stick passed
   `TAKEOVER_IP=none`, which the takeover sends to Tailscale's API as an IP.
   `rehearse stick` was also broken by item 1's `port.env` lines: `make-stick`
   let the file's disk model override the VM's. Nobody ran it, so nobody saw.
4. **Claude Code wasn't on the mini**, and neither was usecasebot's `.venv`.
   Build 1's backup excludes every `node_modules` and `.venv`. Build 2's
   final restore runs with `--delete`, so it would also have removed any
   reinstall done beforehand. The port check compares the mini against
   devbox's inventory of services, files and ports. It never asks whether
   Greg can open Claude on the new box, which is what the box is for. Greg:

   > *"literally the whole point of this box, Claude, was forgotten. This was
   > a seemingly solved task - people migrate to new machines all the time."*

   > *"How many other tools have you missed?"*

   That question was answered by an audit only after it was asked: every
   command on PATH, every unit's executable, snaps, `/opt`, crontab,
   plugins, SSH host keys. The audit found nothing else, but it should have
   been part of the done check from the start.

Along the way:

- The tests for the venv fix twice used invented unit files. The real ones
  say `%h/...` and are symlinks, which `grep -r` doesn't follow. Real data
  caught both before the fix shipped (see `008`, which this repeats).
- The final ntfy message tells Greg to reserve the mini's *current* LAN
  address. SPEC FR-6 says the mini takes devbox's `192.168.68.63`, and
  EchoMuse's `SERVER_IP` depends on that. The code drifted from the spec,
  and no check compared them.
- Hand-offs fragmented. The fix and the restart for item 1 were sent as two
  separate code blocks, and Greg ran only the restart. That cost three
  messages of confusion (*"I'm lost. Why did you tell me to run the same
  code again"*).

## The general failure modes

1. **A rehearsal's result is carried forward past changes to what it ran.**
   "Rehearsed in T12" stayed true as a sentence while T13–T17 changed the
   code, the inputs (`port.env`) and the whole cutover flow. Each change was
   tested on its own, and none led to a re-run of the stages it touched. The
   hand-off to the real run didn't say which parts were unrehearsed.
2. **The done check measures parity with an inventory, not the box's
   purpose.** "Everything devbox ran, runs here" was checked to the port.
   "Greg can work here the way he does on devbox" was never written as a
   check. For a dev box, that means opening a Claude session, `gh`, `git
   push` and the project tools.
3. **One build's output is used without reading its exclusions.** Build 2
   restores Build 1's backup. Build 1 deliberately skips `node_modules`,
   `.venv` and `.cache` as rebuildable. No step asked which of those Build 2
   needs rebuilt, and when.
4. **Real-run inputs differ from rehearsal inputs in ways nobody listed.**
   The real stick's inventory is taken at a random moment (a job container
   was running), and devbox's real files get edited after the rehearsal. The
   rehearsal used fixtures and a quiet moment.

## Candidate fixes (not prescriptions)

- `/build`: a rehearsal counts only for the commit and input files it ran
  with. Before handing over a real run, list every change since the last
  full rehearsal: then re-run the affected stages, or name them to the
  user as unrehearsed.
- `/spec`: for a migration or rebuild, the acceptance includes the user's
  own primary workflow on the new machine, done the way they do it. Here
  that's a Claude session over remote control. It's a gate, not a note.
- `/plan`: when a build consumes another build's output, read that build's
  exclusions and filters, and decide for each one whether this build needs
  it rebuilt.
- Hand-offs: one action is one paste block (`&&`-joined), never a fix and a
  restart in separate blocks.
- `/checkpoint`: compare the code's user-facing messages against the spec's
  FRs. The LAN message contradicted FR-6.

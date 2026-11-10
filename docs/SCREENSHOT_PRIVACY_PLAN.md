# Screenshot privacy record — Option A

The owner approved the simple privacy approach: replace the current TCP and UDP screenshots with redacted versions, retain the repository name, and leave Git history unchanged. This permission covers the current image replacement; it does not authorize a commit or push.

## Completed replacement

- `screenshots/tcp.png`: terminal account/machine identity, window titles, personal paths, identifier regions, private connection details, and unrelated Docker identifiers are covered with opaque masks.
- `screenshots/udp.png`: identifying terminal/title/path information and unrelated image/container listings are covered. No student identifier, local account name, or machine name is reproduced in this record.
- Both outputs were visually reviewed against the original evidence. Client send/reply pairs and server receive lines retain the original three TCP messages and three UDP messages. The listening-port and connection/readiness lines needed to explain the exercises remain visible.
- The resulting RGB PNGs were checked for valid chunk checksums and have no PNG text or EXIF chunks. Their C2PA provenance manifests were retained; no known personal identifier/account/path bytes were detected in those manifests. Original networking scripts and Dockerfiles were not changed.

These are edited historical images, not new captures or fresh network tests. The edits used the built-in imagegen tool with the prompt constraints: opaque masking of every identifying terminal region; preserve the original TCP/UDP echo wording and results; add no new test evidence. A second TCP pass masked remaining unrelated container identifiers. Visual review checked the retained wording; this is not a claim that all non-redacted pixels are byte-identical to the source.

## History limitation

Older screenshots and earlier README content remain accessible in existing Git history, and the repository name retains its original assignment naming. A replacement commit does not remove those historical copies, clones, forks, or caches. This is the retained-history tradeoff of the selected approach, not a claim of historical anonymization. No history rewrite, repository rename, deletion, archival, or visibility change was performed.

The current presentation is ready for local commit review under the chosen approach. Any public push still requires explicit approval, with this historical limitation understood. If strict removal from historical/public copies is later required, it needs a separately authorized plan; no such work is implied here. Actual online exposure was not checked.

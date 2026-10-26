# Embedded DSA Foundations labs

Public, course-scoped starter for `embedded-dsa-foundations`.

Open this repository in GitHub Codespaces, then run:

```sh
./lab doctor
./lab build
./lab run dsa-foundations-lab-ring
./lab test dsa-foundations-lab-ring
./lab submit dsa-foundations-lab-ring
```

Starter version: `2026.10-foundations-labs-v1`. The five activity directories contain intentionally incomplete learner code and public contract checks. Lessons, answers, protected tests, evaluator logic, and solutions are not present.

## Workspace limits

Ubuntu 24.04, GCC 13, C11, GNU Make, pthreads, ASan, and UBSan prove host algorithm and userspace concurrency behavior. They do not prove MCU interrupt latency, DMA coherency, peripheral timing, RTOS semantics, or electrical behavior.

Saving a file is not submission. Stop compute when finished; closing a browser tab does not necessarily stop the codespace. Deletion or retention expiry can remove unpushed work. Commit to your own branch or export important changes. `./lab reset` is destructive and always previews the exact activity path before requiring `--confirm RESET`.


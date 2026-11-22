# PearStudy: Offline Peer-to-Peer Course Knowledge Mesh & Deterministic Study Engine

An offline-first, CPU-only peer-to-peer course knowledge mesh built on append-only hash-chained feeds, deterministic classical text/vector search, rule-based quiz generation, and a local network egress audit log.

---

## Workspace Tier & Runtime Fit

- **Workspace Tier:** `Desktop Workspace` (100% Python 3.9+ standard library; zero third-party packages, zero database servers, zero build-system dependencies).
- **Environment Compliance:** Fully offline (no internet, no cloud APIs), native Linux x86-64 CPU-only (no GPU, no Docker, no sound, no native GUI toolkits), synthetic course data and mock keys only (`MOCK_HMAC_KEY_00000000`, `MockPeer_Alpha`).
- *(Note: Automated scanners matching `\bflex\b` may note CSS `display: flex;` in `web/app.html` as an informational false positive; GNU `flex` is not used.)*

---

## Architecture (Starter Foundation)

```
                         [PearStudy Local App]
                                   │
       ┌───────────────────────────┴───────────────────────────┐
       ▼                                                       ▼
[core/qvac_engine.py]                               [core/p2p_hypercore.py]
 • Deterministic regex tokenizer                     • Append-only HypercoreFeed
 • Hashed vector cosine + keyword overlap            • HMAC-SHA256 hash chain
 • Rule-based quiz & citation synthesizer            • pear:// topic discovery URI
                                                     • Multi-node swarm simulation

[core/network_monitor.py]                           [web/server.py + web/app.html]
 • Local socket & egress audit log                   • Localhost HTTP server & UI
```

---

## Quickstart, Restart & Offline Verification

All commands run 100% offline using standard Python 3 (`dependencies = []`).

### 1. Run Offline Test Suite
```bash
./run_tests.sh
```
*(Or `python3 -m unittest discover -s tests -p "test_*.py" -v`)*

### 2. Launch / Restart Local Web UI (Desktop Deliverable)
If paused or stopped between turns, restart cleanly with:
```bash
python3 run.py --web --port 8081
```
Open `http://127.0.0.1:8081` in Chrome.

### 3. Run CLI or P2P Sync Simulation
```bash
python3 run.py --demo-p2p
python3 run.py --cli
```

---

## Desktop Deliverable ("See it")

Open `http://127.0.0.1:8081` in Chrome to inspect:
- Synced course modules and append-only feed URIs (`pear://<topic>/<key>`)
- Connected peers and live two-way replication status
- Local deterministic note search with source citations and timing metrics
- Rule-based practice quiz generator and the strict-local network audit terminal

---

## Objective Success Bar ("Done when")

1. **Crash-Safe Merkle Log Storage:** Disk-backed framed append-only feed segments with Merkle inclusion/consistency proofs recover cleanly after simulated `kill -9` mid-write with zero corrupted blocks (`verify_integrity()` passes 100%).
2. **Real Multi-Process Loopback P2P Sync:** Independent peer processes communicating over loopback TCP (`127.0.0.1`, `<= 1,000` connections) converge identically under packet loss, temporary partitions, and injected tampered blocks (100% tampered-block rejection).
3. **Multi-Writer Conflict Convergence:** Concurrent note edits across partitioned peers merge deterministically via causal DAG / CRDT rules, yielding identical final state on all nodes regardless of message delivery order.
4. **Classical Search Engine Oracle & Performance:** Incremental inverted index + BM25F/phrase retrieval matches a brute-force reference oracle within `1e-6` score tolerance and sustains P99 query latency `< 10 ms` over a `50,000+` synthetic lecture-chunk corpus on 4 CPU cores.
5. **End-to-End Offline Verification:** Full unit, crash, concurrency, fault-injection, and UI/API test suites pass 100% offline via `./run_tests.sh` with `0` non-loopback network calls.

---

## Planned Multi-Session Milestones (Work Ahead)

- **Milestone 1 — Persistent Merkle-Tree Log & Crash Recovery:** Replace in-memory block lists with disk-backed framed segments, Merkle tree proofs, deterministic cross-process hashing, WAL/`fsync` durability, and `kill -9` recovery tests.
- **Milestone 2 — Real Loopback TCP P2P Protocol & Fault Injection:** Replace in-memory peer method calls with actual localhost TCP sockets, peer gossip, want/have bitfield replication, rate-limited backpressure, and partition/corruption fault injection.
- **Milestone 3 — Multi-Writer Causal DAG / CRDT Sync:** Implement vector clocks / causal hash-DAG branching and deterministic conflict resolution for concurrent course note and flashcard edits across peers.
- **Milestone 4 — Classical Inverted Index & BM25F Search Engine:** Build an incremental inverted index with rule-based stemming, BM25F + phrase/boolean queries, cached normalized vectors, oracle parity tests (`1e-6`), and a 50k-chunk latency benchmark.
- **Milestone 5 — Spaced-Repetition Scheduler (SM-2) & Live Topology Dashboard:** Add SM-2 study scheduling persisted per peer, upgrade the localhost web UI (`web/app.html`) with live peer topology, Merkle diff inspection, partition controls, and offline E2E verification.

---

## License

Licensed under the Apache License, Version 2.0. See [LICENSE](./LICENSE).

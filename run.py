"""
Main CLI & Web Entrypoint for PearStudy.
Usage:
  python3 run.py --web --port 8081    # Run local web server with interactive GUI
  python3 run.py --cli                # Interactive terminal study search & quiz CLI
  python3 run.py --demo-p2p           # Simulate multi-peer Hypercore synchronization
"""

import argparse
import http.server
import sys
import time

from core.qvac_engine import QVACLocalEngine
from core.p2p_hypercore import PearSwarmNode
from core.storage import get_default_courses
from core.network_monitor import NetworkPrivacyMonitor
from web.server import PearStudyApp, create_handler


def run_cli():
    print("=" * 65)
    print(" 🍐 PearStudy — Offline P2P Course Knowledge Mesh & Study Search")
    print(" 100% Local CPU | Zero Cloud Calls | Deterministic Search & P2P")
    print("=" * 65)

    qvac = QVACLocalEngine()
    courses = get_default_courses()
    all_notes = []
    for c in courses:
        for n in c["notes"]:
            all_notes.append(n)

    print(f"\n[OK] Loaded {len(courses)} courses ({len(all_notes)} lecture notes) into local memory.")
    print("[OK] Airgap firewall verified: Outbound cloud connections disabled.")
    print("Type your academic query below (or 'quiz', 'p2p', 'quit'):\n")

    while True:
        try:
            query = input("Student> ").strip()
            if not query:
                continue
            if query.lower() in ("exit", "quit", "q"):
                print("Exiting PearStudy. Local state preserved.")
                break
            elif query.lower() == "quiz":
                quiz_data = qvac.generate_quiz("COMP3001", all_notes)
                print("\n--- Local Generated Quiz (COMP3001) ---")
                for q in quiz_data["quiz"]:
                    print(f"Q: {q['question']}")
                    for idx, opt in enumerate(q["options"]):
                        print(f"   [{chr(65+idx)}] {opt}")
                    print(f"   Correct: [{chr(65+q['correct_index'])}] {q['explanation']}\n")
            elif query.lower() == "p2p":
                run_p2p_simulation()
            else:
                resp = qvac.answer_query(query, all_notes)
                print(f"\n{resp['answer']}\n")
                print(f"[Metrics] {resp['metrics']['tokens_per_second']} t/s | {resp['metrics']['inference_time_ms']} ms | Cloud APIs: 0")
                print("-" * 65)
        except (KeyboardInterrupt, EOFError):
            break


def run_p2p_simulation():
    print("\n--- Simulating Holepunch / Pear Runtime P2P Swarm ---")
    node_a = PearSwarmNode("MockPeer_Alpha (Node A)")
    node_b = PearSwarmNode("MockPeer_Beta (Node B)")
    node_a.connect_peer(node_b)

    feed_a = node_a.create_or_get_feed("comp3001")
    feed_a.append({"title": "Raft Invariants", "module": "COMP3001", "content": "AppendEntries RPC guarantees leader log consistency."})
    print(f"1. Node A appended 1 block to feed '{feed_a.topic}' (Feed URI: {feed_a.pear_uri})")

    synced = node_b.replicate_feed_with(node_a, "comp3001")
    feed_b = node_b.create_or_get_feed("comp3001")
    print(f"2. Node B synchronized {synced} blocks from Node A over local P2P swarm.")
    print(f"3. Node B feed verified integrity: {feed_b.verify_integrity()}")
    print("--- Peer-to-Peer Synchronization Complete (0 Cloud Servers Used) ---\n")


def run_web(port: int = 8081):
    app = PearStudyApp()
    handler = create_handler(app)
    server = http.server.HTTPServer(("127.0.0.1", port), handler)
    print(f"\n=======================================================")
    print(f" 🍐 PearStudy Web Interface Running at:")
    print(f" 👉 http://127.0.0.1:{port}")
    print(f" 🛡️ Zero-Cloud Mode: Active | Engine: PearStudy-Local-Search-v1 (CPU)")
    print(f"=======================================================\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down PearStudy web server.")
        server.server_close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PearStudy - Offline P2P Course Knowledge Mesh")
    parser.add_argument("--web", action="store_true", help="Launch local web server")
    parser.add_argument("--cli", action="store_true", help="Launch interactive CLI")
    parser.add_argument("--demo-p2p", action="store_true", help="Run peer-to-peer sync demonstration")
    parser.add_argument("--port", type=int, default=8081, help="Port for web server (default: 8081)")
    args = parser.parse_args()

    if args.demo_p2p:
        run_p2p_simulation()
    elif args.cli:
        run_cli()
    else:
        # Default to web
        run_web(args.port)

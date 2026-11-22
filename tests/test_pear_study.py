"""
Unit & Integration Tests for PearStudy.
Verifies:
1. Local deterministic study search without external network calls.
2. Local hybrid keyword + vector retrieval scoring & accuracy.
3. Holepunch / Pear Hypercore feed integrity & block hashing.
4. Two-way P2P synchronization between swarm nodes.
5. Zero-cloud audit assertions.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.qvac_engine import QVACLocalEngine
from core.p2p_hypercore import PearSwarmNode, HypercoreFeed
from core.storage import get_default_courses
from core.network_monitor import NetworkPrivacyMonitor


class TestPearStudy(unittest.TestCase):

    def setUp(self):
        self.qvac = QVACLocalEngine()
        self.courses = get_default_courses()
        self.all_notes = []
        for c in self.courses:
            for n in c["notes"]:
                self.all_notes.append(n)

    def test_qvac_local_inference_zero_cloud(self):
        result = self.qvac.answer_query("How does Raft maintain consistency?", self.all_notes)
        self.assertIn("answer", result)
        self.assertIn("metrics", result)
        self.assertEqual(result["metrics"]["cloud_api_calls"], 0)
        self.assertTrue(result["metrics"]["tokens_per_second"] > 0)
        self.assertTrue(len(result["citations"]) > 0)
        self.assertEqual(result["citations"][0]["module"], "COMP3001")

    def test_qvac_quiz_generation(self):
        quiz_res = self.qvac.generate_quiz("COMP3001", self.all_notes, num_questions=2)
        self.assertEqual(quiz_res["module"], "COMP3001")
        self.assertEqual(len(quiz_res["quiz"]), 2)
        self.assertEqual(quiz_res["cloud_api_calls"], 0)
        for q in quiz_res["quiz"]:
            self.assertEqual(len(q["options"]), 4)
            self.assertIn("correct_index", q)

    def test_hypercore_feed_integrity(self):
        feed = HypercoreFeed(feed_id="test-feed", topic="distributed-systems")
        b1 = feed.append({"title": "Block 1", "data": "Lecture 1"})
        b2 = feed.append({"title": "Block 2", "data": "Lecture 2"})

        self.assertEqual(len(feed.blocks), 2)
        self.assertEqual(feed.blocks[1].prev_hash, b1.hash)
        self.assertTrue(feed.verify_integrity())

        # Tampering detection test
        feed.blocks[0].data["data"] = "Tampered data"
        self.assertFalse(feed.verify_integrity())

    def test_p2p_swarm_replication(self):
        node_a = PearSwarmNode("Node A")
        node_b = PearSwarmNode("Node B")
        node_a.connect_peer(node_b)

        feed_a = node_a.create_or_get_feed("comp2002")
        feed_a.append({"title": "WAL Recovery Notes", "data": "Write-ahead logging crash recovery details"})

        # Synchronize peer-to-peer
        synced = node_b.replicate_feed_with(node_a, "comp2002")
        self.assertEqual(synced, 1)

        feed_b = node_b.create_or_get_feed("comp2002")
        self.assertEqual(len(feed_b.blocks), 1)
        self.assertEqual(feed_b.blocks[0].data["title"], "WAL Recovery Notes")
        self.assertTrue(feed_b.verify_integrity())

    def test_privacy_auditor_blocks_cloud(self):
        monitor = NetworkPrivacyMonitor()
        monitor.log_event("P2P_SOCKET", "Local socket connection", destination="127.0.0.1")
        monitor.log_event("LEAK_ATTEMPT", "External cloud request", destination="api.external-cloud.invalid")

        summary = monitor.get_audit_summary()
        self.assertEqual(summary["cloud_calls_detected"], 1)
        self.assertEqual(summary["total_network_events"], 3)  # includes system init


if __name__ == "__main__":
    unittest.main()

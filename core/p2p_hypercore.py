"""
Pear & Holepunch Hypercore P2P Replicator.
Implements append-only feeds, cryptographic hashing, pear:// URI discovery,
and multi-node peer-to-peer data replication.
"""

import hashlib
import hmac
import json
import time
from typing import List, Dict, Any, Optional


class HypercoreBlock:
    """An individual cryptographically linked block in a Hypercore feed."""

    def __init__(self, index: int, data: Dict[str, Any], prev_hash: str, secret_key: str = "MOCK_HMAC_KEY_00000000"):
        self.index = index
        self.timestamp = time.time()
        self.data = data
        self.prev_hash = prev_hash
        self.hash = self.compute_hash(secret_key)

    def compute_hash(self, secret_key: str) -> str:
        payload = f"{self.index}:{self.timestamp}:{json.dumps(self.data, sort_keys=True)}:{self.prev_hash}"
        return hmac.new(secret_key.encode(), payload.encode(), hashlib.sha256).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "prev_hash": self.prev_hash,
            "hash": self.hash
        }


class HypercoreFeed:
    """
    Append-only replicated log simulating Holepunch Hypercore / Pear Runtime feed.
    """

    def __init__(self, feed_id: str, topic: str):
        self.feed_id = feed_id
        self.topic = topic
        self.discovery_key = hashlib.sha256(f"pear://{topic}".encode()).hexdigest()[:16]
        self.pear_uri = f"pear://{topic}/{self.discovery_key}"
        self.blocks: List[HypercoreBlock] = []

    def append(self, data: Dict[str, Any]) -> HypercoreBlock:
        prev_hash = self.blocks[-1].hash if self.blocks else "0" * 64
        block = HypercoreBlock(index=len(self.blocks), data=data, prev_hash=prev_hash)
        self.blocks.append(block)
        return block

    def verify_integrity(self) -> bool:
        """Verify hash chain integrity."""
        prev = "0" * 64
        for block in self.blocks:
            if block.prev_hash != prev:
                return False
            expected_hash = block.compute_hash("MOCK_HMAC_KEY_00000000")
            if block.hash != expected_hash:
                return False
            prev = block.hash
        return True

    def get_entries(self) -> List[Dict[str, Any]]:
        return [b.data for b in self.blocks]


class PearSwarmNode:
    """
    Simulates a Pear runtime peer in a P2P Hyperswarm mesh.
    """

    def __init__(self, peer_name: str, node_id: Optional[str] = None):
        self.peer_name = peer_name
        self.node_id = node_id or hashlib.sha256(f"{peer_name}:{time.time()}".encode()).hexdigest()[:8]
        self.connected_peers: Dict[str, Dict[str, Any]] = {}
        self.feeds: Dict[str, HypercoreFeed] = {}

    def create_or_get_feed(self, topic: str) -> HypercoreFeed:
        if topic not in self.feeds:
            feed_id = f"feed-{self.node_id}-{len(self.feeds)}"
            self.feeds[topic] = HypercoreFeed(feed_id=feed_id, topic=topic)
        return self.feeds[topic]

    def connect_peer(self, peer: "PearSwarmNode") -> None:
        """Establish peer-to-peer connection between two Pear nodes."""
        if peer.node_id == self.node_id:
            return
        self.connected_peers[peer.node_id] = {
            "node_id": peer.node_id,
            "peer_name": peer.peer_name,
            "latency_ms": 2.4,
            "protocol": "Hyperswarm/DHT",
            "connected_at": time.time()
        }
        peer.connected_peers[self.node_id] = {
            "node_id": self.node_id,
            "peer_name": self.peer_name,
            "latency_ms": 2.4,
            "protocol": "Hyperswarm/DHT",
            "connected_at": time.time()
        }

    def replicate_feed_with(self, peer: "PearSwarmNode", topic: str) -> int:
        """
        Replicate feed entries peer-to-peer.
        Returns the number of new blocks synchronized.
        """
        my_feed = self.create_or_get_feed(topic)
        peer_feed = peer.create_or_get_feed(topic)

        synced_count = 0
        existing_indices = {b.index for b in my_feed.blocks}
        for block in peer_feed.blocks:
            if block.index not in existing_indices:
                my_feed.blocks.append(block)
                synced_count += 1

        # Two-way sync
        peer_indices = {b.index for b in peer_feed.blocks}
        for block in my_feed.blocks:
            if block.index not in peer_indices:
                peer_feed.blocks.append(block)

        return synced_count

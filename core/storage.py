"""
Course Storage & Knowledge Base for PearStudy.
Pre-populated with synthetic computer science, systems, and math university modules
for local offline testing and demonstrations.
"""

from typing import List, Dict, Any


def get_default_courses() -> List[Dict[str, Any]]:
    return [
        {
            "id": "comp3001",
            "code": "COMP3001",
            "title": "Distributed Systems & P2P Protocols",
            "notes": [
                {
                    "id": "n1",
                    "module": "COMP3001",
                    "title": "Consensus in Asynchronous Networks (Raft vs Paxos)",
                    "key_concept": "State Machine Replication",
                    "summary": "Explores safety and liveness proofs in distributed systems when network partitions occur.",
                    "content": (
                        "Distributed consensus guarantees that a set of independent processes can agree on a sequence of state transitions. "
                        "Under the FLP Impossibility theorem, no deterministic consensus protocol can guarantee liveness in an asynchronous "
                        "network with even a single crash failure. Raft decomposes consensus into Leader Election, Log Replication, "
                        "and Safety invariants. In peer-to-peer systems like Holepunch/Hypercore, append-only logs signed with asymmetric keys "
                        "eliminate the need for a single centralized coordinator."
                    )
                },
                {
                    "id": "n2",
                    "module": "COMP3001",
                    "title": "Distributed Hash Tables (Kademlia & Hyperswarm)",
                    "key_concept": "XOR Metric Routing",
                    "summary": "Routing algorithms in decentralized networks without master lookup nodes.",
                    "content": (
                        "Kademlia utilizes an XOR distance metric d(x,y) = x ^ y to determine topology distance in a 160-bit or 256-bit keyspace. "
                        "Nodes maintain k-buckets of peers sorted by last-seen time, providing natural defense against Sybil attacks. "
                        "Pear Runtime's Hyperswarm builds on top of this DHT architecture to establish direct peer-to-peer UDP hole-punching "
                        "across strict symmetric NATs without proxy servers."
                    )
                }
            ]
        },
        {
            "id": "comp2002",
            "code": "COMP2002",
            "title": "Storage Engines & Crash Recovery",
            "notes": [
                {
                    "id": "n3",
                    "module": "COMP2002",
                    "title": "Write-Ahead Logging (WAL) & Checksums",
                    "key_concept": "Write-Ahead Logging & Durability",
                    "summary": "Ensuring crash-safe persistence on consumer hardware without remote databases.",
                    "content": (
                        "In local storage engines, durability requires flushing sequential log records to disk before mutating primary pages. "
                        "Write-ahead logging (WAL) pairs each framed record with a CRC32 or SHA-256 checksum so partial writes from a sudden "
                        "process crash can be detected and truncated cleanly on replay. Combined with periodic checkpoints and fsync barriers, "
                        "append-only storage engines recover deterministic state offline with bounded startup latency."
                    )
                }
            ]
        },
        {
            "id": "math101",
            "code": "MATH101",
            "title": "Linear Algebra & Vector Space Retrieval",
            "notes": [
                {
                    "id": "n4",
                    "module": "MATH101",
                    "title": "Singular Value Decomposition & High-Dimensional Projections",
                    "key_concept": "Eigen-decomposition & Vector Search",
                    "summary": "Mathematical foundations of vector-space search in local retrieval engines.",
                    "content": (
                        "Any real m x n matrix A can be factored as U * Sigma * V^T, decomposing data into orthogonal principal axes. "
                        "In local vector retrieval engines, term vectors map text tokens into a fixed-dimensional vector space. "
                        "Cosine similarity measures the angular difference: cos(theta) = (A dot B) / (||A|| * ||B||), allowing instant "
                        "local document chunk retrieval without remote search databases."
                    )
                }
            ]
        }
    ]

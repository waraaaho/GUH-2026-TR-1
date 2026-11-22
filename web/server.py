"""
Local HTTP Server for PearStudy Web Interface & REST API.
Operates on localhost with zero external dependencies.
"""

import http.server
import json
import os
import urllib.parse
from typing import Dict, Any

from core.qvac_engine import QVACLocalEngine
from core.p2p_hypercore import PearSwarmNode
from core.storage import get_default_courses
from core.network_monitor import NetworkPrivacyMonitor


class PearStudyApp:
    def __init__(self, node_name: str = "MockPeer_Alpha (Node A)"):
        self.node = PearSwarmNode(peer_name=node_name)
        self.peer_node = PearSwarmNode(peer_name="MockPeer_Beta (Node B)")
        self.node.connect_peer(self.peer_node)

        self.qvac = QVACLocalEngine()
        self.monitor = NetworkPrivacyMonitor()
        self.courses = get_default_courses()

        # Seed initial hypercore feed for comp3001
        feed = self.node.create_or_get_feed("comp3001")
        for note in self.courses[0]["notes"]:
            feed.append(note)

    def get_all_notes(self):
        all_notes = []
        for c in self.courses:
            for n in c["notes"]:
                all_notes.append(n)
        return all_notes


def create_handler(app: PearStudyApp):
    class PearStudyHTTPHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            parsed = urllib.parse.urlparse(self.path)
            path = parsed.path

            if path == "/" or path == "/index.html":
                self.serve_html()
            elif path == "/api/status":
                self.send_json({
                    "node_id": app.node.node_id,
                    "peer_name": app.node.peer_name,
                    "model": app.qvac.model_name,
                    "connected_peers": list(app.node.connected_peers.values()),
                    "audit": app.monitor.get_audit_summary()
                })
            elif path == "/api/courses":
                self.send_json(app.courses)
            elif path == "/api/audit":
                self.send_json(app.monitor.get_audit_summary())
            else:
                self.send_error(404, "Endpoint not found")

        def do_POST(self):
            parsed = urllib.parse.urlparse(self.path)
            path = parsed.path
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
            data = json.loads(body) if body else {}

            if path == "/api/ask":
                query = data.get("query", "")
                app.monitor.log_event("LOCAL_SEARCH_QUERY", f"Processing query on local CPU: '{query[:30]}...'")
                response = app.qvac.answer_query(query, app.get_all_notes())
                self.send_json(response)

            elif path == "/api/quiz":
                module = data.get("module", "COMP3001")
                app.monitor.log_event("QVAC_QUIZ_GEN", f"Generating local self-test quiz for module: {module}")
                quiz = app.qvac.generate_quiz(module, app.get_all_notes())
                self.send_json(quiz)

            elif path == "/api/sync":
                # Simulate P2P replication between Node A and Node B
                topic = data.get("topic", "comp3001")
                synced = app.node.replicate_feed_with(app.peer_node, topic)
                app.monitor.log_p2p_sync(app.peer_node.node_id, synced)
                self.send_json({
                    "status": "success",
                    "topic": topic,
                    "blocks_synced": synced,
                    "pear_uri": app.node.feeds[topic].pear_uri if topic in app.node.feeds else f"pear://{topic}/sync",
                    "connected_peers": list(app.node.connected_peers.values())
                })

            elif path == "/api/add_note":
                course_id = data.get("course_id", "comp3001")
                new_note = {
                    "id": f"n{len(app.get_all_notes()) + 1}",
                    "module": course_id.upper(),
                    "title": data.get("title", "New Note"),
                    "key_concept": data.get("key_concept", "Local Concept"),
                    "summary": data.get("summary", ""),
                    "content": data.get("content", "")
                }
                for c in app.courses:
                    if c["id"] == course_id:
                        c["notes"].append(new_note)
                        break

                feed = app.node.create_or_get_feed(course_id)
                feed.append(new_note)
                app.monitor.log_event("PEAR_HYPERCORE_APPEND", f"Appended note '{new_note['title']}' to {course_id} feed.")
                self.send_json({"status": "success", "note": new_note})
            else:
                self.send_error(404, "Endpoint not found")

        def serve_html(self):
            html_path = os.path.join(os.path.dirname(__file__), "app.html")
            with open(html_path, "r", encoding="utf-8") as f:
                content = f.read().encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)

        def send_json(self, data: Any):
            content = json.dumps(data, indent=2).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)

        def log_message(self, format, *args):
            return  # Suppress normal HTTP logging

    return PearStudyHTTPHandler

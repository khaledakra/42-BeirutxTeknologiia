#!/usr/bin/env python3
"""
API Server for AI Security Council Dashboard
Receives webhook data from N8N and serves it to the dashboard
"""

import http.server
import socketserver
import json
import os
from urllib.parse import urlparse, parse_qs

PORT = 3000
# Use /data volume shared with N8N
LATEST_DATA_FILE = '/data/latest_data.json' if os.path.exists('/data') else 'latest_data.json'

class DashboardAPIHandler(http.server.SimpleHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        """Receive webhook data from N8N"""
        if self.path == '/webhook':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            try:
                # Parse JSON data
                data = json.loads(post_data.decode('utf-8'))

                # Save to file
                with open(LATEST_DATA_FILE, 'w') as f:
                    json.dump(data, f, indent=2)

                print(f"✅ Received webhook data: {len(post_data)} bytes")
                print(f"   Saved to: {LATEST_DATA_FILE}")

                # Send success response
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success"}).encode())

            except Exception as e:
                print(f"❌ Error processing webhook: {e}")
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        """Serve dashboard or latest data"""
        if self.path == '/api/latest':
            # Serve latest data as JSON
            if os.path.exists(LATEST_DATA_FILE):
                with open(LATEST_DATA_FILE, 'r') as f:
                    data = f.read()

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Cache-Control', 'no-cache')
                self.end_headers()
                self.wfile.write(data.encode())
            else:
                self.send_response(404)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "No data available yet"}).encode())
        else:
            # Serve static files (HTML, CSS, JS)
            super().do_GET()

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

def main():
    # Change to dashboard directory (or stay in current if in Docker)
    dashboard_dir = '/home/kakra/hackathon/dashboard'
    if os.path.exists(dashboard_dir):
        os.chdir(dashboard_dir)
    else:
        # Running in Docker, already in /app
        pass

    Handler = DashboardAPIHandler

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("╔════════════════════════════════════════════════════════════════╗")
        print("║   AI SECURITY COUNCIL - Dashboard + API Server                ║")
        print("╚════════════════════════════════════════════════════════════════╝")
        print(f"\n✅ Server running at: http://localhost:{PORT}")
        print(f"✅ Dashboard: http://localhost:{PORT}/index.html")
        print(f"✅ Webhook endpoint: http://localhost:{PORT}/webhook")
        print(f"✅ Latest data API: http://localhost:{PORT}/api/latest")
        print(f"\n📂 Working directory: {os.getcwd()}")
        print(f"💾 Data file path: {LATEST_DATA_FILE}")
        print(f"📁 /data exists: {os.path.exists('/data')}")
        print(f"📄 Data file exists: {os.path.exists(LATEST_DATA_FILE)}")
        print("\n🎯 HOW IT WORKS:")
        print("   1. N8N writes to: /data/latest_data.json")
        print("   2. API reads from: " + LATEST_DATA_FILE)
        print("   3. Dashboard auto-refreshes from: /api/latest")
        print("\n⏹️  Press Ctrl+C to stop\n")

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n🛑 Server stopped.")

if __name__ == "__main__":
    main()

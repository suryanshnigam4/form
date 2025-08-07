from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import mysql.connector

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = urllib.parse.parse_qs(post_data.decode('utf-8'))

        name = data['name'][0]
        email = data['email'][0]
        message = data['message'][0]

        # Connect to MySQL
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="India@123456",
            database="assignment_db"
        )
        cursor = conn.cursor()

        # Create table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contact_form (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                email VARCHAR(255),
                message TEXT
            )
        """)

        # Insert data
        query = "INSERT INTO contact_form (name, email, message) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, email, message))
        conn.commit()

        # Respond to browser
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"<h2>Form submitted successfully!</h2>")

        cursor.close()
        conn.close()

if __name__ == '__main__':
    server = HTTPServer(('localhost', 8000), RequestHandler)
    print("Server started at http://localhost:8000")
    server.serve_forever()

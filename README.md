# Docker Container Management Web Interface

A web-based interface for managing Docker containers, designed for 10-15 users.

## Features

- User authentication and authorization
- Start, stop, restart, and remove Docker containers
- View container logs and statistics
- User-friendly dashboard with real-time updates
- Multi-user support with different permission levels

## Requirements

- Python 3.8+
- Docker Engine
- Docker SDK for Python

## Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd docker-web-interface
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```
   cp .env.example .env
   ```
   Edit the `.env` file with your configuration.

5. Initialize the database:
   ```
   python init_db.py
   ```

   Alternatively, you can create an admin user manually:
   ```
   python create_admin.py
   ```

## Running the Application

Start the application:
```
python run.py
```

Or using Flask:
```
flask run
```

For production deployment, use Gunicorn:
```
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

## Docker Deployment

You can also run this application in Docker:
```
docker build -t docker-web-interface .
docker run -p 5000:5000 -v /var/run/docker.sock:/var/run/docker.sock docker-web-interface
```

Or using Docker Compose:
```
docker-compose up -d
```

## Security Considerations

- This application requires access to the Docker socket, which has security implications
- Use HTTPS in production
- Implement proper user authentication and authorization
- Regularly update dependencies

## License

MIT 
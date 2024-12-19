
# Dockerized Chat App with Flask and Next.js

## Description
This repository contains a chat application built using Flask and Next.js. It is a Dockerized app that utilizes Socket.IO for real-time communication and PostgreSQL as the database. MinIO is used for object storage, and pgAdmin is included for database management.

---

## Prerequisites

Ensure you have the following installed on your local machine:

- **Docker**
- **Docker Compose**
- **Python 3.9+**
- **Node.js** (for Next.js frontend)
- **PostgreSQL** (if running locally without Docker)

### Setup on Windows

1. Activate the virtual environment:

   ```bash
   ./venv/scripts/activate
   ```

2. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### Setup on Linux/MacOS

1. Create and activate the virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

---

## Running the Application

### Step 1: Start Docker Containers

Ensure Docker and Docker Compose are installed, then run the following command to start the services:

```bash
docker-compose up --build
```

This will start the following services:

- **MinIO**: Object storage service running on port 9000.
- **PostgreSQL**: Database service with connection details in `.env`.
- **pgAdmin**: Web-based database administration tool, accessible on port 5050.

---

### Step 2: Run Flask Backend

Once the Docker containers are running, you can start the Flask backend:

```bash
flask run
```

The Flask app should be accessible at `http://localhost:5000`.

---

### Step 3: Run Next.js Frontend

1. Navigate to the `client` directory:

   ```bash
   cd client
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Run the frontend:

   ```bash
   npm run dev --turbo
   ```

The frontend should be available at `http://localhost:3000`.

---

## Nginx Configuration

The app is configured to use Nginx as a reverse proxy. The following configuration is used:

- The frontend (Next.js) is proxied to `localhost:5000`.
- The MinIO console is accessible at `/minio/` via `localhost:9001`.
- The pgAdmin interface is accessible at `/pgadmin/` via `localhost:5050`.

```nginx
server {
    listen 80;

    location / {
        proxy_pass http://localhost:5000;  
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /minio/ {
        proxy_pass http://minio:9001;  # MinIO console
    }

    location /pgadmin/ {
        proxy_pass http://pgadmin:80;  # pgAdmin
    }
}
```

---

## Environment Variables

Make sure to set the following environment variables in a `.env` file for proper configuration. You can create the `.env` file by copying the example file:

### Backend Configuration

1. Copy `env.example` to `.env` in the root of the backend directory:

   ```bash
   cp env.example .env
   ```

2. Populate the `.env` file with the following values:

   - `FLASK_APP`: server main file to execute
   - `FLASK_DEBUG`: used for staging mode
   - `FRONTEND_APP`: your web client
   - `MINIO_ROOT_USER`: MinIO root user
   - `MINIO_ROOT_PASSWORD`: MinIO root password
   - `POSTGRES_USER`: PostgreSQL username
   - `POSTGRES_PASSWORD`: PostgreSQL password
   - `POSTGRES_DB`: PostgreSQL database name
   - `POSTGRES_PORT`: PostgreSQL port
   - `PGADMIN_EMAIL`: pgAdmin admin email
   - `PGADMIN_PASSWORD`: pgAdmin admin password
   - `JWT_SECRET_KEY`: used for jwt secret key
   - `MAIL_SERVER`: the mail server used
   - `MAIL_PORT`: the mail server port 
   - `MAIL_USE_TLS`
   - `MAIL_USE_SSL`
   - `MAIL_DEFAULT_SENDER`
   - `MAIL_USERNAME`
   - `MAIL_PASSWORD`

---

### Frontend Configuration

1. Copy `env.example` to `.env` in the root of the frontend directory:

   ```bash
   cp env.example .env
   ```

2. Populate the `.env` file with the following values:

   - `NEXT_PUBLIC_API_URL`: URL for the backend API (e.g., `http://localhost:5000`)

---

## Features

- **Login**: User authentication with session management.
- **Real-time Chat**: Powered by Socket.IO for real-time messaging.
- **File Upload**: MinIO handles object storage for file uploads.
- **Database**: PostgreSQL is used to store user and message data.
- **Database Management**: pgAdmin for easy database management.

---

## Troubleshooting

- **MinIO not accessible**: Ensure the MinIO container is running and check the logs for errors.
- **Socket.IO issues**: Ensure both frontend and backend are connected via WebSocket.
- **Database connection**: Double-check the database connection settings in the `.env` file.

---


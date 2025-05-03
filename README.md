# INFO3180 VueJS and Flask Starter

This template helps you get started developing with Vue 3 on the frontend and Flask as an API on the backend.

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=johnsoncodehk.volar) (and disable Vetur) + [TypeScript Vue Plugin (Volar)](https://marketplace.visualstudio.com/items?itemName=johnsoncodehk.vscode-typescript-vue-plugin).

## Flask Backend Setup

### 1. Create and Activate Virtual Environment

```bash
# Create virtual environment
python -m venv venv  # you may need to use python3 instead

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
.\venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory with the following variables:

```
SECRET_KEY=your_secret_key
DATABASE_URL=postgresql://username:password@localhost/database_name
JWT_SECRET_KEY=your_jwt_secret_key
UPLOAD_FOLDER=path/to/upload/folder
```

### 4. Database Migration

Initialize and apply database migrations:

```bash
# Initialize migrations (if not already done)
flask db init

# Generate migration
flask db migrate -m "Initial migration"

# Apply migration
flask db upgrade
```

### 5. Run Development Server

```bash
# Option 1: Using Flask CLI
flask --app app --debug run

# Option 2: Using provided script
# On macOS/Linux:
./run_api.sh
# On Fish shell:
./run_api.fish
```

### 6. Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage report
pytest --cov=app
```

### 7. Production Deployment

For production deployment, use Gunicorn as the WSGI server:

```bash
# Install Gunicorn (already in requirements.txt)
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 "app:create_app()"
```

Consider using a process manager like Supervisor or systemd to manage the Gunicorn process, and a reverse proxy like Nginx to handle client requests.

## Vue Frontend Setup

### 1. Install Node.js Dependencies

```bash
npm install
```

### 2. Compile and Hot-Reload for Development

```bash
npm run dev
```

This will start the Vite development server, typically at http://localhost:5173.

### 3. Compile and Minify for Production

```bash
npm run build
```

This will generate optimized production files in the `dist` directory.

### 4. Preview Production Build Locally

```bash
npm run preview
```

### 5. Production Deployment

To deploy the Vue application to production:

1. Build the application:
   ```bash
   npm run build
   ```

2. Deploy the contents of the `dist` directory to your web server.

3. Configure your web server (like Nginx or Apache) to serve the static files and handle SPA routing:

   Example Nginx configuration:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       root /path/to/dist;
       index index.html;
       
       location / {
           try_files $uri $uri/ /index.html;
       }
   }
   ```

4. For more advanced deployments, consider using CI/CD pipelines with platforms like Netlify, Vercel, or AWS Amplify that can automate the build and deployment process.

## Full-Stack Development Workflow

1. Run the Flask backend API server
2. In a separate terminal, run the Vue frontend development server
3. Make changes to your code and see them reflected in real-time

Happy coding!

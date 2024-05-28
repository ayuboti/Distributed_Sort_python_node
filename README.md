echo "# Distributed Sorting Application

## Overview
This application sorts numbers in a distributed fashion using Flask for the backend.

## Setup
Clone the repository and navigate into the project directory. Run the following commands:

\`\`\`bash
pip install -r requirements.txt
flask run
\`\`\`

## Usage
Navigate to 'http://localhost:5000' in your web browser to use the application.

## Docker
To build and run the application using Docker, execute:

\`\`\`bash
docker build -t sorting-app .
docker run -p 5000:5000 sorting-app
\`\`\`

Access the application at 'http://localhost:5000'." > README.md

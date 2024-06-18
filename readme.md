## Use this script to create the DynamoDB table locally:

    docker-compose up

    export AWS_ACCESS_KEY_ID=abc && export AWS_SECRET_ACCESS_KEY=abc && export AWS_DEFAULT_REGION=eu-west-1 && export TABLE_NAME="local-tasks-api-table" && export DYNAMODB_URL=http://localhost:9999

    poetry run python create_dynamodb_locally.py

    poetry run uvicorn main:app --reload


Post:

    curl --location --request POST 'http://localhost:8000/api/brands' \
    --header 'Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb2duaXRvOnVzZXJuYW1lIjoiam9obkBkb2UuY29tIn0.6UvNP3lIrXAinXYqH4WzyNrYCxUFIRhAluWyAxcCoUc' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "name": "Useless"
    }'

Get:

    curl --location --request GET 'http://localhost:8000/api/brands' \
    --header 'Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb2duaXRvOnVzZXJuYW1lIjoiam9obkBkb2UuY29tIn0.6UvNP3lIrXAinXYqH4WzyNrYCxUFIRhAluWyAxcCoUc'
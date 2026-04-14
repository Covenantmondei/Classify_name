# Classify Name

A Django REST API that classifies names by gender using the Genderize.io API. This application provides an endpoint to determine the likely gender of a person based on their name, with confidence scoring and result caching for optimal performance.

## Features

- **Gender Classification**: Classify names by gender using the Genderize.io API
- **Confidence Scoring**: Returns confidence metrics including probability and sample size
- **Smart Caching**: Caches results to reduce API calls and improve response times
- **RESTful API**: Built with Django REST Framework for easy integration
- **Error Handling**: Comprehensive error handling with appropriate HTTP status codes
- **CORS Support**: Enabled for cross-origin requests from any domain
- **Input Validation**: Validates input to ensure proper query parameters

## Tech Stack

- **Framework**: Django 6.0.4
- **API Framework**: Django REST Framework
- **HTTP Client**: HTTPX
- **Caching**: Django Cache Framework
- **CORS**: Django CORS Headers
- **Database**: SQLite3
- **Python Version**: 3.x

## Project Structure

```
.
├── classify/              # Main Django project configuration
│   ├── settings.py       # Django settings and configuration
│   ├── urls.py          # Main URL routing
│   ├── asgi.py          # ASGI configuration
│   ├── wsgi.py          # WSGI configuration
│   └── __init__.py
├── classifyname/          # Main application
│   ├── views.py         # API views (Query endpoint)
│   ├── urls.py          # Application URL routing
│   ├── models.py        # Database models
│   ├── admin.py         # Django admin configuration
│   ├── apps.py          # App configuration
│   ├── tests.py         # Unit tests
│   └── migrations/      # Database migrations
├── manage.py            # Django management script
├── db.sqlite3           # SQLite database
└── README.md           # This file
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Classify
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Start the development server:
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/`

## API Endpoints

### Classify Name

**Endpoint**: `GET /api/classify`

**Query Parameters**:
- `name` (required): The name to classify (must be a string, not a number)

**Request Example**:
```
GET /api/classify?name=John
```

**Success Response (200 OK)**:
```json
{
  "status": "success",
  "result": {
    "name": "John",
    "gender": "male",
    "probability": 0.98,
    "sample_size": 1250,
    "is_confident": true,
    "processed_at": "2026-04-14T10:30:45+00:00"
  }
}
```

**Error Response - Missing Parameter (400 Bad Request)**:
```json
{
  "status": "error",
  "message": "Name parameter is required."
}
```

**Error Response - Invalid Input (422 Unprocessable Entity)**:
```json
{
  "status": "error",
  "message": "Name parameter must be a string."
}
```

**Error Response - API Failure (500 Internal Server Error)**:
```json
{
  "status": "error",
  "message": "Failed to classify the name."
}
```

## Response Fields

- **name**: The name that was classified
- **gender**: The predicted gender ("male" or "female")
- **probability**: Confidence score between 0 and 1 indicating the likelihood of the prediction
- **sample_size**: Number of samples used in the Genderize.io database for this name
- **is_confident**: Boolean flag indicating high confidence (probability >= 0.7 and sample_size >= 100)
- **processed_at**: ISO 8601 timestamp when the API processed the request

## Caching

Results are cached automatically using Django's cache framework. Cache keys are formatted as `classifyname:{name.lower()}` to ensure consistent caching regardless of input case. Cached results are returned for the same name within the cache TTL, reducing external API calls.

## Configuration

Key settings in `classify/settings.py`:
- **DEBUG**: Set to `False` in production
- **SECRET_KEY**: Change this to a secure random value in production
- **ALLOWED_HOSTS**: Configure with your domain names in production
- **CORS_ALLOW_ALL_ORIGINS**: Set to `False` and configure specific origins in production

## Development

### Running Tests

```bash
python manage.py test
```

### Django Admin

Access the Django admin panel at `http://localhost:8000/admin/` with superuser credentials.

### Creating a Superuser

```bash
python manage.py createsuperuser
```

## Deployment Considerations

Before deploying to production:

1. Set `DEBUG = False` in settings.py
2. Generate a new `SECRET_KEY` and keep it secure
3. Configure `ALLOWED_HOSTS` with your domain names
4. Set up a production-grade database (PostgreSQL recommended)
5. Configure appropriate caching backend (Redis recommended instead of default cache)
6. Review and restrict `CORS_ALLOW_ALL_ORIGINS` to specific trusted origins
7. Set up HTTPS/SSL certificates
8. Use environment variables for sensitive configuration
9. Configure proper logging and monitoring
10. Set up a production WSGI server (Gunicorn, uWSGI, etc.)

## Dependencies

Key Python packages required (see requirements.txt for full list):
- django >= 6.0.4
- djangorestframework
- django-cors-headers
- httpx

## API Rate Limiting

Note: Genderize.io has rate limits on their free tier. Monitor your API usage to stay within limits. Consider implementing rate limiting on your Django application if needed.

## Troubleshooting

**Issue**: "Name parameter is required" error
- Solution: Ensure you're passing the `name` query parameter in your request

**Issue**: "Name parameter must be a string" error
- Solution: The name parameter cannot be purely numeric. Use a string value instead

**Issue**: "Failed to classify the name" error
- Solution: Check your internet connection and ensure Genderize.io API is accessible

**Issue**: Slow responses
- Solution: Check if caching is properly configured. Cached responses should be much faster

## License

This project is provided as-is for educational and development purposes.

## Contributing

To contribute improvements or report issues:

1. Create a feature branch (`git checkout -b feature/AmazingFeature`)
2. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
3. Push to the branch (`git push origin feature/AmazingFeature`)
4. Open a pull request

## Support

For questions or issues, please reach out through the project repository or contact the maintainers.

# Weather Forecast API

This project provides a FastAPI-based web service to fetch and visualize weather data based on latitude and longitude coordinates.

## Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/rbshah29/get-temp-backend.git
    cd get-temp-backend
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Running the Application

1. Start the FastAPI server:
    ```sh
    uvicorn main:app --host 0.0.0.0 --port 8000
    ```

2. The server will be running at `http://localhost:8000`.

## API Endpoints

### Home

- **URL:** `/`
- **Method:** `GET`
- **Description:** Returns a welcome message.

### Get Weather

- **URL:** `/weather`
- **Method:** `POST`
- **Description:** Fetches and visualizes hourly temperature data for the given latitude and longitude.
- **Request Body:**
    ```json
    {
        "latitude": <latitude_value>,
        "longitude": <longitude_value>
    }
    ```
- **Response:** Returns a plot image file showing the hourly temperature over time.

### API Documentation

- Visit `http://localhost:8000/docs` to access the interactive API documentation and test the available endpoints directly from your browser.
- Alternatively, you can use Postman to test the API endpoints by sending requests to `http://localhost:8000`.


## Example Request

```sh
curl -X POST "http://localhost:8000/weather" -H "Content-Type: application/json" -d '{"latitude": 40.7128, "longitude": -74.0060}'
```

## Dependencies

- FastAPI
- Pydantic
- Requests
- Requests-Cache
- Pandas
- Matplotlib
- Uvicorn
- OpenMeteo-Requests
- Retry-Requests

## License

This project is licensed under the MIT License.

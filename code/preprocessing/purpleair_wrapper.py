"""
PurpleAir API Wrapper Class

Provides a Python interface for interacting with the PurpleAir API.

It includes:
- Initialization with API key handling.
- Methods to fetch latest sensor data by index.
- Retrieval of historical PM2.5 data for multiple sensors.
- Support for bounding box queries or filtering by sensor indices.
- Formatting of API responses into pandas DataFrames.

Designed for clean integration of PurpleAir data into air quality pipelines and analyses.
"""

import requests
import pandas as pd
import os
import time
from typing import Optional, List, Any

class PurpleAirAPI:
    def __init__(self, api_key: Optional[str] = None) -> None:
        """
        Initialize the PurpleAirAPI class.

        Parameters:
        api_key (Optional[str]): The API key for accessing the PurpleAir API. If None, the API will look for the key in the
        environment variable 'PURPLE_AIR_API_KEY'.
        """
        self.api_key: str = api_key or os.getenv('PURPLE_AIR_API_KEY')
        
        # Check if the API key is provided
        if not self.api_key:
            raise ValueError("API key is required. Please provide it as an argument or set the 'PURPLE_AIR_API_KEY' " \
                             "environment variable.")

        self.base_url: str = 'https://api.purpleair.com/v1/'
        self.headers: Dict[str, str] = {
            'X-API-Key': self.api_key
        }

    def get_latest_data(self, sensor_index: int, fields: Optional[List[str]] = None) -> Any:
        """
        Get the latest data for a sensor index.

        Parameters:
        sensor_index (int): A sensor index to fetch data for.
        fields (Optional[List[str]]): A list of fields to include in the response. If None, defaults to a predefined set of fields.

        Returns:
        Any: The latest data for the specified sensors.
        """
        url = f"{self.base_url}sensors/:"

        # Check if the fields are provided
        # If not, set default fields
        params = {
            'fields': ','.join(fields) if fields else 'sensor_index,pm2.5',
        }

        if not isinstance(sensor_index, int):
            raise ValueError(f"Sensor index must be a integer. Got {type(sensor_index)} instead.")
        
        url = url + str(sensor_index)
        response = requests.get(url, headers=self.headers, params=params)
        
        # Check if the response is successful
        if response.status_code == 200:
            sensor_data = response.json()

            # Check if the response contains the expected data
            if 'data' in sensor_data:
                df = pd.DataFrame(sensor_data['data'], columns=sensor_data.get('fields', []))
                df['sensor_index'] = sensor_index  # Add sensor index to the DataFrame
            else:
                raise Exception(f"Unexpected response format: {sensor_data}")
        else:
            raise Exception(f"Error fetching data: {response.status_code} - {response.text}")

        # Combine all data frames into one
        if df is not None:
            return df
        else:
            return pd.DataFrame()  # Return an empty DataFrame if no data is fetched
        
    def get_sensor_history(self, sensor_indices: List[int], fields: List[str], start_time: Optional[str] = None, 
                           end_time: Optional[str] = None, average: Optional[int] = None) -> Any:
        """
        Get the historical data for a list of sensor indices.

        Parameters:
        sensor_indices (List[str]): A list of sensor indices to fetch data for.
        start_time (Optional[str]): The start time for the data retrieval in ISO 8601 format. If None, defaults to the last 24 hours.
        end_time (Optional[str]): The end time for the data retrieval in ISO 8601 format. If None, defaults to now.
        fields (Optional[List[str]]): A list of fields to include in the response. If None, defaults to a predefined set of fields.
        average (Optional[int]): The desired average in minutes. One of the following:
            0 (real-time), 10 (default if not specified), 30, 60, 360 (6 hour), 1440 (1 day), 
            10080 (1 week), 43200 (1 month), 525600 (1 year).
            The amount of data that can be returned in a single response depends on the average used. 
            Time limits for each average are found in our looping API calls community article.

        Returns:
        Any: The historical data for the specified sensors.
        """
        # Convert start_time and end_time to UNIX timestamps if provided
        if start_time:
            start_timestamp = pd.to_datetime(start_time).timestamp()
        else:
            start_timestamp = pd.Timestamp.now() - pd.Timedelta(days=1)
            start_timestamp = start_timestamp.timestamp()

        if end_time:
            end_timestamp = pd.to_datetime(end_time).timestamp()
        else:
            end_timestamp = pd.Timestamp.now().timestamp()

        if average is None:
            average = 10

        # Check if the average is valid
        if average not in [0, 10, 30, 60, 360, 1440, 10080, 43200, 525600]:
            raise ValueError("Invalid average value. Must be one of the following: "
                             "0 (real-time), 10 (default), 30, 60, 360 (6 hour), "
                             "1440 (1 day), 10080 (1 week), 43200 (1 month), "
                             "525600 (1 year).")

        # Check if the fields are provided
        # If not, set default fields
        params = {
            'fields': ','.join(fields),
            'start_timestamp': start_timestamp,
            'end_timestamp': end_timestamp,
            'average': average,
        }
        
        data_frames = []

        for sensor_index in sensor_indices:
            if not isinstance(sensor_index, int):
                raise ValueError(f"Sensor index must be an integer. Got {type(sensor_index)} instead.")
            
            # Replace the placeholder with the actual sensor index
            sensor_url = f"{self.base_url}sensors/{sensor_index}/history"
            response = requests.get(sensor_url, headers=self.headers, params=params)
            
            # Check if the response is successful
            if response.status_code == 200:
                sensor_data = response.json()

                # Check if the response contains the expected data
                if 'data' in sensor_data:
                    df = pd.DataFrame(sensor_data['data'], columns=sensor_data.get('fields', []))
                    df['sensor_index'] = sensor_index  # Add sensor index to the DataFrame
                    data_frames.append(df)
                else:
                    raise Exception(f"Unexpected response format: {sensor_data}")
            else:
                raise Exception(f"Error fetching data: {response.status_code} - {response.text}")
            
            # Add a delay to avoid hitting the API rate limit
            time.sleep(5)  # Adjust the sleep time as needed

        # Combine all data frames into one
        if data_frames:
            return pd.concat(data_frames, ignore_index=True)
        else:
            return pd.DataFrame()
        

    def get_sensors_data(self, fields: List[str], sensor_indices: Optional[List[int]] = None, 
                         nw_lat: Optional[int] = None, nw_lng: Optional[int] = None, 
                         se_lat: Optional[int] = None, se_lng: Optional[int] = None) -> Any:
        """
        Get the data for all sensors within a bounding box.

        Parameters:
        fields (List[str]): A list of fields to include in the response.
        sensor_indices (Optional[List[int]]): A list of sensor indices to fetch data for. If None, fetches data for all sensors.
        nw_lat (Optional[int]): The latitude of the northwest corner of the bounding box.
        nw_lng (Optional[int]): The longitude of the northwest corner of the bounding box.
        se_lat (Optional[int]): The latitude of the southeast corner of the bounding box.
        se_lng (Optional[int]): The longitude of the southeast corner of the bounding box.

        Returns:
        Any: The data for all sensors within the specified bounding box.
        """
        url = f"{self.base_url}sensors"

        # Check if the fields are provided
        # If not, set default fields
        params = {
            'fields': ','.join(fields),
        }

        # Check if the sensor indices are provided
        if sensor_indices:
            if not isinstance(sensor_indices, list):
                raise ValueError(f"Sensor indices must be a list. Got {type(sensor_indices)} instead.")
            sensor_indices = ','.join(sensor_indices)
            params['show_only'] = sensor_indices

        # Check if the bounding box coordinates are provided
        if nw_lat and nw_lng and se_lat and se_lng:
            params['nwlat'] = nw_lat
            params['nwlng'] = nw_lng
            params['selat'] = se_lat
            params['selng'] = se_lng

        response = requests.get(url, headers=self.headers, params=params)
        
        # Check if the response is successful
        if response.status_code == 200:
            sensor_data = response.json()

            # Check if the response contains the expected data
            if 'data' in sensor_data:
                df = pd.DataFrame(sensor_data['data'], columns=sensor_data.get('fields', []))
            else:
                raise Exception(f"Unexpected response format: {sensor_data}")
        else:
            raise Exception(f"Error fetching data: {response.status_code} - {response.text}")

        # Combine all data frames into one
        if df is not None:
            return df
        else:
            return pd.DataFrame()
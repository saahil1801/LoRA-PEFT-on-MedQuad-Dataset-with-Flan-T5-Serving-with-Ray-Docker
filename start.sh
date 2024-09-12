#!/bin/sh
python3.10 api_serve.py &  # Start the Ray Serve API script
sleep 10  # Give Ray Serve some time to initialize
serve run api_serve:biomedical &  # Start Ray Serve deployment
sleep 10  # Wait until Ray Serve deployment is up
streamlit run app.py  # Start Streamlit application

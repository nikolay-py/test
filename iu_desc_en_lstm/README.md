# Image Description EN LSTM-model

## Initial setup

### Environment variables file
1. Create an .env file in /iu_ml_models/iu_tags_en_nfnet directory
```
cd iu_desc_en_lstm
touch .env
```
2. Copy example variables from below code, change `HOST_IMAGE_DIR` var
```  
cat <<EOT > .env
# routing
HOST_IMAGE_DIR='path to shared files on host system' # CHANGE_ME
CONTAINER_IMAGE_DIR=/shared_files
# pytest
PYTEST_HOST_PORT=http://localhost:16002
# set device to 'cpu' for dev machines, 'cuda' for prod
MODEL_DEVICE=cuda
GUNICORN_TIMEOUT=15
PRETRAINED_FASTERRCNN_VERSION=2021-11-28
PREDTRAINED_FILENAME=resnet152-394f9c45.pth
PREDTRAINED_FILE_DOWNLOAD_URL=https://download.pytorch.org/models/resnet152-394f9c45.pth

WEIGHTS_VERSION=2021-11-28
ENCODER_WEIGHTS_FILENAME=encoder.pkl
DECODER_WEIGHTS_FILENAME=decoder.pkl
ENCODER_WEIGHTS_DOWNLOAD_URL=https://github.com/MindSetLib/iu_models_mirror/releases/download/v1.0/encoder.pkl
DECODER_WEIGHTS_DOWNLOAD_URL=https://github.com/MindSetLib/iu_models_mirror/releases/download/v1.0/decoder.pkl
APP_PORT=16002
EOT
```

### Download weights file for lstm-model
1. For download a new weights file you need to set new nfnet-model parameters in .env.
2. Run in terminal for beginning download:
```
bash download_decoder_weights.sh
bash download_encoder_weights.sh
bash download_predtrained_file.sh
```

## Run application with Docker
Enable Docker BuildKit using
```
export DOCKER_BUILDKIT=1 && export COMPOSE_DOCKER_CLI_BUILD=1
```

Development version:
```
docker-compose up --build
```
Production version
```
docker-compose -f docker-compose.prod.yml up --build -d
```

Verify server is up:
```
curl --location --request GET 'http://localhost:36002/health'
```
Verify model is running:
```
curl --location --request POST 'http://localhost:36002/api/image_desc_en' \
   --header 'Content-Type: application/json' \
   --data-raw '{
       "path": "images/demo/2021-12-01/72fcb356-5282-11ec-8689-0242ac1b0006.jpg"
   }'
```
Measure execution time:
```
time curl --location --request POST 'http://localhost:36002/api/image_desc_en' \
   --header 'Content-Type: application/json' \
   --data-raw '{
       "path": "images/demo/2021-12-01/72fcb356-5282-11ec-8689-0242ac1b0006.jpg"
   }'
```
## Run application locally

### Create Python virtual environment
```
python3.9 -m venv env
source env/bin/activate
```

### Set up local shared_files directory
Set `CONTAINER_IMAGE_DIR` in `.env` file to `'shared_files'`. And create folder:
```
mkdir shared_files
```

### Install python packages and start Flask app
Create virtual environment, install dependencies and start Flask server using:
```
pip install -r requirements/development.txt
export APP_SETTINGS=init_config.DevelopmentConfig
python run_app.py
```


## How run Pytest
- Create Python virtual environment (see section "Run application locally")
- Create virtual environment, install dependencies and start Flask server using:
```
pip install -r requirements/development.txt
export APP_SETTINGS=init_config.DevelopmentConfig
```
- Go to directory test_api
```
cd test_api
```
- Run pytest with a valid host and port
```
PYTEST_HOST_PORT=http://localhost:16002 pytest
```
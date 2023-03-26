import argparse
import os
from PIL import Image
import requests
from tqdm import tqdm

def resize_image(image, size):
    """Resize an image to the given size."""
    return image.resize(size, Image.ANTIALIAS)


def download_weights(url, path_to_put):
    # Streaming, so we can iterate over the response.
    response = requests.get(url, stream=True)

    if response.ok:
        total_size_in_bytes = int(response.headers.get('content-length', 0))
        block_size = 1024
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)

        if not os.path.exists('weights'):
            os.makedirs('weights')

        with open(path_to_put, 'wb') as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)
        progress_bar.close()

        if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
            if os.path.exists('weights'):
                shutil.rmtree('weights')
            raise FileNotDownloaded('Failed to download file.')
    else:
        raise FileNotDownloaded(f'Failed to download file. Server response: {response.status_code}')
        

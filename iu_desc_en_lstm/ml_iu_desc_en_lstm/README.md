Building simple image captioning model using CNN (resnet151) and RNN (LSTM).

-----
Check the configuration files. ```config.py```. the attributes in the config class are used as default values to the following python files.


# Dataset
To download the dataset you have to run the bash file:
```bash
    ./download.sh
```

Output:
 - **data/train2014** folder with training images.
 - **data/val2014** folder with validation images.
 - **data/annotations** with json files containing the captions for the validation and the training images.


------
# Building Vocabulary

Parameters:
- caption_path: path for train annotation file
- vocab_path: path for saving vocabulary wrapper
- threshold: minimum word count threshold
   
   
``` 
  python build_vocab.py 
```
Output:
   - On the console we will see some information about the process of the building our vocab wrapper.
   - the vocabularity wrapper will be saved in tokenizer/vocab.pkl
    
---------
# Traingin

Parameters:
- model_path: path for saving trained models
- crop_size: size for randomly cropping images
- vocab_path: path for vocabulary wrapper
- log_step: step size for prining log info
- device: device to run the model on
- embed_size: dimension of word embedding vectors
- hidden_size: dimension of lstm hidden states
- num_layers: number of layers in lstm
- num_epochs
- batch_size
- learning_rate


``` 
  python train.py
```

Output:
   - On the console we will see some information about the process of the training like the loss and perplexity values.
   - The trained Encoder and Decoder will be saved in weights/encoder.pkl and weights/decoder.pkl respectivly.
    
----------
# Inferencing

Parameters:
- path2img: input image for generating caption
- device: device to run the model on

``` 
   python python inference.py --image=path/to/image
```

Output:
    - The captions string of the image.
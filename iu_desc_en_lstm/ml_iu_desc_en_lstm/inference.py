import torch
import numpy as np 
import argparse
import pickle 
import os
from torchvision import transforms 
from ml_iu_desc_en_lstm.build_vocab import Vocabulary
from ml_iu_desc_en_lstm.model import EncoderCNN, DecoderRNN
from PIL import Image
from ml_iu_desc_en_lstm.utils import *
from ml_iu_desc_en_lstm.config import Config


def load_image(image_path, transform=None):
    image = Image.open(image_path).convert('RGB')
    image = image.resize([224, 224], Image.LANCZOS)
    if transform is not None:
        image = transform(image).unsqueeze(0)
    
    return image


def main(args):
    cfg= Config()
    # Device configuration
    device = torch.device(args.device)
            
    embed_size= cfg.embed_size
    hidden_size= cfg.hidden_size
    num_layers= cfg.num_layers
    
    encoder_path = cfg.encoder_path
    decoder_path = cfg.decoder_path
    vocab_path= cfg.vocab_path
        
    # Image preprocessing
    transform = transforms.Compose([
        transforms.ToTensor(), 
        transforms.Normalize((0.485, 0.456, 0.406), 
                             (0.229, 0.224, 0.225))])
    
    # Load vocabulary wrapper
    with open(vocab_path, 'rb') as f:
        vocab = pickle.load(f)

    # Build models
    encoder = EncoderCNN(embed_size).eval()  # eval mode (batchnorm uses moving mean/variance)
    decoder = DecoderRNN(embed_size, hidden_size, len(vocab), num_layers)
    encoder = encoder.to(device)
    decoder = decoder.to(device)

    # Load the trained model parameters
    encoder.load_state_dict(torch.load(encoder_path))
    decoder.load_state_dict(torch.load(decoder_path))

    # Prepare an image
    image = load_image(args.image, transform)
    image_tensor = image.to(device)
    
    # Generate an caption from the image
    feature = encoder(image_tensor)
    sampled_ids = decoder.sample(feature)
    sampled_ids = sampled_ids[0].cpu().numpy() # (1, max_seq_length) -> (max_seq_length)
    
    # Convert word_ids to words
    sampled_caption = []
    for word_id in sampled_ids:
        word = vocab.idx2word[word_id]
        sampled_caption.append(word)
        if word == '<end>':
            break
    sentence = ' '.join(sampled_caption[1:-1])
    
    # Print out the image and the generated caption
    print (sentence)


if __name__ == '__main__':
    cfg= Config()
    parser = argparse.ArgumentParser()
    parser.add_argument('--path2img', type=str, required=True, help='input image for generating caption')
    parser.add_argument('--device', type=str, default=cfg.device, help='device to run the model on')
    args = parser.parse_args()
    main(args)

import os
import pickle

import torch
from init_config import Config
from torchvision import transforms
from ml_iu_desc_en_lstm.build_vocab import Vocabulary
from ml_iu_desc_en_lstm.inference import load_image
from ml_iu_desc_en_lstm.model import EncoderCNN, DecoderRNN
from ml_iu_desc_en_lstm.utils import download_weights


def init_model():
    device = torch.device(Config.MODEL_DEVICE)

    embed_size = Config.EMBED_SIZE
    hidden_size = Config.HIDDEN_SIZE
    num_layers = Config.NUM_LAYERS

    encoder_path = Config.ENCODER_WEIGHTS_FILE_PATH
    decoder_path = Config.DECODER_WEIGHTS_FILE_PATH
    vocab_path = Config.VOCAB_PATH

    # if not os.path.exists(encoder_path):
    #     download_weights(str(os.environ.get('ENCODER_WEIGHTS_DOWNLOAD_URL')),
    #                      encoder_path)

    # if not os.path.exists(decoder_path):
    #     download_weights(str(os.environ.get('DECODER_WEIGHTS_DOUNLOAD_URL')),
    #                      decoder_path)

    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.485, 0.456, 0.406),
                             (0.229, 0.224, 0.225))])

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

    return transform, device, encoder, decoder, vocab


def get_description(device, transform, encoder, decoder, vocab, image_path):
    args = {'image': image_path, 'device': device}

    image = load_image(args['image'], transform)
    image_tensor = image.to(device)

    feature = encoder(image_tensor)
    sampled_ids = decoder.sample(feature)
    sampled_ids = sampled_ids[0].cpu().numpy()

    sampled_caption = []
    for word_id in sampled_ids:
        word = vocab.idx2word[word_id]
        sampled_caption.append(word)
        if word == '<end>':
            break
    sentence = ' '.join(sampled_caption[1:-1])

    return {
        "desc_model_ver": Config.WEIGHTS_VERSION,
        "description": sentence
    }

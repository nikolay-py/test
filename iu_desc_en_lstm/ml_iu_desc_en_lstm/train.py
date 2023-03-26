import argparse
import torch
import torch.nn as nn
import numpy as np
import os
import pickle
from build_vocab import Vocabulary
from model import EncoderCNN, DecoderRNN
from torch.nn.utils.rnn import pack_padded_sequence
from torchvision import transforms
from data import * 
from config import Config


def main(args):
    # Device configuration
    device = torch.device(args.device)

    # Create model directory
    if not os.path.exists(args.model_path):
        os.makedirs(args.model_path)
    
    # Image preprocessing, normalization for the pretrained resnet
    transform = transforms.Compose([ 
        transforms.RandomCrop(args.crop_size),
        transforms.RandomHorizontalFlip(), 
        transforms.ToTensor(), 
        transforms.Normalize((0.485, 0.456, 0.406), 
                             (0.229, 0.224, 0.225))])
    
    # Load vocabulary wrapper
    with open(args.vocab_path, 'rb') as f:
        vocab = pickle.load(f)
    
    # Build data loader
    train_loader = get_loader('data/train2014', 'data/annotations/captions_train2014.json', vocab, transform, args.batch_size, shuffle=True, num_workers=0) 
    val_loader = get_loader('data/val2014', 'data/annotations/captions_val2014.json', vocab, transform, args.batch_size, shuffle=True, num_workers=0)
    
    # Build the models
    encoder = EncoderCNN(args.embed_size).to(device)
    decoder = DecoderRNN(args.embed_size, args.hidden_size, len(vocab), args.num_layers).to(device)
    
    # Loss and optimizer
    criterion = nn.CrossEntropyLoss()
    params = list(decoder.parameters()) + list(encoder.linear.parameters()) + list(encoder.bn.parameters())
    optimizer = torch.optim.Adam(params, lr=args.learning_rate)
    
    # Train the models
    best_val_loss = 100000
    for epoch in range(args.num_epochs):
        total_step = len(train_loader)
        for i, (images, captions, lengths) in enumerate(train_loader):
               
            # Set mini-batch dataset
            images = images.to(device)
            captions = captions.to(device)
            targets = pack_padded_sequence(captions, lengths, batch_first=True)[0]
            
            # Forward, backward and optimize
            features = encoder(images)
            outputs = decoder(features, captions, lengths)
            loss = criterion(outputs, targets)
            decoder.zero_grad()
            encoder.zero_grad()
            loss.backward()
            optimizer.step()

            # Print log info
            if i % args.log_step == 0:
                print('Train Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}, Perplexity: {:5.4f}'
                      .format(epoch, args.num_epochs, i, total_step, loss.item(), np.exp(loss.item()))) 
            
        with torch.no_grad():
            total_step = len(val_loader)
            val_loss = 0
            for i, (images, captions, lengths) in enumerate(val_loader):
               
                # Set mini-batch dataset
                images = images.to(device)
                captions = captions.to(device)
                targets = pack_padded_sequence(captions, lengths, batch_first=True)[0]

                # Forward, backward and optimize
                features = encoder(images)
                outputs = decoder(features, captions, lengths)
                loss = criterion(outputs, targets)
                val_loss += loss.item()
                # Print log info
                if i % args.log_step == 0:
                    print('Val Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}, Perplexity: {:5.4f}'
                          .format(epoch, args.num_epochs, i, total_step, loss.item(), np.exp(loss.item()))) 
            val_loss /= total_step
            
            # Save the model checkpoints
            if val_loss < best_val_loss:
                torch.save(decoder.state_dict(), os.path.join(args.model_path, 'decoder.pkl'))
                torch.save(encoder.state_dict(), os.path.join(args.model_path, 'encoder.pkl'))
                best_val_loss = val_loss

                
if __name__ == '__main__':
    cfg= Config()
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_path', type=str, default=cfg.model_path , help='path for saving trained models')
    parser.add_argument('--crop_size', type=int, default=cfg.crop_size , help='size for randomly cropping images')
    parser.add_argument('--vocab_path', type=str, default=cfg.vocab_path, help='path for vocabulary wrapper')
    parser.add_argument('--log_step', type=int , default=cfg.log_step, help='step size for prining log info')
    parser.add_argument('--device', type=str, default=cfg.device, help='device to run the model on')
    
    # Model parameters
    parser.add_argument('--embed_size', type=int , default=cfg.embed_size, help='dimension of word embedding vectors')
    parser.add_argument('--hidden_size', type=int , default=cfg.hidden_size, help='dimension of lstm hidden states')
    parser.add_argument('--num_layers', type=int , default=cfg.num_layers, help='number of layers in lstm')
    
    # Training parameters
    parser.add_argument('--num_epochs', type=int, default=cfg.num_epochs)
    parser.add_argument('--batch_size', type=int, default=cfg.batch_size)
    parser.add_argument('--learning_rate', type=float, default=cfg.learning_rate)
    args = parser.parse_args()
    main(args)
class Config(object):
    def __init__(self):

        # Training parameters
        self.learning_rate = 0.001
        self.batch_size = 128
        self.num_epochs= 5

        # Model parameters
        self.num_layers = 1
        self.hidden_size = 512
        self.embed_size = 256
        

        # Backbone
        self.device = 'cpu'
        self.log_step = 10
        self.encoder_path = 'weights/encoder.pkl'
        self.decoder_path = 'weights/decoder.pkl'
        self.vocab_path = 'tokenizer/vocab.pkl'
        
        # Basic
        self.crop_size = 224
        self.model_path = 'weights/'
        
        self.caption_path='data/annotations/captions_train2014.json'
        self.threshold= 4

        
import numpy as np
import tensorflow as tf

class PositionalEncoding(tf.keras.layers.Layer):
    def __init__(self, pos, d_model):
        super(PositionalEncoding, self).__init__()
        self.positional_encoding = self.get_positional_encoding(pos, d_model)

    def get_angles(self, pos, i, d_model):
        angle_rates = 1 / np.power(10000, (2 * (i//2)) / np.float32(d_model))
        return pos * angle_rates

    def get_positional_encoding(self, pos, d_model):
        pos = np.arange(pos)[:, np.newaxis]
        i = np.arange(d_model)[np.newaxis, :]

        angle_rads = self.get_angles(pos, i, d_model)
        angle_rads[:, 0::2] = np.sin(angle_rads[:, 0::2])
        angle_rads[:, 1::2] = np.cos(angle_rads[:, 1::2])

        positional_encoding = angle_rads[np.newaxis, ...]
        positional_encoding = tf.cast(positional_encoding, dtype=tf.float32)
        return positional_encoding

    def call(self, embedding):
        output = embedding + self.positional_encoding[:, :tf.shape(embedding)[1], :]
        return output


def scaled_dot_product_attention(query, key, value, mask):
    dot_product_attention = tf.matmul(query, key, transpose_b=True)
    d_k = tf.cast(tf.shape(key)[-1], tf.float32)
    
    attention_score = dot_product_attention / tf.math.sqrt(d_k)

    if mask is not None:
        attention_score += (mask * -1e9)
    
    attention_distribution = tf.nn.softmax(attention_score, axis=-1)

    attention_value = tf.matmul(attention_distribution, value)
    return attention_value, attention_distribution


class MultiHeadAttention(tf.keras.layers.Layer):
    def __init__(self, d_model, num_heads, name='multi_head_attention'):
        super(MultiHeadAttention, self).__init__(name=name)
        self.d_model = d_model
        self.num_heads = num_heads
        assert d_model % self.num_heads == 0
        self.d_v = d_model // num_heads

        self.query_weight = tf.keras.layers.Dense(units=d_model)
        self.key_weight = tf.keras.layers.Dense(units=d_model)
        self.value_weight = tf.keras.layers.Dense(units=d_model)
        self.multihead_attetion_weight = tf.keras.layers.Dense(units=d_model)

    def split_heads(self, input, batch_size):
        input = tf.reshape(input, shape=(batch_size, -1, self.num_heads, self.d_v))
        input = tf.transpose(input, perm=[0, 2, 1, 3])
        return input

    def call(self, input):
        query, key, value, mask = input['query'], input['key'], input['value'], input['mask']
        batch_size = tf.shape(query)[0]

        query = self.query_weight(query)
        key = self.key_weight(key)
        value = self.value_weight(value)

        query = self.split_heads(query, batch_size)
        key = self.split_heads(key, batch_size)
        value = self.split_heads(value, batch_size)

        attention, _ = scaled_dot_product_attention(query, key, value, mask)
        attention = tf.transpose(attention, perm=[0, 2, 1, 3])

        concatenated_attention = tf.reshape(attention, (batch_size, -1, self.d_model))
        multihead_attention = self.multihead_attetion_weight(concatenated_attention)
        
        return multihead_attention


def create_padding_mask(x):
    mask = tf.cast(tf.math.equal(x, 0), tf.float32)
    mask = mask[:, tf.newaxis, tf.newaxis, :]
    return mask


def encoder_layer(d_model, num_heads, d_ff, dropout, name='encoder_layer'):
    input = tf.keras.Input(shape=(None, d_model), name='input')
    padding_mask = tf.keras.Input(shape=(1, 1, None), name='padding_mask')
    input_data = {'query': input, 'key': input, 'value': input, 'mask': padding_mask}

    self_attention = MultiHeadAttention(d_model, num_heads, name='self_attention')(input_data)
    self_attention = tf.keras.layers.Dropout(rate=dropout)(self_attention)
    self_attention = tf.keras.layers.LayerNormalization(epsilon=1e-6)(input + self_attention)

    output = tf.keras.layers.Dense(units=d_ff, activation='relu')(self_attention)
    output = tf.keras.layers.Dense(units=d_model)(output)
    output = tf.keras.layers.Dropout(rate=dropout)(output)
    output = tf.keras.layers.LayerNormalization(epsilon=1e-6)(self_attention + output)
    
    model = tf.keras.Model(inputs=[input, padding_mask], outputs=output, name=name)
    return model


def encoder(vocab_size, num_layers, d_model, num_heads, d_ff, dropout, name='encoder'):
    input = tf.keras.Input(shape=(None,), name='input')
    padding_mask = tf.keras.Input(shape=(1, 1, None), name='padding_mask')

    embedding = tf.keras.layers.Embedding(vocab_size, d_model)(input)
    embedding *= tf.math.sqrt(tf.cast(d_model, tf.float32))

    positional_encoding = PositionalEncoding(vocab_size, d_model)(embedding)
    output = tf.keras.layers.Dropout(rate=dropout)(positional_encoding)

    for i in range(num_layers):
        output = encoder_layer(d_model=d_model, num_heads=num_heads, d_ff=d_ff, dropout=dropout, name=f'encoder_layer{i}')(inputs=[output, padding_mask])
    
    model = tf.keras.Model(inputs=[input, padding_mask], outputs=output, name=name)
    return model


def create_look_ahead_mask(x):
    seq_len = tf.shape(x)[1]
    look_ahead_mask = 1 - tf.linalg.band_part(tf.ones((seq_len, seq_len)), -1, 0)
    padding_mask = create_padding_mask(x)
    mask = tf.maximum(look_ahead_mask, padding_mask)
    return mask


def decoder_layer(d_model, num_heads, d_ff, dropout, name='decoder_layer'):
    input = tf.keras.Input(shape=(None, d_model), name='input')
    encoder_output = tf.keras.Input(shape=(None, d_model), name='encoder_output')
    look_ahead_mask = tf.keras.Input(shape=(1, None, None), name='look_ahead_mask')
    padding_mask = tf.keras.Input(shape=(1, 1, None), name='padding_mask')

    input_data1 = {'query': input, 'key': input, 'value': input, 'mask': look_ahead_mask}

    masked_self_attention = MultiHeadAttention(d_model, num_heads, name='masked_self_attention')(input_data1)
    masked_self_attention = tf.keras.layers.LayerNormalization(epsilon=1e-6)(input + masked_self_attention )

    input_data2 = {'query': masked_self_attention, 'key': encoder_output, 'value': encoder_output, 'mask': padding_mask}

    encoder_decoder_attention = MultiHeadAttention(d_model, num_heads, name='encoder_decoder_attention')(input_data2)
    encoder_decoder_attention = tf.keras.layers.Dropout(rate=dropout)(encoder_decoder_attention)
    encoder_decoder_attention = tf.keras.layers.LayerNormalization(epsilon=1e-6)(masked_self_attention + encoder_decoder_attention)

    output = tf.keras.layers.Dense(units=d_ff, activation='relu')(encoder_decoder_attention)
    output = tf.keras.layers.Dense(units=d_model)(output)
    output = tf.keras.layers.Dropout(rate=dropout)(output)
    output = tf.keras.layers.LayerNormalization(epsilon=1e-6)(encoder_decoder_attention + output)

    model = tf.keras.Model(inputs=[input, encoder_output, look_ahead_mask, padding_mask], outputs=output, name=name)
    return model


def decoder(vocab_size, num_layers, d_model, num_heads, d_ff, dropout, name='decoder'):
    input = tf.keras.Input(shape=(None,), name='input')
    encoder_output = tf.keras.Input(shape=(None, d_model), name='encoder_output')
    look_ahead_mask = tf.keras.Input(shape=(1, None, None), name='look_ahead_mask')
    padding_mask = tf.keras.Input(shape=(1, 1, None), name='padding_mask')

    embedding = tf.keras.layers.Embedding(vocab_size, d_model)(input)
    embedding *= tf.math.sqrt(tf.cast(d_model, tf.float32))
    
    positional_encoding = PositionalEncoding(vocab_size, d_model)(embedding)
    output = tf.keras.layers.Dropout(rate=dropout)(positional_encoding)

    for i in range(num_layers):
        output = decoder_layer(d_model=d_model, num_heads=num_heads, d_ff=d_ff, dropout=dropout, name=f'decoder_layer{i}')(
            inputs=[output, encoder_output, look_ahead_mask, padding_mask])
    
    model = tf.keras.Model(inputs=[input, encoder_output, look_ahead_mask, padding_mask], outputs=output, name=name)
    return model


def transformer(vocab_size, num_layers, d_model, num_heads, d_ff, dropout):
    input = tf.keras.Input(shape=(None,), name='input')
    decoder_input = tf.keras.Input(shape=(None,), name='decoder_input')

    encoder_padding_mask = tf.keras.layers.Lambda(create_padding_mask, output_shape=(1, 1, None), name='encoder_padding_mask')(input)
    look_ahead_mask = tf.keras.layers.Lambda(create_look_ahead_mask, output_shape=(1, None, None), name='look_ahead_mask')(decoder_input)
    decoder_padding_mask = tf.keras.layers.Lambda(create_padding_mask, output_shape=(1, 1, None), name='decoder_padding_mask')(input)

    encoder_output = encoder(vocab_size=vocab_size, num_layers=num_layers, d_model=d_model, num_heads=num_heads, d_ff=d_ff, dropout=dropout)(
        inputs=[input, encoder_padding_mask])
    decoder_output = decoder(vocab_size=vocab_size, num_layers=num_layers, d_model=d_model, num_heads=num_heads, d_ff=d_ff, dropout=dropout)(
        inputs=[decoder_input, encoder_output, look_ahead_mask, decoder_padding_mask])
    output = tf.keras.layers.Dense(units=vocab_size, name='output')(decoder_output)
    
    model = tf.keras.Model(inputs=[input, decoder_input], outputs=output)
    return model
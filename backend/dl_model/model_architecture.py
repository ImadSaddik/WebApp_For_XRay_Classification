import tensorflow as tf


def convolution_block(inputs, filters, kernel_size=(3, 3), strides=(1, 1), padding='same'):
    x = tf.keras.layers.BatchNormalization()(inputs)
    x = tf.keras.layers.ReLU()(x)
    x = tf.keras.layers.Conv2D(
        filters, kernel_size, strides=strides, padding=padding)(x)
    return x


def dense_block(inputs, filters, blocks):
    x = inputs
    for _ in range(blocks):
        conv1 = convolution_block(x, filters)
        conv2 = convolution_block(conv1, filters)
        x = tf.keras.layers.Concatenate()([x, conv2])
    return x


def transition_block(inputs, filters):
    x = tf.keras.layers.BatchNormalization()(inputs)
    x = tf.keras.layers.ReLU()(x)
    x = tf.keras.layers.Conv2D(
        filters, (1, 1), strides=(1, 1), padding='same')(x)
    x = tf.keras.layers.AveragePooling2D((2, 2), strides=(2, 2))(x)
    return x


def chexnet_model(input_shape=(224, 224, 3), num_classes=14):
    inputs = tf.keras.layers.Input(shape=input_shape)

    # Initial Convolutional Layer
    x = tf.keras.layers.Conv2D(
        64, (7, 7), strides=(2, 2), padding='same')(inputs)
    x = tf.keras.layers.MaxPooling2D((3, 3), strides=(2, 2), padding='same')(x)

    # Dense Blocks
    x = dense_block(x, 64, 6)
    x = transition_block(x, 64)
    x = dense_block(x, 128, 12)
    x = transition_block(x, 128)
    x = dense_block(x, 256, 24)
    x = transition_block(x, 256)
    x = dense_block(x, 512, 16)

    # Batch Normalization and ReLU Activation
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.ReLU()(x)

    # Global Average Pooling
    x = tf.keras.layers.GlobalAveragePooling2D()(x)

    # Output Layer
    outputs = tf.keras.layers.Dense(6, activation='sigmoid')(x)

    # Create model
    model = tf.keras.Model(inputs=inputs, outputs=outputs)

    return model

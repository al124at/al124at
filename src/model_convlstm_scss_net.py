from tensorflow.keras.models import Model
from tensorflow.keras.layers import (
    BatchNormalization,
    Conv2D,
    Conv2DTranspose,
    MaxPooling2D,
    Dropout,
    UpSampling2D,
    Input,
    concatenate,
    Activation,
    ConvLSTM2D,
)
import tensorflow as tf


def conv2_block(inputs, filters, batch_norm=True, name_prefix=None):
    """
    Classic 2x(Conv2D -> BN -> ReLU)
    input:  (B, H, W, C)
    output: (B, H, W, filters)
    """
    x = inputs
    for i in range(2):
        x = Conv2D(filters=filters, kernel_size=(3, 3), padding="same",
                   name=None if name_prefix is None else f"{name_prefix}_conv{i+1}")(x)
        if batch_norm:
            x = BatchNormalization(name=None if name_prefix is None else f"{name_prefix}_bn{i+1}")(x)
        x = Activation("relu", name=None if name_prefix is None else f"{name_prefix}_relu{i+1}")(x)
    return x


def deconv2_block(inputs, filters, batch_norm=True, name_prefix=None):
    """
    2x(Conv2DTranspose -> BN -> ReLU)
    input:  (B, H, W, C)
    output: (B, H, W, filters)
    """
    x = inputs
    for i in range(2):
        x = Conv2DTranspose(filters=filters, kernel_size=(3, 3), padding="same",
                            name=None if name_prefix is None else f"{name_prefix}_deconv{i+1}")(x)
        if batch_norm:
            x = BatchNormalization(name=None if name_prefix is None else f"{name_prefix}_bn{i+1}")(x)
        x = Activation("relu", name=None if name_prefix is None else f"{name_prefix}_relu{i+1}")(x)
    return x


def scss_net_convlstm(
    input_shape,              # (T, H, W, C)
    filters=32,             
    layers=4,
    batch_norm=True,
    drop_prob=0.0,
    # ConvLSTM (early fusion) settings
    convlstm_filters=None,    
    convlstm_kernel=(3, 3),
    convlstm_dropout=0.0,     
    convlstm_recurrent_dropout=0.0,
    post_convlstm_conv=True,  
):
    """
    
        Input (B,T,H,W,C)
            -> ConvLSTM2D (collapses time early) => (B,H,W,F0)
            -> CNN Encoder
            -> CNN Decoder
            -> mask for last frame

    Why this is "early fusion":
      ConvLSTM sees full-resolution frames (H,W) and accumulates temporal context
      BEFORE any strong downsampling, helping to keep small details.

    Output: (B, H, W, 1) with sigmoid.
    """
    dropout = drop_prob != 0.0
    if convlstm_filters is None:
        convlstm_filters = filters

    inputs = Input(shape=input_shape, name="input_tensor")  # (T,H,W,C)

    # --- Early temporal fusion ---
    x = ConvLSTM2D(
        filters=convlstm_filters,
        kernel_size=convlstm_kernel,
        padding="same",
        return_sequences=False,   # collapse time -> (B,H,W,F0)
        dropout=convlstm_dropout,
        recurrent_dropout=convlstm_recurrent_dropout,
        name="early_convlstm",
    )(inputs)

    if batch_norm:
        x = BatchNormalization(name="early_convlstm_bn")(x)
    x = Activation("relu", name="early_convlstm_relu")(x)

    # optional stabilization / extra capacity right after temporal fusion
    if post_convlstm_conv:
        x = conv2_block(x, filters, batch_norm=batch_norm, name_prefix="post_temporal")

    # --- Encoder (normal, no TimeDistributed) ---
    encoder_skips = []
    f = filters
    for layer_idx in range(layers):
        if dropout and layer_idx >= 2:
            x = Dropout(drop_prob, name=f"enc_dropout_{layer_idx}")(x)

        x = conv2_block(x, f, batch_norm=batch_norm, name_prefix=f"enc_{layer_idx}")
        encoder_skips.append(x)
        x = MaxPooling2D((2, 2), name=f"enc_pool_{layer_idx}")(x)
        f *= 2

    # --- Bottleneck (pure CNN) ---
    if dropout:
        x = Dropout(drop_prob, name="bottleneck_dropout")(x)

    x = conv2_block(x, f, batch_norm=batch_norm, name_prefix="bottleneck")

    # --- Decoder ---
    for ii, skip in enumerate(reversed(encoder_skips)):
        f //= 2
        if dropout and ii < 2:
            x = Dropout(drop_prob, name=f"dec_dropout_{ii}")(x)

        x = UpSampling2D((2, 2), name=f"dec_upsample_{ii}")(x)
        x = concatenate([x, skip], name=f"dec_concat_{ii}")
        x = deconv2_block(x, f, batch_norm=batch_norm, name_prefix=f"dec_{ii}")

    # --- Output ---
    outputs = Conv2D(filters=1, kernel_size=(1, 1), padding="same", name="mask_logits")(x)
    outputs = Activation("sigmoid", name="mask")(outputs)

    return Model(inputs=inputs, outputs=outputs, name="scss_net_convlstm_early")

import numpy as np
from tensorflow.keras import backend as K
import tensorflow as tf

"""
Metrics and losses used in the project:
- soft metrics for training/validation
- numpy metrics for final test evaluation
"""

# ============================================================
# classical metrics for TEST (after thresholding)
# ============================================================

def dice_np(y_true, y_pred, smooth=1.0):
    intersection = np.sum(y_true * y_pred)
    return 2 * (intersection + smooth) / (np.sum(y_true) + np.sum(y_pred) + smooth)


def iou_np(y_true, y_pred, smooth=1.0):
    intersection = np.sum(y_true * y_pred)
    union = np.sum(y_true + y_pred) - intersection
    return (intersection + smooth) / (union + smooth)


# ============================================================
# Soft metrics for TRAIN / VAL
# ============================================================

def dice_soft(y_true, y_pred, smooth=1e-6):
    y_true = tf.cast(y_true, tf.float32)
    y_pred = tf.cast(y_pred, tf.float32)

    intersection = tf.reduce_sum(y_true * y_pred, axis=[1, 2, 3])
    denom = tf.reduce_sum(y_true, axis=[1, 2, 3]) + tf.reduce_sum(y_pred, axis=[1, 2, 3])
    dice = (2.0 * intersection + smooth) / (denom + smooth)
    return tf.reduce_mean(dice)


def iou_soft(y_true, y_pred, smooth=1e-6):
    y_true = tf.cast(y_true, tf.float32)
    y_pred = tf.cast(y_pred, tf.float32)

    intersection = tf.reduce_sum(y_true * y_pred, axis=[1, 2, 3])
    union = tf.reduce_sum(y_true + y_pred, axis=[1, 2, 3]) - intersection
    iou = (intersection + smooth) / (union + smooth)
    return tf.reduce_mean(iou)


# ============================================================
# losses
# ============================================================

def dice_loss(y_true, y_pred):
    return 1.0 - dice_soft(y_true, y_pred)

bce = tf.keras.losses.BinaryCrossentropy()

def bce_dice_loss(y_true, y_pred):
    return bce(y_true, y_pred) + dice_loss(y_true, y_pred)



import numpy as np
from PIL import Image
import tensorflow as tf

def rotate_crop_scale_and_pad(original, data_idx, data, pad_black=True):
    """
    Rotate, crop, scale, and pad an image based on bounding box data.

    Args:
        original (PIL.Image): Original image to transform.
        data_idx (int): Index of the bounding box in the data dictionary.
        data (dict): Dictionary containing bounding box information (e.g., 'left', 'top', 'width', 'height').
        pad_black (bool): Whether to pad with black (True) or average border color (False).

    Returns:
        tuple: Transformed image (PIL.Image), scale ratio (float), 
               padding offsets (dx, dy), and bounding box coordinates.

    Example:
        rotate_crop_scale_and_pad(image, 0, data)
        # Output: (<PIL.Image>, 0.8, 10, 15, ...)
    """
    angle = 0
    height = data['height'][data_idx]
    width = data['width'][data_idx]
    min_x, min_y = 0
    max_x = min_x + width
    max_y = min_y + height

    output = original.rotate(angle, center=(min_x, min_y))
    crop = output.crop((min_x, min_y, max_x, max_y))

    ratio = min(224 / crop.width, 224 / crop.height)
    new_crop = crop.resize((int(crop.width * ratio), int(crop.height * ratio)))
    new_crop_np = np.array(new_crop)

    pixel_1 = new_crop_np[1, 1]
    pixel_2 = new_crop_np[1, new_crop_np.shape[-1] - 1]
    pixel_3 = new_crop_np[new_crop_np.shape[0] - 1, 1]
    pixel_4 = new_crop_np[new_crop_np.shape[0] - 1, new_crop_np.shape[-1] - 1]
    avg = np.rint(np.mean([pixel_1, pixel_2, pixel_3, pixel_4], axis=0)).astype(
        np.uint8
    )

    color = tuple(avg) if not pad_black else (0, 0, 0)
    new_image = Image.new(new_crop.mode, (224, 224), color)
    dx = (224 - new_crop.width) // 2
    dy = (224 - new_crop.height) // 2
    new_image.paste(new_crop, (dx, dy))
    return new_image, ratio, dx, dy, min_x, min_y, angle, crop


def load_and_pad_img(image):
    """
    Resize and pad an image to fit a 224x224 frame while maintaining aspect ratio.

    Args:
        image (PIL.Image): Input image to resize and pad.

    Returns:
        PIL.Image: Padded and resized image.

    Example:
        load_and_pad_img(image)
        # Output: <PIL.Image>
    """
    width, height = image.size
    ratio = min(224 / width, 224 / height)
    image = image.resize((int(width * ratio), int(height * ratio)))
    width, height = image.size
    if height < 224:
        # If width is shorter than height pad top and bottom.
        top_padding = (224 - height) // 2
        bottom_padding = 224 - height - top_padding
        padded_image = Image.new('RGB', (width, 224), (255, 255, 255))
        padded_image.paste(image, (0, top_padding))
    else:
        # Otherwise pad left and right.
        left_padding = (224 - width) // 2
        right_padding = 224 - width - left_padding
        padded_image = Image.new('RGB', (224, height), (255, 255, 255))
        padded_image.paste(image, (left_padding, 0))
    return padded_image

def scale_and_pad(original, pad_black=True):
    """
    Scale and pad an image to 224x224 dimensions.

    Args:
        original (PIL.Image): Input image to scale and pad.
        pad_black (bool): Whether to pad with black (True) or average border color (False).

    Returns:
        tuple: Padded image (PIL.Image), scale ratio (float), 
               padding offsets (dx, dy), and the resized image.

    Example:
        scale_and_pad(image)
        # Output: (<PIL.Image>, 0.9, 10, 15, ...)
    """
    ratio = min(224 / original.width, 224 / original.height)
    original_np = np.array(original)
    new_crop = original.resize((int(original.width * ratio), int(original.height * ratio)))
    pixel_1 = original_np[1, 1]
    pixel_2 = original_np[1, original_np.shape[-1]-1]
    pixel_3 = original_np[original_np.shape[0]-1, 1]
    pixel_4 = original_np[original_np.shape[0]-1, original_np.shape[-1]-1]
    avg = np.rint(np.mean([pixel_1, pixel_2, pixel_3, pixel_4], axis=0)).astype(np.uint8)

    color = tuple(avg) if not pad_black else (0, 0, 0)
    new_image = Image.new(new_crop.mode, (224, 224), color)
    dx = (224 - new_crop.width) // 2
    dy = (224 - new_crop.height) // 2
    new_image.paste(new_crop, (dx, dy))
    return new_image, ratio, dx, dy, new_crop


def encode_images_in_batches(images, batch_size=32):
    """
    Encode images in batches for efficient processing.

    Args:
        images (list[PIL.Image]): List of images to encode.
        batch_size (int): Number of images per batch.

    Returns:
        tuple: List of encoded batches (list of tf.Tensor), 
               and the original image batches (list of np.array).

    Example:
        encode_images_in_batches(images)
        # Output: ([<tf.Tensor>, ...], [<np.array>, ...])
    """
    def encode_image(image):
        image_np = np.array(image)[:, :, :3]
        encoded_jpeg = tf.io.encode_jpeg(image_np)
        return tf.reshape(encoded_jpeg, (1,)), image_np

    encoded_batches = []
    original_batches = []

    num_batches = len(images) // batch_size + (1 if len(images) % batch_size != 0 else 0)

    for i in range(num_batches):
        start_idx = i * batch_size
        end_idx = min(start_idx + batch_size, len(images))
        current_batch = images[start_idx:end_idx]

        encoded_batch = []
        original_batch = []
        for image in current_batch:
            encoded, original = encode_image(image)
            encoded_batch.append(encoded)
            original_batch.append(original)

        encoded_batches.append(tf.stack(encoded_batch))
        original_batches.append(np.stack(original_batch))

    return encoded_batches, original_batches

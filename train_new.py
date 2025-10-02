
import matplotlib.pyplot as plt
import numpy as np
import os
import tensorflow as tf
from tensorflow.keras.applications import EfficientNetB4
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.applications.efficientnet import preprocess_input

#setting up training DS

train_dir = '/Volumes/Blue Drive/iNatDataset/plants_split/train'
validation_dir = '/Volumes/Blue Drive/iNatDataset/plants_split/val'
test_dir = '/Volumes/Blue Drive/iNatDataset/plants_split/test'

BATCH_SIZE=16
IMG_SIZE=(380,380)

## Load up Datasets
train_dataset = tf.keras.utils.image_dataset_from_directory(train_dir,
                                                            shuffle=True,
                                                            batch_size=BATCH_SIZE,
                                                            image_size=IMG_SIZE)



val_dataset = tf.keras.utils.image_dataset_from_directory(validation_dir,
                                                          shuffle=True,
                                                          batch_size=BATCH_SIZE,
                                                          image_size=IMG_SIZE)

test_dataset = tf.keras.utils.image_dataset_from_directory(test_dir,
                                                          shuffle=False,
                                                          batch_size=BATCH_SIZE,
                                                          image_size=IMG_SIZE)

class_names = train_dataset.class_names
num_classes = len(class_names)

## Autotune for GPU optimization

AUTOTUNE = tf.data.AUTOTUNE
train_dataset = train_dataset.prefetch(buffer_size=AUTOTUNE)
val_dataset   = val_dataset.prefetch(buffer_size=AUTOTUNE)
test_dataset  = test_dataset.prefetch(buffer_size=AUTOTUNE)


## Display the first 9 images and their labels



##print(train_dataset.class_names)

plt.figure(figsize=(10,10))
for images, labels in train_dataset.take(1):
  for i in range(9):
    ax = plt.subplot(3,3, i+1)
    plt.imshow(images[i].numpy().astype("uint8"))
    plt.title(class_names[labels[i]])
    plt.axis('off')

## Seperate a test set from the val set

val_batches = tf.data.experimental.cardinality(val_dataset)
## print(val_batches)



## Create data augmentation to prevent overfitting on images

data_augmentation = tf.keras.Sequential([
    tf.keras.layers.RandomFlip("horizontal_and_vertical"),
    tf.keras.layers.RandomRotation(0.2),
    tf.keras.layers.RandomZoom(0.2),
    tf.keras.layers.RandomContrast(0.2),
    tf.keras.layers.RandomBrightness(factor=0.2),  # TF ≥ 2.15
])




## adding the extra dimension of the color channels to create required shape dimensions
IMG_SHAPE = IMG_SIZE + (3,)
base_model = EfficientNetB4(
    input_shape=IMG_SHAPE,
    include_top=False,
    weights="imagenet"
)

## FREEZING THE BASE MODEL
base_model.trainable = False
base_model.summary()

## Using Global Average Pooling to convert from 5x5x1280 to flatten features into a 1280 element vector per image
global_average_layer = tf.keras.layers.GlobalAveragePooling2D()


## Building Model out of all the parts

inputs = tf.keras.Input(shape=IMG_SHAPE)

## Preprocessing stage:
x = data_augmentation(inputs)
x = preprocess_input(x)
## Feed new data into the pre-trained base model with training turned off
x = base_model(x, training=False)
x = tf.keras.layers.GlobalAveragePooling2D()(x)
x = tf.keras.layers.Dropout(0.3)(x)
outputs = tf.keras.layers.Dense(num_classes, activation="softmax")(x)

#Assemble model
model = tf.keras.Model(inputs, outputs)

model.summary()

##callback definition
callbacks = [
    EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True),
    ModelCheckpoint("plantdex_best.keras", save_best_only=True)
]

## Compile the model

base_learning_rate = 0.0001
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=base_learning_rate),
              loss=tf.keras.losses.SparseCategoricalCrossentropy(),
              metrics=['accuracy']
              )

initial_epochs = 25
history = model.fit(train_dataset, validation_data=val_dataset, epochs=initial_epochs, callbacks=callbacks)

model.save("plantdex_mobilenetv3.keras")

# Unfreeze top N layers of base model
base_model.trainable = True
for layer in base_model.layers[:-30]:   # freeze all but last 50 layers
    layer.trainable = False

# Re-compile with a lower learning rate
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
    loss=tf.keras.losses.SparseCategoricalCrossentropy(),
    metrics=["accuracy"]
)

# Continue training
fine_tune_epochs = 10
total_epochs = initial_epochs + fine_tune_epochs

history_fine = model.fit(
    train_dataset,
    validation_data=val_dataset,
    epochs=total_epochs,
    initial_epoch=history.epoch[-1],
    callbacks=callbacks  # continue from where it left off
)

model.save("plantdex_mobilenetv3_fine.keras")

loss, accuracy = model.evaluate(test_dataset)
print('Test accuracy :', accuracy)
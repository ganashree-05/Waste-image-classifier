import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras import layers, models
import os
import json

# Paths
train_dir = "dataset/train"
val_dir = "dataset/val"
test_dir = "dataset/test"

IMG_SIZE = (224, 224)
BATCH_SIZE = 32

# Data Generators
train_gen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=25,
    zoom_range=0.2,
    horizontal_flip=True
).flow_from_directory(
    train_dir,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical'
)

val_gen = ImageDataGenerator(rescale=1./255).flow_from_directory(
    val_dir,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical'
)

# ✅ SAVE CLASS INDICES (VERY IMPORTANT)
os.makedirs("model", exist_ok=True)
with open("model/classes.json", "w") as f:
    json.dump(train_gen.class_indices, f)

print("Class Indices:", train_gen.class_indices)

# Load Pretrained Model
base_model = MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,
    weights='imagenet'
)

# Freeze base layers
for layer in base_model.layers:
    layer.trainable = False

# Custom Layers
x = base_model.output
x = layers.GlobalAveragePooling2D()(x)
x = layers.BatchNormalization()(x)   # ✅ improves stability
x = layers.Dense(128, activation='relu')(x)
x = layers.Dropout(0.5)(x)           # ✅ prevents overfitting
output = layers.Dense(train_gen.num_classes, activation='softmax')(x)

# Final Model
model = models.Model(inputs=base_model.input, outputs=output)

# Compile
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Train
history = model.fit(
    train_gen,
    validation_data=val_gen,
    epochs=10   # increased for better learning
)

# Save model
model.save("model/waste_model.h5")

print("✅ Model Trained & Saved Successfully!")
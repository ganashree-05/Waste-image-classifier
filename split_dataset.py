import os
import shutil
import random

base_dir = "dataset"
train_dir = os.path.join(base_dir, "train")
val_dir = os.path.join(base_dir, "val")
test_dir = os.path.join(base_dir, "test")

classes = os.listdir(train_dir)

val_ratio = 0.15
test_ratio = 0.15

for cls in classes:
    cls_path = os.path.join(train_dir, cls)
    images = os.listdir(cls_path)

    random.shuffle(images)

    total = len(images)
    val_count = int(val_ratio * total)
    test_count = int(test_ratio * total)

    val_imgs = images[:val_count]
    test_imgs = images[val_count:val_count + test_count]

    # Move to validation
    for img in val_imgs:
        src = os.path.join(cls_path, img)
        dst = os.path.join(val_dir, cls, img)
        shutil.move(src, dst)

    # Move to test
    for img in test_imgs:
        src = os.path.join(cls_path, img)
        dst = os.path.join(test_dir, cls, img)
        shutil.move(src, dst)

print("✅ Split completed!")
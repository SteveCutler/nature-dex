import os
import shutil
import random

# Paths
data_dir = "/Volumes/Blue Drive/iNatDataset/train" 
output_dir = "/Volumes/Blue Drive/iNatDataset/plants_split"

# Split ratios
train_split = 0.7
val_split = 0.15
test_split = 0.15

# Seed for reproducibility
random.seed(42)

# Make output dirs
for split in ["train", "val", "test"]:
    split_dir = os.path.join(output_dir, split)
    os.makedirs(split_dir, exist_ok=True)

# Iterate over classes
for class_name in os.listdir(data_dir):
    class_dir = os.path.join(data_dir, class_name)
    if not os.path.isdir(class_dir):
        continue
    
    images = os.listdir(class_dir)
    random.shuffle(images)

    n_total = len(images)
    n_train = int(train_split * n_total)
    n_val = int(val_split * n_total)

    train_imgs = images[:n_train]
    val_imgs = images[n_train:n_train+n_val]
    test_imgs = images[n_train+n_val:]

    # Create class dirs inside each split
    for split, split_imgs in zip(["train", "val", "test"], [train_imgs, val_imgs, test_imgs]):
        split_class_dir = os.path.join(output_dir, split, class_name)
        os.makedirs(split_class_dir, exist_ok=True)
        for img in split_imgs:
            src = os.path.join(class_dir, img)
            dst = os.path.join(split_class_dir, img)
            shutil.copy2(src, dst)

print("Dataset split complete!")

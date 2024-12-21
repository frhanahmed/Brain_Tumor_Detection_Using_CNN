import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Step 1: Load and preprocess the data
def load_data(data_dir, img_size):
    data = []
    labels = []
    categories = os.listdir(data_dir)  # Ensure there are only 'yes' and 'no'
    print(f"Categories found: {categories}")  # Debugging
    for label, category in enumerate(categories):
        category_path = os.path.join(data_dir, category)
        for img_name in os.listdir(category_path):
            try:
                img_path = os.path.join(category_path, img_name)
                img = cv2.imread(img_path, cv2.IMREAD_COLOR)
                img = cv2.resize(img, (img_size, img_size))
                data.append(img)
                labels.append(label)
            except Exception as e:
                print(f"Error loading image: {e}")
    return np.array(data), np.array(labels)

# Define paths and parameters
data_dir = r'C:/Users/frhan/Desktop/03_Farhan/Brain Tumor Detection/Brain_Tumor_Datasets/train'  # Update with your dataset path
img_size = 128

# Load dataset
X, y = load_data(data_dir, img_size)

# Verify the loaded data
num_classes = len(np.unique(y))  # Should be 2 for 'yes' and 'no'
print(f"Number of classes: {num_classes}")
print(f"Unique labels: {np.unique(y)}")  # Debugging

# Normalize and one-hot encode data
X = X / 255.0
y = to_categorical(y, num_classes=num_classes)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 2: Augment the data (To increase the size of the dataset if there is insufficient data)
datagen = ImageDataGenerator(
    rotation_range=20,
    zoom_range=0.15,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True,
    fill_mode="nearest"
)
datagen.fit(X_train)

# Step 3: Build the CNN model
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(img_size, img_size, 3)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(num_classes, activation='softmax')  # Output matches number of classes
])
# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Step 4: Train the model
history = model.fit(
    datagen.flow(X_train, y_train, batch_size=32),
    epochs=3,  #Adjust the number of epochs(iterations) according to your models requirements..git 
    validation_data=(X_test, y_test)
)

# Step 5: Evaluate the model (To check the performance of the model)
test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=2)
print(f"Test Accuracy: {test_accuracy*100:.2f}%")

# Step 6: Visualize training results
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.legend()
plt.title("Model Accuracy")
plt.xlabel("Epochs")
plt.ylabel("Accuracy")
plt.show()

plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.legend()
plt.title("Model Loss")
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.show()

# Step 7: Make Predictions
def predict_image(image_path, model):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (img_size, img_size)) / 255.0
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    prediction = model.predict(img)
    return "Tumor" if np.argmax(prediction) == 1 else "No Tumor"

# Test prediction (Testing the performance of the model by testing different images)
image_path = r'C:/Users/frhan/Desktop/03_Farhan/Brain Tumor Detection/Brain_Tumor_Datasets/test/no/24 no.jpg'  # Update with your test image path
result = predict_image(image_path, model)
print(f"Prediction: {result}")
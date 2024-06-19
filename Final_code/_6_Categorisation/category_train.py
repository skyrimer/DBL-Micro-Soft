import joblib
import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from sklearn.utils.class_weight import compute_class_weight

# Step 1: Load the data
data = pd.read_excel("_6_Categorisation\clean_labels.xlsx").query(
    "Category != 'Undefined category'"
)

# Step 3: Convert text data to numerical format using TF-IDF
tfidf_vectorizer = TfidfVectorizer(max_features=5000)
X = tfidf_vectorizer.fit_transform(data["text"]).toarray()
y = data["Category"]

# Step 4: Addressing Imbalance using SMOTE
smote = SMOTE(random_state=42)  # Ensuring reproducibility
X_resampled, y_resampled = smote.fit_resample(X, y)

# Step 5: Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X_resampled, y_resampled, test_size=0.05, random_state=42
)

# Step 6: Encode the labels
label_encoder = LabelEncoder()
label_encoder.fit(y_resampled)  # Fit the encoder on the resampled labels
y_train_encoded = label_encoder.transform(y_train)
y_test_encoded = label_encoder.transform(y_test)

# Step 7: Compute class weights``
class_weights = compute_class_weight(
    "balanced", classes=label_encoder.classes_, y=y_resampled
)
class_weight_dict = {i: class_weights[i] for i in range(len(class_weights))}

# Step 8: Create and train the SVM model with a linear kernel
svm_model = SVC(
    kernel="linear", probability=True, random_state=42, class_weight=class_weight_dict
)
svm_model.fit(X_train, y_train_encoded)

# Save the model, vectorizer, and label encoder
joblib.dump(svm_model, r"_6_Categorisation\svm_model.joblib")
joblib.dump(tfidf_vectorizer, r"_6_Categorisation\tfidf_vectorizer.joblib")
joblib.dump(label_encoder, r"_6_Categorisation\label_encoder.joblib")

# Team 01 | Final Submission

**Track:** Track B – Sentiment Analysis  
**Language:** Kamba (kam-KE)  
**Application Domain:** University Student Life & Campus Services Feedback  

## 🔗 Project Links
* **Demo & Presentation Video:**https://drive.google.com/file/d/1GtUvXtiUQyqzul92bDUi7WUo0pGZmCj-/view?usp=sharing
* **Original Team Repository:** https://github.com/austinmuendomuia/NLP-DATATHON-TEAM_1
* **Frozen Commit SHA:** 5bbc61d28f24376da8c48c352cfc0ede200beec4

## 💡 The Problem
Many commonly used sentiment analysis systems are trained primarily on high-resource languages. Their performance does not easily transfer to Kamba due to differences in vocabulary, morphology, and negation. There is a need for a documented, reviewable Kamba dataset and baseline classifier capable of distinguishing favorable, unfavorable, and neutral statements within the domain of campus services and student life.

## 🛠️ Our Approach
1. **Data Collection:** We authored, reviewed, and finalized a highly balanced dataset of 300 Kamba sentences (100 positive, 100 negative, 100 neutral).
2. **Splitting:** Data was strictly partitioned into 60% Train, 20% Dev, and 20% Test splits (exactly class-balanced), ensuring closely related minimal pairs stayed in the same split.
3. **Modelling:** We trained a character-level TF-IDF Vectorizer combined with a Logistic Regression baseline. 
4. **Demonstration:** We adapted the `app.py` Streamlit interface to accept new Kamba input, predict the sentiment, display uncalibrated probabilities, and transparently explain specific failure cases.

## 📊 Actual Results
Our frozen evaluation run on the 60-example test split yielded:
* **Test Accuracy:** 83.33%
* **Macro-F1:** 83.24%
* **Positive F1:** 83.33% | **Negative F1:** 84.09% | **Neutral F1:** 82.28%

## ⚠️ Limitations
* **Model Simplicity:** As a character n-gram frequency classifier, the model struggles with deep grammar, such as missing Kamba double-negation prefixes (e.g., *ndu-*).
* **Narrow Domain:** The model may be unreliable if tested on topics entirely outside of campus feedback.
* **Small Dataset:** 300 records is sufficient for a prototype but does not capture the full morphological variety of Kamba dialects. 

## 👥 Member Contributions
* **Austin Muendo:** UI/App development, model training, evaluation pipeline, video demonstration recording.
* **Ian Kitheka:** Dataset documentation, language review, annotation guidelines, structural validation, and final project report.
*(Note: A third team member was originally planned but withdrew due to personal circumstances. Work was redistributed among the two active members.)*
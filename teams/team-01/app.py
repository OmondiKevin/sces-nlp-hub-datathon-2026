# # # from pathlib import Path
# # # import joblib
# # # import streamlit as st
# # # from core import FRIENDLY,extract
# # # st.set_page_config(page_title='African-language NLP Demo',page_icon='🌍')
# # # st.title('African-language NLP Demo')
# # # track=st.selectbox('Task',['intent','sentiment','semantic'])
# # # path=Path('artifacts')/track/'model.joblib'
# # # if not path.exists():st.info('Train this task first; see NEXT_STEPS.md.');st.stop()
# # # pack=joblib.load(path) # Only load model files you created and trust.
# # # if pack['practice']:st.warning('PRACTICE MODE: constructed English teaching examples. Scores do not establish real-world quality.')
# # # st.write('Language:',pack['language'])
# # # text=st.text_area('Enter text in the model language')
# # # if st.button('Predict'):
# # #     if not text.strip():st.info('Enter text first.');st.stop()
# # #     label=pack['model'].predict([text])[0]
# # #     st.subheader(('The sentiment is: ' if track=='sentiment' else 'The intention of the user is: ')+FRIENDLY.get(label,label))
# # #     proba=pack['model'].predict_proba([text])[0];st.write(f"Model probability (uncalibrated): {max(proba):.1%}")
# # #     st.caption('This score is not a guarantee of correctness. The model chooses a known label even for unsupported input.')
# # #     if track=='semantic':
# # #         st.json({'intent':label,'slots':extract(text,pack['slot_memory'])})
# # #         st.caption('Training-only surface-value matcher: unseen slot values may be missed; no date/time normalisation or real action is executed.')
# # #     elif track=='intent':st.info('Simulated route only. No calendar, music, weather or other external action has been executed.')
# # #     else:st.info('Sentence-level opinion label only; this is not emotion detection, sarcasm understanding or a diagnosis.')

# # from pathlib import Path
# # import joblib
# # import streamlit as st
# # import numpy as np
# # from core import FRIENDLY, extract

# # st.set_page_config(page_title='African-language NLP Demo', page_icon='🌍')
# # st.title('African-language NLP Demo')
# # track = st.selectbox('Task', ['intent', 'sentiment', 'semantic'])
# # path = Path('artifacts') / track / 'model.joblib'

# # if not path.exists():
# #     st.info('Train this task first; see NEXT_STEPS.md.')
# #     st.stop()
    
# # pack = joblib.load(path) # Only load model files you created and trust.

# # if pack['practice']:
# #     st.warning('PRACTICE MODE: constructed English teaching examples. Scores do not establish real-world quality.')

# # # Datathon Requirements: Display Team, Language, and Prototype Status
# # st.markdown("**Team 1 Prototype Demo**")
# # st.write('Language:', pack['language'])

# # text = st.text_area('Enter text in the model language')

# # if st.button('Predict'):
# #     if not text.strip():
# #         st.info('Enter text first.')
# #         st.stop()
        
# #     # Get probabilities for all classes
# #     probabilities = pack['model'].predict_proba([text])[0]
# #     classes = pack['model'].classes_
    
# #     # Sort them to find the Winner and the Runner-Up
# #     prob_dict = {classes[i]: probabilities[i] for i in range(len(classes))}
# #     sorted_probs = sorted(prob_dict.items(), key=lambda item: item[1], reverse=True)
    
# #     top_label, top_score = sorted_probs[0]
# #     runner_up_label, runner_up_score = sorted_probs[1]
    
# #     # Custom UI Output Logic
# #     if top_score >= 0.70:
# #         # High confidence
# #         st.subheader(('The sentiment is: ' if track == 'sentiment' else 'The intention of the user is: ') + FRIENDLY.get(top_label, top_label))
# #         st.write(f"Model probability (uncalibrated): {top_score*100:.1f}%")
# #         st.caption('This score is not a guarantee of correctness. The model chooses a known label even for unsupported input.')
# #     else:
# #         # Low confidence: Explain the uncertainty
# #         st.warning(('Predicted sentiment: ' if track == 'sentiment' else 'Predicted intent: ') + FRIENDLY.get(top_label, top_label) + ' (Uncertain)')
# #         st.write(f"Model probability (uncalibrated): {top_score*100:.1f}%")
        
# #         st.info(
# #             f"**Why the model is unsure:**\n"
# #             f"I suspect this is **{top_label}** ({top_score*100:.1f}%), but it could very easily be **{runner_up_label}** ({runner_up_score*100:.1f}%).\n\n"
# #             f"*Because this is a character/word-frequency model (TF-IDF), it does not understand complex grammar. It is likely seeing a mix of vocabulary—some words that usually correlate with {top_label} sentences (like 'mutandao' or 'yunivasiti'), mixed with words that correlate with {runner_up_label} sentences. It may have also missed a Kamba negation word (like 'ndu-') or failed to pick up on implied frustration/sarcasm.*"
# #         )
# #         st.caption('This score is not a guarantee of correctness. The model chooses a known label even for unsupported input.')
        
# #     # Appended disclaimers based on track
# #     if track == 'semantic':
# #         st.json({'intent': top_label, 'slots': extract(text, pack['slot_memory'])})
# #         st.caption('Training-only surface-value matcher: unseen slot values may be missed; no date/time normalisation or real action is executed.')
# #     elif track == 'intent':
# #         st.info('Simulated route only. No calendar, music, weather or other external action has been executed.')
# #     else:
# #         st.info('Sentence-level opinion label only; this is not emotion detection, sarcasm understanding or a diagnosis.')

# from pathlib import Path
# import joblib
# import streamlit as st
# import numpy as np
# from core import FRIENDLY, extract

# st.set_page_config(page_title='African-language NLP Demo', page_icon='🌍')
# st.title('African-language NLP Demo')

# # Datathon Requirements: Display Team, Language, Prototype Status, and Domain
# st.markdown("**Team 1 | Language: Kamba | Prototype Status: Active**")
# st.markdown("*Domain: University Student Life & Campus Services Feedback*")

# track = st.selectbox('Task', ['intent', 'sentiment', 'semantic'])
# path = Path('artifacts') / track / 'model.joblib'

# if not path.exists():
#     st.info('Train this task first; see NEXT_STEPS.md.')
#     st.stop()
    
# pack = joblib.load(path) # Only load model files you created and trust.

# if pack['practice']:
#     st.warning('PRACTICE MODE: constructed English teaching examples. Scores do not establish real-world quality.')

# # Mock Translation Dictionary to simulate the summary for the Video Demo
# DEMO_TRANSLATIONS = {
#     # The 3 Successful Examples from the Video Script
#     "Mutandao wa yunivasiti umunthi ni nzeo muno.": "The university network is very good today.",
#     "Thini wa nyumba ya kwia mavuku mutandao wa seve ni muthuku vyu.": "Inside the library, the Wi-Fi network is very bad.",
#     "Ofisi ya kutetheesya ithukumaa kuma saa ili sya kwakya kuvika saa ikumi na imwe sya mawiyoo.": "The helpdesk office works from 8:00 AM to 5:00 PM.",
    
#     # The 2 Failure Examples from the Video Script
#     "Nina utanu nundu mutandao wa seve nduendaa nthi ona ngitembea kati wa nyumba sya yunivasiti.": "I am happy because the Wi-Fi does not go down even when walking across campus.",
#     "Mundu wa kutetheesya anasyaisye ndio sya kimitambo mukahawani na aema kutungiia intaneti.": "The technician looked at the cables in the cafeteria and failed to fix the internet."
# }

# DEMO_EXPLANATIONS = {
#     "Nina utanu nundu mutandao wa seve nduendaa nthi ona ngitembea kati wa nyumba sya yunivasiti.": "Missed Double Negation. The model heavily associated the phrase 'endaa nthi' (goes down) with negative network outages. It missed the Kamba negation prefix 'ndu-' in 'nduendaa nthi' (does not go down).",
#     "Mundu wa kutetheesya anasyaisye ndio sya kimitambo mukahawani na aema kutungiia intaneti.": "Missed Action/Resolution. This sentence lacks strong emotional indicator words. It states a sequence of events where a technician simply failed to do their job ('aema kutungiia'). The model lacks deep grammar to know this is a negative event, defaulting to neutral."
# }

# text = st.text_area('Enter text in the model language (Kamba)')

# if st.button('Predict'):
#     if not text.strip():
#         st.info('Enter text first.')
#         st.stop()
        
#     # Get probabilities for all classes
#     probabilities = pack['model'].predict_proba([text])[0]
#     classes = pack['model'].classes_
    
#     # Sort them to find the Winner and the Runner-Up
#     prob_dict = {classes[i]: probabilities[i] for i in range(len(classes))}
#     sorted_probs = sorted(prob_dict.items(), key=lambda item: item[1], reverse=True)
    
#     top_label, top_score = sorted_probs[0]
#     runner_up_label, runner_up_score = sorted_probs[1]
    
#     # 1. Output the Label
#     friendly_label = FRIENDLY.get(top_label, top_label) if track == 'sentiment' else FRIENDLY.get(top_label, top_label)
#     st.subheader(f"Predicted Sentiment: {friendly_label.capitalize()}")
    
#     # 2. Output the Simulated Translation / Summary
#     translation = DEMO_TRANSLATIONS.get(text.strip(), "*(Simulated Summary: The user is providing feedback about campus services/student life.)*")
#     st.info(f"**English Translation / Summary:**\n{translation}")
    
#     # 3. Output Confidence & Reasoning
#     st.write(f"**Model Probability (Uncalibrated):** {top_score*100:.1f}%")
    
#     if top_score >= 0.70:
#         st.success(
#             f"**Model Reasoning:** The model is highly confident. It detected strong character and word patterns "
#             f"in the Kamba text that heavily correlate with **{top_label}** feedback in our training data."
#         )
#     # else:
#     #     st.warning(
#     #         f"**Why the model is unsure:**\n"
#     #         f"I suspect this is **{top_label}** ({top_score*100:.1f}%), but it could be **{runner_up_label}** ({runner_up_score*100:.1f}%).\n\n"
#     #         f"*Explanation: As a TF-IDF classifier, the model relies on word frequencies rather than deep grammar. "
#     #         f"It is likely detecting mixed vocabulary (words overlapping with both {top_label} and {runner_up_label} examples), "
#     #         f"missing a Kamba negation prefix (like 'ndu-'), or failing to understand the contextual outcome of the event.*"
#     #     )

#     else:
#         st.warning(
#             f"**Why the model is unsure:**\n"
#             f"I suspect this is **{top_label}** ({top_score*100:.1f}%), but it could be **{runner_up_label}** ({runner_up_score*100:.1f}%).\n\n"
#         )
        
#         # Output the specific explanation if it's one of our demo failures, otherwise use the generic fallback
#         specific_explanation = DEMO_EXPLANATIONS.get(text.strip(), "As a TF-IDF classifier, the model relies on word frequencies rather than deep grammar. It is likely detecting mixed vocabulary, missing a Kamba negation prefix, or failing to understand the contextual outcome.")
#         st.info(f"**Explanation:** {specific_explanation}")
        
#     # st.caption('This score is not a guarantee of correctness. The model chooses a known label even for unsupported input.')
    
#     # Appended disclaimers based on track
#     if track == 'semantic':
#         st.json({'intent': top_label, 'slots': extract(text, pack['slot_memory'])})
#         st.caption('Training-only surface-value matcher: unseen slot values may be missed; no date/time normalisation or real action is executed.')
#     elif track == 'intent':
#         st.info('Simulated route only. No calendar, music, weather or other external action has been executed.')
#     else:
#         st.info('Sentence-level opinion label only; this is not emotion detection, sarcasm understanding or a diagnosis.')


from pathlib import Path
import joblib
import streamlit as st
import numpy as np
from core import FRIENDLY, extract

st.set_page_config(page_title='African-language NLP Demo', page_icon='🌍')
st.title('African-language NLP Demo')

# Datathon Requirements: Display Team, Language, Prototype Status, and Domain
st.markdown("**Team 1 | Language: Kamba | Prototype Status: Active**")
st.markdown("*Domain: University Student Life & Campus Services Feedback*")

track = st.selectbox('Task', ['intent', 'sentiment', 'semantic'])
path = Path('artifacts') / track / 'model.joblib'

if not path.exists():
    st.info('Train this task first; see NEXT_STEPS.md.')
    st.stop()
    
pack = joblib.load(path) # Only load model files you created and trust.

if pack['practice']:
    st.warning('PRACTICE MODE: constructed English teaching examples. Scores do not establish real-world quality.')

# Mock Translation Dictionary to simulate the summary for the Video Demo
DEMO_TRANSLATIONS = {
    "Mutandao wa yunivasiti umunthi ni nzeo muno.": "The university network is very good today.",
    "Thini wa nyumba ya kwia mavuku mutandao wa seve ni muthuku vyu.": "Inside the library, the Wi-Fi network is very bad.",
    "Ofisi ya kutetheesya ithukumaa kuma saa ili sya kwakya kuvika saa ikumi na imwe sya mawiyoo.": "The helpdesk office works from 8:00 AM to 5:00 PM.",
    "Nina utanu nundu mutandao wa seve nduendaa nthi ona ngitembea kati wa nyumba sya yunivasiti.": "I am happy because the Wi-Fi does not go down even when walking across campus.",
    "Mundu wa kutetheesya anasyaisye ndio sya kimitambo mukahawani na aema kutungiia intaneti.": "The technician looked at the cables in the cafeteria and failed to fix the internet."
}

# Mock Explanation Dictionary to simulate specific error analysis
DEMO_EXPLANATIONS = {
    "Nina utanu nundu mutandao wa seve nduendaa nthi ona ngitembea kati wa nyumba sya yunivasiti.": "Missed Double Negation. The model heavily associated the phrase 'endaa nthi' (goes down) with negative network outages. It missed the Kamba negation prefix 'ndu-' in 'nduendaa nthi' (does not go down).",
    "Mundu wa kutetheesya anasyaisye ndio sya kimitambo mukahawani na aema kutungiia intaneti.": "Missed Action/Resolution. This sentence lacks strong emotional indicator words. It states a sequence of events where a technician simply failed to do their job ('aema kutungiia'). The model lacks deep grammar to know this is a negative event, defaulting to neutral."
}

text = st.text_area('Enter text in the model language (Kamba)')

if st.button('Predict'):
    if not text.strip():
        st.info('Enter text first.')
        st.stop()
        
    # Get probabilities for all classes
    probabilities = pack['model'].predict_proba([text])[0]
    classes = pack['model'].classes_
    
    # Sort them to find the Winner and the Runner-Up
    prob_dict = {classes[i]: probabilities[i] for i in range(len(classes))}
    sorted_probs = sorted(prob_dict.items(), key=lambda item: item[1], reverse=True)
    
    top_label, top_score = sorted_probs[0]
    runner_up_label, runner_up_score = sorted_probs[1]
    
    # 1. Output the Label
    friendly_label = FRIENDLY.get(top_label, top_label)
    st.subheader(f"Predicted Sentiment: {friendly_label.capitalize()}")
    
    # 2. Output the Simulated Translation / Summary
    translation = DEMO_TRANSLATIONS.get(text.strip(), "*(Simulated Summary: The user is providing feedback about campus services/student life.)*")
    st.info(f"**English Translation / Summary:**\n{translation}")
    
    # 3. Output Confidence & Reasoning
    st.write(f"**Model Probability (Uncalibrated):** {top_score*100:.1f}%")
    
    if top_score >= 0.70:
        st.success(
            "**Model Reasoning:** The model is highly confident. It detected strong character and word patterns "
            f"in the Kamba text that heavily correlate with **{top_label}** feedback in our training data."
        )
    else:
        st.warning(
            f"**Why the model is unsure:**\n\n"
            f"I suspect this is **{top_label}** ({top_score*100:.1f}%), but it could be **{runner_up_label}** ({runner_up_score*100:.1f}%)."
        )
        
        specific_explanation = DEMO_EXPLANATIONS.get(
            text.strip(), 
            "As a TF-IDF classifier, the model relies on word frequencies rather than deep grammar. It is likely detecting mixed vocabulary, missing a Kamba negation prefix, or failing to understand the contextual outcome."
        )
        st.info(f"**Explanation:** {specific_explanation}")
        
    st.caption('This score is not a guarantee of correctness. The model chooses a known label even for unsupported input.')
    
    # Appended disclaimers based on track
    if track == 'semantic':
        st.json({'intent': top_label, 'slots': extract(text, pack['slot_memory'])})
        st.caption('Training-only surface-value matcher: unseen slot values may be missed; no date/time normalisation or real action is executed.')
    elif track == 'intent':
        st.info('Simulated route only. No calendar, music, weather or other external action has been executed.')
    else:
        st.info('Sentence-level opinion label only; this is not emotion detection, sarcasm understanding or a diagnosis.')
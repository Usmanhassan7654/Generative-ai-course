"""Module 05 beginner practice. Prepared by Engr Usman Hasan.
Fictional parcel policies. Requires Google API access and quota.
"""
import os
from getpass import getpass
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from sklearn.metrics.pairwise import cosine_similarity

PARCELS = {
    "PK101": "Out for delivery in Multan.",
    "PK102": "In transit to Karachi.",
    "PK103": "Delivered in Lahore.",
}

def lookup_parcel(tracking_id):
    clean_id = tracking_id.strip().upper()
    return PARCELS.get(clean_id, "Tracking number not found in the classroom data.")


parcel_information = [
    "Standard delivery takes 3 to 5 working days.",
    "Cash on delivery lets you pay when the parcel arrives.",
    "For a damaged parcel, contact support with photos.",
]

def search_parcel_information(question):
    # Ignore spaces at the start and end.
    question = question.strip()
    if not question:
        return "Please enter a delivery question.", None

    # Convert just the new question into numbers.
    question_vector = embeddings.embed_query(question)

    # Compare it with the policy vectors prepared earlier.
    scores = cosine_similarity([question_vector], parcel_vectors)[0]

    # Remember the position of the largest score.
    best_index = 0
    for i in range(len(scores)):
        if scores[i] > scores[best_index]:
            best_index = i

    # Return saved information; we are not generating a new answer.
    return parcel_information[best_index], float(scores[best_index])

if __name__ == "__main__":
    load_dotenv()
    if not os.getenv("GOOGLE_API_KEY"):
        os.environ["GOOGLE_API_KEY"] = getpass("Enter your Google key: ")
    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("A Google key is required.")
    embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
    parcel_vectors = embeddings.embed_documents(parcel_information)
    print("Module 4 ID example:", lookup_parcel("PK101"))
    print("Now ask a general delivery question. Type exit to stop.")
    print("The closest text can be irrelevant. Inspect each result.")
    while True:
        question = input("Question: ").strip()
        if question.lower() == "exit":
            break
        try:
            information, score = search_parcel_information(question)
            print("Closest saved information:", information)
            if score is not None:
                print("Similarity:", round(score, 3))
        except Exception as error:
            print("Request failed:", type(error).__name__)
            print("Check key, internet, model access and quota before retrying.")

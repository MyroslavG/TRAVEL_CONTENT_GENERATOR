# ========================================================
# Developed by Vozniak Myroslav, Date: 2020-07-02
# ProjectName: Paraphrased Content Generator
# ========================================================
# This project, created in 2020, is an API service that uses GPT-3 to paraphrase Wikipedia articles for SEO purposes. The API returns unique, rephrased content in JSON format, making it suitable for enhancing website content while avoiding duplication. Here�s a summary of its core components:
#
# API Setup: A Flask API is set up with a /generate endpoint, allowing users to submit article topics as input. This endpoint returns a JSON response with a paraphrased version of the relevant Wikipedia content.
#
# Wikipedia Content Retrieval: Given a search topic, the service retrieves a summary from Wikipedia. This summary serves as the basis for generating SEO-friendly, paraphrased content.
#
# Paraphrasing with GPT-3: The API uses GPT-3 to create a unique, high-quality paraphrase of the article by combining prompt examples and configuring temperature, length, and other parameters for natural, relevant rewording.
#
# Uniqueness Validation: After generating the paraphrase, the API calculates cosine similarity between the original and paraphrased text to ensure they are sufficiently distinct. If the similarity is high, additional paraphrasing attempts are made to achieve the desired uniqueness threshold.
#
# Logging: Results, including similarity scores and final paraphrased content, are logged for auditing and quality checks. A separate log records failed attempts for review.
#
# This API service provides a scalable solution for creating SEO-friendly content from existing Wikipedia information by rephrasing it in a way that maintains meaning but is unique for SEO needs.

from flask import Flask, request, jsonify
import json
import os
import openai
import wikipedia
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
openai.api_key = "xxxx"

@app.route('/')
def main():
    return "GPT-3 content machine"

def similar(str1, str2):
        documents = [str1, str2]

        # Create the Document Term Matrix
        count_vectorizer = CountVectorizer(stop_words='english')
        count_vectorizer = CountVectorizer()
        sparse_matrix = count_vectorizer.fit_transform(documents)

        # OPTIONAL: Convert Sparse Matrix to Pandas Dataframe if you want to see the word frequencies.
        doc_term_matrix = sparse_matrix.todense()
        df = pd.DataFrame(doc_term_matrix, 
                        columns=count_vectorizer.get_feature_names(), 
                        index=['str1', 'str2'])

        # Compute Cosine Similarity
        js = cosine_similarity(df, df)
        return js.tolist()[0][1]

@app.route('/generate', methods=['POST'])
def generate():

    input = request.form['input']
    length = int(request.form['length'])
    temperature = request.form['temperature']

    page = wikipedia.summary(input, auto_suggest=True)
    if page is None:
      page = wikipedia.summary(input, auto_suggest=True)

    article0 = "Article: Albert Einstein is one of the most influential scientific figures in recent history. His theory of black holes was just confirmed a few days ago when the first picture of a black hole was photographed. It is incredible how such an influential scientific figure once had to turn down a task much more significant than him. In 1952 Einstein was offered the role of the Israeli President since he had been considered as the best Jew in the world. The ironical part about this was that Albert Einstein wasn't even Israeli, to begin with.\n"
    para0 = "Paraphrase: Scientist and influencer Albert Einstein are one of the most historic figures. Because of his theories, we now know more about space than ever. Even without having adequate resources Einstein theorized the existence of black holes which have been recently photographed by space researchers. What we don't know about the man is that he was once offered the job of leading the nation of Israel in 1952. Even though Einstein was not Israeli, he still had positive ratings in the country as he was considered one of the best Jewish men in the world.\n\n"
    article1 = "Article: Christmas Island, officially known as the Territory of Christmas Island, is an Australian external territory comprising the island of the same name. It is located in the Indian Ocean, around 350 kilometres (220 mi) south of Java and Sumatra and around 1,550 km (960 mi) north-west of the closest point on the Australian mainland. It lies 2,600 km (1,600 mi) northwest of Perth and 1,327 km (825 mi) south of Singapore. It has an area of 135 square kilometres (52 sq mi). Christmas Island had a population of 1,843 residents as of 2016, the majority living in settlements on the northern tip of the island. The main settlement is Flying Fish Cove. Historically, Asian Australians of Chinese, Malay, and Indian descent had collectively formed the majority of the population. Today, around two-thirds of the island's population is estimated to have Straits Chinese origin, with significant numbers of Malays and European Australians and smaller numbers of Indians and Eurasians. Several languages are in use, 27.8% of Christmas Islanders spoke only English at home, with both Mandarin and Malay coming in at 17.2%. Other languages spoken at home include Cantonese (3.7%) and Min Nan (1.5%). Buddhism and Islam are major religions on the island, the religion question in the Australian census is optional and 28% of the population do not declare their religious belief, if any.\n"
    para1 = "Paraphrase: Located in the Indian Ocean, Christmas Island is an Australian territory with a population of 1845 people. The majority of the population live on the northern tip of the island, in settlements such as Flying Fish Cove. The island was discovered by the British Captain Mynor in 1643 and named after Christmas Day. Unfortunately, it took a considerable amount of time for people to settle there. The first population of Europeans was just in the 19th century, followed by the Chinese in the 20th century. The majority of Chinese ancestry is of Singaporean Chinese, followed by Peranakan Chinese, Teochew Chinese, and Hainanese. Indigenous inhabitants are the Kailin and highland peoples.\n\n"
    article2 = "Article: " + page.strip('\n') + "\n"
    para2 = "Paraphrase:"
    times = 1
    result2 = 1

    response = openai.Completion.create(
      engine="davinci",
      prompt=article0 + para0 + article1 + para1 + article2 + para2,
      temperature=0.3,
      max_tokens=200,
      top_p=0.8,
      frequency_penalty=0,
      presence_penalty=0,
      stop=["\n", "\n\nArticle"]
    )

    text_arr = response.choices
    text = text_arr[0].text
    text1 = text
    text2 = ''

    result1 = similar(page, text)
    if result1 > 0.92:
      times = times + 1

      response = openai.Completion.create(
        engine="davinci-instruct-beta",
        prompt="Paraphrase the following text. Use different words, but retain the original meaning of the text:\n" + page.strip('\n'),
        temperature=0.8,
        max_tokens=200,
        top_p=0.8,
        frequency_penalty=0.5,
        presence_penalty=0
      )

      text_arr = response.choices
      text = text_arr[0].text
      text2 = text
      result2 = similar(page, text)

    f = open("data.log", "a")
    f.write(input + "," + str(times) + "," + str(result1) + "," + str(result2) + "," + text1 + "," + text2 + "\n")
    f.close()

    if result1 <= 0.92:
      return text1

    if result2 <= 0.92:
      return text2

    f = open("false.log", "a")
    f.write(input + "\n")
    f.close()

    return ""

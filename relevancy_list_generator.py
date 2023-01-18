import json
import variables
import find_file_path
import openai
import unicode_converter
import ast
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
from revChatGPT.ChatGPT import Chatbot

def generate_list2(category):
    prompt = f"""Write a very long list of all keywords that you would expect in a {category} related article. Each value in this list will only be 1-2 words long. Write this list in the form of a python list, it must match this exact format: ["keyword1", "keyword2", "keyword3"]"""
    chatbot = Chatbot({
        "session_token": "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..8i8mgPEYeSg_o0Ti.Gs1JRvVXJjyW1jTcc_FKbOAer0hoJsXt9000-Ryqb7GOaB1MGZK7-FlK7oow839jkhBuPs1SK3jDqog6kRK-rJplZ9RMuNg3Lq40GsbLkt7PUo0U45q-CVtI9FQR_0eZkNrq7gmVCkMWUxeChBIgO8HklB9DO-Ne7s2PvWIEUT-7E7Sz-01SMHfNj9O0P26DiYaQ8TUBbNML9uRl-o5F5JUX_7oO2Q_h08mANDEXM-FD1OItdJtAQGnittoDttmKs-2W7V2WRrAmEhfWjCHFmg6FPGmnnqgm5n6jgrE8Y-96ArxhQwAb9-fEj38RvP5IYcStk7wh_vhb6nFjTt4JOaYHH7CcHdhU9e-U3Q2rIPvTv1vKqAmL_BEJl7whAsbBcofyS1IXFQKhxrO-riZkF54OzS-TLdouVZzWxVHVUrI2J8dgZN25pfTCIykj0Med22xMnNtl5l4yC6J3H_WUHe-lRSMIDeGHAe019RGvuYCLgUrZ5lHqHfYXXwWnsybvVon61GjaKjlhpwFJKqebiHxlG_ak53dXUHAtAQGqBnmCyHkyyuttxsO1SlzVa9M-CK3X39hBshl-aL6CiIs5zaDuNY0zstLR-YKHoiKcT-OorJfzU0VVjQPWV8F-zplIzbafc1uD8PC8JZFg157tF-YULgXaKEJ8Oy5Harxo1c6vw9yO_qOiTHvhpxlhfJHyxy_8bCd23GwGmUiP-uzd4qvVqLpXZUeR6xvw8uZkfmV_KNTg0LUyp8x-qwsARniz8ouyOW6157dS9W3cY8wrWI73siyFsrImsrzDKYDyYXWJbhJKxT1I6e8uxsLPEc_DYJ5DVnWT4WecmoP0aVUK5nrXkqd8ILvV8Kv_K6PPrWn_sMxj6ZloQDmActyUBxtbEkN_1GlpfNT3lB_n9tuRzXxv54Gb_KwzD_TtZAt6isHf4HvGR28hkishyLSOeoh6u6zZFn58zGpeTEitL5fMFoU79q2XNnM25qUoPM2LJcD3LMOE2riQbG9v90xHEu9LXBFE1Q_2ddc2cdlCtL9YB6yZuoHYgWAaTZJ-KB5Ccy9BjCG_XcknMJpfG5IThpq0vzmUfzuMfBXR3euLSU8e3K3tHv4kC8DBxJTGCvUCxHG42DU2wV0viQMWwY5PdwLrJCgvTC6Xy80pIDfUDblD8Aoj5JU7i88Hhg6wHpreVj88ay7Wq_YMrSOH3Hoavj-90xDhZNQumMnyPOFW2_2F87nMwC36YcUqnjylbrAnBMRa5IwYPpyKqiffipwbGDYphx8pWxF7JsYwKr04RZhm80a8VL1t5RNVeOqjX7mFTG7QfmFBebMJF4Vkr-i5LxkBOQPQTMrmqp56V92dIHmn9nOR3kZGsfGyHHYJ9RKu1yPR_do2o7HZla1MTllz4m3Q6MblbG5y-vdDt6Rp7Wo7UB0uBmcZd35gqn3JvNe2YX9_6QgrrKVbvn_aDPyLUlPvLePjiHdJ0-Sxk2i_H-2bj4_cUj85UlWmkk9hgxmuSZwslHUkfTZ6XT-0dJP49FD1EVEEw2L1qTKaf4KnbnTVZNm8AGRi_mO4xHEsR4Ml5v4VuARlyZOkMM4F4yjoUN8SqoHIpPpptZxWba19okgIjn30ti5OhZBAwFEdr3kG5Y5FGCoz9pROlot9852mGgSqKUE2IZ5yp_TX99hdJZbM8qsDzW4UOSaV-IoiWtC_CgCAiDgL93tgAwPMNwycLct-uO_X9YYEGBuiHp4-zgQ86ygkcCg6ACXsWSYjYuBufP4i9ep2TM5ZvOXLTC9IdzHybBQJiK9b8Qb4G2zzuiLGWVTDfxZ4YyhPEYFUUXVTaxQgKrYibqHhWWzP2dquYLw6GwEJPzZi8SGUZaiA4b85jVBjKHPZaleHGQPS4QWcmE5ixGCJqRgSxCNA06ZEph5e-0j3vobl-UEYBHcRh3Er5EqIqYirvngmnpc9yfTY4kNVNnyz5nvhtN6NgI5m48C4GN55-KW4KBDVwMlWu7rM_Pa1yCvlH5buIv3kLjB6QyJUwEUQwFLoqPqFZH2u2jog-i6saCMluIAfl1qlZbub3sMii0ZqbOOGIipnvJCcfQLuuHmW2qZOeH4RiO-CumlWcwKh0uPfuRa6rSvTQAfdv7p7Wdq3josWP-FnfkUGAjZc3g8RYOlbeEL6OJCwFuMtjfKSIQs1CvhCnpenuJDLsWtgB2ZDRHlNyMTypY7X9BC1pNTlP3AZl7EuWcPApYIQfSUy8kN0uD1UmJ88sAVbnEnAMSG-3gxN.jtVlJpOvW3UHnmrpfq9dzw"
    }, conversation_id=None, parent_id=None) # You can start a custom conversation

    response = chatbot.ask(prompt, conversation_id=None, parent_id=None) # You can specify custom conversation and parent ids. Otherwise it uses the saved conversation (yes. conversations are automatically saved)
    print(response)
    print(response["message"])
    return response["message"]

def generate_list(category):
    prompt = f"""You are a python function that responds with a list which is ingested into another service. Your function is to generate a long list of keywords that you might find for {category} related articles. Each value in this list will only be 1 word long. Write this list in the form of a python list, it must match this exact format: ["keyword1", "keyword2", "keyword3"]"""
    print(prompt)
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt = prompt,
        temperature=0.9,
        max_tokens=2000,
        top_p=1,
        frequency_penalty=1,
        presence_penalty=1
    )
    response = response.choices[0].text
    response = response.replace("\\", "")
    response = response.replace("\n", "")
    return response


def get_category_details(category):
    prompt = f"""Write a very long list of all keywords that you would expect in a {category} related article. Each value in this list will only be 1-2 words long. Write this list in the form of a python list, it must match this exact format: ["keyword1", "keyword2", "keyword3"]"""
    chatbot = Chatbot({
        "session_token": "INSERT_SESSION_TOKEN"
    }, conversation_id=None, parent_id=None) # You can start a custom conversation

    response = chatbot.ask(prompt, conversation_id=None, parent_id=None) # You can specify custom conversation and parent ids. Otherwise it uses the saved conversation (yes. conversations are automatically saved)
    print(response)
    print(response["message"])
    return response["message"]



def category_list(category):
    categoryName = variables.categoryNames[category]
    with open("categories/categoryKeywords.json", "r") as j:
        data = json.load(j)
        if category not in data:
            newList = generate_list2(categoryName)

            newList = unicode_converter.main(newList)
            newList = ast.literal_eval(newList)
            print(newList)
            data[category] = newList
            with open("categories/categoryKeywords.json", "w") as j:
                json.dump(data, j, indent=4)




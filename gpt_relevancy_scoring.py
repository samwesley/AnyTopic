import find_file_path
import openai
import json
import variables
import os
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def category_details(category,details):
    #category_details = "I'm not looking for any subtopics in particular, I'm interested in new technology and general news. I'm looking for news that's within the past month. I'm looking for both news and articles from scientific journals and magazines. "
    intro = f"You are a news curator, I am coming to you asking for news related to {category}. {details}. Based on this guidance, generate a single integer score from 0-10 of how relevant the following article is for me. Format the score as x/10. Article title: "
    return intro

def article_analysis(input, category, details):
    structure = "{relevancy_score : Enter relevancy score here, two_summary: Enter summary here, classification: Enter classification here}"
    intro = f"You are a news curator, I am coming to you asking for news related to {category}. {details}. Based on this guidance, return json with the following fields. A single integer score from 0-10 of how relevant the following article is for me (0 meaning do not ever read, 10 meaning drop everything and read right now). Title this fiield relevancy_score and format the score as only the numerator out of 10. If this score is higher than 4, do the following. Extract the key points from the following article and write a short 2 sentence summary of the article to be used for an email newsletter. Only respond with 2 sentences and tile this field two_summary. Lastly, return a python readable list of classifications for this article and title this field classifications. JSON should be in this format: {structure} Article :{input}"
    prompt = intro
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt = prompt,
        temperature=0,
        max_tokens=500,
        top_p=1,
        frequency_penalty=1,
        presence_penalty=1
    )
    text = response.choices[0].text
    print(text)
    est = response.usage.total_tokens * 0.00002
    print("{} estimated cost: {}".format("relevancy",est))
    global total_cost
    total_cost += est
    global relevancy_cost
    relevancy_cost += est
    global total_count
    total_count += 1
    return text

details = "Use the following rubric: 20% of score based on: must be new technology going into space or helping for space ecosystem. 20% for funding or creation of new space companies. 10% for current news <30 days old. 50% for the news specifically being related to something off earth, in space."

category = "Space Technology"

article = """Technology can change the world in ways that are unimaginable, until they happen. Switching on an electric light would have been unimaginable for our medieval ancestors. In their childhood, our grandparents would have struggled to imagine a world connected by smartphones and the internet.\n\nSimilarly, it is hard for us to imagine the arrival of all those technologies that will fundamentally change the world we are used to.\n\nWe can remind ourselves that our own future might look very different from the world today by looking back at how rapidly technology has changed our world in the past. That\u2019s what this article is about.\n\nOne insight I take away from this long-term perspective is how unusual our time is. Technological change was extremely slow in the past\u2014the technologies that our ancestors got used to in their childhood were still central to their lives in their old age. In stark contrast to those days, we live in a time of extraordinarily fast technological change. For recent generations, it was common for technologies that were unimaginable in their youth to become common later in life.\n\nThe Long-Run Perspective on Technological Change\n\nThe big visualization offers a long-term perspective on the history of technology.1\n\nThe timeline begins at the center of the spiral. The first use of stone tools, 3.4 million years ago, marks the beginning of this history of technology.2 Each turn of the spiral then represents 200,000 years of history. It took 2.4 million years\u201412 turns of the spiral\u2014for our ancestors to control fire and use it for cooking.3\n\nTo be able to visualize the inventions in the more recent past\u2014the last 12,000 years\u2014I had to unroll the spiral. I needed more space to be able to show when agriculture, writing, and the wheel were invented. During this period, technological change was faster, but it was still relatively slow: several thousand years passed between each of these three inventions.\n\nFrom 1800 onwards, I stretched out the timeline even further to show the many major inventions that rapidly followed one after the other.\n\nThe long-term perspective that this chart provides makes it clear just how unusually fast technological change is in our time.\n\nYou can use this visualization to see how technology developed in particular domains. Follow, for example, the history of communication: from writing, to paper, to the printing press, to the telegraph, the telephone, the radio, all the way to the internet and smartphones.\n\nOr follow the rapid development of human flight. In 1903, the Wright brothers took the first flight in human history (they were in the air for less than a minute), and just 66 years later, we landed on the moon. Many people saw both within their lifetimes: the first plane and the moon landing.\n\nThis large visualization also highlights the wide range of technology\u2019s impact on our lives. It includes extraordinarily beneficial innovations, such as the vaccine that allowed humanity to eradicate smallpox, and it includes terrible innovations, like the nuclear bombs that endanger the lives of all of us.\n\nWhat will the next decades bring?\n\nThe red timeline reaches up to the present and then continues in green into the future. Many children born today, even without any further increases in life expectancy, will live well into the 22nd century.\n\nNew vaccines, progress in clean, low-carbon energy, better cancer treatments\u2014a range of future innovations could very much improve our living conditions and the environment around us. But, as I argue in a series of articles, there is one technology that could even more profoundly change our world: artificial intelligence.\n\nOne reason why artificial intelligence is such an important innovation is that intelligence is the main driver of innovation itself. This fast-paced technological change could speed up even more if it\u2019s not only driven by humanity\u2019s intelligence, but artificial intelligence too. If this happens, the change that is currently stretched out over the course of decades might happen within very brief time spans of just a year. Possibly even faster.4\n\nI think AI technology could have a fundamentally transformative impact on our world. In many ways it is already changing our world, as I documented in this companion article. As this technology is becoming more capable in the years and decades to come, it can give immense power to those who control it (and it poses the risk that it could escape our control entirely).\n\nSuch systems might seem hard to imagine today, but AI technology is advancing very fast. Many AI experts believe that there is a very real chance that human-level artificial intelligence will be developed within the next decades, as I documented in this article.\n\nTechnology Will Continue to Change the World\u2014We Should All Make Sure That It Changes It for the Better\n\nWhat is familiar to us today\u2014photography, the radio, antibiotics, the internet, or the International Space Station circling our planet\u2014was unimaginable to our ancestors just a few generations ago. If your great-great-great grandparents could spend a week with you they would be blown away by your everyday life.\n\nWhat I take away from this history is that I will likely see technologies in my lifetime that appear unimaginable to me today.\n\nIn addition to this trend towards increasingly rapid innovation, there is a second long-run trend. Technology has become increasingly powerful. While our ancestors wielded stone tools, we are building globe-spanning AI systems and technologies that can edit our genes.\n\nBecause of the immense power that technology gives those who control it, there is little that is as important as the question of which technologies get developed during our lifetimes. Therefore I think it is a mistake to leave the question about the future of technology to the technologists. Which technologies are controlled by whom is one of the most important political questions of our time, because of the enormous power that these technologies convey to those who control them.\n\nWe all should strive to gain the knowledge we need to contribute to an intelligent debate about the world we want to live in. To a large part this means gaining the knowledge, and wisdom, on the question of which technologies we want.\n\nAcknowledgements: I would like to thank my colleagues Hannah Ritchie, Bastian Herre, Natasha Ahuja, Edouard Mathieu, Daniel Bachler, Charlie Giattino, and Pablo Rosado for their helpful comments to drafts of this essay and the visualization. Thanks also to Lizka Vaintrob and Ben Clifford for a conversation that initiated this visualization.\n\nThis article was originally published on Our World in Data and has been republished here under a Creative Commons license. Read the original article.\n\nImage Credit: Pat Kay / Unsplash"""

print(article_analysis(article, category, details))

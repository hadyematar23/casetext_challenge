import openai
from dotenv import load_dotenv
import os

def query_openai(case_text):
  
  load_dotenv()
  api_key = os.getenv('OPENAI_API_KEY')

  openai.api_key = api_key

  json_string = """
  {
  "data":
  [
  {
  "treated case": here the large language model will provide the name of the case that is being negatively referenced,
  "typeOfTreatment": here the large language model will indicate the type of treatment that is provided, 
  "textOfTreatment": here the large language model will provide the most relevant 2-3 sentences from the text where the case provides negative treatment. Please provide a direct quote or quotes from the text that discusses the negative treatment. Most likely, this will be the part of the excerpt that you relied upon in making your determination that negative treatment occurred., 
  "explanation": here the large language model will provide a brief 2 sentence response as to why you made this determination that the treated case was negatively treated by the case excerpt you have been provided 
  },
  {
  "treated case": here the large language model will provide the name of the case that is being negatively referenced,
  "typeOfTreatment": here the large language model will indicate the type of treatment that is provided, 
  "textOfTreatment": here the large language model will provide the most relevant 2-3 sentences from the text where the case provides negative treatment. Please provide a direct quote or quotes from the text that discusses the negative treatment. Most likely, this will be the part of the excerpt that you relied upon in making your determination that negative treatment occurred., 
  "explanation": here the large language model will provide a brief 2 sentence response as to why you made this determination that the treated case was negatively treated by the case excerpt you have been provided
  }
  ]... and so on and so forth for each case that receives negative treatment
  }"""

  empty_json = """
  {
  "data": 
  []
  }
  """

  parts_of_case = break_prompt_into_parts(case_text, part_size=7000, overlap = 100)

  initial_prompt = f"""This is the first prompt in a set of 2 to 3 prompts that build on each other. It serves as instructions for what you should do with the next prompts you will receive. In the following prompts, you will be given either part of all of the text of an individual legal case. Your task is to identify within the portion of text I provide you the cases that other legal cases that the text refers to and how that text addressed them. If you see that a case is cited multiple times, you only need to return one reference to this case in your response. You are looking to characterize the types of negative treatment that the text I gave you has of the cases it cites. Where the excerpt given provides negative treatment of another case, the excerpt will usually indicate the name of the case it is providing negative treatment of and then some justification, rationale, or logic for why it is negatively treating the case. It is important that you limit your query strictly to the text provided. Do not rely on any of your foundational knowledge or 'inherent knowledge.' I will define negative treatment for you so you know what you are looking for: negative treatment happens when the excerpt you are provided cites to another case but the excerpt you are provided overrules, reverses, distinguishes its facts from, or otherwise criticizes the ruling of the earlier case. The types of negative treatment into which I would like you to categorize each response are as follows: overruled, reversed, questioned, distinguished, criticized, declined to follow, and cited.
  
  There are many ways a case can negatively treat another case. The most extreme is if a case explicitly overturns or overrules the core decision and legal tenant of the case it references. It can also describe a case which one party to the litigation claims that its legal principle would be applicable here but the excerpt will indicate why the court believes that case is different (this is called distinguish). The case could also provide negative treatment of another case by limitings how far the central legal tenet established in the other case goes. It may also simply speak negatively about another case without explicitly changing the fact that the other case is established law.  These are just examples of types of negative treatment are not an exhaustive list of what you man encounter in the prompots I am providing you.  When presenting your findings, return the information in the following JSON format: {json_string}. I need the information to be provided directly in this JSON format, without any text before or after it. Now I will discuss more about how the prompts are broken up. As a case is quite long, I may have to break up the case into several prompts. Each prompt will be around 7000 characters. So the first prompt will be the first 7000 characters of the case, the second prompt will be character 6900-13900. The next prompt is characters 13800-20800 of the text, and so on and so forth. I have provided a 100 character overlap for reasons of continuity. You may receive a prompt that starts in the middle of the case. This happens because of the maximum token size. Just assess it according to the text from the case that you do have and according to the guidelines I have provided you. For this, and only this prompt, you do not need to respond. For the remaining prompts, your response is to be limited to the JSON I have described."""

  conversation = [{"role": "user", "content": initial_prompt}]
  response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=conversation)
  responses = {"response1": response}
  for i, part in enumerate(parts_of_case, start=2):  
    conversation = [
        {"role": "user", "content": initial_prompt},  
        {"role": "assistant", "content": responses[f'response{i-1}']['choices'][0]['message']['content']},  
        {"role": "user", "content": part}  
    ]
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=conversation)
    responses[f"response{i}"] = response

  return responses
    
def break_prompt_into_parts(prompt, part_size, overlap):
    parts = []
    count = 1
    for i in range(0, len(prompt), part_size):
        modified_part =  prompt[i:i + part_size - overlap] 
        parts.append(modified_part)
        count += 1
    return parts




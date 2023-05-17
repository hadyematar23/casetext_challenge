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
  "typeOfTreatment": here the large language model will provide the type of treatment that is provided, 
  "textOfTreatment": here the large language model will provide the most relevant 2-3 sentences from the text where the case provides negative treatment. This must be direct quotes from the text even if it seems awkwardly written, 
  "explanation": here the large language model will provide a brief 2 sentence response as to why you made this determination that the treated case was negatively treated by the case excerpt you have been provided 
  },
  {
  "treated case": "here the large language model will provide the name of the case that is being negatively referenced",
  "typeOfTreatment": "here the large language model will provide the type of treatment that is provided", 
  "textOfTreatment": here the large language model will provide the most relevant 2-3 sentences from the text where the case provides negative treatment. This must be direct quotes from the text even if it seems awkwardly written, 
  "explanation": here the large language model will provide a brief 2 sentence response as to why you made this determination that the treated case was negatively treated by the case excerpt you have been provided 
  }
  ]... and so on and so forth
  }"""

  empty_json = """
  {
  "data": 
  []
  }
  """

  parts_of_case = break_prompt_into_parts(case_text, part_size=9000)

  initial_prompt = f"""This is the first prompt in a set of prompts that build on each other. In the following prompts, you will be given either part of all of the text of an individual legal case. I will refer to the entirity of the case as Case A throughout this set of prompts. Your task is to identify if the portion of text I provide you of Case A provides 'negative treatment' of any other case. It is important that you limit your query strictly to the text of Case A and your analysis of negative treatment is based on the text that I have provided you for the prompt. Do not rely on any of your foundational knowledge or 'inherent knowledge.' Negative treatment happens when a case published at a later date than another case overrules, reverses, challenges, fails to follow, distinguishes its facts from, fails to follow, or otherwise criticizes the ruling of an earlier case. In a situation where Case A provides negative treatment of another case, Case A will explicitly indicate the name of the case it is providing negative treatment and then some justification for why it is negatively treating the case. There are many ways Case A can negatively treat another case. The most extreme is if Case A explicitly overturns or overrules the core decision and legal tenant of the case it references. Case A could also provide negative treatment of another case by limitings how far the central legal tenet established in the other case goes. It may also simply speak negatively about another case without explicitly changing the fact that the other case is established law. It can also describe a case which may appear to have a controlling legal tenet that would apply here but explain how Case A or the other case are in fact different. The types of negative treatment into which I would like you to categorize each response are as follows: overruled, reversed, questioned, disapproved, distinguished, limited, superseded, limited, declined to follow, and. When presenting your findings, return the information in the following JSON format: {json_string}. If you do not find any cases that have been negatively treated within the input, then return this json: {empty_json} . I need the information to be provided directly in this JSON format, without any text before or after it. As the case is quite long, I will have to break up the case into several prompts, but I have structured it in such a way that you will have memory of the previous prompts. Each prompt will be around 10000 characters. So the first prompt will the first 10000 characters of the case, the second prompt will be the second 10000 prompts of the case, and so on and so forth. The prompts will be numbered so you can keep track of them as such. I will start the prompt with THIS IS THE BEGINNING OF PART 1 OF THE CASE and end it with THIS IS THE END OF PART 1 OF THE CASE. The next prompt will read THIS IS THE BEGINNING OF PART 2 OF THE CASE and end with THIS IS THE END OF PART 2 OF THIS CASE. You may find yourself at a situation where you are starting at PART 2 (or PART 3) of the case and do not know what is in Part 1 of the case. This happens because of the maximum token size. Just assess it according to the text from the case that you do have and according to the guidelines I have provided you. For this, and only this prompt, you do not need to respond. For the remaining prompts, your response is to be limited to the JSON I have described."""

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
    
def break_prompt_into_parts(prompt, part_size):
    parts = []
    count = 1
    for i in range(0, len(prompt), part_size):
        modified_part = f"THIS IS THE BEGINNING OF PART {count} OF THE CASE" + prompt[i:i + part_size] + f"THIS IS THE END OF PART {count} OF THE CASE"
        parts.append(modified_part)
        count += 1
    return parts




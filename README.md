# Hady Matar Tech Challenge for Casetext

This code was created as part of a code/tech challenge application process for the Backend and Prompt Engineer Position at Casetext. 

To setup: 

First, clone down the repo to your local device. When you open it, you should see: 
```
function.py 
main.py 
openaicall.py 
requirements.txt
.gitignore 
``` 

The API call relies on OpenAI 'gpt-3.5-turbo'. You can make your own API key for that [here](https://platform.openai.com/account/api-keys)

Then, you can create the virtual environment, actiavte it, and install the dependencies: 

```
python3 -m venv env 
source env/bin/activate
pip install -r requirements.txt
```

Next, you will need to create a folder in the root directory named '.env' which will be where your API key is housed: 

From the root directory: 
```
touch .env
```

Copy and paste the following into the .env file, replacing [INSERT YOUR KEY HERE] with your actual API key as a string. 

OPENAI_API_KEY= [INSERT YOUR KEY HERE]

## Functionality 

This code will permit you to insert the SLUG for a case in the 'main.py' folder where it says [INSERT SLUG HERE] and then run: 

```
python3 main.py 
```
If you insert a pdb breakpoint on line 4 of the main.py file, you can inspect the result. You can also add a print(treatments) on line 4 so it prints to the console. 

Additionally, you can enter a python shell and call the function there: 

```
python3
from function import extract_negative_treatments
treatments = extract_negative_treatments(slug='in-re-lee-342013')
```
After these run, you can inspect the variable treatments within the python shell. 

## Extension and Areas to Improve 

The most difficult part of this was figuring out how to have the query stay under 4097 tokens given the length of some of the cases. I dealt with this by breaking up the cases into portions of a certain character limit and running a query on each portion, including, along with the query, the prompt and the previous portion of the case that had been fed into the large language model. The ideal balance would be to find a portion size that is large enought to minimize the number of queries you are running but small enough that the code does not break. Most of the time, this worked with 8000-10000 character queries but, occasionally, it broke. For this reason, I chose a conservative number -- 7000 characters. An extension would look at how this could be optimized.  


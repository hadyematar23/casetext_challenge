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

## Response Structure

For each prompt, the relevant portion returned is a JSON string formatted as such: 

```
{
  "data":
  [
  {
  "treated case": the treated case,
  "typeOfTreatment": type of treatment provided, 
  "textOfTreatment": a direct quote from the case where it provides this treatment, 
  "explanation": the large language model's explanation  
}
```
Each treated case is a separate JSON string with this information. 

The ultimate structure returned will be an accumulation of the various prompts. For example, if you run 

```
python3
from function import extract_negative_treatments
treatments = extract_negative_treatments(slug='in-re-lee-342013')
```
treatments is a list, with each element of the list being a JSON string made up of the response from that prompt. 

This is what a sample element of treatments would look like: 


>>> treatments[0]
'{\n  "data": [\n    {\n      "treated case": "Plotkin v. Plotkin, Del.Super., 32 Del. 455, 125 A. 455 (1924)",\n      "typeOfTreatment": "overruled",\n      "textOfTreatment": "The trial court\'s decision granting summary judgment is based upon the Doctrine. This antiquated doctrine was first applied by Delaware courts in the seminal case of Plotkin v. Plotkin, Del.Super., 32 Del. 455, 125 A. 455 (1924).",\n      "explanation": "The excerpt clearly states that the Doctrine was first applied by Delaware courts in the case of Plotkin v. Plotkin. This also implies that the ruling in that case established the Doctrine and served as legal precedent. However, in this excerpt, it is stated that the Doctrine is an antiquated doctrine and is no longer viable concept and meets the needs of modern society. Therefore, it can be concluded that the ruling in Plotkin v. Plotkin has been overruled by this case."\n    },\n    {\n      "treated case": "Alfree v. Alfree, Del.Supr., 410 A.2d 161, 162 (1979)",\n      "typeOfTreatment": "overruled",\n      "textOfTreatment": "After most recently reviewing the Doctrine in 1979, this Court held that \\"it retains sufficient merit to warrant continued adherence.\\" Alfree v. Alfree, Del.Supr., 410 A.2d 161, 162 (1979).",\n      "explanation": "The excerpt indicates that prior to the current case, the most recent review of the Doctrine was done in Alfree v. Alfree and the court decided that the Doctrine should be adhered to as it still retains sufficient merit. However, in the current case, the court has decided that the Doctrine no longer meets the needs of modern society and is no longer viable. Therefore, it can be concluded that the ruling in Alfree v. Alfree has been overruled by this case."\n    }\n  ]\n}'


The JSON would need to be parsed so that you can work with it. 

## Extensions and Areas to Improve in Future iterations: Notes Regarding Funtionality of Prompt 

### Overinclusiveness 

I found that the prompt functioned much more robustly if I did not try to excessively try to limit it to only negative treatment. When I did that, I found that it would often fail to return many cases. As a result, some of the prompts may return a case that was cited without any negative treatment, with the JSON structure indicating that the case was "cited." In a further iteration, I would have gone through and removed any dictionaries in which the "typeOfTreatment" was listed as "cited."

Obviously, this has the unintended impact of raising the computing costs required, both potentially in terms of price and the length of time the API call takes. Further iterations would work on the redundancy of the prompt. As a design choice given the requested time constraints, I chose to overinclude cases with an easy signifier that would permit us to exclude them if we choose. 

### Token Restrictions 

The most difficult part of this was figuring out how to have the query stay under 4097 tokens given the length of some of the cases. I dealt with this by breaking up the cases into portions of a certain character limit and running a query on each portion, including, along with the query, the prompt and the previous portion of the case that had been fed into the large language model. The ideal balance would be to find a portion size that is large enought to minimize the number of queries you are running but small enough that the code does not break. Most of the time, this worked with 8000-10000 character queries but, occasionally, it broke. For this reason, I chose a conservative number -- 7000 characters. An extension would look at how this could be optimized. 

### Case Repitition 

Because I had to break up the case into several prompts and token restrictions, prompt 3 may not know that prompt 1 already dealt with the same case. Some cases, as such, may be repeated. Similar to the concerns regarding overinclusiveness, you could manually remove those cases, or run a separate GPT API call to condense them into one. 



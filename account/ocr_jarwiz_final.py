
import google.generativeai as genai
from pathlib import Path
"""## SET API KEY"""

# Used to securely store your API key
#from google.colab import userdata
GOOGLE_API_KEY='AIzaSyC3DPlgi-CbVswU70CiQxm9XwjDyi_2eIY'
#GOOGLE_API_KEY=userdata.get('GOOGLE_API_KEY')

verified = False
genai.configure(api_key=GOOGLE_API_KEY)


"""## LIST OF MODELS"""

for m in genai.list_models():
  if 'generateContent' in m.supported_generation_methods:
    print(m.name)

# Model Configuration
MODEL_CONFIG = {
  "temperature": 0.2,
  "top_p": 1,
  "top_k": 32,
  "max_output_tokens": 4096,
}

## Safety Settings of Model
safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]




model = genai.GenerativeModel(model_name = "gemini-pro-vision",
                              generation_config = MODEL_CONFIG,
                              safety_settings = safety_settings)


@staticmethod
def image_format(image_path):
  global imgpath
  imgpath=image_path
  img = Path(image_path)
  verified = True
  if not img.exists():
    raise FileNotFoundError(f"Could not find image: {img}")

  image_parts = [
        {
            "mime_type": "image/png", ## Mime type are PNG - image/png. JPEG - image/jpeg. WEBP - image/webp
            "data": img.read_bytes()
        }
    ]
  return image_parts

"""## GEMINI MODEL OUTPUT"""

def gemini_output(image_path, system_prompt, user_prompt):
  
  image_info = image_format(image_path)
  input_prompt = [system_prompt, image_info[0], user_prompt]
  response = model.generate_content(input_prompt)
  return response.text
  
#from google.colab import drive
#drive.mount('/content/drive')



#gemini_output(image_path,system_prompt,user_prompt)



#system_prompt = "Convert Invoice data into json format with appropriate json tags as required for the data in image "

#user_prompt = "Convert  data into json format with the company name and the appropriate json tags as required for the data in image "
#user_prompt="Classify the file as one of the following:Tickets, Hotel vouchers, Legal agreements, Bank statements, Expense vouchers, Medical report"





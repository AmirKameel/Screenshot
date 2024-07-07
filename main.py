import os
import base64
import requests
import webbrowser
import csv
from dotenv import load_dotenv
from flask import Flask, render_template_string, send_file
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
import os
import base64
import requests
import webbrowser
from dotenv import load_dotenv
from flask import Flask, render_template_string

from taipy.gui import Gui, notify
import taipy.gui.builder as tgb

from PIL import Image

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

index = 0
query_image_path = ""
query_message = ""
messages = []
gpt_messages = []
messages_dict = {}
current_task = ""
generated_file_paths = []
latest_html_code = ""




# Function to log data to CSV (if required for the application)
def log_to_csv(user_input, response):
    csv_file_path = "chat_log.csv"
    if not os.path.exists(csv_file_path):
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["User Input", "Generated Site"])
    with open(csv_file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([user_input, response])


        

def on_init(state):
    state.conv.update_content(state, "")
    state.messages_dict = {}
    initial_instruction = {
        'role': 'system',
        'content': """You are an expert Tailwind developer"""
    }
    state.messages = [
        {
            "role": "assistant",
            "style": "assistant_message",
            "content": "Welcome to Webmecano! Please choose an option:",
        },
    ]
    state.gpt_messages = [initial_instruction]
    new_conv = create_conv(state)
    state.conv.update_content(state, new_conv)

def create_conv(state):
    messages_dict = {}
    with tgb.Page() as conversation:
        for i, message in enumerate(state.messages):
            text = message["content"].replace("<br>", "\n").replace('"', "'")
            messages_dict[f"message_{i}"] = text
            tgb.text(
                "{messages_dict['" + f"message_{i}" + "'] if messages_dict else ''}",
                class_name=f"message_base {message['style']}",
                mode="md",
            )
            if message["role"] == "assistant" and i == len(state.messages) - 1:
                if message["content"] == "Welcome to Webmecano! Please choose an option:":
                    tgb.button(
                        "Convert Screenshot to Website",
                        class_name="w-1/2 mt-8 mr-2 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded",
                        id="screenshot_to_website_button",
                        on_action=choose_screenshot_to_website,
                    )
                    tgb.button(
                        "Create Website from Scratch",
                        class_name="w-1/2 mt-4 mr-2 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded",
                        id="website_from_scratch_button",
                        on_action=choose_website_from_scratch,
                    )
                elif "Your site has been generated" in message["content"]:
                    tgb.button(
                        "View Generated Site",
                        class_name="fullwidth plain",
                        id=f"view_site_button_{i}",
                        on_action=view_generated_site,
                    )
    state.messages_dict = messages_dict
    return conversation

def choose_screenshot_to_website(state):
    global current_task
    current_task = "screenshot_to_website"
    website_name=""
    User_first_name=""
    user_last_name=""
    user_email=""
    website_catogery=""
    additional_info=""

    state.gpt_messages.append({
        "role": "system",
        "content": """
   Gather User Information:
one by one:
First Name
Last Name
Email
Website Name
Website Category
Confirm the Information:

Ask the user to confirm the provided information.
If they say "no," ask for corrections and confirm again.

After confirming the information, ask the user for the screenshot.

        You are an expert Tailwind developer.
        You take screenshots of a reference web page from the user and then build single-page apps using Tailwind, HTML, and JS.
        You might also be given a screenshot (The second image) of a web page that you have already built and asked to update it to look more like the reference image (The first image).
        do not reply with any text explanation like got it or here is the code or anything. just reply with the code:
        - Make sure the app looks exactly like the screenshot.
        -Return only the full code in <html></html> tags.
        Do not include markdown "```" or "```html" at the start or end.
        - Pay close attention to background color, text color, font size, font family, padding, margin, border, etc. Match the colors and sizes exactly.
        - Use the exact text from the screenshot.
        - Do not add comments in the code such as "<!-- Add other navigation links as needed -->" and "<!-- ... other news items ... -->". Write the full code.
        - Repeat elements as needed to match the screenshot. For example, if there are 15 items, the code should have 15 items. Do not leave comments like "<!-- Repeat for each news item -->".
        - For images, use placeholder images from https://placehold.co and include a detailed description of the image in the alt text so that an image generation AI can generate the image later.
        For Arabic websites:
        Implement right-to-left (RTL) text direction. Use dir="rtl" and class="text-right" where appropriate.
        Use Arabic fonts or specific fonts as shown in the screenshot. Google Fonts can be used if specified.
        Pay special attention to text alignment and direction, especially for mixed content with both Arabic and English text.
        Use the exact text from the screenshot, including Arabic text if present.
        - Every time user ask for updates just update the latest code you did then send another message ask for the feedback from the user.
        In terms of libraries,
        - Use this script to include Tailwind: <script src="https://cdn.tailwindcss.com"></script>
        - You can use Google Fonts.
        - Font Awesome for icons: <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css"></link>
  
        """
    })
    state.messages.append(
        {
            "role": "assistant",
            "style": "assistant_message",
            "content": "Great! please provide your first name",
        }
    )
    state.conv.update_content(state, create_conv(state))

def choose_website_from_scratch(state):
    global current_task
    current_task = "website_from_scratch"
    website_name=""
    User_first_name=""
    user_last_name=""
    user_email=""
    website_catogery=""
    additional_info=""

    state.gpt_messages.append({
        "role": "system",
        "content": """
       Gather User Information:
one by one:
First Name
Last Name
Email
Website Name
Website Category
website details
Confirm the Information:

Ask the user to confirm the provided information.
If they say "no," ask for corrections and confirm again.
Generate the HTML Code:

Use the confirmed information to edit a webpage with the given template.
edit the title and the paragraphs and headlines make the same code but with the user specifications
- For images, use placeholder images from https://placehold.co and include a detailed description of the image in the alt text so that an image generation AI can generate the image later.
just reply with the code not any text explantion
No additional comments in the HTML.
here is the template : 
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Small Apps | Bootstrap App Landing Template</title>
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="description" content="Bootstrap App Landing Template">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
  <meta name="author" content="Themefisher">
  <meta name="generator" content="Themefisher Small Apps Template v1.0">

  <!-- Favicon -->
  <link rel="shortcut icon" href="images/favicon.png" />

  <!-- CSS -->
  <link rel="stylesheet" href="plugins/bootstrap/bootstrap.min.css">
  <link rel="stylesheet" href="plugins/themify-icons/themify-icons.css">
  <link rel="stylesheet" href="plugins/slick/slick.css">
  <link rel="stylesheet" href="plugins/slick/slick-theme.css">
  <link rel="stylesheet" href="plugins/fancybox/jquery.fancybox.min.css">
  <link rel="stylesheet" href="plugins/aos/aos.css">
  <link rel="stylesheet" href="css/style.css">
</head>
<body class="body-wrapper" data-spy="scroll" data-target=".privacy-nav">

<nav class="navbar main-nav navbar-expand-lg px-2 px-sm-0 py-2 py-lg-0">
  <div class="container">
    <a class="navbar-brand" href="index.html"><img src="images/logo.png" alt="logo"></a>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav">
      <span class="ti-menu"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav ml-auto">
        <li class="nav-item dropdown active">
          <a class="nav-link dropdown-toggle" href="#" data-toggle="dropdown">Home <span><i class="ti-angle-down"></i></span></a>
          <ul class="dropdown-menu">
            <li><a class="dropdown-item active" href="index.html">Homepage</a></li>
            <li><a class="dropdown-item" href="homepage-2.html">Homepage 2</a></li>
            <li><a class="dropdown-item" href="homepage-3.html">Homepage 3</a></li>
            <li class="dropdown-submenu">
              <a class="dropdown-item dropdown-toggle" href="#!" id="dropdown0301" role="button" data-toggle="dropdown">Sub Menu</a>
              <ul class="dropdown-menu" aria-labelledby="dropdown0301">
                <li><a class="dropdown-item" href="index.html">Submenu 11</a></li>
                <li><a class="dropdown-item" href="index.html">Submenu 12</a></li>
              </ul>
            </li>
          </ul>
        </li>
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" href="#" data-toggle="dropdown">Pages <span><i class="ti-angle-down"></i></span></a>
          <ul class="dropdown-menu">
            <li><a class="dropdown-item" href="team.html">Team</a></li>
            <li><a class="dropdown-item" href="career.html">Career</a></li>
            <li><a class="dropdown-item" href="blog.html">Blog</a></li>
            <li><a class="dropdown-item" href="blog-single.html">Blog Single</a></li>
            <li><a class="dropdown-item" href="privacy-policy.html">Privacy</a></li>
            <li><a class="dropdown-item" href="FAQ.html">FAQ</a></li>
            <li><a class="dropdown-item" href="sign-in.html">Sign In</a></li>
            <li><a class="dropdown-item" href="sign-up.html">Sign Up</a></li>
            <li><a class="dropdown-item" href="404.html">404</a></li>
            <li><a class="dropdown-item" href="comming-soon.html">Coming Soon</a></li>
            <li class="dropdown-submenu">
              <a class="dropdown-item dropdown-toggle" href="#!" id="dropdown0501" role="button" data-toggle="dropdown">Sub Menu</a>
              <ul class="dropdown-menu" aria-labelledby="dropdown0501">
                <li><a class="dropdown-item" href="index.html">Submenu 21</a></li>
                <li><a class="dropdown-item" href="index.html">Submenu 22</a></li>
              </ul>
            </li>
          </ul>
        </li>
        <li class="nav-item"><a class="nav-link" href="about.html">About</a></li>
        <li class="nav-item"><a class="nav-link" href="contact.html">Contact</a></li>
      </ul>
    </div>
  </div>
</nav>

<section class="section gradient-banner">
  <div class="shapes-container">
    <div class="shape" data-aos="fade-down-left" data-aos-duration="1500" data-aos-delay="100"></div>
    <div class="shape" data-aos="fade-down" data-aos-duration="1000" data-aos-delay="100"></div>
    <div class="shape" data-aos="fade-up-right" data-aos-duration="1000" data-aos-delay="200"></div>
    <div class="shape" data-aos="fade-up" data-aos-duration="1000" data-aos-delay="200"></div>
    <div class="shape" data-aos="fade-down-left" data-aos-duration="1000" data-aos-delay="100"></div>
    <div class="shape" data-aos="zoom-in" data-aos-duration="1000" data-aos-delay="300"></div>
    <div class="shape" data-aos="fade-down-right" data-aos-duration="500" data-aos-delay="200"></div>
    <div class="shape" data-aos="zoom-out" data-aos-duration="2000" data-aos-delay="500"></div>
  </div>
  <div class="container">
    <div class="row align-items-center">
      <div class="col-md-6 order-2 order-md-1 text-center text-md-left">
        <h1 class="text-white font-weight-bold mb-4">Showcase your app with Small Apps</h1>
        <p class="text-white mb-5">Besides its beautiful design. Laapp is an incredibly rich core framework for you to showcase your App.</p>
        <a href="FAQ.html" class="btn btn-main-md">Download Now</a>
      </div>
      <div class="col-md-6 text-center order-1 order-md-2">
        <img class="img-fluid" src="images/mobile.png" alt="screenshot">
      </div>
    </div>
  </div>
</section>

<section class="section pt-0 position-relative pull-top">
  <div class="container">
    <div class="rounded shadow p-5 bg-white">
      <div class="row text-center">
        <div class="col-lg-4 col-md-6 mt-5 mt-md-0">
          <i class="ti-paint-bucket text-primary h1"></i>
          <h3 class="mt-4 text-capitalize h5">Themes Made Easy</h3>
          <p class="regular text-muted">Lorem ipsum dolor sit amet consectetur adipisicing elit. Aliquam non, recusandae tempore ipsam dignissimos molestias.</p>
        </div>
        <div class="col-lg-4 col-md-6 mt-5 mt-md-0">
          <i class="ti-shine text-primary h1"></i>
          <h3 class="mt-4 text-capitalize h5">Powerful Design</h3>
          <p class="regular text-muted">Lorem ipsum dolor sit amet consectetur adipisicing elit. Aliquam non, recusandae tempore ipsam dignissimos molestias.</p>
        </div>
        <div class="col-lg-4 col-md-12 mt-5 mt-lg-0">
          <i class="ti-thought text-primary h1"></i>
          <h3 class="mt-4 text-capitalize h5">Creative Content</h3>
          <p class="regular text-muted">Lorem ipsum dolor sit amet consectetur adipisicing elit. Aliquam non, recusandae tempore ipsam dignissimos molestias.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="feature section pt-0">
  <div class="container">
    <div class="row">
      <div class="col-lg-6 ml-auto">
        <div class="image-content" data-aos="fade-right">
          <img class="img-fluid" src="images/feature/feature-new-01.jpg" alt="ipad">
        </div>
      </div>
      <div class="col-lg-6 mr-auto align-self-center">
        <div class="feature-content">
          <h2>Small Apps launch faster than ever</h2>
          <p class="desc">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Eveniet ipsa nulla delectus earum ratione tempore maiores, numquam temporibus in labore, laborum.</p>
          <ul class="feature-list">
            <li><i class="ti-check"></i>Fully Responsive</li>
            <li><i class="ti-check"></i>Multi-Device Testing</li>
            <li><i class="ti-check"></i>Clean & Modern Design</li>
            <li><i class="ti-check"></i>Great User Experience</li>
          </ul>
          <a href="about.html" class="btn btn-main-md">Learn More</a>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="row">
      <div class="col-lg-10 mx-auto">
        <div class="section-title text-center">
          <h2>Pricing Plan</h2>
          <p class="mb-5">Lorem ipsum dolor sit amet consectetur adipisicing elit. Voluptatem quia eligendi, fugit ex aspernatur reiciendis, velit sed, atque minima ipsa nisi.</p>
        </div>
        <div class="pricing-table">
          <div class="row text-center">
            <div class="col-lg-4 col-md-6">
              <div class="single-table">
                <div class="table-top">
                  <h3>Free</h3>
                  <p class="price"><span>$</span>00</p>
                </div>
                <ul class="table-content">
                  <li><i class="ti-check"></i>1 GB Storage</li>
                  <li><i class="ti-check"></i>Single User</li>
                  <li><i class="ti-check"></i>Minimal Features</li>
                  <li><i class="ti-close"></i>No Customer Support</li>
                  <li><i class="ti-close"></i>No Updates</li>
                </ul>
                <div class="table-bottom">
                  <a href="#" class="btn btn-main-md">Choose Plan</a>
                </div>
              </div>
            </div>
            <div class="col-lg-4 col-md-6">
              <div class="single-table">
                <div class="table-top">
                  <h3>Standard</h3>
                  <p class="price"><span>$</span>49</p>
                </div>
                <ul class="table-content">
                  <li><i class="ti-check"></i>10 GB Storage</li>
                  <li><i class="ti-check"></i>Up to 5 Users</li>
                  <li><i class="ti-check"></i>Standard Features</li>
                  <li><i class="ti-check"></i>Email Support</li>
                  <li><i class="ti-close"></i>No Updates</li>
                </ul>
                <div class="table-bottom">
                  <a href="#" class="btn btn-main-md">Choose Plan</a>
                </div>
              </div>
            </div>
            <div class="col-lg-4 col-md-6 mx-auto">
              <div class="single-table">
                <div class="table-top">
                  <h3>Premium</h3>
                  <p class="price"><span>$</span>99</p>
                </div>
                <ul class="table-content">
                  <li><i class="ti-check"></i>Unlimited Storage</li>
                  <li><i class="ti-check"></i>Unlimited Users</li>
                  <li><i class="ti-check"></i>All Features</li>
                  <li><i class="ti-check"></i>24/7 Support</li>
                  <li><i class="ti-check"></i>Free Updates</li>
                </ul>
                <div class="table-bottom">
                  <a href="#" class="btn btn-main-md">Choose Plan</a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- JavaScript -->
<script src="plugins/jQuery/jquery.min.js"></script>
<script src="plugins/bootstrap/bootstrap.min.js"></script>
<script src="plugins/slick/slick.min.js"></script>
<script src="plugins/fancybox/jquery.fancybox.min.js"></script>
<script src="plugins/syotimer/jquery.syotimer.min.js"></script>
<script src="plugins/aos/aos.js"></script>
<script src="js/script.js"></script>
</body>
</html>

        """
    })
    state.messages.append(
        {
            "role": "assistant",
            "style": "assistant_message",
            "content": "Great! please provide your first name",
        }
    )
    state.conv.update_content(state, create_conv(state))

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def query_gpt4o(state):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}",
    }

    if current_task == "screenshot_to_website" and state.query_image_path != "":
        base64_image = encode_image(state.query_image_path)
        message = {
            "role": "user",
            "content": [
                {"type": "text", "text": f"{state.query_message}"},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                },
            ],
        }
    else:
        message = {
            "role": "user",
            "content": [{"type": "text", "text": f"{state.query_message}"}],
        }

    state.gpt_messages.append(message)

    payload = {
        "model": "gpt-4o",
        "messages": state.gpt_messages,
        "max_tokens": 4000,
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
    )

    if response.status_code != 200:
        notify(state, "error", "Failed to query GPT-4o API")
        return "Sorry, there was an error with the API request."

    response_json = response.json()

    if "choices" not in response_json or len(response_json["choices"]) == 0:
        notify(state, "error", "Unexpected API response format")
        return "Sorry, there was an error with the API response."

    return response_json["choices"][0]["message"]["content"].replace("\n\n", "\n")

def is_change_request(query):
    change_keywords = ["change", "improve", "update", "modify", "enhance", "alter", "revise", "edit", "tweak", "refine", "adjust", "add", "remove", "delete", "make"]
    return any(keyword in query.lower() for keyword in change_keywords)

        

def send_message(state):
    global index
    global generated_file_paths
    global latest_html_code

    if state.query_image_path and current_task == "screenshot_to_website":
        state.messages.append(
            {
                "role": "user",
                "style": "user_message",
                "content": f"{state.query_message}\n![user_image]({state.query_image_path})",
            }
        )
    else:
        state.messages.append(
            {
                "role": "user",
                "style": "user_message",
                "content": state.query_message,
            }
        )
    
    state.conv.update_content(state, create_conv(state))
    notify(state, "info", "Sending message...")

    if is_change_request(state.query_message) and latest_html_code:
        state.gpt_messages.append({
            "role": "system",
            "content": f"The current version of the site is:\n\n{latest_html_code}\n\nMake the requested changes to this code."
        })
    
    response_content = query_gpt4o(state)
    
    state.messages.append(
        {
            "role": "assistant",
            "style": "assistant_message",
            "content": response_content,
        }
    )
    state.conv.update_content(state, create_conv(state))
    
    log_to_csv(state.query_message, response_content)
    
    state.query_message = ""
    state.query_image_path = ""

    if current_task in ["screenshot_to_website", "website_from_scratch"]:
        latest_html_code = response_content
        
        generated_file_paths = [save_html_response(latest_html_code, f"generated_site_{index}.html")]

    notify(state, "success", "Your site has been generated! Use the button in the sidebar to view it.")
    index += 1

def save_html_response(content, filename):
    if not os.path.exists('generated_sites'):
        os.makedirs('generated_sites')

    file_path = f"generated_sites/{filename}"
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    return file_path


def view_generated_site(state):

     global generated_file_paths

     paths = []
     for path in generated_file_paths:
         if os.path.exists(path):
             paths.append(f'https://webmecano.onrender.com/generated_sites/'+os.path.basename(path))
         else:
             notify(state, "error", f"Generated file {path} not found.")
     if paths:
         paths_text = "\n".join(paths)
         notify(state, "info", f"Generated file paths:\n{paths_text}")
     else:
         notify(state, "error", "No valid generated site found to display.")

def upload_image(state):
    global index
    image = Image.open(state.query_image_path)
    image.thumbnail((300, 300))
    image.save(f"images/example_{index}.png")
    state.query_image_path = f"images/example_{index}.png"
    index += 1
    send_message(state)

def reset_chat(state):
    global current_task
    global latest_html_code
    current_task = ""
    latest_html_code = ""
    state.messages = []
    state.gpt_messages = []
    state.query_message = ""
    state.query_image_path = ""
    state.conv.update_content(state, create_conv(state))
    on_init(state)

with tgb.Page() as page:
    with tgb.layout(columns="300px 1"):
        with tgb.part(class_name="sidebar"):
            tgb.text("## Build your website with webmecano", mode="md")
            tgb.button(
                "New Conversation",
                class_name="fullwidth plain",
                id="reset_app_button",
                on_action=reset_chat,
            )
            tgb.html("br")
            tgb.image(
                content="{query_image_path}", width="250px", class_name="image_preview"
            )
            tgb.button(
                "View Generated Site",
                class_name="fullwidth mt-2 bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded",
                id="view_generated_site_button",
                on_action=view_generated_site,
            )

        with tgb.part(class_name="p1"):
            tgb.part(partial="{conv}", height="600px", class_name="card card_chat")
            with tgb.part("card mt1"):
                tgb.input(
                    "{query_message}",
                    on_action=send_message,
                    change_delay=-1,
                    label="Write your message:",
                    class_name="fullwidth",
                )
                tgb.file_selector(
                    content="{query_image_path}",
                    on_action=upload_image,
                    extensions=".jpg,.jpeg,.png",
                    label="Upload an image",
                    change_delay=0
                )


#m flask import Flask, render_template_string

# Initialize the Flask application
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))  # Use the PORT environment variable or default to 5000
    gui = Gui(page)
    conv = gui.add_partial("")
    print(f"Running server on http://0.0.0.0:{port}")
    gui.run(host="0.0.0.0", port=port, title="webmecano",dark_mode=False, margin="0px",debug=True)

#if __name__ == "__main__":
#    gui = Gui(page)
#    conv = gui.add_partial("")
#    gui.run(title="🤖Webmecano", dark_mode=False, margin="0px", debug=True)

#else:
#    flask_app.run(host='0.0.0.0', port=5000, debug=True)



import os
import base64
import requests
import webbrowser
from flask import Flask, render_template, request, redirect, url_for, jsonify
from dotenv import load_dotenv
from PIL import Image
from taipy.gui import Gui, notify
import taipy.gui.builder as tgb

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

index = 0
query_image_path = ""
query_message = ""
messages = []
gpt_messages = []
messages_dict = {}

generated_file_path = ""  # Global variable to store the latest generated file path

def on_init(state):
    state.conv.update_content(state, "")
    state.messages_dict = {}
    initial_instruction = {
        'role': 'system',
        'content': """You are an expert Tailwind developer
You take screenshots of a reference web page from the user, and then build single page apps 
using Tailwind, HTML and JS.
You might also be given a screenshot(The second image) of a web page that you have already built, and asked to
update it to look more like the reference image(The first image).

- Make sure the app looks exactly like the screenshot.
- Pay close attention to background color, text color, font size, font family, 
padding, margin, border, etc. Match the colors and sizes exactly.
- Use the exact text from the screenshot.
- Do not add comments in the code such as "<!-- Add other navigation links as needed -->" and "<!-- ... other news items ... -->" in place of writing the full code. WRITE THE FULL CODE.
- Repeat elements as needed to match the screenshot. For example, if there are 15 items, the code should have 15 items. DO NOT LEAVE comments like "<!-- Repeat for each news item -->" or bad things will happen.
- For images, use placeholder images from https://placehold.co and include a detailed description of the image in the alt text so that an image generation AI can generate the image later.

In terms of libraries,

- Use this script to include Tailwind: <script src="https://cdn.tailwindcss.com"></script>
- You can use Google Fonts
- Font Awesome for icons: <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css"></link>

Return only the full code in <html></html> tags.
Do not include markdown "```" or "```html" at the start or end. if the user ask for updates return all the code with any explainations just return all the code"""
    }
    state.messages = [
        {
            "role": "assistant",
            "style": "assistant_message",
            "content": "Hi, Frontend developer! please provide your screenshot",
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
                tgb.button(
                    "View Generated Site",
                    class_name="fullwidth plain",
                    id=f"view_site_button_{i}",
                    on_action=view_generated_site,
                )
    state.messages_dict = messages_dict
    return conversation

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def query_gpt4o(state):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}",
    }

    if state.query_image_path != "":
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
        "max_tokens": 3000,
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

def send_message(state):
    global index
    global generated_file_path  # Ensure we use the global variable

    if state.query_image_path == "":
        state.messages.append(
            {
                "role": "user",
                "style": "user_message",
                "content": state.query_message,
            }
        )
    else:
        state.messages.append(
            {
                "role": "user",
                "style": "user_message",
                "content": f"{state.query_message}\n![user_image]({state.query_image_path})",
            }
        )
    state.conv.update_content(state, create_conv(state))
    notify(state, "info", "Sending message...")
    response_content = query_gpt4o(state)
    state.messages.append(
        {
            "role": "assistant",
            "style": "assistant_message",
            "content": response_content,
        }
    )
    state.conv.update_content(state, create_conv(state))
    state.query_message = ""
    state.query_image_path = ""

    # Save the response content to an HTML file
    generated_file_path = save_html_response(response_content)
    index += 1  # Increment the index after saving

def save_html_response(content):
    global index  # Ensure we use the global variable

    # Ensure the directory exists
    if not os.path.exists('generated_sites'):
        os.makedirs('generated_sites')

    # Save the HTML content to a file
    file_path = f"generated_sites/generated_site_{index}.html"
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    return file_path

def view_generated_site(state):
    global generated_file_path  # Ensure we use the global variable

    if os.path.exists(generated_file_path):
        webbrowser.open('file://' + os.path.realpath(generated_file_path))
    else:
        notify(state, "error", "No generated site found to display.")

def upload_image(state):
    global index
    image = Image.open(state.query_image_path)
    image.thumbnail((300, 300))
    image.save(f"images/example_{index}.png")
    state.query_image_path = f"images/example_{index}.png"
    index += 1

def reset_chat(state):
    state.messages = []
    state.gpt_messages = []
    state.query_message = ""
    state.query_image_path = ""
    state.conv.update_content(state, create_conv(state))
    on_init(state)

with tgb.Page() as page:
    with tgb.layout(columns="300px 1"):
        with tgb.part(class_name="sidebar"):
            tgb.text("## Screenshot to code", mode="md")
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
                )

if __name__ == "__main__":
    gui = Gui(page)
    conv = gui.add_partial("")
    gui.run(title="🤖Webmecano", dark_mode=False, margin="0px", debug=True)

import os
import base64
import requests
import webbrowser
from dotenv import load_dotenv

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

generated_file_path = ""  # Global variable to store the latest generated file path


def on_init(state):
    state.conv.update_content(state, "")
    state.messages_dict = {}
    initial_instruction = {
        'role': 'system',
        'content': """Design a fantastic website with the following specifications:
You are an expert frontend developer
first ask the user you want to a screenshot to code or website from scartch based on your queiries
You take screenshots of a reference web page from the user, and then build single page apps 
using HTML, CSS and JS.
You might also be given a screenshot(The second image) of a web page that you have already built, and asked to
update it to look more like the reference image(The first image).

- Make sure the app looks exactly like the screenshot.
- Pay close attention to background color, text color, font size, font family, 
padding, margin, border, etc. Match the colors and sizes exactly.
- Use the exact text from the screenshot.
- Do not add comments in the code such as "<!-- Add other navigation links as needed -->" and "<!-- ... other news items ... -->" in place of writing the full code. WRITE THE FULL CODE.
- Repeat elements as needed to match the screenshot. For example, if there are 15 items, the code should have 15 items. DO NOT LEAVE comments like "<!-- Repeat for each news item -->" or bad things will happen.
- For images, use unsplash method and include a detailed description of the image in the alt text so that an image generation AI can generate the image later.

In terms of libraries,
- You can use Google Fonts
- Font Awesome for icons: <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css"></link>

Return only the full code in <html></html> tags.
Do not include markdown "```" or "```html" at the start or end. if the user ask for updates return all the code with any explainations just return all the code
or if the user want to create a website from some queries use this templete then change the content and other relevnt info based on user inputs
Frontend:

Use HTML, CSS, and JavaScript.
The website should have a modern, responsive design.
Include animations and interactive elements to enhance user experience.
Ensure cross-browser compatibility.
return all the frontend (html , css , js) in one page under the html tags i will provide you an example of a landing page you can take it like standard template with the exact look and change specific contents based on user input like website name the content of page like the catogrey and the contct info and so on I will provide it bellow .
Note : if the user ask for some improvements edit based on the last code you generate it then return it all with the improvments.
replace all images with unsplash method
make him a website is undreamble 
just return the code without any explainition. Do not include markdown "```" or "```html" at the start or end
 :index.html:<!DOCTYPE html>
<html lang="en">
<head>
	
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width; initial-scale=1.0">
	<link rel="shortcut icon" type="image/x-icon" href="img/favicon.png">
	<link rel="stylesheet" type="text/css" href="css/bootstrap.min.css">
	<link rel="stylesheet" type="text/css" href="css/main.css">
	<link rel="stylesheet" type="text/css" href="css/uikit.min.css"> 
	<link rel="stylesheet" type="text/css" href="css/fontawesome/css/all.css">
	<title>Glozzome</title>
</head>
<body>

	<!-- Navbar Section Start -->
	<nav class="navbar navbar-dark navbar-expand-lg"  uk-sticky="top:100; animation: uk-animation-slide-top; bottom: #sticky-on-scroll-up">
		<div class="container">
			<a href="index.html" class="navbar-brand">
				<img src="img/logo1.png" class="img-fluid p-0" style="width: 35%; filter: brightness(0) invert(1);">
				<div class="ml-2 p-0 d-inline webT">Glozzome</div>
			</a>
			<button class="navbar-toggler navbar-toggler-right" data-toggle="collapse" data-target="#navBar">
				<span class="navbar-toggler-icon"></span>
			</button>
			<div class="collapse navbar-collapse" id="navBar">
				<ul class="navbar-nav  ml-auto ">

					<li class="nav-item active">
						<a class="nav-link " href="index.html">Home</a>
					</li>
					<li class="nav-item">
						<a class="nav-link" href="about.html">About</a>
					</li>
					<li class="nav-item">
						<a class="nav-link" href="services.html">Services</a>
					</li>
					<li class="nav-item">
						<a class="nav-link" href="blog.html">Blog</a>
					</li>
					<li class="nav-item">
						<a class="nav-link" href="contact.html">Contact</a>
					</li>
				</ul>
			</div>
		</div>
	</nav>
	<!-- Nav Section End -->

	<!-- Slider Section Start -->
	<section id="slider" class="bg-dark"> 
		<div id="myCarousel" class="carousel slide" data-ride="carousel">
			<ol class="carousel-indicators">
				<li class="active" data-slide-to="0" data-target="#myCarousel"></li>
				<li data-target="#myCarousel" data-slide-to="1"></li>
				<li data-target="#myCarousel" data-slide-to="2"></li>
				<li data-target="#myCarousel" data-slide-to="3"></li>
			</ol>
			<div class="carousel-inner" role="listbox">
				<div class="carousel-item crs-img-1 active">
					<div class="container">
						<div class="carousel-caption pb-5 mb-5 text-left">
							<h2 class="display-4 text-light">Heading One</h2>
							<p class="lead">
								Lorem ipsum ut do dolor excepteur adipisicing et minim consectetur <br>elit laborum quis nostrud eiusmod.
							</p>
							<a href="#" class="btn btn-success">See More</a>
						</div>
					</div>
				</div>
				<div class="carousel-item crs-img-2">
					<div class="container">
						<div class="carousel-caption mb-5 text-center">
							<h2 class="display-4 text-light">Heading Two</h2>
							<p>
								Lorem ipsum ut do dolor excepteur adipisicing et minim consectetur elit laborum quis nostrud eiusmod.
							</p>
							<a href="#" class="btn btn-warning">Read More</a>
						</div>
					</div>
				</div>
				<div class="carousel-item crs-img-3">
					<div class="container">
						<div class="carousel-caption pb-5 mb-5 text-right">
							<h2 class="display-4 text-light">Heading Three</h2>
							<p>
								Lorem ipsum ut do dolor excepteur adipisicing et minim <br>consectetur elit laborum quis nostrud eiusmod.
							</p>
							<a href="#" class="btn btn-info">Learn More</a>
						</div>
					</div>
				</div>
				<div class="carousel-item crs-img-4">
					<div class="container">
						<div class="carousel-caption pb-5 mb-5 text-left">
							<h2 class="display-4 text-light">Heading Four</h2>
							<p>
								Lorem ipsum ut do dolor excepteur adipisicing et minim consectetur elit <br>laborum quis nostrud eiusmod.
							</p>
							<a href="#" class="btn btn-success">Read More</a>
						</div>
					</div>
				</div>
			</div>
			<a href="#myCarousel" class="carousel-control-prev" data-slide="prev">
				<span class="carousel-control-prev-icon"></span>
			</a>
			<a href="#myCarousel" class="carousel-control-next" data-slide="next">
				<span class="carousel-control-next-icon"></span>
			</a>
		</div>		
	</section>
	<!-- Slider Section End -->

	<!-- Showcase Section Start -->
	<section id="showcase">
		<div class="container">
			<div class="row py-5 text-center">
				<div class="col-lg-4 col-md-4">
					<i class="fas fa-cogs mb-3"></i>
					<h3>Turning Gears</h3>
					<p class="lead mt-2">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Neque, totam accusamus veritatis fugiat animi pariatur.</p>
				</div>
				<div class="col-lg-4 col-md-4">
					<i class="fas fa-cloud mb-3"></i>
					<h3>Sending Data</h3>
					<p class="lead mt-2">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Neque, totam accusamus veritatis fugiat animi pariatur.</p>
				</div>
				<div class="col-lg-4 col-md-4">
					<i class="fas fa-cart-plus mb-3"></i>
					<h3>Making Money</h3>
					<p class="lead mt-2">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Neque, totam accusamus veritatis fugiat animi pariatur.</p>
				</div>
			</div>
		</div>
	</section>
	<!-- Showcase Section End -->

	<!-- Get Started Section Start -->
	<section id="get-started"   class="text-center py-5 text-light">
		<div class="inner-overlay">
			<div class="container">
				<div class="row">
					<div class="col mt-5 pt-4 gC">
						<h3 class="text-light">Are You Ready To Get Started?</h3>
						<p class="lead">
							Lorem ipsum dolor sit amet, consectetur adipisicing elit. Rem quaerat voluptatem laboriosam vero recusandae repellendus? Impedit iure est sit voluptatum blanditiis cum sequi laudantium quod dicta, a quaerat vel, obcaecati!
						</p>
					</div>
				</div>
			</div>
		</div>
	</section>
	<!-- Get Started Section End -->

	<!-- Info Section Start -->
	<section id="info" class="py-5">
		<div class="container">
			<div class="row">
				<div class="col-lg-6 col-md-6 col-sm-6 justify-content-center text-left infoS">
					<h3 >Lorem Ipsum Dolor Sit</h3>
					<p class="lead">
						Lorem ipsum dolor sit amet, consectetur adipisicing elit. Eaque dignissimos recusandae nobis reiciendis voluptatem quae iusto, fugiat itaque iste explicabo.
					</p>
					<a href="#" class="btn btn-outline-dark">Read More</a>
				</div>
				<div class="col-lg-6 col-md-6 col-sm-6 align-self-center">
					<img src="img/info.jpg" class="img-fluid">
				</div>
			</div>
		</div>
	</section>
	<!-- Info Section End -->

	<!-- Video Section Start -->
	<section id="video" class="text-center text-light">
		<div class="video-overlay">
			<div class="container">
				<div class="row">
					<div class="col mt-5 pt-4">
						<div uk-lightbox>
							<a href="https://youtu.be/uVqv7vIKOwM">
								<i class="fas fa-play"></i>
							</a>
						</div>
						<h2 class=" mt-5 text-light">Hack The Planet</h2>
						<p class="lead">Click Play Button To See</p>
					</div>
				</div>
			</div>
		</div>
	</section>
	<!-- Video Section End -->

	<!-- Gallery Section Start -->
	<section id="gallery" class="py-5" uk-lightbox>
		<div class="container">
			<div class="row text-center">
				<div class="col">
					<h2 class="mb-0">Photo Gallery</h2>
					<p class="lead m-0">Click to check out our photos</p>
				</div>
			</div>
			<div class="row mt-3">
				<div class="col-lg-4 col-md-4 col-sm-4">
					<a href="img/gallery1.jpg">
						<img src="img/gallery1.jpg" class="img-fluid">
					</a>
				</div>
				<div class="col-lg-4 col-md-4 col-sm-4">
					<a href="img/gallery2.jpg">
						<img src="img/gallery2.jpg" class="img-fluid">
					</a>
				</div>
				<div class="col-lg-4 col-md-4 col-sm-4">
					<a href="img/gallery3.jpg">
						<img src="img/gallery3.jpg" class="img-fluid">
					</a>
				</div>
			</div>
			<div class="row mt-3">
				<div class="col-lg-4 col-md-4 col-sm-4">
					<a href="img/gallery4.jpg">
						<img src="img/gallery4.jpg" class="img-fluid">
					</a>
				</div>
				<div class="col-lg-4 col-md-4 col-sm-4">
					<a href="img/gallery5.jpg">
						<img src="img/gallery5.jpg" class="img-fluid">
					</a>
				</div>
				<div class="col-lg-4 col-md-4 col-sm-4">
					<a href="img/gallery6.jpg">
						<img src="img/gallery6.jpg" class="img-fluid">
					</a>
				</div>
			</div>
			<div class="row mt-3">
				<div class="col-lg-4 col-md-4 col-sm-4">
					<a href="img/gallery7.jpg">
						<img src="img/gallery7.jpg" class="img-fluid">
					</a>
				</div>
				<div class="col-lg-4 col-md-4 col-sm-4">
					<a href="img/gallery8.jpg">
						<img src="img/gallery8.jpg" class="img-fluid">
					</a>
				</div>
				<div class="col-lg-4 col-md-4 col-sm-4">
					<a href="img/gallery9.jpg">
						<img src="img/gallery9.jpg" class="img-fluid">
					</a>
				</div>
			</div>
		</div>
	</section>
	<!-- Gellery Section End -->

	<!-- Subscribe Section Start -->
	<section id="subscribe" class="text-center py-5 bg-dark text-light">
		<div class="container">
			<div class="row">
				<div class="col">
					<h2 class="text-light">Signup For Our Newsletter</h2>
					<p class="lead">
						Lorem ipsum dolor sit amet, consectetur adipisicing elit. Veritatis magnam similique esse assumenda quasi repellendus illum perferendis quos aliquid possimus.				
					</p>
					<form class="form-inline justify-content-center ">
						<input type="text" placeholder="Enter name" class="form-control m-2">
						<input type="email" placeholder="Enter email" class="form-control m-2">
						<input type="submit" value="Subscribe" class=" btn btn-primary m-2">
					</form>
				</div>
			</div>
		</div>
	</section>
	<!-- Subcribe Section End -->

	<!-- Footer Section Start -->
	<footer id="footer" class="py-3 text-center text-light">
		<div class="container">
			<div class="row">
				<div class="col">
					<h2 class="display-5 mb-0 text-light">Glozzome</h2>
					<div class="d-flex flex-row justify-content-center p-3">
						<div class="px-5">
							<a href="#">
								<i class="fab fa-facebook-f"></i>
							</a>
						</div>
						<div class="px-5">
							<a href="#">
								<i class="fab fa-linkedin-in"></i>
							</a>
						</div>
						<div class="px-5">
							<a href="#">
								<i class="fab fa-twitter"></i>
							</a>
						</div>
					</div>
				</div>
			</div>
			<div class="row">
				<div class="col">
					Glozzome.com © 2019 All Rights Reserved by MrhRifat
				</div>
			</div>
		</div>
	</footer>

"""


    }
    state.messages = [
        {
            "role": "assistant",
            "style": "assistant_message",
            "content": "hi",
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

def save_html_response(html_content):
    global index  # Ensure we use the global variable

    # Ensure the directory exists
    if not os.path.exists('generated_sites'):
        os.makedirs('generated_sites')

    # Save the HTML content to a file
    file_path = f"generated_sites/generated_site_{index}.html"
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(html_content)

    return file_path

import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import quote
def view_generated_site(state):
    global generated_file_path

    if not generated_file_path:
        notify(state, "error", "No site has been generated yet.")
        return

    # Use your domain or IP address here
    domain = "https://webmecano5.onrender.com"  # Replace with your actual domain
    # or
    # domain = "192.168.1.100"  # Replace with your server's IP address

    # Generate the URL to access the file
    file_name = os.path.basename(generated_file_path)
    file_url = f"https://{domain}/generated_sites/{quote(file_name)}"
    
    # Add the clickable link to the chat
    state.messages.append(
        {
            "role": "assistant",
            "style": "link_message",
            "content": f"[View Generated Site]({file_url})",
        }
    )
    state.conv.update_content(state, create_conv(state))
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

load_dotenv()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))  # Use the PORT environment variable or default to 5000
    gui = Gui(page)
    conv = gui.add_partial("")
    print(f"Running server on http://0.0.0.0:{port}")
    gui.run(host="0.0.0.0", port=port, title="webmecano",dark_mode=False, margin="0px",debug=True)

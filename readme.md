# DisabledDriver
## Overview
DisabledDriver is an innovative project with the goal of making the internet more accessible and easier to navigate for individuals with disabilities or anyone seeking a more streamlined online experience. This project harnesses the power of AI, specifically OpenAI's GPT-40-mini model, to assist users in performing various online tasks with minimal manual input.

## Key Features
- AI-Driven Navigation: DisabledDriver uses ChatGPT to interact with websites via Selenium, automating tasks such as filling out forms, playing music, and finding news articles. The AI guides Selenium in making decisions, allowing users to complete tasks hands-free.
- Speech Recognition Support: For added convenience, the project includes speech recognition as an input method. Users can simply speak their commands, and the system will process their input and carry out the corresponding actions. To activate this feature, click on the input field, speak your command, and press the enter button to submit.

## Getting Started
Prerequisites
Before you can use DisabledDriver, you need to ensure you have the following:
- OpenAI API Key: You must have access to an OpenAI API key with permissions for the GPT-40-mini model. This key will allow the project to utilize the AI's capabilities.
- Key File: Create a key.txt file in the root directory of the project. This file should contain your OpenAI API key.
- Python Environment: Ensure you have Python installed on your system. The project is built using Python, and you'll need it to run the script.

Installation
Clone the repository to your local machine.

git clone https://github.com/Pymaster3119/DisabledDriver.git
Navigate to the project directory.

cd DisabledDriver
Install the required dependencies. This project relies on several Python packages, which can be installed using pip:

pip install -r requirements.txt
Place your OpenAI API key in a key.txt file in the project's root directory.

Running the Project
To start using DisabledDriver, simply run the main.py script:

python main.py
Once the script is running, you can begin interacting with the AI through the command-line interface or the speech recognition feature.

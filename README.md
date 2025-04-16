# Recipe Recommender Bot

**Recipe Recommender Bot** is an intuitive Streamlit application that helps you discover personalized recipes tailored to your dietary needs, cuisine preferences, and meal goals. Powered by [Agno](https://github.com/agno-agi/agno), OpenAI's GPT-4o, and SerpAPI, the bot conducts intelligent culinary research and presents a structured, easy-to-follow recipe — ready for your next meal.

## Folder Structure

```
Recipe-Recommender-Bot/
├── recipe-recommender-bot.py
├── README.md
└── requirements.txt
```

- **recipe-recommender-bot.py**: The main Streamlit application.
- **requirements.txt**: Required Python packages.
- **README.md**: This documentation file.

## Features

- **Culinary Preferences Input**  
  Choose your dietary preferences, cuisine types, dish format, cooking time, serving size, and optional ingredient exclusions.

- **AI-Powered Recipe Discovery**  
  The Recipe Researcher agent creates a focused Google search using SerpAPI based on your inputs and fetches the most relevant recipe links.

- **Personalized Recipe Generation**  
  The Recipe Recommender agent reads those results and selects the best-fit recipe aligned with your criteria, formatting it cleanly in Markdown.

- **Structured Markdown Output**  
  The recipe includes prep time, ingredients, instructions, nutritional highlights, substitution tips, and a final link to the full recipe.

- **Download Option**  
  Download your recipe as a `.txt` file to keep or share with others.

- **Clean Streamlit UI**  
  Built with Streamlit to ensure a smooth, responsive, and visually clean user experience.

## Prerequisites

- Python 3.11 or higher  
- An OpenAI API key ([Get one here](https://platform.openai.com/account/api-keys))  
- A SerpAPI key ([Get one here](https://serpapi.com/manage-api-key))

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/akash301191/Recipe-Recommender-Bot.git
   cd Recipe-Recommender-Bot
   ```

2. **(Optional) Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate        # On macOS/Linux
   # or
   venv\Scripts\activate           # On Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the app**:
   ```bash
   streamlit run recipe-recommender-bot.py
   ```

2. **In your browser**:
   - Add your OpenAI and SerpAPI keys in the sidebar.
   - Fill in your dietary, cuisine, and recipe preferences.
   - Click **🍽️ Generate Recipe**.
   - View and download your personalized AI-generated recipe.

3. **Download Option**  
   Use the **📥 Download Recipe** button to save your recipe as a `.txt` file.

---

## Code Overview

- **`render_culinary_preferences()`**: Collects dietary needs, cuisine types, meal goals, cooking time, and notes.
- **`render_sidebar()`**: Handles OpenAI and SerpAPI key inputs securely using Streamlit's session state.
- **`generate_recipe()`**:  
  - Uses the `Recipe Researcher` agent to search for recipes via SerpAPI.  
  - Sends the results to the `Recipe Recommender` agent to format a single best-match recipe.
- **`main()`**: Handles app layout, input collection, agent orchestration, and result rendering.

## Contributions

Contributions are welcome! Feel free to fork the repo, report bugs, suggest improvements, or open a pull request. Please ensure your changes are clean, documented, and aligned with the project’s purpose.
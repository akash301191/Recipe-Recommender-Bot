import streamlit as st
from agno.agent import Agent
from agno.tools.serpapi import SerpApiTools
from agno.models.openai import OpenAIChat

from textwrap import dedent

def render_culinary_preferences():
    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    # Column 1: Dietary & Cuisine Preferences
    with col1:
        st.subheader("🍽️ Dietary & Cuisine")
        dietary_preferences = st.multiselect(
            "Dietary Preferences*",
            ["Vegan", "Vegetarian", "Gluten-free", "Dairy-free", "Low-carb", "High-protein", "No restrictions"]
        )
        cuisine_type = st.multiselect(
            "Cuisine Type*",
            ["Indian", "Italian", "Mediterranean", "Asian", "Mexican", "American", "Middle Eastern", "Surprise me!"]
        )
        meal_goal = st.selectbox(
            "Meal Goal (optional)",
            ["No specific goal", "Weight loss", "Muscle gain", "Energy boost", "Comfort food", "Quick & easy"]
        )

    # Column 2: Meal Type & Time
    with col2:
        st.subheader("⏲️ Meal Preferences")
        meal_type = st.selectbox(
            "Type of Dish*",
            ["Main course", "Side dish", "Soup or stew", "Salad", "Snack", "Dessert", "No preference"]
        )
        prep_time = st.selectbox(
            "Preferred Cooking Time*",
            ["Under 15 minutes", "15–30 minutes", "30–60 minutes", "No time limit"]
        )
        servings = st.number_input("Number of Servings*", min_value=1, step=1)

    # Column 3: Optional Notes
    with col3:
        st.subheader("📝 Notes")
        avoid_ingredients = st.text_input("Ingredients to Avoid (optional)", placeholder="e.g., Mushrooms, peanuts")
        extra_notes = st.text_area("Other Preferences (optional)", placeholder="e.g., Prefer low-spice dishes")

    # Display user selections for review/debug
    user_preferences = f"""
    **Culinary Preferences Summary:**
    - Dietary Preferences: {', '.join(dietary_preferences) if dietary_preferences else 'Not specified'}
    - Cuisine Type: {', '.join(cuisine_type) if cuisine_type else 'Not specified'}
    - Meal Goal: {meal_goal}
    - Dish Type: {meal_type}
    - Cooking Time: {prep_time}
    - Servings: {int(servings)}
    - Avoid Ingredients: {avoid_ingredients if avoid_ingredients.strip() else 'None'}
    - Notes: {extra_notes if extra_notes.strip() else 'None'}
    """
    return user_preferences

def render_sidebar():
    st.sidebar.title("🔐 API Configuration")
    st.sidebar.markdown("---")

    # OpenAI API Key input
    openai_api_key = st.sidebar.text_input(
        "OpenAI API Key",
        type="password",
        help="Don't have an API key? Get one [here](https://platform.openai.com/account/api-keys)."
    )
    if openai_api_key:
        st.session_state.openai_api_key = openai_api_key
        st.sidebar.success("✅ OpenAI API key updated!")

    # SerpAPI Key input
    serp_api_key = st.sidebar.text_input(
        "Serp API Key",
        type="password",
        help="Don't have an API key? Get one [here](https://serpapi.com/manage-api-key)."
    )
    if serp_api_key:
        st.session_state.serp_api_key = serp_api_key
        st.sidebar.success("✅ Serp API key updated!")

    st.sidebar.markdown("---")

def generate_recipe(user_culinary_preferences):
    # Invoke Recipe Researcher Agent
    research_agent = Agent(
        name="Recipe Researcher",
        role="Finds recipe suggestions that match the user's dietary needs, cuisine preferences, and cooking goals.",
        model=OpenAIChat(id='gpt-4o', api_key=st.session_state.openai_api_key),
        description=dedent("""
            You are a culinary research expert. Given a user's food preferences, dietary restrictions, and meal goals,
            your job is to find relevant recipes and cooking ideas that best fit their needs.
            You will generate a focused, natural language search query, search the web, and extract the 10 most relevant recipe links.
        """),
        instructions=[
            "Carefully read the user's preferences, including diet type, cuisine choices, dish type, cooking time, and serving size.",
            "Based on this, generate ONE concise and effective search term (e.g., 'easy vegan Mediterranean salad for two' or 'low-carb Indian dinner under 30 minutes').",
            "Keep the search query targeted to the most important user inputs. Avoid vague terms like 'best recipes'.",
            "Use `search_google` with the generated search query.",
            "From the search results, extract the top 10 most relevant recipe links or page summaries.",
            "Prioritize results from trusted recipe sources (e.g., AllRecipes, BBC Good Food, Minimalist Baker, NYT Cooking).",
            "Do not invent or assume recipe details. Rely only on search result content.",
        ],
        tools=[SerpApiTools(api_key=st.session_state.serp_api_key)],
        add_datetime_to_instructions=True,
    )

    research_response = research_agent.run(user_culinary_preferences)
    research_results = research_response.content 

    # Invoke Recipe Recommender Agent 
    recommender_agent = Agent(
            name="Recipe Recommender",
            role="Analyzes recipe links and matches them with user preferences to suggest a personalized recipe.",
            model=OpenAIChat(id='o3-mini', api_key=st.session_state.openai_api_key),
            description=dedent("""
                You are a culinary assistant specialized in personalized recipe recommendations.
                You are given:
                1. A structured summary of the user's dietary needs, cuisine preferences, dish type, meal goals, and time constraints.
                2. A list of recipe URLs or summaries from trusted cooking websites.

                Your task is to read and extract relevant recipe information from the URLs and recommend a single best-fit recipe that aligns with the user’s inputs.
            """),
            instructions=[
                "Start by reading the structured user preferences. Pay close attention to:",
                "- **Dietary Preferences**: Ensure the recipe adheres to these restrictions.",
                "- **Cuisine Type**: Prioritize matching cuisines (e.g., Indian, Mediterranean).",
                "- **Meal Goal**: Choose a recipe that supports the user's goal (e.g., weight loss, quick meal).",
                "- **Dish Type**: Match the format (e.g., salad, snack, soup).",
                "- **Prep Time**: Respect the user's time constraint.",
                "- **Servings**: Ensure the recipe matches or is adaptable to the serving size.",
                "- **Avoid Ingredients**: Exclude recipes containing listed items.",
                "- **Notes**: Adapt the recommendation using any extra preferences (e.g., no blender, low-spice).",

                "Then read through each of the recipe links provided in the research results.",
                "Select the recipe that best matches all user criteria. Do NOT invent recipes — only use what is found in the sources.",
                "Once a recipe is chosen, extract and format the following details using Markdown:",

                "- **Recipe Title (Use markdown `##` )**",
                "- **Prep Time**",
                "- **Servings**",
                "- **Ingredients** (Use markdown `###` )",
                "- **Brief Cooking Instructions (6–8 lines, Use markdown `###`)**",
                "- **Nutritional Highlights** (if available, Use markdown `###`)",
                "- **Optional Substitution Tips** (based on user notes, Use markdown `###`)",
                "- **Link to Full Recipe** (place this as the final line of the recipe)",

                "Present the output in clean, readable Markdown format.",
                "Do not generate multiple recipe options. Return only the best match.",
                "Start directly with the recipe title as a Markdown heading. Do not include introductory text or summary.",
            ],
            add_datetime_to_instructions=True,
        )

    recommender_input = f"""
    User's Culinary Preferences:
    {user_culinary_preferences}

    Research Results:
    {research_results}

    Use these details to generate a personalized recipe for the user.
    """

    recommender_response = recommender_agent.run(recommender_input)
    recipe = recommender_response.content 

    return recipe

def main() -> None:
    # Page config
    st.set_page_config(page_title="Recipe Recommender Bot", page_icon="🍲", layout="wide")

    # Custom styling
    st.markdown(
        """
        <style>
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        div[data-testid="stTextInput"], div[data-testid="stSelectbox"], div[data-testid="stMultiselect"] {
            max-width: 1200px;
            margin-left: auto;
            margin-right: auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Header and intro
    st.markdown("<h1 style='font-size: 2.5rem;'>🍲 Recipe Recommender Bot</h1>", unsafe_allow_html=True)
    st.markdown(
        "Welcome to Recipe Recommender Bot — an intuitive Streamlit assistant that helps you discover personalized recipes based on your dietary needs and cuisine preferences.",
        unsafe_allow_html=True
    )

    render_sidebar()
    user_culinary_preferences = render_culinary_preferences()

    st.markdown("---")

    if st.button("🍽️ Generate Recipe"):
        if not hasattr(st.session_state, "openai_api_key"):
            st.error("Please provide your OpenAI API key in the sidebar.")
        elif not hasattr(st.session_state, "serp_api_key"):
            st.error("Please provide your SerpAPI key in the sidebar.")
        else:
            with st.spinner("Finding the perfect recipe for you..."):
                recipe = generate_recipe(user_culinary_preferences)
                st.session_state.recipe_result = recipe

    if "recipe_result" in st.session_state:
        st.markdown(st.session_state.recipe_result, unsafe_allow_html=True)
        st.markdown("---")

        st.download_button(
            label="📥 Download Recipe",
            data=st.session_state.recipe_result,
            file_name="personalized_recipe.txt",
            mime="text/plain"
        )

if __name__ == "__main__":
    main()
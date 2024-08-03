pip install streamlit openai matplotlib pandas

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import openai

st.title("🎈 Analytics Feedback Chatbot")
st.write(
    "Welcome [X]"
)
# Set your OpenAI API key
openai.api_key = 'your_openai_api_key_here'
st.write("Ask your questions about your analytics feedback visuals. Refer to graphs by their IDs.")

# Example DataFrames for different graphs
data1 = {
    'Assignment': ['Assignment 1', 'Assignment 2', 'Assignment 3'],
    'Score': [85, 90, 78]
}
df1 = pd.DataFrame(data1)

data2 = {
    'Week': ['Week 1', 'Week 2', 'Week 3'],
    'Attendance': [95, 85, 88]
}
df2 = pd.DataFrame(data2)

# Display the dataframes and graphs
st.write("Graph 1: Student Scores")
fig1, ax1 = plt.subplots()
ax1.bar(df1['Assignment'], df1['Score'])
st.pyplot(fig1)

st.write("Graph 2: Weekly Attendance")
fig2, ax2 = plt.subplots()
ax2.plot(df2['Week'], df2['Attendance'])
st.pyplot(fig2)

# Graph selection
graph_selection = st.selectbox("Select a graph to ask about:", ["Graph 1", "Graph 2"])

# User input
user_input = st.text_input("You: ", "Type your question here...")

if user_input:
    # Extract graph information
    graph_info = {
        "Graph 1": f"Graph 1 shows student scores: {df1.to_dict()}",
        "Graph 2": f"Graph 2 shows weekly attendance: {df2.to_dict()}"
    }

    referred_graph = graph_info[graph_selection]
    
    # Full input for the API
    full_input = f"{user_input}\n\n{referred_graph}"

    # Call the OpenAI API
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=full_input,
        max_tokens=150
    )

    st.write(f"Chatbot: {response.choices[0].text.strip()}")

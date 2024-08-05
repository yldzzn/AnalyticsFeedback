import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import openai

st.title("🎈 Analytics Feedback Chatbot")
st.write(
    "Welcome [X]"
)
# Set your OpenAI API key

with st.sidebar:
    openai.api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")

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
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai.api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=openai.api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)

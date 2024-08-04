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

def query_openai(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Sample data for visualizations
def load_data():
    engagement_data = {
        'Date': pd.date_range(start='1/1/2023', periods=12, freq='M'),
        'Engagement': [70, 80, 75, 90, 85, 78, 88, 92, 95, 90, 85, 88]
    }
    performance_data = {
        'Date': pd.date_range(start='1/1/2023', periods=12, freq='M'),
        'Performance': [65, 75, 70, 85, 80, 73, 83, 87, 90, 85, 80, 83]
    }
    return pd.DataFrame(engagement_data), pd.DataFrame(performance_data)

# Streamlit app
def main():
    st.title("Learning Analytics Dashboard")

    # Load and display data
    engagement_df, performance_df = load_data()
    
    graph_options = {
        "Student Engagement Over Time": {
            "description": "This chart shows student engagement over the semester, including class participation and attendance.",
            "data": engagement_df,
            "column": "Engagement"
        },
        "Student Performance Over Time": {
            "description": "This chart shows student performance over the semester, based on grades and assessments.",
            "data": performance_df,
            "column": "Performance"
        }
    }

    # Dropdown to select graph
    graph_choice = st.selectbox("Choose a graph to display:", list(graph_options.keys()))
    
    if graph_choice:
        selected_graph = graph_options[graph_choice]
        st.subheader(graph_choice)
        st.line_chart(selected_graph["data"].set_index('Date'))

        # Chatbot interaction
        st.subheader("Ask a Question About the Graph")
        user_query = st.text_input("Enter your question here:")

        if st.button("Get Answer"):
            if user_query:
                prompt = f"Graph Description: {selected_graph['description']}\nUser Question: {user_query}"
                response = query_openai(prompt)
                st.write(f"**AI Response:** {response}")
            else:
                st.write("Please enter a question.")

if __name__ == "__main__":
    main()
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
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)

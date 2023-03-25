import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Define a function to analyze the data
def analyze_data(data):
    # Create a pandas DataFrame from the data
    df = pd.DataFrame(data)
    # Set the learner names as the DataFrame index
    df.set_index('Learner name', inplace=True)
    # Create a bar chart of the total scores
    total_chart = px.bar(df, y='Total', labels={'index': 'Learner name', 'Total': 'Score'})
    # Create a stacked bar chart of the individual question scores
    stacked_chart = px.bar(df, barmode='stack', labels={'index': 'Learner name', 'value': 'Score'})
    # Create a horizontal bar chart of the average scores on each question
    avg_chart = px.bar(df.mean().reset_index(), x='index', y=0, labels={'index': 'Question', 0: 'Average Score'})
    # Create a donut chart of the distribution of scores across the six questions
    donut_chart = go.Figure(data=[go.Pie(labels=df.columns[:-1], values=df.mean()[:-1], hole=.3)])
    donut_chart.update_layout(title='Distribution of Scores Across Questions')
    # Create a scatter matrix of the scores on different questions for each learner
    scatter_matrix = px.scatter_matrix(df, dimensions=df.columns[:-1], color=df.index, labels={col: 'Question ' + col[-1] for col in df.columns[:-1]}, title='Scores on Different Questions for Each Learner')
    # Create a 3D scatter plot of the scores on questions 1, 2, and 3 for each learner
    scatter_3d = px.scatter_3d(df, x='Question 1', y='Question 2', z='Question 3', color=df.index, title='Scores on Questions 1, 2, and 3 for Each Learner')
    # Create a line chart of the trend of scores over time
    trend_chart = px.line(df, x=df.index, y='Total', title='Trend of Scores Over Time')
    # Return the charts as a dictionary
    return {'Total Scores': total_chart, 'Question Scores': stacked_chart, 'Average Scores': avg_chart, 'Distribution of Scores': donut_chart, 'Scatter Matrix': scatter_matrix, '3D Scatter Plot': scatter_3d, 'Trend of Scores': trend_chart}

# Define the Streamlit app
def main():
    # Set the app title
    st.title('Excel File Analyzer')
    # Create a file uploader component
    file = st.file_uploader('Upload an Excel file', type='xlsx')
    # Define a list of chart options
    chart_options = ['Total Scores', 'Question Scores', 'Average Scores', 'Distribution of Scores', 'Scatter Matrix', '3D Scatter Plot', 'Trend of Scores']
    # Create a radio button to select the chart to display
    chart_option = st.sidebar.radio('Select a chart', chart_options, index=0)
    # If a file has been uploaded
    if file is not None:
        # Read the Excel file into a pandas DataFrame
        data = pd.read_excel(file)
        # Analyze the data
        charts = analyze_data(data)
        # Display the selected chart
        st.plotly_chart(charts[chart_option])

# Run the app
if __name__ == '__main__':
    main()

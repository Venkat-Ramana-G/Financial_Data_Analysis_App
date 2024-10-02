import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests

# Replace with your actual News API key
NEWS_API_KEY = '819afac21fe0423b87f367244e163c97'

def main():
    # Header
    st.markdown("<h1 style='text-align: center;'>Financial Data Analysis App</h1>", unsafe_allow_html=True)
    
    st.sidebar.title("24MAI0091 VENKAT RAMANA'S MULTI-PAGE APP")
    menu = ["Home", "Stock Statistics", "Portfolio Analysis", "Stock Forecasting", "Market Sentiment"]
    choice = st.sidebar.selectbox("Select Page", menu)

    # Footer
    st.markdown("<footer style='text-align: center;'><p>Contact: guntupalli.venkat2024@vitstudent.ac.in</p></footer>", unsafe_allow_html=True)

    if choice == "Home":
        home_page()
    elif choice == "Stock Statistics":
        stock_statistics()
    elif choice == "Portfolio Analysis":
        portfolio_analysis()
    elif choice == "Stock Forecasting":
        stock_forecasting()
    elif choice == "Market Sentiment":
        market_sentiment()

# Home Page
def home_page():
    st.title("Financial Data Analysis")
    st.write("""\
        Welcome to the Financial Data Analysis App! Prepared By 24MAI0091 VENKAT RAMANA 
        Navigate through the sidebar to explore stock data, portfolio analysis, forecasting, and sentiment analysis.
    """)

# Page 1: Stock Statistics (Preloaded Data)
def stock_statistics():
    st.title("Stock Data & Statistics")
    
    # Preloaded stock data (S&P 500 dataset)
    url = "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/master/data/constituents.csv"
    data = pd.read_csv(url)
    
    st.write("### S&P 500 Stock Data")
    st.write(data.head(30))

    with st.expander("Show Basic Statistics"):
        st.write("### Basic Statistics")
        st.write(data.describe())

    with st.expander("Show Stock Prices Over Time"):
        st.write("### Stock Prices Over Time")
        
        # Generate random stock data for demonstration purposes
        dates = pd.date_range(start="2020-01-01", periods=200)
        stock_prices = np.random.uniform(100, 500, size=200)  # Changed size to 200 to match dates
        
        df = pd.DataFrame({"Date": dates, "Price": stock_prices})
        df.set_index("Date", inplace=True)
        
        st.line_chart(df["Price"])

# Page 2: Portfolio Analysis (Preloaded Data)
def portfolio_analysis():
    st.title("Portfolio Analysis")
    
    # Simulated portfolio data with 50 rows
    np.random.seed(42)  # For reproducibility

    # List of assets
    assets = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']
    
    # Generate random allocations (making sure they sum to 100)
    allocations = np.random.choice(range(1, 21), size=50)  # Random allocations between 1 and 20
    allocations = allocations / allocations.sum() * 100  # Normalize to sum to 100

    # Generate random returns (for example purposes)
    returns = np.random.uniform(low=5, high=25, size=50)  # Random returns between 5% and 25%

    # Create DataFrame
    portfolio_data = pd.DataFrame({
        'Asset': np.random.choice(assets, size=50),  # Randomly choose assets from the list
        'Allocation': allocations,
        'Return': returns
    })

    # Display the portfolio data
    st.write("### Portfolio Data")
    st.dataframe(portfolio_data)

    # You can add plots based on this data if required
    st.write("### Portfolio Performance")
    
    # Example plot of asset allocation
    fig, ax = plt.subplots(figsize=(8, 4))
    portfolio_data.groupby('Asset')['Allocation'].sum().plot(kind='pie', autopct='%1.1f%%', ax=ax)
    ax.set_ylabel('')
    ax.set_title('Asset Allocation in Portfolio')
    st.pyplot(fig)

    # Example plot of returns distribution
    st.write("### Returns Distribution")
    fig2, ax2 = plt.subplots(figsize=(8, 4)) 
    portfolio_data['Return'].plot(kind='hist', bins=10, ax=ax2, color='skyblue', edgecolor='black')
    ax2.set_title('Returns Distribution')
    ax2.set_xlabel('Return (%)')
    ax2.set_ylabel('Frequency')
    st.pyplot(fig2)

# Page 3: Stock Forecasting (Preloaded Data)
def stock_forecasting():
    st.title("Stock Forecasting")

    # Generate random stock data for demonstration purposes
    dates = pd.date_range(start="2021-01-01", periods=200)
    prices = np.random.uniform(50, 300, size=(200,))  # Ensure 200 prices

    stock_df = pd.DataFrame({"Date": dates, "Price": prices})

    st.write("### Stock Prices with Moving Average")
    stock_df.set_index('Date', inplace=True)
    stock_df['Moving Average'] = stock_df['Price'].rolling(window=20).mean()

    st.line_chart(stock_df[['Price', 'Moving Average']])

    # Simple Forecast: predicting next price as the last value
    predicted_price = stock_df['Price'].iloc[-1]
    st.write(f"Predicted next price: {predicted_price:.2f}")

# Page 4: Market Sentiment (Web Scraping)
def market_sentiment():
    st.title("Market Sentiment Analysis")

    search_term = st.text_input("Enter stock symbol or keyword for news:")
    if st.button("Fetch News"):
        if search_term:
            url = f'https://newsapi.org/v2/everything?q={search_term}&apiKey={NEWS_API_KEY}'
            response = requests.get(url)
            data = response.json()

            st.write("### Scraped Headlines:")
            
            if data.get("status") == "ok" and data.get("articles"):
                headlines = data['articles'][:5]  # Get top 5 headlines
                headlines_text = [article['title'] for article in headlines]
                
                for headline in headlines_text:
                    st.write(f"- {headline}")

                # Example sentiment analysis; replace this with your actual analysis logic
                sentiment = np.random.choice(['Positive', 'Neutral', 'Negative'], size=len(headlines_text))

                # Create DataFrame
                sentiment_df = pd.DataFrame({
                    'Headline': headlines_text,
                    'Sentiment': sentiment
                })
                st.write("### Sentiment Analysis")
                st.write(sentiment_df)

                # Sentiment Distribution
                st.write("### Sentiment Distribution")
                fig, ax = plt.subplots()
                sentiment_df['Sentiment'].value_counts().plot(kind='bar', ax=ax)
                ax.set_ylabel('Frequency')
                ax.set_title('Sentiment Distribution')
                st.pyplot(fig)

            else:
                st.write("No headlines found for this search term.")

if __name__ == "__main__":
    main()

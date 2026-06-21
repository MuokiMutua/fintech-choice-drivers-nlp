import pandas as pd
from google_play_scraper import Sort, reviews
import time

def harvest_app_reviews():
    print("Initializing Google Play Store Scraper...")
    
    # We use general, globally recognized app package IDs (like Chase, PayPal) 
    # so the script works out-of-the-box for your portfolio without targeting specific local banks.
    TARGET_APPS = {
        "com.chase.sig.android": "Traditional Bank A",        # e.g., Chase Bank
        "com.citi.citimobile": "Traditional Bank B",          # e.g., Citi Mobile
        "com.paypal.android.p2pmobile": "Digital Fintech A",  # e.g., PayPal
        "com.squareup.cash": "Digital Fintech B"              # e.g., Cash App
    }
    
    all_reviews = []
    reviews_per_app = 800  # Grab 800 reviews per app to build a solid dataset
    
    for app_id, generic_name in TARGET_APPS.items():
        print(f"\nHarvesting data for: {generic_name} ({app_id})...")
        
        try:
            # Fetch reviews (using 'us' region for these global apps to ensure high volume)
            result, continuation_token = reviews(
                app_id,
                lang='en', 
                country='us', 
                sort=Sort.NEWEST, 
                count=reviews_per_app
            )
            
            # Process and format the raw data
            for rev in result:
                all_reviews.append({
                    "App_Category": generic_name,
                    "App_Type": "Traditional Bank" if "Bank" in generic_name else "Digital Fintech",
                    "Score": rev['score'],
                    "Review_Date": rev['at'],
                    "Review_Content": rev['content'],
                    "Thumbs_Up": rev['thumbsUpCount']
                })
                
            print(f"✓ Successfully harvested {len(result)} reviews.")
            
            # Be polite to the servers
            time.sleep(2)
            
        except Exception as e:
            print(f"❌ Error scraping {generic_name}: {e}")

    # Convert the list of dictionaries to a Pandas DataFrame
    df = pd.DataFrame(all_reviews)
    
    # Save the dataset to a CSV file
    output_file = "financial_app_reviews.csv"
    df.to_csv(output_file, index=False)
    
    print("\n" + "="*50)
    print(f"DATA HARVEST COMPLETE!")
    print(f"Total reviews collected: {len(df)}")
    print(f"Dataset saved to: {output_file}")
    print("="*50)
    print("\nSample Data:")
    print(df[['App_Category', 'Score', 'Review_Content']].head(3))

if __name__ == "__main__":
    harvest_app_reviews()
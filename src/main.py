from processing import data, web

if __name__ == "__main__":
    try:
        data.clean_table()
        web.scrape()
    
    except Exception as e:
        print(f"Error: {e}")   
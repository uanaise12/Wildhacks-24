from scholarly import scholarly
import KeyTopicsGenerator



def RetrieveTopics(summary):
	main_topics = summary.split('**')[1:]  # Split by main topics

	topics_list = []
	for i in range(0, len(main_topics), 2):  # Step by 2 to pair titles with their content
		topic_title = main_topics[i].strip()
		if topic_title in ["Main Topics", "Main Topics:", "Subtopics"]:
			continue
		topics_list.append(topic_title)  # Add to the list of main topics
	cleaned_topics = [element.replace(":", "") for element in topics_list]

	return cleaned_topics

#queries search helper

def search_google_scholar(topic, limit=10):
	# Search for the topic
	search_query = scholarly.search_pubs(topic)

	articles_data = []
	try:
		for _ in range(limit):
			article = next(search_query)
			# Extract the necessary data
			if 'eprint_url' in article:
				data = {
					'url': article.get('eprint_url', 'URL not available'),
					'citedby': article.get('num_citations', 0),  # Citation count
					'year': article['bib'].get('pub_year', 'Year not available')  # Publication year
				}
					
				articles_data.append(data)
	except StopIteration:
		pass

	return articles_data

def balance_articles(articles_data, balance_count=5):
	# Sort articles by citation count and year, descending
	most_cited = sorted(articles_data, key=lambda x: x['citedby'], reverse=True)[:balance_count]
	most_recent = sorted(articles_data, key=lambda x: x['year'], reverse=True)[:balance_count]

	# Combine and deduplicate the lists
	balanced_articles = {art['url']: art for art in most_cited + most_recent}.values()

	return list(balanced_articles)

def fetch_balanced_articles_for_topics(summary):
	topics_with_balanced_articles = {}
	topics_list = RetrieveTopics(summary)

	for topic in topics_list:
		print(f"Fetching balanced articles for Topic: '{topic}'")
		articles_data = search_google_scholar(topic)
		balanced_articles = balance_articles(articles_data)
		topics_with_balanced_articles[topic] = [art['url'] for art in balanced_articles]

	return topics_with_balanced_articles


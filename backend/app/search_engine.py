from app.scrapers.rabindustries_scraper import RabIndustriesScraper
from app.scrapers.ballardintl_scraper import BallardIntlScraper
from app.scrapers.robotsdoneright_scraper import RobotsDoneRightScraper
from concurrent.futures import ThreadPoolExecutor, as_completed
from app.utils import call_open_ai_calculate_relevance
from app.typesense_client import typesenseClient
import uuid


def run_scraper(scraper, search_term):
    print(f"Calling Scraper: {scraper}")
    return scraper.scrape(search_term=search_term)


def calculate_relevance(result, query):
    content = call_open_ai_calculate_relevance(query, result).lower()
    return 'invalid' not in content


def normalize_query(q: str) -> str:
    # Convert to lowercase and strip leading/trailing whitespace
    return ' '.join(q.lower().strip().split())


class SearchEngine:
    def __init__(self):
        self.scrapers = {
            'R.A.B. Industries': RabIndustriesScraper(),
            'Robots Done Right': RobotsDoneRightScraper(),
            'Ballard Intl': BallardIntlScraper()
        }
        self.source_priority = {
            'R.A.B. Industries': 1,
            'Robots Done Right': 2,
            'Ballard Intl': 3
        }

    def rank_results(self, results):
        # Sort by source priority
        sorted_by_priority = sorted(results, key=lambda x: self.source_priority[x['source']])
        return sorted_by_priority

    def cache_results(self, results):
        for result in results:
            result['id'] = str(uuid.uuid4())
            # Exclude embedding field from being stored
            if 'embedding' in result:
                del result['embedding']
            typesenseClient.collections['products'].documents.create(result)

    def get_cached_results(self, q):
        normalized_query = normalize_query(q)
        try:
            cached_results = typesenseClient.collections['products'].documents.search({
                'q': normalized_query,
                'query_by': 'title'
            })
            return [hit['document'] for hit in cached_results['hits']]
        except Exception as e:
            print(f"Error fetching cached results: {e}")
            return []

    def search(self, q):
        normalized_query = normalize_query(q)

        # Check for cached results
        # cached_results = self.get_cached_results(normalized_query)
        # if cached_results:
        #     print(f"Cache hit for query: {normalized_query}")
        #     return cached_results

        print(f"Cache miss for query: {normalized_query}. Running scrapers.")
        # If no cached results, perform search
        with ThreadPoolExecutor(max_workers=3) as executor:
            future_to_scraper = {
                executor.submit(run_scraper, scraper, normalized_query): name
                for name, scraper in self.scrapers.items()
            }

            results = []
            for future in as_completed(future_to_scraper):
                scraper_name = future_to_scraper[future]
                try:
                    scraper_results = future.result()
                    for result in scraper_results:
                        result['source'] = scraper_name
                        results.append(result)
                except Exception as exc:
                    print(f"Scraper {scraper_name} generated an exception: {exc}")

        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_relevance = {
                executor.submit(calculate_relevance, result, normalized_query): result
                for result in results
            }

            valid_results = []
            for future in as_completed(future_to_relevance):
                result = future_to_relevance[future]
                try:
                    if future.result():
                        valid_results.append(result)
                except Exception as exc:
                    print(f"Relevance calculation generated an exception: {exc}")

        ranked_results = self.rank_results(valid_results)
        # self.cache_results(ranked_results)
        print(f"COUNT OF RESULTS for query {normalized_query}: {len(ranked_results)}")
        return ranked_results

    def get_one_product_per_source(self, q):
        results = self.search(q)
        seen_sources = set()
        unique_results = []

        for result in results:
            if result['source'] not in seen_sources:
                unique_results.append(result)
                seen_sources.add(result['source'])

        # Ensure only one result per scraper/source is returned
        final_results = []
        for source in self.scrapers.keys():
            for result in unique_results:
                if result['source'] == source:
                    final_results.append(result)
                    break

        return final_results

    def refresh_data(self):
        try:
            # Fetch all stored titles from Typesense
            stored_titles = typesenseClient.collections['products'].documents.search({
                'q': '*',
                'query_by': 'title',
                'per_page': 250
            })

            titles = [hit['document']['title'] for hit in stored_titles['hits']]

            for title in titles:
                results = self.search(title)
                print("RESULTS", results)

            return {"message": "Data refreshed successfully"}
        except Exception as exc:
            raise Exception(f"Error refreshing data: {exc}")


if __name__ == "__main__":
    search_engine = SearchEngine()
    query = "arcmate 120i"
    all_results = []
    count = []

    for i in range(10):
        results = search_engine.search(query)
        count.append({
            "count": len(results),
            "results": [{"number": idx + 1, "source": res['source'], "title": res['title'], "url": res['url']} for
                        idx, res in enumerate(results)]
        })
        all_results.extend(results)
    import json

    # Write the results to output.txt
    with open("output.txt", "w") as outfile:
        json.dump(count, outfile, indent=4)

    print(count)

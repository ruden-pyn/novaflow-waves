import re

def parse_task(task: str):

    task = task.lower()

    # detect number of results
    number_match = re.search(r'\d+', task)
    num_results = int(number_match.group()) if number_match else 3

    if "search" in task or "find" in task or "look for" in task:

        query = task.replace("search", "")
        query = query.replace("find", "")
        query = query.replace("look for", "")

        query = query.strip()

        return {
            "action": "search",
            "query": query,
            "count": num_results
        }

    return {"action": "unknown"}

from internet import search_web


def research_topic(topic):

    results = search_web(topic)

    summary = f"""
Research results for: {topic}

{results}
"""

    return summary
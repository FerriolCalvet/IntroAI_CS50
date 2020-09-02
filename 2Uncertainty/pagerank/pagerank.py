import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    N = len(corpus)
    links = corpus[page]
    N_links = len(links)
    prob_dist = {}
    for pp in corpus.keys():
        prob_dist[pp] = (1 - damping_factor) / N

    for linked_pp in links:
        prob_dist[linked_pp] += damping_factor / N_links

    return prob_dist
    # raise NotImplementedError


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    cummulative_probs = {}

    for page in list(corpus.keys()):
        cummulative_probs[page] = 0

    for i in range(n):
        sampled_page = random.sample(list(corpus.keys()), 1)[0]
        output_dict = transition_model(corpus, sampled_page, damping_factor)
        for ele in list(output_dict.keys()):
            cummulative_probs[ele] += output_dict[ele]

    for pages in list(cummulative_probs.keys()):
        cummulative_probs[pages] = cummulative_probs[pages] / n

    return cummulative_probs

    # raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    dict_links_to_page = {}
    for main_page in list(corpus.keys()):
        dict_links_to_page[main_page] = set()
        for page2 in list(corpus.keys()):
            if main_page in corpus[page2]:
                dict_links_to_page[main_page].add(page2)
    # print(dict_links_to_page)

    N = len(corpus)
    init_cummulative_probs = {}
    for page in list(corpus.keys()):
        init_cummulative_probs[page] = (1-damping_factor) / N
    # print(init_cummulative_probs)


    max_diff = 1
    pagerank = {}
    for page in list(corpus.keys()):
        pagerank[page] = 1 / N

    while max_diff > 0.001:
        new_pagerank = init_cummulative_probs.copy()

        for page in list(corpus.keys()):
            page_links = dict_links_to_page[page]
            accumulated = 0
            for coming_link in page_links:
                nl_i = len(dict_links_to_page[coming_link])
                if nl_i > 0:
                    accumulated += (pagerank[coming_link] / nl_i)
                else:
                    accumulated += (pagerank[coming_link] / N)
            new_pagerank[page] += (damping_factor * accumulated)

        max_diff = 0
        for ele in list(new_pagerank.keys()):
            abs_diff = abs(new_pagerank[ele] - pagerank[ele])
            if abs_diff > max_diff:
                max_diff = abs_diff

        pagerank = new_pagerank
        # print(max_diff)

    return pagerank

    # raise NotImplementedError


if __name__ == "__main__":
    main()

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

    distribution = {}
    links = corpus[page]

    if len(links) == 0:
        damping_factor = 0

    for key in corpus:
        distribution[key] = (1-damping_factor)/(len(corpus))
        if  key in links:
            distribution[key] += damping_factor/len(links)
    
    return distribution

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    sample_pages = dict.fromkeys(corpus, 0)
    page = random.choice(list(corpus.keys()))
    sample_pages[page] += 1/n

    for _ in range(n-1):
        distribution = transition_model(corpus,page,damping_factor)
        page = random.choices(list(distribution.keys()),list(distribution.values()))[0]
        sample_pages[page] += 1/n
    
    return sample_pages


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    iterate_pages = dict.fromkeys(corpus, 1/len(corpus))
    diferenca = float("inf")

    while diferenca >= 1e-3:
        diferenca = float("-inf")
        prev_pages = iterate_pages.copy()
        for page in corpus:
            soma = 0

            for possible_link in corpus:
                num_links = len(corpus[possible_link])

                if page in corpus[possible_link] or num_links == 0:
                    if num_links == 0:
                        num_links = len(corpus)
                    soma += prev_pages[possible_link]/num_links

            new_rank = (1-damping_factor)/len(corpus) + damping_factor*soma
            diferenca = max(abs(new_rank - prev_pages[page]),diferenca)
            iterate_pages[page] = new_rank

    return iterate_pages


if __name__ == "__main__":
    main()

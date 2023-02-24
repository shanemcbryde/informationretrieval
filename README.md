## Information Retrieval 

The program implements a simple vector-based information retrieval system.  Keyword search in its basic form takes a sequence of words representing a query (e.g. "book, fish, worry, don't") then seeks documents that relate to these keywords by performing direct lookup, i.e. finding the documents in which they appear, or finding documents which are similar. It will performs the following tasks:

1. Collect a repository of pages from Wikipedia,  drawn at random from the Wikipedia index pages: (https://en.wikipedia.org/wiki/Wikipedia:Contents/A–Z_index), The number of documents will be specified by the user.  

2. These documents are then stored on disk within the current directory as a set of text files in the form `wiki-page#.txt`.

3. Accept a user provided query and perform a search of the terms within the above random Wikipedia pages.

4. Return a list of links to the top 10 pages (or fewer if the user specifies a number less than 10) that best match the user query.


<b>ATTENTION!!!</b>
You may need to run the identified commented out section at the top of the code one time prior to running the program. This will execute the download of required nltk assets. Simply uncomment the code, run the program, comment out the code for additional runs.

### Execute from command line:
1) Navigate to the directory containing the python file `Information-Retrieval.py`.
2) Execute the command: `python Information-Retrieval.py`
3) You will be asked for the number of Wikipedia pages to include in the search.
4) After collecting the Wikipedia pages, you will be asked to provide a search query.
5) Program will execute and display the resulting Wikipedia links in order of relevance.
6) Multiple queries can be run. Or, submit `q` to quit the execution. 

### Alternatively,
1) Open the Jypyter file `Information-Retrieval.ipynb` in Notebook.
2) Click the `Run` icon from the menu bar.
3) You will be asked for the number of Wikipedia pages to include in the search.
4) After collecting the Wikipedia pages, you will be asked to provide a search query.
5) Results are displayed below the cell.
6) Multiple queries can be run. Or, submit `q` to quit the execution.

As an aside: There is a bug in JupyterLab (perhaps Notebook as well) such that if a displayed link ends in a closing parentheses, the closing parentheses will be displayed but will not be part of the actual clickable displayed link resulting in an incorrect url with the missing closing parentheses.

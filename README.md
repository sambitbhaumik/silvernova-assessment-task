# Silvernova Assessment Task

Solution for legal RAG Application

## Your info (please fill out)

Try to answer as thruthfully as possible.

| Name                     | xxxxx        |
|--------------------------|--------------|
| E-Mail:                  | xxxxx@xxx.xx |
| Approx. Time To Complete | 6-7 hours     |
| My github:               | sambitbhaumik      |

## Setup

```bash
pip install -r requirements.txt
```

## Chunking strategy

I used a hierarchical chunking strategy.

Example:

```
# Chapter 1          (level 1)
## Section 1.1       (level 2)
### Subsection 1.1.1 (level 3)
## Section 1.2       (level 2)
```

The stack changes would be:
```
# Chapter 1 (level 1)
Stack: [Chapter 1]
## Section 1.1 (level 2)
Stack: [Chapter 1, Section 1.1]
### Subsection 1.1.1 (level 3)
Stack: [Chapter 1, Section 1.1, Subsection 1.1.1]
## Section 1.2 (level 2)
First, pops everything >= level 2
Stack becomes: [Chapter 1]
Then adds new section
Final Stack: [Chapter 1, Section 1.2]
```

## Run
```bash
# Get the file's content as markdown
./associate --mode=get-markdown

# Index the documents
./associate --mode=index-files

# Search for documents based on similarity
./associate --mode=search "[question]"

# Ask a question about the documents
./associate "[question]"
```

To use on Windows replace `./associate` with `.\associate.bat`

## LLM Response

The LLM Response is formatted as Markdown.

#### Query: `Where are the offices of XYZ Solutions Ltd.?` 

#### Answer:

**Office Location of XYZ Solutions Ltd.**<br><br>Based on the provided context, the office location of XYZ Solutions Ltd. can be determined from the Mutual Non-Disclosure Agreement (NDA) document.<br><br>* **Document:** NDA_filled.md, section '# MUTUAL NON-DISCLOSURE AGREEMENT'<br>* **Relevant Passage:**<br>"2. XYZ Solutions Ltd., having its **registered office or based in 456 King’s Road, London, SW3 5EE, United Kingdom**..."<br>* **Direct Quote (Office Location):** 456 King’s Road, London, SW3 5EE, United Kingdom<br><br>**Answer:** The office of XYZ Solutions Ltd. is located at **456 King’s Road, London, SW3 5EE, United Kingdom**.
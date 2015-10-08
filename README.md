# Architecture:

Gmail <-----> Flask App (Python) <-----> Wave Analytics

Storage: MongoDB

# Technologies:
## Why Python? Why Flask?
- Python has a great set of libraries for data analysis
- Flask is super lightweight and great for small projects

## Why MongoDB?
- Initially planned to use HBase+Phoenix (in core)
- Had versioning issues between Salesforce HBase and Python

## Why no Data science packages?
- Too much time was spent on trying to fix the HBase connection
- Didn’t use 3rd party libraries (like Pandas) to format data

# If we have more time...
- Analyze the emails’ subjects and bodies
- Group related emails together and supply “smarter” data to Wave Analytics
  - For example, what are the emails related to a particular sale?
- A nicer UI for the Python server so the users can configure
  - For example, only emails containing certain keywords will be retrieved
  - For example, only emails from a certain period will be retrieved

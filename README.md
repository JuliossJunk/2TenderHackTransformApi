
# My second hackathon project aka DocManager

The DocManager project is a modern solution for effective work with procurement documentation. Based on a fast and powerful Fast API server, it provides optimized processing of data from the database, ensuring the reliability and security of information storage.

## The main functions of DocManager:

- Working with data from the database: fast and convenient document management on the server, the ability to search, sort and filter data by various parameters.
- Versioning of document changes: saving and controlling all changes made to documents, with the ability to view and compare versions, as well as save the date and author of each change (analogous to the Git version control system).
- Comparing changes: a function that allows you to visually see the difference between different versions of a document (analogous to Git Diff).
- The ability to roll back to any version of changes: providing the ability to revert the document to any previous version, if necessary.
- Creating a PDF file based on changes: creating a neat and readable PDF document based on the changes made, which allows you to quickly and conveniently familiarize yourself with the changes in the document.
- Uploading data to the server: the ability to upload new documents or applications in any format to the server for centralized storage and management.


# Run the project

## Installation

Install my project dependencies with pip:

```bash
  pip install -r requirements.txt
```
## Starting the fastApi server

Just copy/past this part

```terminal
  uvicorn api:app --reload
```

    
## API Reference (A small part)
To fully work with the Api, you need a working database specified in the code, which has been self-destructed for a long time. In places where the database is specified, it can be replaced)
#### Check if the Api is working

```http
  GET /back/
```

#### Get item (required actual database)
Returns all versions of the document that only these users have worked on

```http
  GET /back/get_all_versions/?{ProviderID}&{CustomerID}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `ProviderID`      | `string` | **Not required**. Id of item to get |
| `CustomerID`      | `string` | **Not required**. Id of item to get |



# Authors

- [@octokatherine](https://www.github.com/octokatherine)


# Appendix

## At this hackathon, the team and I took second place x(


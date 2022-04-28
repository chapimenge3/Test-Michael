# Test-Michael
This is test project intended for Michael.T.

# How to run the project

    1. doker compose up( if this is not working follow the below steps)
    2. docker build
    3. docker compose up( to detach and run it in background add -d to the command `docker compose up -d`)
    4. docker-compose up( if you are not using docker the latest version of docker)

# How to Test

Tests are implemented to check the validity of the api endpoint and the models. To run the test we need to run the following command:

    1. docker compose run web python testproject/manage.py test api

# Available Command 

    - docker compose run web python testproject/manage.py savecountries - save countries to database
    - docker compose run web python testproject/manage.py saveloans - save loans to database
    - docker compose run web python testproject/manage.py saveprojects - save projects to database
    - docker compose run web python testproject/manage.py savesectors - save sectors to database

# Avaialable Endpoints

    - http://localhost:8000/api/countries/ - get all countries
    - http://localhost:8000/api/loans/ - get loans 
    - http://localhost:8000/api/projects/ - get projects
    - http://localhost:8000/api/sectors/ - get sectors
    - http://localhost:8000/api/filters/ - get filters

# Available Filters

for all of the api except for the filters endpoint, you can use the following filters:

    - sortColumn
    - sortDir
    - pageNumber
    - itemPerPage
    - pageable
    - language
    - defaultLanguage
    - loanPartYearFrom
    - loanPartYearTo
    - orCountries
    - orCountries
    - orSectors

Just like the https://www.eib.org website, the filters are applied in the endpoints too.


Developer: Temkin Mengistu.
Email: chapimenge3@gmail.com

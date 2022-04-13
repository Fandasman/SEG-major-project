# Team Nonconformist Computer Science Students Major Group project

## Team members
The members of the team are:
- Garik Chilingaryan
- Daphnee Brunschwig
- Guneek Deol
- Mugur-Cristian Iacob
- Lubna Taraki
- Frantisek Hermanek
- Xiaojun Liang

## Project structure
The project is called `system`.  It consists of a single app `clubs` and a `system` folder containing framework specific files.

## Deployed version of the application
The deployed version of the application can be found at this [URL](https://agile-gorge-39941.herokuapp.com/).

The application will be deployed by April 15th 2022, as per the specified deadline.

## Installation instructions

IN ORDER TO MAKE THE RECOMMENDER SYSTEM FUNCTION PROPERLY, MAKE SURE model.pkl IS IN THE MAIN DIRECTORY OF THE PROJECT

To install the software and use it in your local development environment, you must first set up and activate a local development environment.  From the root of the project:

```
$ virtualenv venv
$ source venv/bin/activate
```

Install all required packages:

```
$ pip3 install -r requirements.txt
```

Used packages include:

	asgiref==3.4.1
	beautifulsoup4==4.10.0
	coverage==6.0.1
	Django==3.2.5
	django-bootstrap-pagination==1.7.1
	django-bootstrap-v5==1.0.11
	django-multiselectfield==0.1.12
	django-widget-tweaks==1.4.9
	Faker==9.0.0
	libgravatar==1.0.0
	numpy==1.22.2
	pandas==1.4.1
	python-dateutil==2.8.2
	pytz==2021.3
	six==1.16.0
	soupsieve==2.3.1
	sqlparse==0.4.2
	text-unidecode==1.3
	tqdm==4.62.3
	django-multiselectfield==0.1.12
	django-location-field==2.1.0
	scikit-surprise==1.1.1

As specified in requirements.txt.

Migrate the database:

```
$ python3 manage.py migrate
```

Seed the development database locally with:

```
$ python3 manage.py seed --main_dataset ./main-data.csv --books_dataset ./new-books-data.csv
```
In case you would like to store the aforementioned files in another directory, specify the path.
Make sure the main_data.csv and new_books_data.csv are in the main directory of the project in order for the command to function properly.

Or if you wish to seed the data set from a url source, use:

```
$ python3 manage.py seed
```
The default option is seeding from url, but this can be updated if url does not function in seed.py. See the documentation there for reference!


Unseed the development database with:

```
$ python3 manage.py unseed
```

Run all tests with:
```
$ python3 manage.py test
```

Generate a test code coverage report with:
```
$ coverage run manage.py test
$ coverage report
```

For more coverage information, use:
```
$ coverage run manage.py test
$ coverage report
$ coverage html
$ open htmlcov/index.html
```

## Model and Datasets
The pretrained model and all the datasets can be found [here](https://drive.google.com/file/d/1AmuWPyvTZaOlMmha1ozlP_dchP0FJ6MX/view?usp=sharing)

## Sources
The packages used by this application are specified in `requirements.txt`

Certain sections of the code, such as basic views and tests were taken from the Clucker application developed during the first semester of teaching of the Software Engineering Group Project module in the 2021/2022 class.

Some sections were also inspired by the Chess Club group project developed as assessed coursework for the same module in the 2021/2022 class. That project itself uses code presented in Clucker as well. As such, similarities in the source code between those two specific applications can be expected.


The code for the calendar used in the user profile view was inspired by the code provided at: https://www.huiwenteo.com/normal/2018/07/24/django-calendar.html.

The code for the search engine functionality was also inspired by what was provided at: https://www.codingforentrepreneurs.com/blog/a-multiple-model-django-search-engine.

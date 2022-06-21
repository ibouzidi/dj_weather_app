# Weather-App-Django

This is a simple weather app that uses Open Weather API and Django as backend Framework.

<h3>Links </h3>
<ul>
<li><a href="https://openweathermap.org/api">Open Weather API</a></li>
</ul>

### Setup
1. Clone this repository: <pre> git clone https://github.com/ibouzidi/weather_app.git </pre>
2. Install requirements : <pre> pip install -r requirements.txt</pre>
3. Migrate database : <pre>python manage.py migrate<pre>
4. Run server : <pre>python manage.py runserver</pre>

### Setup admin
1. Create super user: <pre>python manage.py createsuperuser</pre>
2. Access Aadmin page with super user login and password.

### Load data
1. Go to weather/fixtures and add your city preference.
2. Load these data with : <pre>python manage.py loaddata city</pre>






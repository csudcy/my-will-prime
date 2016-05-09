# My Will Prime

This is a re-implementation of [my-will](https://github.com/csudcy/my-will) using the HipChat Connect API.


## Running on Cloud9

```bash
# Setup mongodb - https://community.c9.io/t/setting-up-mongodb/1717
mkdir mongo_data
echo 'mongod --bind_ip=$IP --dbpath=mongo_data --nojournal --rest "$@"' > mongod
chmod a+x mongod
./mongod &

# Setup redis - https://community.c9.io/t/setting-up-redis/1719
sudo service redis-server start

# Run the app:
mkvirtualenv venv
pip install -r requirements.txt
export MWP_ADDON_KEY="my-will-prime"
export MWP_ADDON_NAME="My Will Prime"
export MWP_BASE_URL="https://my-will-prime-<your-username>.c9users.io"

# export MWP_TRIGGER="..."
# export HUKD_API_KEY="..."
# export GOOGLE_API_KEY="..."

python -m mwp
```


## Running on Heroku

**TODO**


## Configuration

`My Will Prime` is configured via environment variables. The configuration options are:
* `MWP_HOST` (default: `0.0.0.0`) - The host IP to bind to
* `MWP_PORT` (default: `8080`) - The post to bind to
* `MWP_TRIGGER` (default `/mwp`) - The text to prefix most plugin triggers with
* All the `ac-flask-hipchat` options listed below but prefixed with `MWP_` instead of `AC_`. The options you should set are:
  * `MWP_ADDON_KEY` - The key for this addon
  * `MWP_ADDON_NAME` - The description for this addon
  * `MWP_BASE_URL` - The URL which this addon can be accessed at
* Some plugins need an API key:
  * `GOOGLE_API_KEY` - For searching Youtube
  * `HUKD_API_KEY` - For getting Hot UK Deals


## AC-Flask-Hipchat

Will Prime is based on [ac-flask-hipchat](https://bitbucket.org/atlassianlabs/ac-flask-hipchat), a [Flask](http://flask.pocoo.org/) based webserver which makes [Hipchat Connect](https://developer.atlassian.com/hipchat) based interaction easy.

However, I cannot find any documentation for it. Therefore, I will try to write down what I find here.


### Configuration

Configuration is done via environment variables. Any variable prefixed with `AC_` will be loaded into `app.config`. The variables used by ac-flask-hipchat are:

* These configure various parts on the [capability descriptor](https://developer.atlassian.com/hipchat/tutorials/building-an-add-on-with-your-own-technology-stack#Buildinganadd-onwithyourowntechnologystack-Exposeacapabilitydescriptor):
  * `AC_ADDON_DESCRIPTION`
  * `AC_ADDON_KEY`
  * `AC_ADDON_NAME`
  * `AC_ADDON_VENDOR_NAME`
  * `AC_ADDON_VENDOR_URL`
* `AC_AVATAR_URL` - ?
* `AC_BASE_URL` - The URL which this addon can be accessed at
* `AC_CORS_WHITELIST` - Something relating to cross origin requests
* All the [Flask config options](http://flask.pocoo.org/docs/0.10/config/#builtin-configuration-values)
* `MONGOHQ_URL` - For connecting to [Mongo HQ](https://devcenter.heroku.com/articles/mongohq)
* `REDISTOGO_URL` - For connecting to [Redis To Go](https://devcenter.heroku.com/articles/redistogo)
* `WERKZEUG_RUN_MAIN` -  I think this is used internally by Werkzeug to determine if it is the master process


## Writing Plugins

Some brief notes:
* When writing a plugin, you can use `%TRIGGER%` in the regex and it will be substituted for the `MWP_TRIGGER` environment variable
* You can also use `%TRIGGER%` in doc strings


## Todo


### To fix:
* Connect4
  * Didnt properly detect X win in cols 2345 (detected it when 6 was put in)


### To improve:
* Hangman
  * Make it look better
  * Persist over restart
  * Keep stats
    * Word length vs. guesses taken
    * Correct vs. incorrect guesses
    * Words that have been used (& their definitions)
    * Actual letter frequency vs. guessed letter frequency
    * Correct guesses per person vs. incorrect
* Wikipedia - doesnt show the normal URL summary :/ 
* Remind Me
  * Actually set reminders!
  * Make summarising with tomorrow work


### To implement:
* Text FX:
  * Lorem ipsum
  * Hodor
* Lists & searching (admin through web?):
  * Board Games
  * Lunch
* Search internet sites:
  * Sporcle
  * Wiktionary
  * XKCD
  * Dilbert
  * Nutscapes
* Basic responders:
  * War games
  * Word of the day
  * Hello
  * Goodbye
* Random:
  * In a specific room, set a random topic every 10 minutes from chatoms
  * Rage
  * Random rage
  * Random refusal to work
  * Willisms

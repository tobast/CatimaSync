# Catima Sync - Server

This is the server part of Catima Sync.

## Initial setup

```python3
# Create a virtualenv
virtualenv -p python3 venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For development only

# Setup the settings
cp catima_sync/settings{_XXX,}.py  # Where XXX = prod or dev
$EDITOR catima_sync/settings.py  # Edit at least the FIXMEs

# Collect static files
./manage.py collectstatic

# Initialize the database
./manage.py migrate
```

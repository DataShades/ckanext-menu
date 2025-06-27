1. Activate your CKAN virtual environment, for example:

     . /usr/lib/ckan/default/bin/activate

2. Clone the source and install it on the virtualenv
```
git clone https://github.com/Datashades/ckanext-menu.git
cd ckanext-menu
pip install -e .
```
3. Add `menu` to the `ckan.plugins` setting in your CKAN
   config file (by default the config file is located at
   `/etc/ckan/default/ckan.ini`).

3. Initialize `menu` table in the DB.
```
ckan -c CKAN_CONFIG_PATH db upgrade -p menu
```

4. Restart CKAN
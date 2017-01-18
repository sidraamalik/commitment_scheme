You require python virtual environment. After that, get into the virtual environment.

Example:
```
virtualenv .venv
. .venv/bin/activate
pip install -r development.txt
python setup.py develop
```

To run the script, run:
```
python commitmentscheme/run.py
```

Now you can start running scripts in ```scripts``` folder.
```
#Order
./scripts/create_user.sh

# Run this more than once
./scripts/create_message.sh
./scripts/create_message.sh

./scripts/get_all_messages.sh
./scripts/get_message.sh
./scripts/verify_message.sh
./scripts/reveal_message.sh

# Notice the change in message
./scripts/get_all_messages.sh

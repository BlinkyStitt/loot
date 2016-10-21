# loot
#

FROM python:2.7-alpine

# since we are using upstream's python image that installs python into /usr/local/bin, its fine to use /usr/local/bin/pip for this. we still use virtualenv for the app code so its all owned by the user
RUN pip install --no-cache-dir virtualenv

# create a user
RUN adduser -S loot

USER loot
ENV HOME=/home/loot
WORKDIR /home/loot
RUN virtualenv ~/pyenv
ENV PATH="$HOME/pyenv/bin:$PATH"

# install the code in a two step process to keep the cache smarter
ADD requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY . /home/loot/src/loot
# todo: i wish copy would keep the user...
USER root
RUN chown -R loot:nogroup /home/loot/src

# install the app as the user, run the --help once to make sure it works
USER loot
WORKDIR /home/loot/src/loot
RUN pip install --no-cache-dir -r requirements.txt -e . \
 && loot --help

# todo: this is acting weird. when i do run it wont see any args and just always prints the help text...
ENTRYPOINT ["/home/loot/pyenv/bin/loot"]
CMD ["--help"]

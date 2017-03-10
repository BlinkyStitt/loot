FROM bwstitt/python-alpine:python2

# install the code in a two step process to keep the cache smarter
ADD requirements.txt /src/requirements.txt
RUN su-exec abc:abc pip install --no-cache-dir -r /src/requirements.txt

COPY . /src
# todo: i wish copy would keep the user...
RUN chown -R abc:abc /src

# install the app as the user, run the --help once to make sure it works
USER user
WORKDIR /src
RUN pip install --no-cache-dir -r requirements.txt -e . \
 && loot --help

# todo: this is acting weird. when i do run it wont see any args and just always prints the help text...
ENTRYPOINT ["loot"]
CMD ["--help"]

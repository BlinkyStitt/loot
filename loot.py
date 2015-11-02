#!/usr/bin/env python

import operator
import re
import yaml

import click


class Valuable(object):

    def __init__(self, name, short, value, game_data):
        self.game_data = game_data
        self.name = str(name)
        self.short = str(short) if short else None
        self.value = int(value)

    def __repr__(self):
        return "Valuable(name='{}', value='{} {}')".format(
            self.name,
            self.value,
            self.game_data['base_unit'],
        )

    def __str__(self):
        return "{}".format(
            self.short or self.name,
            # self.value,
        )

    def __cmp__(self, other):
        return cmp(self.value, other.value)

    def __hash__(self):
        return hash((self.name, self.value))


class Character(object):

    def __init__(self, name, game_data):
        self.game_data = game_data
        self.name = name
        self.valuables = {}

    def add_valuable(self, valuable, num):
        if valuable not in self.valuables:
            self.valuables[valuable] = 0
        self.valuables[valuable] += num

    @property
    def total_value(self):
        total = 0

        for valuable, num in self.valuables.iteritems():
            total += valuable.value * num

        return total

    def __repr__(self):
        return "Character(name='{}', total_value='{}')".format(
            self.name,
            self.total_value,
        )

    def __str__(self):
        # todo: figure out how to get X
        return "Character {} gets {} {} worth of valuables:\n{}".format(
            self.name,
            self.total_value,
            self.game_data['base_unit'],
            "\n".join([
                "- {} {}".format(n, v)
                for v, n in sort_dict_descending_keys(self.valuables)
            ]),
        )

    def __cmp__(self, other):
        return cmp(self.total_value, other.total_value)


def sort_dict_descending_keys(data):
    return sorted(
        data.items(),
        key=operator.itemgetter(0),
        reverse=True
    )


def split(party, valuable, num_valuables):
    num_party = len(party)

    while num_valuables > 0:
        # if everybody is equal, split as many coins as possible
        if num_valuables >= num_party and party_equal(party):
            pre_split_valuables = num_valuables
            split_valuables, num_valuables = divmod(num_valuables, num_party)
            click.echo(
                "split {} {} into {} piles of {} with {} leftover...".format(
                    pre_split_valuables,
                    valuable,
                    num_party,
                    split_valuables,
                    num_valuables,
                )
            )
            for p in party:
                p.add_valuable(valuable=valuable, num=split_valuables)

        if num_valuables:
            click.echo("giving 1 of {} {} to the poorest character...".format(
                num_valuables,
                valuable,
            ))

            # pick the poorest party member
            p = min(party)

            p.add_valuable(valuable=valuable, num=1)
            num_valuables -= 1


def party_equal(party):
    if len(party) <= 1:
        return True

    p0_value = party[0].total_value

    for p in party[1:]:
        if p.total_value != p0_value:
            return False

    return True


@click.command()
@click.argument('valuables', nargs=-1, type=click.UNPROCESSED)
@click.option(
    '-g', '--game-data',
    default='games/dnd.yaml',
    type=click.File(),
)
@click.option('-n', '--num-party', prompt=True, type=int)
def main(
    game_data,
    num_party,
    valuables,
):
    game_data = yaml.load(game_data)

    possible_valuables = []
    for v_name, v_data in game_data['valuables'].iteritems():
        v = Valuable(
            game_data=game_data,
            name=v_name,
            short=v_data.get('short', None),
            value=v_data['value'],
        )
        possible_valuables.append(v)

    # parse valuables
    parsed_valuables = {}
    r = re.compile('^ *(\d+) *(.+) *$')
    for v in valuables:  # collection of strings
        m = r.match(v)
        if not m:
            click.confirm("Unable to parse '%s'. Skip it?" % v, abort=True)
            continue

        num, name_or_short = m.groups()

        if not num:
            click.confirm("No num while parsing '%s'. Skip it?" % v, abort=True)
            continue

        num = int(num)

        if not name_or_short:
            click.confirm("No name while parsing '%s'. Skip it?" % v, abort=True)
            continue

        # todo: this could be faster
        found = False
        for pv in possible_valuables:
            if name_or_short not in (pv.name, pv.short):
                continue

            if pv not in parsed_valuables:
                parsed_valuables[pv] = 0

            parsed_valuables[pv] += num
            found = True
            break

        if not found:
            click.confirm("Unable to find data for '%s'. Skip it?" % name_or_short, abort=True)
            # todo: prompt the name/short/value and save it to yaml

    party = []
    for x in xrange(num_party):
        party.append(Character(name=x, game_data=game_data))

    # split up the most expensive things first
    for valuable, num in sort_dict_descending_keys(parsed_valuables):
        split(party, valuable, num)

    click.echo("")
    if party_equal(party):
        click.echo("The loot divided equally :)")
    else:
        click.echo("The loot did not divide equally :(")

    map(click.echo, party)


if __name__ == '__main__':
    main()
